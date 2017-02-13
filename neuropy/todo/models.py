"""Model for users todos."""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from userprofile.models import UserProfile


@python_2_unicode_compatible
class Todo(models.Model):
    """Model for an individual Todo."""

    PRIORITY_CHOICES = (
        (1, 'Now'),
        (2, 'Urgent'),
        (3, 'Semi Urgent'),
        (4, 'Non Urgent'),
    )

    EASE_CHOICES = (
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Difficult'),
    )

    self.title = models.CharField()
    self.description =
    self.date = 
    self.duration = models.IntegerField(blank=True, null=True)
    self.ease = models.IntegerField(choices=EASE_CHOICES)
    self.priority = models.IntegerField(choices=PRIORITY_CHOICES)
    self.owner =  models.ForeignKey(UserProfile,
                                     related_name='todo',
                                     blank=True,
                                     null=True
                                     )

    def __str__(self):
        """String representation of Todo."""
        return self.title