"""Medication model- no user relation."""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import validate_comma_separated_integer_list


@python_2_unicode_compatible
class Medication(models.Model):
    """Medication instace class."""

    name = models.CharField(
        max_length=20,
        default='CONCERTA')
    med_type = models.CharField(max_length=20, default='stimulant')
    treating_dis = models.CharField(max_length=25, default='ADD/ADHD')
    half_life = models.DurationField()
    ramp_up = models.DurationField()
    peak_period = models.DurationField()
    easy_start = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    easy_end = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    medium_start = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    medium_end = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    peak_start = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    peak_end = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    post_peak_medium_start = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    post_peak_medium_end = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    post_peak_easy_start = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    post_peak_easy_end = models.CharField(validators=[validate_comma_separated_integer_list], max_length=50)
    # Ease_priority_matrix=models.CharField

    def __str__(self):
        """String representation of Medication."""
        return self.name
