from django.views.generic import detail, UpdateView
from userprofile.models import Profile
from django.urls import reverse_lazy


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
    fields = [
        'active_period_start',
        'active_period_end',
        'peak_period',
        'dose_time'
    ]
    success_url = reverse_lazy('profile')

    def get_object(self):
        """Return logged in users profile."""
        return self.request.user.profile
