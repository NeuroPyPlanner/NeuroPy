"""Form module."""

from django import forms
from userprofile.models import Profile
from medication.models import Medication


class ProfileForm(forms.ModelForm):
    """Update form for users profile."""

    def __init__(self, *args, **kwargs):
        """Setup the form fields to include User properties."""
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["First Name"] = forms.CharField(
            initial=self.instance.user.first_name)
        self.fields["Last Name"] = forms.CharField(
            initial=self.instance.user.last_name)
        self.fields["Email"] = forms.EmailField(
            initial=self.instance.user.email)
        del self.fields["user"]

    class Meta:
        """Model for form and fields to exclude."""

        model = Profile
        exclude = []


class MedicationForm(forms.ModelForm):
    """Create a form allowing the user to base the schedule on a medication."""

    def __init__(self, *args, **kwargs):
        """Set up form fields."""
        MEDICATION_CHOICES = (
            ("CONCERTA", "Concerta"),
            ("ADDERALL", "Adderall"),
            ("FOCALIN", "Focalin"),
            ("Ritalin LA", "Ritalin LA"),
            ("Vyvanse", "Vyvanse")
        )
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["Medication: "] = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=MEDICATION_CHOICES,
        )

    class Meta:
        """Model for form and fields to exclude."""

        model = Medication
        exclude = []