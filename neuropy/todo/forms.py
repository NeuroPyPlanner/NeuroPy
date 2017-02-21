"""Form module."""

from django import forms
from todo.models import Todo


class TodoForm(forms.ModelForm):
    """Update form for users profile."""

    def __init__(self, *args, **kwargs):
        """Setup the form fields to include User properties."""
        super(TodoForm, self).__init__(*args, **kwargs)

        PRIORITY_CHOICES = (
            (4, 'Now'),
            (3, 'Urgent'),
            (2, 'Semi Urgent'),
            (1, 'Non Urgent'),
        )

        EASE_CHOICES = (
            (3, 'Difficult'),
            (2, 'Medium'),
            (1, 'Easy'),
        )
        self.fields['title'] = forms.CharField(initial=self.instance.title)
        self.fields['description'] = forms.CharField(widget=forms.Textarea, initial=self.instance.description)
        self.fields['date'] = forms.DateField(widget=forms.SelectDateWidget(), initial=self.instance.date)
        self.fields['duration'] = forms.IntegerField(min_value=1, initial=self.instance.duration)
        self.fields['ease'] = forms.ChoiceField(choices=EASE_CHOICES)
        self.fields['priority'] = forms.ChoiceField(choices=PRIORITY_CHOICES)

    class Meta:
        """Model for form and fields to exclude."""

        model = Todo
        exclude = ['owner', 'start_time', 'end_time']
