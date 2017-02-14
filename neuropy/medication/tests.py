"""Tests for medication app."""

from django.test import TestCase
from medication.models import Medication
import datetime


class MedicationTestCase(TestCase):
    """Test the Medication model."""

    def medication_instance(self):
        """Create An Instance of a Medication and Save to DB."""
        name = 'CONCERTA',
        med_type = 'stimulant',
        treating_dis = 'ADD/ADHD',
        half_life = datetime.timedelta(hours=3, minutes=30),  # 03:30:00
        ramp_up = datetime.timedelta(hours=4, minutes=30),  # 04:30:00
        peak_period = datetime.timedelta(hours=7),  # 07:00:00

        objects = Medication.objects.create(
            name=name,
            med_type=med_type,
            treating_dis=treating_dis,
            half_life=half_life,
            ramp_up=ramp_up,
            peak_period=peak_period
        )

        objects.save()
        return objects.id

    def test_name(self):
        """Test that a medication instance has a name."""
        #med_id = self.medication_instance()
        medication = Medication.objects.get(name="CONCERTA")
        self.assertTrue(medication.name == "CONCERTA")

    def test_med_type(self):
        """Test medication instance type."""
        #med_id = self.medication_instance()
        medications = Medication.objects.filter(med_type="stimulant")
        for medication in medications:
            assert medication.med_type == "stimulant"

    def test_delete_med(self):
        """Test fetching medication after delete throws an exception."""
        #med_id = self.medication_instance()
        medication = Medication.objects.get(name="CONCERTA")
        medication.delete()
        with self.assertRaises(Medication.DoesNotExist):
            Medication.objects.get(name="CONCERTA")
