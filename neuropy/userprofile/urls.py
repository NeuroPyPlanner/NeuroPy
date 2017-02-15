"""Profile urls."""
from django.conf.urls import url
from .views import ProfileView, EditProfile

urlpatterns = [
    url(r'^edit/$', EditProfile.as_view(), name='edit-profile'),
    url(r'^$', ProfileView.as_view(), name='profile')
]
