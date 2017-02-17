"""Views for profile."""

import os
import httplib2
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, FormView
from userprofile.forms import ProfileForm, MedicationForm
from userprofile.models import Profile
from todo.views import create_event_list, calender_insert
from userprofile.models import CredentialsModel
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib import xsrfutil
from neuropy import settings
from oauth2client.client import flow_from_clientsecrets


CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'neuropy', 'client_secret.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://localhost:8000/oauth2callback'
)

class ProfileView(LoginRequiredMixin, DetailView):
    """View for profile."""

    login_required = True
    model = Profile
    template_name = 'userprofile/profile.html'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        """Attach form to detail view page."""
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['form'] = MedicationForm
        return context

    def get_object(self):
        """Return logged in user."""
        return self.request.user


class ProfileFormView(LoginRequiredMixin, FormView):
    """Form view for reference by profile view so we can include a form."""

    form_class = MedicationForm
    success_url = reverse_lazy('create_sched')

    def form_valid(self, form):
        """Return HttpResponse when valid data is posted."""
        medication = form.cleaned_data['medication']
        priority_list = create_event_list(medication.name, self.request.user.profile)

        storage = DjangoORMStorage(CredentialsModel, 'user_id', self.request.user, 'credential')
        credential = storage.get()
        if credential is None or credential.invalid:
            FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                           self.request.user)
            authorize_url = FLOW.step1_get_authorize_url()
            return HttpResponseRedirect(authorize_url)
        else:
            http = httplib2.Http()
            http = credential.authorize(http)

            for event in priority_list:
                google_event = {}
                if event['ease'] == 'easy':
                    google_event['colorId'] = 3
                elif event['ease'] == 'medium':
                    google_event['colorId'] = 2
                else:
                    google_event['colorId'] = 11

                google_event['description'] = event['description']
                google_event['summary'] = event['title']
                google_event['start'] = {'dateTime': event['start'].isoformat() + '-08:00'}
                google_event['end'] = {'dateTime': event['end'].isoformat() + '-08:00'}
                google_event['reminders'] = {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ]
                }
                calender_insert(http, google_event, self.request.user.email)
                event['start'] = event['start'].strftime("%H:%M")
                event['end'] = event['end'].strftime("%H:%M")
            return HttpResponseRedirect(reverse_lazy('schedule'))

        self.request.session['some_list'] = priority_list
        return HttpResponseRedirect(self.get_success_url())


class EditProfile(LoginRequiredMixin, UpdateView):
    """Edit users profile."""

    login_required = True
    template_name = 'userprofile/edit_profile.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        """Return logged in users profile."""
        return self.request.user.profile

    def form_valid(self, form):
        """Save object after post."""
        self.object = form.save()
        self.object.user.first_name = form.cleaned_data['First Name']
        self.object.user.last_name = form.cleaned_data['Last Name']
        self.object.user.email = form.cleaned_data['Email']
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
