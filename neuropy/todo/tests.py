"""Test for todo app."""

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy

from todo.views import create_event_list
from todo.models import Todo
from userprofile.models import Profile
import factory
from bs4 import BeautifulSoup
import datetime

class TodoFactory(factory.django.DjangoModelFactory):
    """Create test instance of todos."""

    class Meta:
        """Invoke Todo instance using Todo model class."""

        model = Todo

    description = factory.Sequence(lambda n: "Todo {}".format(n))
    title = factory.Sequence(lambda n: "Some Todo {}".format(n))


class UserFactory(factory.django.DjangoModelFactory):
    """Create test instance of User Class."""

    class Meta:
        """Invoke user instance using User model class."""

        model = User

    username = factory.Sequence(lambda n: "User {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@gmail.com".format(x.username.replace(" ", ""))
    )


def add_user_group():
    """
    Add a simulated default user group.

    This will require edits as we add features and permissions.
    Commented lines are example lines for adding permissions to the group.
    """
    new_group, created = Group.objects.get_or_create(name='user')
    # permission = Permission.objects.get(name='permission_name')
    # new_group.permissions.add(permission)
    new_group.save()


class TodoTestCase(TestCase):
    """The Todo Model test class."""

    def setUp(self):
        """The setup and buildout for users, todos."""
        add_user_group()
        self.users = [UserFactory.create() for i in range(20)]
        self.todos = [TodoFactory.create() for i in range(20)]

    def test_todo_exists(self):
        """Test existance of a todo."""
        this_todo = self.todos[0]
        this_todo.save()
        self.assertTrue(self.todos[0])

    def test_unique_todo_created(self):
        """Test that the number of todos in the database equla the nuber of todos created."""
        self.assertTrue(Todo.objects.count() == 20)

    def test_todo_has_attributes(self):
        """Test todo is created with attributes."""
        todo1 = self.todos[0]
        attributes = ['title',
                      'description',
                      'date',
                      'ease',
                      'duration',
                      'priority',
                      'owner']
        for attribute in attributes:
            self.assertTrue(hasattr(todo1, attribute))

    def test_owner_is_a_profile(self):
        """Test owner is an instance of a Profile."""
        todo1 = self.todos[0]
        todo1.owner = self.users[0].profile
        self.assertIsInstance(todo1.owner, Profile)

    def test_profile_has_a_todo(self):
        """Test profile has associated attribute todo."""
        todo1 = self.todos[0]
        todo1.owner = self.users[0].profile
        self.assertTrue(hasattr(self.users[0].profile, 'todo'))

    def test_todo_str_method_returns_username(self):
        """Test str method on todo returns the title."""
        todo = Todo.objects.first()
        self.assertTrue(str(todo) == todo.title)

    def test_assign_multiple_todos_to_single_user(self):
        """Test the many-to-one relationship between todo and user works."""
        todo1 = self.todos[4]
        todo2 = self.todos[5]
        owner = self.users[6].profile
        todo1.owner, todo2.owner = owner, owner
        todo1.save()
        todo2.save()
        self.assertTrue(owner.todo.count() == 2)


