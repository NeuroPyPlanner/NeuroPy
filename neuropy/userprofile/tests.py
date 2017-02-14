"""Tests for the userprofile app."""

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User, Group, Permission
from userprofile.models import Profile
import factory
from django.core.urlresolvers import reverse_lazy

from bs4 import BeautifulSoup


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


class UserFactory(factory.django.DjangoModelFactory):
    """Build users."""

    class Meta:
        """Meta."""

        model = User

    username = factory.Sequence(lambda n: 'user_number_{}'.format(n))
    email = factory.LazyAttribute(
        lambda x: '{}@cbt.com'.format(x.username.replace(" ", ""))
    )


class ProfileTestCase(TestCase):
    """Test the profile model."""

    def setUp(self):
        """Set up to test user profiles."""
        add_user_group()
        self.users = [UserFactory.create() for i in range(20)]

    def test_profile_is_made_when_user_is_saved(self):
        """Test that a profile is made for each user save event."""
        self.assertTrue(Profile.objects.count() == 20)

    def test_profile_associated_with_users(self):
        """Test that the profile is linked with a user."""
        profile = Profile.objects.first()
        self.assertTrue(hasattr(profile, 'user'))
        self.assertIsInstance(profile.user, User)

    def test_user_sees_profile(self):
        """Test that the user model is related to a profile model."""
        user = self.users[0]
        self.assertIsInstance(user.profile, Profile)
        self.assertTrue(hasattr(user, 'profile'))

    def test_user_in_group(self):
        """Test that created users are added to user group."""
        user = self.users[0]
        group = user.groups.first()
        self.assertTrue(group.name == 'user')

    def test_profile_has_attributes(self):
        """Test that the profile has attributes and assigns defaults."""
        # import pdb; pdb.set_trace()
        users = self.users
        attributes = [
            'active_period_start', 'active_period_end', 'peak_period', 'dose_time'
        ]
        for user in users:
            for attribute in attributes:
                self.assertTrue(hasattr(user.profile, attribute))


class FrontendTestCases(TestCase):
    """Test the frontend of the imager_profile site."""

    def setUp(self):
        """Set up client and request factory."""
        self.client = Client()
        self.request = RequestFactory()

    def test_home_route_templates(self):
        """Test the home route templates are correct."""
        response = self.client.get(reverse_lazy('home'))
        self.assertTemplateUsed(response, "neuropy/base.html")
        self.assertTemplateUsed(response, "neuropy/home.html")

    def test_login_redirect_code(self):
        """Test built-in login route redirects properly."""
        add_user_group()
        user_register = UserFactory.create()
        user_register.username = "username"
        user_register.set_password("rutabega")
        user_register.save()
        response = self.client.post(reverse_lazy("login"), {
            "username": user_register.username,
            "password": "rutabega"
        })
        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.url == '/')

    def test_login_has_input_fields(self):
        """Test login has input fields."""
        response = self.client.get(reverse_lazy('login'))
        parsed_html = BeautifulSoup(response.content, "html5lib")
        self.assertTrue(len(parsed_html.find_all('input')) == 3)

    def test_registeration_has_input_fields(self):
        """Test registeration has input fields."""
        response = self.client.get(reverse_lazy('registration_register'))
        parsed_html = BeautifulSoup(response.content, "html5lib")
        self.assertTrue(len(parsed_html.find_all('input')) == 6)

    def test_registration_has_tos(self):
        """Test registration form has TOS."""
        response = self.client.get(reverse_lazy('registration_register'))
        parsed_html = BeautifulSoup(response.content, 'html5lib')
        self.assertTrue(parsed_html.find('h3').text == ' Terms of Service ')

    def test_registration_has_tos_tick_box(self):
        """Test registration form has input for tos."""
        response = self.client.get(reverse_lazy('registration_register'))
        parsed_html = BeautifulSoup(response.content, 'html5lib')
        tos = parsed_html.findAll('input', attrs={'name': 'tos'})
        self.assertTrue(len(tos) == 1)
