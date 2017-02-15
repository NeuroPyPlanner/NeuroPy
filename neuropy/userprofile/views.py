"""Views for profile."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, FormView
from userprofile.forms import ProfileForm, MedicationForm
from userprofile.models import Profile


class ProfileView(LoginRequiredMixin, DetailView):
    """View for profile."""

    login_required = True
    model = Profile
    template_name = 'userprofile/profile.html'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        """Attach form to detail view page."""
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['form'] = MedicationForm
        return context

    def get_object(self):
        """Return logged in user."""
        return self.request.user


class ProfileFormView(LoginRequiredMixin, FormView):
    """Form view for reference by profile view so we can include a form."""

    form_class = MedicationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        """When medication is chosen, schedule the user's todos."""
        return HttpResponseRedirect(self.get_success_url())

    def todo_buckets(self):
        """Take all the user's todo items and sorts them by ease/priority."""


class EditProfile(LoginRequiredMixin, UpdateView):
    """Edit users profile."""

    login_required = True
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