class TodoFrontEndTestCase(TestCase):
    """The Todo route and view test class."""

    def setUp(self):
        """The setup and buildout for users, todos."""
        self.client = Client()
        self.request = RequestFactory()
        add_user_group()
        self.users = [UserFactory.create() for i in range(20)]
        self.todos = [TodoFactory.create() for i in range(20)]

    def generate_todos(self):
        """Generate todos."""
        user = self.users[5]
        todo1 = self.todos[0]
        todo2 = self.todos[2]
        todo3 = self.todos[1]
        todo1.owner, todo2.owner, todo3.owner = user.profile, user.profile, user.profile

        todo1.date = datetime.date.today()
        todo2.date = datetime.date.today()
        todo3.date = datetime.date.today()

        todo1.ease = 1
        todo2.ease = 2
        todo3.ease = 3

        todo1.priority = 2
        todo2.priority = 3
        todo3.priority = 4

        todo1.duration = 1
        todo2.duration = 2
        todo3.duration = 3

        user.save()
        todo1.save()
        todo2.save()
        todo3.save()
        return user.profile, [todo1, todo2, todo3]

    def make_user_and_login(self):
        """Make user and login."""
        add_user_group()
        user_register = UserFactory.create()
        user_register.is_active = True
        user_register.username = "bobdole"
        user_register.first_name = 'Bob'
        user_register.last_name = 'Dole'
        user_register.email = 'awesome@gmail.com'
        user_register.set_password("rutabega")
        user_register.save()
        self.client.post("/login/", {
            "username": user_register.username,
            "password": "rutabega"

        })
        return self.client, user_register

    def test_todo_list_route_is_status_ok(self):
        """Funcional test for todo list."""
        self.client.force_login(self.users[0])
        response = self.client.get(reverse_lazy("list_todo"))
        self.assertTrue(response.status_code == 200)

        """Test todo list returns the right templates."""
        self.client.force_login(self.users[0])
        response = self.client.get(reverse_lazy("list_todo"))
        self.assertTemplateUsed(response, "neuropy/layout.html")
        self.assertTemplateUsed(response, "todo/list_todo.html")

    def test_todo_detail_route_is_status_ok(self):
        """Funcional test for todo list."""
        self.client.force_login(self.users[0])
        todo = self.todos[0]
        todo.owner = self.users[0].profile
        todo.save()
        response = self.client.get('/profile/todo/' + str(todo.pk))
        self.assertTrue(response.status_code == 200)

    def test_todo_detail_route_uses_right_templates(self):
        """Test todo list returns the right templates."""
        self.client.force_login(self.users[0])
        todo = self.todos[0]
        todo.owner = self.users[0].profile
        todo.save()
        response = self.client.get('/profile/todo/' + str(todo.pk))
        self.assertTemplateUsed(response, "neuropy/layout.html")
        self.assertTemplateUsed(response, "todo/detail_todo.html")

    def test_edit_todo_default_values(self):
        """Test that the response when calling the edit todo views includes default values."""
        todo = self.todos[0]
        self.client.force_login(self.users[0])
        response = self.client.get(reverse_lazy(
            'edit_todo', kwargs={'pk': todo.id})
        )
        self.assertTrue('Edit a To-Do item' in response.content.decode())

    def test_todo_list_route_displays_correctly(self):
        """Test todo list route displays correctly."""
        self.client.force_login(self.users[0])
        user = self.users[0]
        todo = self.todos[3]
        todo.owner = user.profile
        todo.save()
        response = self.client.get(reverse_lazy("list_todo"))
        parsed_html = BeautifulSoup(response.content, 'html5lib')
        self.assertTrue(len(parsed_html.find_all('article')) == 1)

    def test_edit_todo_will_change_template(self):
        """Test edit todo will redirect to profile."""
        client, user = self.make_user_and_login()
        todo = self.todos[9]
        todo.owner = user.profile
        todo.save()

        response = client.post('/profile/todo/' + str(todo.id) + '/edit/', {
            "title": "Todo 1",
            "description": "Some Text",
            "duration": "1",
            "priority": "1",
            "ease": "1",
            "date_month": "1",
            "date_year": "2017",
            "date_day": "2",
        }, follow=True)
        self.assertTrue(b'Todo 1' in response.content)

    def test_edit_todo_will_redirect_to_todo_list(self):
        """Test edit todo will redirect to todo list."""
        client, user = self.make_user_and_login()
        todo = self.todos[9]
        todo.owner = user.profile
        todo.save()

        response = client.post('/profile/todo/' + str(todo.id) + '/edit/', {
            "title": "Todo 1",
            "description": "Some Text",
            "duration": "1",
            "priority": "1",
            "ease": "1",
            "date_month": "1",
            "date_year": "2017",
            "date_day": "2",
        })
        self.assertRedirects(response, '/profile/todo/')

    def test_add_todo_will_redirect_to_todo_list(self):
        """Test add todo will redirect to todo list."""
        client, user = self.make_user_and_login()

        response = client.post('/profile/todo/add/', {
            "title": "Todo 1",
            "description": "Some Text",
            "duration": "1",
            "priority": "1",
            "ease": "1",
            "date_month": "1",
            "date_year": "2017",
            "date_day": "2",
        })
        self.assertRedirects(response, '/profile/todo/')

    def test_add_todo_will_redirect_with_new_content(self):
        """Test add todo will redirect to todo list with new content."""
        client, user = self.make_user_and_login()

        response = client.post('/profile/todo/add/', {
            "title": "Todo 1",
            "description": "Some Text",
            "duration": "1",
            "priority": "1",
            "ease": "1",
            "date_month": "1",
            "date_year": "2017",
            "date_day": "2",
        }, follow=True)
        self.assertTrue(b'Todo 1' in response.content)

    def test_add_with_missing_fields_will_not_redirect(self):
        """Test add todo will not redirect if fields missing."""
        client, user = self.make_user_and_login()

        response = client.post('/profile/todo/add/', {
            "title": "Todo 1",
            "description": "Some Text",
            "duration": "1",
            "priority": "1",
            "ease": "1",
        })
        self.assertFalse(response.status_code == 302)

    def test_edit_with_missing_fields_will_not_redirect(self):
        """Test add todo will not redirect if fields missing."""
        client, user = self.make_user_and_login()
        todo = self.todos[9]
        todo.owner = user.profile
        todo.save()

        response = client.post('/profile/todo/' + str(todo.id) + '/edit/', {
            "title": "Todo 1",
            "description": "Some Text",
            "duration": "1",
            "priority": "1",
            "ease": "1",
        })
        self.assertFalse(response.status_code == 302)

    def test_add_todo_status_code_302(self):
        """Test add todo status code 302."""
        user = self.users[4]
        self.client.force_login(user)
        html = self.client.get('/profile/todo/add/').content
        html = BeautifulSoup(html, "html5lib")
        csrf = html.find("input", {"name": 'csrfmiddlewaretoken'})['value']
        response = self.client.post('/profile/todo/add/', {
            "csrfmiddlewaretoken": csrf,
            "title": "Buy Google",
            "description": "Then Buy Amazon",
            "date_month": "1",
            "date_day": "6",
            "date_year": "2017",
            "duration": "4",
            "ease": "2",
            "priority": "1",
        })
        self.assertTrue(response.status_code == 302)

    def test_add_todo_saves_db_and_shows_to_list(self):
        """Test add todo saves db and shows to list."""
        user = self.users[4]
        self.client.force_login(user)
        html = self.client.get('/profile/todo/add/').content
        html = BeautifulSoup(html, "html5lib")
        csrf = html.find("input", {"name": 'csrfmiddlewaretoken'})['value']
        self.client.post('/profile/todo/add/', {
            "csrfmiddlewaretoken": csrf,
            "title": "Buy Google",
            "description": "Then Buy Amazon",
            "date_month": "1",
            "date_day": "6",
            "date_year": "2017",
            "duration": "4",
            "ease": "2",
            "priority": "1",
        })
        html = self.client.get('/profile/todo/').content
        html = str(html)
        self.assertTrue('Buy Google' in html)
        self.assertTrue('Priority: 1' in html)

    def test_add_todo_saves_db_and_shows_to_detail_todo_view(self):
        """Test add todo saves db and shows to detail todo view."""
        user = self.users[4]
        self.client.force_login(user)
        html = self.client.get('/profile/todo/add/').content
        html = BeautifulSoup(html, "html5lib")
        csrf = html.find("input", {"name": 'csrfmiddlewaretoken'})['value']
        self.client.post('/profile/todo/add/', {
            "csrfmiddlewaretoken": csrf,
            "title": "Buy Google",
            "description": "Then Buy Amazon",
            "date_month": "1",
            "date_day": "6",
            "date_year": "2017",
            "duration": "4",
            "ease": "2",
            "priority": "1",
        })
        pk = Todo.objects.get(title='Buy Google').id
        html = self.client.get('/profile/todo/' + str(pk)).content
        html = str(html)
        self.assertTrue('Buy Google' in html)
        self.assertTrue('<p><strong>Priority: </strong>1</p>' in html)
        self.assertTrue('<p><strong>Ease: </strong>2</p>' in html)
        self.assertTrue('<p><strong>Duration: </strong>4</p>' in html)
        self.assertTrue('<p><strong>Description: </strong>Then Buy Amazon</p>' in html)

    def test_edit_todo_status_code_302(self):
        """Test edit todo status code 302."""
        user = self.users[4]
        self.client.force_login(user)
        html = self.client.get('/profile/todo/add/').content
        html = BeautifulSoup(html, "html5lib")
        csrf = html.find("input", {"name": 'csrfmiddlewaretoken'})['value']
        self.client.post('/profile/todo/add/', {
            "csrfmiddlewaretoken": csrf,
            "title": "Buy Google",
            "description": "Then Buy Amazon",
            "date_month": "1",
            "date_day": "6",
            "date_year": "2017",
            "duration": "4",
            "ease": "2",
            "priority": "1",
        })
        pk = Todo.objects.get(title='Buy Google').id
        html = self.client.get('/profile/todo/' + str(pk) + '/edit/').content
        html = BeautifulSoup(html, "html5lib")
        csrf = html.find("input", {"name": 'csrfmiddlewaretoken'})['value']
        response = self.client.post('/profile/todo/' + str(pk) + '/edit/', {
            "csrfmiddlewaretoken": csrf,
            "title": "Buy Earth",
            "description": "Then Buy 7/11",
            "date_month": "2",
            "date_day": "7",
            "date_year": "2018",
            "duration": "3",
            "ease": "1",
            "priority": "1",
        })
        self.assertTrue(response.status_code == 302)

    def test_priority_now_does_not_duplicate(self):
        """Test that a priority to-do does not show as duplicate events."""
        from todo.views import create_event_list
        profile, todo_lst = self.generate_todos()
        todos = create_event_list("CONCERTA", profile)
        # import pdb; pdb.set_trace()
        seen_tasks = []
        # bucket_list = [priority_now, hard, medium, easy]
        # for bucket in bucket_list:
        for todo in todos:
            if todo in seen_tasks:
                raise ValueError("Todo already exists")
            else:
                seen_tasks.append(todo)
        self.assertTrue(todos[0]['description'] == 'Todo 381' and todos[1]['description'] == 'Todo 381')
        return seen_tasks

    def test_edit_todo_saves_db_and_shows_to_detail_todo_view(self):
        """Test edit todo saves db and shows to detail todo view."""
        user = self.users[4]
        self.client.force_login(user)
        html = self.client.get('/profile/todo/add/').content
        html = BeautifulSoup(html, "html5lib")
        csrf = html.find("input", {"name": 'csrfmiddlewaretoken'})['value']
        self.client.post('/profile/todo/add/', {
            "csrfmiddlewaretoken": csrf,
            "title": "Buy Google",
            "description": "Then Buy Amazon",
            "date_month": "1",
            "date_day": "6",
            "date_year": "2017",
            "duration": "4",
            "ease": "2",
            "priority": "1",
        })
        pk = Todo.objects.get(title='Buy Google').id
        html = self.client.get('/profile/todo/' + str(pk) + '/edit/').content
        html = BeautifulSoup(html, "html5lib")
        csrf = html.find("input", {"name": 'csrfmiddlewaretoken'})['value']
        self.client.post('/profile/todo/' + str(pk) + '/edit/', {
            "csrfmiddlewaretoken": csrf,
            "title": "Buy Earth",
            "description": "Then Buy 7/11",
            "date_month": "2",
            "date_day": "7",
            "date_year": "2018",
            "duration": "3",
            "ease": "1",
            "priority": "1",
        })
        html = self.client.get('/profile/todo/' + str(pk)).content
        html = str(html)
        self.assertTrue('Buy Earth' in html)
        self.assertTrue('<p><strong>Priority: </strong>1</p>' in html)
        self.assertTrue('<p><strong>Ease: </strong>1</p>' in html)
        self.assertTrue('<p><strong>Duration: </strong>3</p>' in html)
        self.assertTrue('<p><strong>Description: </strong>Then Buy 7/11</p>' in html)


