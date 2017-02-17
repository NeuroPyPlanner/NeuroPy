"""Views allowing the user to interact with their own todo items."""

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        # PermissionRequiredMixin,
                                        UserPassesTestMixin,
                                        )
from todo.models import Todo
from medication.models import Medication
from userprofile.models import Profile
from todo.forms import TodoForm
from django.shortcuts import get_object_or_404
from apiclient import discovery
import datetime
import dateutil.parser
from userprofile.models import CredentialsModel
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib import xsrfutil
import httplib2
import os
from neuropy import settings
from oauth2client.client import flow_from_clientsecrets


class AddTodo(LoginRequiredMixin, CreateView):
    """Add todo."""

    login_url = reverse_lazy('login')
    login_required = True

    model = Todo
    template_name = "todo/add_todo.html"

    form_class = TodoForm

    success_url = reverse_lazy('list_todo')

    def form_valid(self, form):
        """Form should update the photographer to the user."""
        self.object = form.save(commit=False)
        self.object.owner = Profile.objects.get(user=self.request.user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EditTodo(LoginRequiredMixin, UpdateView):
    """Edit todo."""

    # permission_required = "todo.change_todo"
    login_required = True

    model = Todo
    template_name = "todo/edit_todo.html"

    form_class = TodoForm

    success_url = reverse_lazy('list_todo')


class ListTodo(LoginRequiredMixin, ListView):
    """Lists the todo items attached to a specific user."""

    login_url = reverse_lazy('login')
    login_required = True
    template_name = "todo/list_todo.html"
    model = Todo

    def get_context_data(self):
        """Return a dict of all todos, filtering out todos."""
        the_user = self.request.user
        owned_todos = Todo.objects.filter(owner=the_user.profile)
        return {'todos': owned_todos}


class DetailTodo(UserPassesTestMixin, DetailView):
    """Allow user to view details on a specific todo list item."""

    login_url = reverse_lazy('login')
    login_required = True
    model = Todo
    template_name = "todo/detail_todo.html"

    def test_func(self):
        """Override the userpassestest test_func."""
        todo = get_object_or_404(Todo, id=self.kwargs['pk'])
        return todo.owner.user == self.request.user


def calendar_get(http, date):
    """Get and return users calendar."""
    year, month, day, = date.split('-')
    start = datetime.date(
        year=int(year), month=int(month), day=int(day)
    ).isoformat() + 'T00:00:01-08:00'
    end = datetime.date(
        year=int(year), month=int(month), day=int(day)
    ).isoformat() + 'T23:59:59-08:00'
    service = discovery.build('calendar', 'v3', http=http)
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime',
        timeZone='PST'
    ).execute()
    return events_result.get('items', [])


def calender_insert(http, event):
    """Insert entries and calender."""
    service = discovery.build('calendar', 'v3', http=http)
    event = service.events().insert(calendarId='prmary', body=event).execute()
    return event


def calender_update(http, event):
    """Insert entries and calender."""
    service = discovery.build('calendar', 'v3', http=http)
    event = service.events().update(calendarId='prmary', body=event).execute()
    return event

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'neuropy', 'client_secret.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://localhost:8000/oauth2callback'
)


def create_event_list(drug_name, profile):
    """Create dictionary objects to be inserted into google cal."""
    today = datetime.date.today()

    easy = Todo.objects.filter(owner=profile, date=today, ease=1)
    medium = Todo.objects.filter(owner=profile, date=today, ease=2)
    hard = Todo.objects.filter(owner=profile, date=today, ease=3)
    priority_now = Todo.objects.filter(owner=profile, date=today, priority=4).order_by('ease')
    bucket_list = [priority_now, hard, medium, easy]

    today = datetime.date.today()
    start_time = datetime.datetime(today.year, today.month, today.day, 9)

    def td(time):
        pt = datetime.datetime.strptime(time, '%H:%M:%S')
        return pt.second + pt.minute + pt.hour * 3600

    drug = Medication.objects.get(name=drug_name)
    peak_end = start_time + datetime.timedelta(hours=td(drug.peak_end))
    # medium_start = start_time + datetime.timedelta(hours=td(drug.post_peak_medium_start))
    easy_start = start_time + datetime.timedelta(hours=td(drug.post_peak_easy_start))

    events_list = []
    for idx, bucket in enumerate(bucket_list):
        priority_dict = {}

        for event in bucket:
            priority_dict['description'] = event.description
            priority_dict['title'] = event.title
            priority_dict['start'] = start_time
            end_time = start_time + datetime.timedelta(hours=event.duration)
            priority_dict['end'] = end_time

            if idx == 0 or idx == 1:
                priority_dict['ease'] = 'hard'

            if idx == 2 and priority_dict['start'] < peak_end:
                priority_dict['ease'] = 'hard'

            elif idx == 3 and priority_dict['start'] < easy_start:
                priority_dict['ease'] = 'medium'

            priority_dict['start'] = start_time.strftime("%H:%M")
            priority_dict['end'] = end_time.strftime("%H:%M")
            events_list.append(dict(priority_dict))

            start_time = start_time + datetime.timedelta(hours=event.duration)
        print('priority_dict: ', priority_dict)
    return events_list


class ScheduleView(LoginRequiredMixin, TemplateView):
    """Schedule View."""

    template_name = "todo/schedule_view.html"

    def get(self, request, *args, **kwargs):
        """Get the data and render."""
        context = self.get_context_data(**kwargs)
        storage = DjangoORMStorage(CredentialsModel, 'user_id', request.user, 'credential')
        credential = storage.get()
        if credential is None or credential.invalid:
            FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                           request.user)
            authorize_url = FLOW.step1_get_authorize_url()
            return HttpResponseRedirect(authorize_url)
        else:
            http = httplib2.Http()
            http = credential.authorize(http)
            now = str(datetime.datetime.now()).split()[0]
            events = calendar_get(request.oauth.http, now)
            context["events"] = events
            for event in events:
                try:
                    event["start"]["dateTime"] = dateutil.parser.parse(event["start"]["dateTime"])
                except KeyError:
                    event["start"]["dateTime"] = 'No Time Specified'
                try:
                    event["end"]["dateTime"] = dateutil.parser.parse(event["end"]["dateTime"])
                except KeyError:
                    event["end"]["dateTime"] = 'No Time Specified'
            return self.render_to_response(context)


class CreateScheduleView(LoginRequiredMixin, TemplateView):
    """Prioritized Schedule View."""

    template_name = "todo/create_schedule.html"

    def get(self, request, *args, **kwargs):
        """."""
        priority_list = self.request.session['some_list']
        context = self.get_context_data(**kwargs)
        context['todos'] = priority_list

        return self.render_to_response(context)
