"""Tests for the userprofile app."""

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User, Group, Permission
from userprofile.models import Profile, CredentialsModel
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

    def test_credentials_model_has_user_id_attribute(self):
        """Test Credentials Model has user_id attribute."""
        self.assertTrue(hasattr(CredentialsModel, 'user_id'))

    def test_credentials_model_has_credential_attribute(self):
        """Test Credentials Model has credential attribute."""
        self.assertTrue(hasattr(CredentialsModel, 'credential'))


class FrontendTestCases(TestCase):
    """Test the frontend of the imager_profile site."""

    def setUp(self):
        """Set up client and request factory."""
        add_user_group()
        self.client = Client()
        self.request = RequestFactory()
        self.users = [UserFactory.create() for i in range(20)]

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

    def test_profile_route_has_all_info(self):
        """Test profile route has all info."""
        client, user = self.make_user_and_login()
        html = client.get('/profile/').content
        html = str(html)
        self.assertTrue('Bob Dole' in html)
        self.assertTrue('bobdole' in html)
        self.assertTrue('awesome@gmail.com' in html)
        self.assertTrue('8 a.m.' in html)
        self.assertTrue('10 p.m.' in html)
        self.assertTrue('Morning' in html)

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

    def test_that_edit_will_edit_the_model(self):
        """Test that edit will edit the model."""
        client, user = self.make_user_and_login()
        html = client.get('/profile/edit/').content
        html = BeautifulSoup(html, "html5lib")
        csrf = html.find("input", {"name": 'csrfmiddlewaretoken'})['value']
        client.post('/profile/edit/', {
            "csrfmiddlewaretoken": csrf,
            "First Name": "Sam",
            "Last Name": "Glad",
            "Email": "samglad@gmail.com",
            "active_period_start": "09:00:00",
            "active_period_end": "23:00:00",
            "peak_period": "early_bird",
            "dose_time": "09:00:00"
        })
        html = client.get('/profile/').content
        html = str(html)
        self.assertTrue('Sam Glad' in html)
        self.assertTrue('bobdole' in html)
        self.assertTrue('samglad@gmail.com' in html)
        self.assertTrue('9 a.m.' in html)
        self.assertTrue('11 p.m.' in html)
        self.assertTrue('early_bird' in html)

    def test_edit_will_redirect_to_profile(self):
        """Test edit will redirect to profile."""
        client, user = self.make_user_and_login()
        html = client.get('/profile/edit/').content
        html = BeautifulSoup(html, "html5lib")
        csrf = html.find("input", {"name": 'csrfmiddlewaretoken'})['value']
        response = client.post('/profile/edit/', {
            "csrfmiddlewaretoken": csrf,
            "First Name": "Sam",
            "Last Name": "Glad",
            "Email": "samglad@gmail.com",
            "active_period_start": "09:00:00",
            "active_period_end": "23:00:00",
            "peak_period": "early_bird",
            "dose_time": "09:00:00"
        })
        self.assertRedirects(response, '/profile/')

    def test_profile_templates(self):
        """Test the profile templates are correct."""
        self.client.force_login(self.users[0])
        response = self.client.get(reverse_lazy('profile'))
        self.assertTemplateUsed(response, "neuropy/base.html")
        self.assertTemplateUsed(response, "neuropy/layout.html")
        self.assertTemplateUsed(response, "userprofile/profile.html")

    def test_edit_profile_templates(self):
        """Test the edit profile templates are correct."""
        self.client.force_login(self.users[0])
        response = self.client.get(reverse_lazy('edit-profile'))
        self.assertTemplateUsed(response, "neuropy/base.html")
        self.assertTemplateUsed(response, "neuropy/layout.html")
        self.assertTemplateUsed(response, "userprofile/edit_profile.html")

    def test_profile_includes_medication_table(self):
        """Test that the user profile page includes the medication table."""
        response = self.client.get(reverse_lazy('profile'))
        parsed_html = BeautifulSoup(response.content, 'html5lib')
        self.assertTrue(parsed_html.find('p').text == ' Terms of Service ')