# --------------- Algorithm Unittests ------------------
    def test_todo_ease_level_is_correct(self):
        """Test todo ease level is correct."""
        profile, todos = self.generate_todos()
        todos = create_event_list("CONCERTA", profile)
        self.assertTrue(len(todos) == 4)

    def test_todo_is_in_order(self):
        """Test todo is arranged in right order."""
        profile, todo_lst = self.generate_todos()
        todos = create_event_list("CONCERTA", profile)
        self.assertTrue(todos[0]['title'] == todo_lst[2].title)
        self.assertTrue(todos[2]['title'] == todo_lst[1].title)

    def test_todos_are_correct_ease_level(self):
        """Test todo is assigned to correct ease levels."""
        profile, todo_lst = self.generate_todos()
        todos = create_event_list("CONCERTA", profile)
        self.assertTrue(todos[0]['ease'] == 'hard')
        self.assertTrue(todos[1]['ease'] == 'hard')

    def test_todo_created_on_profile_on_wrong_date(self):
        """Test todo is created for current date."""
        user = self.users[5]
        todo1 = self.todos[0]
        todo2 = self.todos[2]
        todo1.owner, todo2.owner = user.profile, user.profile

        todo1.date = datetime.date(1, 2, 3)
        todo2.date = datetime.date(1, 2, 3)

        todo1.ease = 1
        todo2.ease = 2

        todo1.priority = 2
        todo2.priority = 3

        todo1.duration = 1
        todo2.duration = 2

        user.save()
        todo1.save()
        todo2.save()

        events = create_event_list('CONCERTA', user.profile)
        self.assertFalse(events)

    def test_todo_duration(self):
        """Test todo duration is equal to diff between end and start time of todo."""
        profile, todo_lst = self.generate_todos()
        todos = create_event_list("CONCERTA", profile)
        diff_todos_1 = todos[1]['end'] - todos[1]['start']
        self.assertTrue(datetime.timedelta(hours=todo_lst[2].duration) == diff_todos_1)

