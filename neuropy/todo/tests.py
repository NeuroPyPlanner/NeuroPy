"""Test for todo app."""

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy

from todo.models import Todo
from userprofile.models import Profile
import factory


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

    def test_todo_list_route_is_status_ok(self):
        """Funcional test for todo list."""
        self.client.force_login(self.users[0])
        response = self.client.get(reverse_lazy("list_todo"))
        self.assertTrue(response.status_code == 200)

    def test_todo_list_route_uses_right_templates(self):
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
