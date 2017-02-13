"""Profile urls."""
from django.conf.urls import url
from .views import ProfileView, EditProfile
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^edit/$', login_required(EditProfile.as_view()), name='edit-profile'),
    url(r'^$', login_required(ProfileView.as_view()), name='profile')
]
