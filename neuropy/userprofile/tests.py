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


class FrontendTestCases(TestCase):
    """Test the frontend of the imager_profile site."""

    def setUp(self):
        """Set up client and request factory."""
        self.client = Client()
        self.request = RequestFactory()

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

    def test_home_route_templates(self):
        """Test the home route templates are correct."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "neuropy/base.html")
        self.assertTemplateUsed(response, "neuropy/home.html")

    def test_login_redirect_code(self):
        """Test built-in login route redirects properly."""
        add_user_group()
        user_register = UserFactory.create()
        user_register.is_active = True
        user_register.username = "username"
        user_register.set_password("rutabega")
        user_register.save()
        response = self.client.post("/login/", {
            "username": user_register.username,
            "password": "rutabega"

        })
        self.assertRedirects(response, '/')

    def test_login_has_input_fields(self):
        """Test login has input fields."""
        response = self.client.get('/login/')
        parsed_html = BeautifulSoup(response.content, "html5lib")
        self.assertTrue(len(parsed_html.find_all('input')) == 4)

    def test_registeration_has_input_fields(self):
        """Test registeration has input fields."""
        response = self.client.get('/accounts/register/')
        parsed_html = BeautifulSoup(response.content, "html5lib")
        self.assertTrue(len(parsed_html.find_all('input')) == 5)

    def test_profile_route_has_all_info(self):
        """Test profile route has all info."""
        client, user = self.make_user_and_login()
        html = client.get('/profile/').content
        html = str(html)
        self.assertTrue('Bob Dole' in html)
        self.assertTrue('bobdole' in html)
        self.assertTrue('awesome@gmail.com' in html)
        self.assertTrue('Active Period Start: 8 a.m.' in html)
        self.assertTrue('Active Period End: 10 p.m.' in html)
        self.assertTrue('Peak Period: Morning' in html)
        self.assertTrue('Dose Time: 8 a.m.' in html)

    def test_edit_route_shows_info(self):
        """Test_edit_route_shows_info."""
        client, user = self.make_user_and_login()
        html = client.get('/profile/edit/').content
        parsed_html = BeautifulSoup(html, "html5lib")

        def return_value(id):
            return parsed_html.find("input", {"id": id})['value']

        self.assertTrue(return_value('id_First Name') == 'Bob')
        self.assertTrue(return_value('id_Last Name') == 'Dole')
        self.assertTrue(return_value('id_Email') == 'awesome@gmail.com')
        self.assertTrue(return_value('id_active_period_start') == '08:00:00')
        self.assertTrue(return_value('id_active_period_end') == '22:00:00')
        self.assertTrue(len(parsed_html.find_all('option')) == 6)
        self.assertTrue(return_value('id_dose_time') == '08:00:00')
