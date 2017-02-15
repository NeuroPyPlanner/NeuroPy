from django.contrib import admin
from userprofile.models import CredentialsModel
from userprofile.models import Profile

admin.site.register(CredentialsModel)
admin.site.register(Profile)
