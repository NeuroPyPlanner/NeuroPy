from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Medication(models.Model):
    """."""

    name = models.CharField(
        max_length=20,
        default='CONCERTA')
    med_type = models.CharField(max_length=20, default='stimulant')
    treating_dis = models.CharField(max_length=25, default='ADD/ADHD')
    half_life = models.TimeField()
    ramp_up = models.DurationField()
    peak_period = models.DurationField()
    # Ease_priority_matrix=models.CharField

    def __str__(self):
        """."""
        return "name: {}, med_type: {}, treating_dis: {}, half_life: {}, ramp_up: {}, peak_period: {}".format(self.name, self.med_type, self.treating_dis, self.half_life, self.ramp_up, self.peak_period)
