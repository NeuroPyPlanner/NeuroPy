from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User, Group, Permission
from userprofile.models import Profile
import factory
from django.core.urlresolvers import reverse_lazy


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
        lambda x: '{}@cbt.com'.format(x.username.replace(" ",""))
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
        self.assertIsInstance(str(user.profile, Profile))
        self.assertTrue(hasattr(user, 'profile'))

    def test_user_in_group(self):
        """Test that created users are added to user group."""
        user = self.users[0]
        group = user.groups.first()
        self.assertTrue(group.name == 'user')

