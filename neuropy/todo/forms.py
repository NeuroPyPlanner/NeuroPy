"""Form module."""

from django import forms
from todo.models import Todo


class TodoForm(forms.ModelForm):
    """Update form for users profile."""

    def __init__(self, *args, **kwargs):
        """Setup the form fields to include User properties."""
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
        import pdb; pdb.set_trace()
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField(initial=self.instance.user.profile.todo.title)
        self.fields['description'] = forms.CharField(widget=forms.Textarea, initial=self.instance.user.profile.todo.description)
        self.fields['date'] = forms.DateField(widget=forms.SelectDateWidget(), initial=self.instance.user.profile.todo.date)
        self.fields['duration'] = forms.IntegerField(min_value=1, initial=self.instance.user.profile.todo.duration)
        self.fields['ease'] = forms.ChoiceField(choices=EASE_CHOICES)
        self.fields['priority'] = forms.ChoiceField(choices=PRIORITY_CHOICES)

    class Meta:
        """Model for form and fields to exclude."""

        model = Todo
        exclude = []
