"""Tests for medication app."""

from django.test import TestCase
from medication.models import Medication
import factory
import datetime


class MedicationFactory(factory.django.DjangoModelFactory):
    """Create test instance of todos."""

    class Meta:
        """Invoke Todo instance using Todo model class."""

        model = Medication

    name = 'CONCERTA'
    med_type = 'stimulant'
    treating_dis = 'ADD/ADHD'
    half_life = datetime.timedelta(hours=3, minutes=30)  # 03:30:00
    ramp_up = datetime.timedelta(hours=4, minutes=30)  # 04:30:00
    peak_period = datetime.timedelta(hours=7)  # 07:00:00


class MedicationTestCase(TestCase):
    """Test the Medication model."""

    def setUp(self):
        """Setup for medications."""
        self.medications = [MedicationFactory.create() for i in range(10)]

    def test_name(self):
        """Test that a medication instance has a name."""
        medication = self.medications[1]
        medication = Medication.objects.get(id=medication.id)
        self.assertTrue(medication.name == "CONCERTA")

    def test_treating_disorder(self):
        """Test that a medication instance has a name."""
        medication = self.medications[1]
        medication = Medication.objects.get(id=medication.id)
        self.assertTrue(medication.treating_dis == "ADD/ADHD")

    def test_med_type(self):
        """Test medication instance type."""
        medication = self.medications[1]
        medications = Medication.objects.get(id=medication.id)
        self.assertTrue(medication.med_type == "stimulant")

    def test_change_data(self):
        """Test Editing medication data."""
        medication = self.medications[1]
        medication = Medication.objects.get(id=medication.id)
        medication.peak_period = datetime.timedelta(hours=10)
        medication.save()
        medication = Medication.objects.get(id=medication.id)
        self.assertTrue(medication.peak_period == datetime.timedelta(hours=10))

    def test_delete_med(self):
        """Test fetching medication after delete throws an exception."""
        medication = self.medications[1]
        medication = Medication.objects.get(id=medication.id)
        medication.delete()
        with self.assertRaises(Medication.DoesNotExist):
            Medication.objects.get(id=medication.id)
