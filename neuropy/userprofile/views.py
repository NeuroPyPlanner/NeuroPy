from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

PROFILE_TEMPLATE_PATH = "userprofile/profile.html"


class Profile(LoginRequiredMixin, ListView):
    """View for the user's own profile."""

    login_url = reverse_lazy('login')

    model = User
    template_name = PROFILE_TEMPLATE_PATH


class EditProfile(PermissionRequiredMixin, UpdateView):
    """Allows the User to edit their profile."""

    permission_required = "userprofile.change_profile"

    template_name = "userprofile/edit_album.html"
    model = Profile
    fields = ['active_period_start', 'active_period_end', 'peak_period', 'dose_time']
    success_url = reverse_lazy('userprofile:profile')
