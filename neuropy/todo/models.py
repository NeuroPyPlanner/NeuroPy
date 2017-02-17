"""Model for users todos."""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from userprofile.models import Profile


@python_2_unicode_compatible
class Todo(models.Model):
    """Model for an individual Todo."""

    PRIORITY_CHOICES = (
        (4, 'Non Urgent'),
        (3, 'Urgent'),
        (2, 'Semi-Urgent'),
        (1, 'Now'),
    )

    EASE_CHOICES = (
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Difficult'),
    )

    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)
    duration = models.PositiveIntegerField(default=1)
    start_time = None
    end_time = None
    ease = models.PositiveIntegerField(choices=EASE_CHOICES, default=1)
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, default=4)
    owner = models.ForeignKey(Profile,
                              related_name='todo',
                              blank=True,
                              null=True
                              )

    def __str__(self):
        """String representation of Todo."""
        return self.title
