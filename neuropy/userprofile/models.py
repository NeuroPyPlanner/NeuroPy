from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import time
from oauth2client.contrib.django_util.models import CredentialsField


class CredentialsModel(models.Model):
    """Google Credential Model."""

    user_id = models.OneToOneField(User)
    credential = CredentialsField()


@python_2_unicode_compatible
class Profile(models.Model):
    """The user's profile in the database."""

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )
    PEAK_PERIOD_CHOICES = [
        ('early_bird', 'Early Bird'),
        ('morning', 'Morning'),
        ('midday', 'Midday'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('night_owl', 'Night Owl'),
    ]
    active_period_start = models.TimeField(default=time(hour=8))
    active_period_end = models.TimeField(default=time(hour=22))
    peak_period = models.CharField(
        max_length=15,
        choices=PEAK_PERIOD_CHOICES,
        default='Morning'
    )
    dose_time = models.TimeField(default=time(hour=8))

    def __str__(self):
        """String representation of Todo."""
        return self.user.username


@receiver(post_save, sender=User)
def build_profile(sender, instance, **kwargs):
    """Attaches a profile to a user whenever a user is made."""
    if kwargs["created"]:
        group = Group.objects.get(name='user')
        instance.groups.add(group)
        new_profile = Profile(user=instance)
        new_profile.save()
