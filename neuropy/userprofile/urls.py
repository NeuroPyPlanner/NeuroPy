"""Profile urls."""
from django.conf.urls import url
from django.views.decorators.http import require_POST
from .views import ProfileView, EditProfile, ProfileFormView

urlpatterns = [
    url(r'^edit/$', EditProfile.as_view(), name='edit-profile'),
    url(r'^$', ProfileView.as_view(), name='profile'),
    url(r'submission_form/$', require_POST(ProfileFormView.as_view()), name='profile_form')
]
