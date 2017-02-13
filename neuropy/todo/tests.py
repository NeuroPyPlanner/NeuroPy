"""Test for todo app."""

from django.test import TestCase
from todo.models import Todo
from django.contrib.auth.models import User
import factory


class TodoFactory(factory.django.DjangoModelFactory):
    """Create test instance of todos."""

    class Meta:
        """Invoke Todo instance using Todo model class."""

        model = Todo

    description = factory.Sequence(lambda n: "Todo {}".format(n))
    title = "Some Todo"


class UserFactory(factory.django.DjangoModelFactory):
    """Create test instance of User Class."""

    class Meta:
        """Invoke user instance using User model class."""

        model = User

    username = factory.Sequence(lambda n: "User {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@gmail.com".format(x.username.replace(" ", ""))
    )


class UserTestCase(TestCase):
    """The User Model test class."""

    def setUp(self):
        """The setup and buildout for users, todos."""
        self.users = [UserFactory.create() for i in range(20)]
        self.todos = [TodoFactory.create() for i in range(20)]

    def test_todo_exists(self):
        """Test existance of a todo."""
        this_todo = self.todos[0]
        this_todo.save()
        self.assertTrue(self.todos[0])

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
