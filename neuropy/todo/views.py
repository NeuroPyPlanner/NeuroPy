"""Views allowing the user to interact with their own todo items."""

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        # PermissionRequiredMixin,
                                        UserPassesTestMixin,
                                        )
from todo.models import Todo
from todo.forms import TodoForm
from userprofile.models import Profile
from django.shortcuts import get_object_or_404
from apiclient import discovery
import datetime
import dateutil.parser


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


class ScheduleView(TemplateView):
    """Schedule View."""

    template_name = "todo/schedule_view.html"

    def get(self, request, *args, **kwargs):
        """Get the data and render."""
        context = self.get_context_data(**kwargs)
        if request.oauth.has_credentials() and not request.oauth.credentials.access_token_expired:
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
        else:
            return HttpResponseRedirect(request.oauth.get_authorize_redirect())
