"""Profile urls."""
from django.conf.urls import url
from .views import ProfileView, EditProfile
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(ProfileView.as_view()), name='profile')
]
