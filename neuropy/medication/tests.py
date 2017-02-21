"""Tests for medication app."""

from django.test import TestCase
from medication.models import Medication
import factory
import datetime


class MedicationTestCase(TestCase):
    """Test the Medication model."""

    def setUp(self):
        """Setup for medications."""
        self.medications = [medication for medication in Medication.objects.all()]

    def test_all_meds_are_present(self):
        """Test top all ADHD medications are present."""
        self.assertTrue(self.medications[0].name == 'CONCERTA')
        self.assertTrue(self.medications[1].name == 'ADDERALL')
        self.assertTrue(self.medications[2].name == 'Focalin')
        self.assertTrue(self.medications[3].name == 'Ritalin LA')
        self.assertTrue(self.medications[4].name == 'Vyvanse')

    def test_medication1_info_is_correct(self):
        """Test that a medication instance has a name."""
        med1 = self.medications[0]
        self.assertTrue(med1.name == "CONCERTA")
        self.assertTrue(med1.med_type == 'stimulant')
        self.assertTrue(med1.treating_dis == 'ADD/ADHD')
        self.assertTrue(med1.half_life == datetime.timedelta(hours=3, minutes=30))
        self.assertTrue(med1.ramp_up == datetime.timedelta(hours=3, minutes=30))

    def test_treating_disorder_are_all_same(self):
        """Test that a medication instance has a name."""
        for medication in self.medications:
            self.assertTrue(medication.treating_dis == "ADD/ADHD")

    def test_med_type_are_all_same(self):
        """Test medicatcion instance type."""
        for medication in self.medications:
            self.assertTrue(medication.med_type == "stimulant")

    def test_no_dupelicate_medication(self):
        """Test that there are no duplicates of a medication."""
        seen_meds = []
        for medication in self.medications:
            if medication in seen_meds:
                raise ValueError("Medication already exists")
            else:
                seen_meds.append(medication)
        return seen_meds

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
