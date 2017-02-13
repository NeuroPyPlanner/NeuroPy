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
