"""Code for return auth."""
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.contrib.auth.decorators import login_required
from oauth2client.client import flow_from_clientsecrets
from userprofile.models import CredentialsModel
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from oauth2client.contrib import xsrfutil
from neuropy import settings
import os


CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secret.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://ec2-52-14-126-118.us-east-2.compute.amazonaws.com/oauth2callback'
)


@login_required
def auth_return(request):
    """Oauth return view."""
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.GET['state'],
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET['code'])
    storage = DjangoORMStorage(CredentialsModel, 'user_id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/")
