"""Views for profile."""
from django.views.generic import detail, UpdateView
from userprofile.models import Profile
from django.urls import reverse_lazy
from userprofile.forms import ProfileForm
from django.http import HttpResponseRedirect


class ProfileView(detail.DetailView):
    """View for profle."""

    model = Profile
    template_name = 'userprofile/profile.html'
    slug_field = 'id'

    def get_object(self):
        """Return logged in user."""
        return self.request.user


class EditProfile(UpdateView):
    """Add Album."""

    template_name = 'userprofile/edit_profile.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        """Return logged in users profile."""
        return self.request.user.profile

    def form_valid(self, form):
        """Save object after post."""
        self.object = form.save()
        self.object.user.first_name = form.cleaned_data['First Name']
        self.object.user.last_name = form.cleaned_data['Last Name']
        self.object.user.email = form.cleaned_data['Email']
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
