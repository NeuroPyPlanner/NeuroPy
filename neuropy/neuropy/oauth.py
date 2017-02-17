"""Code for return auth."""
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.contrib.auth.decorators import login_required
from oauth2client.client import OAuth2WebServerFlow
from userprofile.models import CredentialsModel
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from oauth2client.contrib import xsrfutil
from neuropy import settings

FLOW = OAuth2WebServerFlow(
    client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://localhost:8000/oauth2callback',
    prompt='consent'
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