# -----------------------             ---------------------------

    def test_logged_out_todo_fails(self):
        """Test that a logged out user cannot create a todo."""
        response = self.client.get(reverse_lazy('add_todo'))
        parsed_html = BeautifulSoup(response.content, "html5lib")
        self.assertFalse(parsed_html.find_all('div'))

    def test_logged_out_schedule_fails(self):
        """Test that a logged out user cannot see a schedule."""
        response = self.client.get(reverse_lazy('schedule'))
        parsed_html = BeautifulSoup(response.content, "html5lib")
        self.assertFalse(parsed_html.find_all('div'))

    def test_logged_out_edit_todo_fails(self):
        """Test that a logged out user cannot edit a todo."""
        response = self.client.get(reverse_lazy('edit_todo', kwargs={'pk': self.todos[0].id}))
        parsed_html = BeautifulSoup(response.content, "html5lib")
        self.assertFalse(parsed_html.find_all('div'))

    def test_logged_out_detail_todo_fails(self):
        """Test that a logged out user cannot see todo details."""
        with self.assertRaises(AttributeError,):
            self.client.get(reverse_lazy('show_todo', kwargs={'pk': self.todos[0].id}))

    def test_logged_out_build_schedule_fails(self):
        """Test that a logged out user cannot build a schedule."""
        response = self.client.get(reverse_lazy('create_sched'))
        parsed_html = BeautifulSoup(response.content, "html5lib")
        self.assertFalse(parsed_html.find_all('div'))

    def test_edit_todo_without_csrf_fails(self):
        """Test edit todo will fail without a csrf token."""
        self.client.force_login(self.users[0])
        html = self.client.get(reverse_lazy('edit_todo', kwargs={'pk': self.todos[0].id})).content
        html = BeautifulSoup(html, "html5lib")
        self.client.post(reverse_lazy('edit_todo', kwargs={'pk': self.todos[0].id}), {
            "csrfmiddlewaretoken": "",
            "title": "sam spade",
            "description": "Some Text",
            "duration": "1",
            "priority": "1",
            "ease": "1",
            "date_month": "1",
            "date_year": "2017",
            "date_day": "2",
        })
        self.assertFalse(self.todos[0].title == 'sam spade')

    def test_add_todo_without_csrf_fails(self):
        """Test add todo will fail without a csrf token."""
        self.client.force_login(self.users[0])
        html = self.client.get(reverse_lazy('add_todo')).content
        html = BeautifulSoup(html, "html5lib")
        self.client.post(reverse_lazy('add_todo'), {
            "csrfmiddlewaretoken": "",
            "title": "sam spade",
            "description": "Some Text",
            "duration": "1",
            "priority": "1",
            "ease": "1",
            "date_month": "1",
            "date_year": "2017",
            "date_day": "2",
        })
        with self.assertRaises(AttributeError):
            self.todos[0].todo

    def test_schedule_view_returns(self):
        """Test that schedule view returns the right page."""
        self.client.force_login(self.users[0])
        session = self.client.session
        session['some_list'] = [{},{},{}]
        session.save()
        html = self.client.get(reverse_lazy('create_sched')).content
        parsed_html = BeautifulSoup(html, "html5lib")
        self.assertTrue(len(parsed_html.find_all('div')) == 10)
