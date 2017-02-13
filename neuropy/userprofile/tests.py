"""Tests for the imager_profile app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
import factory
from bs4 import BeautifulSoup


class UserFactory(factory.django.DjangoModelFactory):
    """Makes users."""

    class Meta:
        """Meta."""

        model = User

    username = factory.Sequence(lambda n: "Prisoner_number_{}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
    )


class FrontendTestCases(TestCase):
    """Test the frontend of the imager_profile site."""

    def setUp(self):
        """Set up client and request factory."""
        self.client = Client()
        self.request = RequestFactory()

    def test_home_route_templates(self):
        """Test the home route templates are correct."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "neuropy/base.html")
        self.assertTemplateUsed(response, "neuropy/home.html")

    def test_login_redirect_code(self):
        """Test built-in login route redirects properly."""
        user_register = UserFactory.create()
        user_register.is_active = True
        user_register.username = "username"
        user_register.set_password("potatoes")
        user_register.save()
        response = self.client.post("/login/", {
            "username": user_register.username,
            "password": "potatoes"

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
