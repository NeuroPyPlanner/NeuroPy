"""Views allowing the user to interact with their own todo items."""

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        # PermissionRequiredMixin,
                                        UserPassesTestMixin,
                                        )
from todo.models import Todo
from medication.models import Medication
from userprofile.models import Profile
from todo.forms import TodoForm
from userprofile.models import Profile
from django.shortcuts import get_object_or_404
from apiclient import discovery
import datetime


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


def calendar_get(http, now=datetime.datetime.utcnow().isoformat() + 'Z'):
    """Get and return users calendar."""
    service = discovery.build('calendar', 'v3', http=http)
    events_result = service.events().list(
        calendarId='primary', timeMin=now, singleEvents=True,
        orderBy='startTime').execute()
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


class CreateScheduleView(UserPassesTestMixin, DetailView):
    """Create schedule in order of priority."""

    login_url = reverse_lazy('login')
    login_required = True
    model = Todo
    template_name = "todo/create_schedule.html"

    def create_event_list(self, drug_name):
        """Create dictionary objects to be inserted into google cal."""
        easy = Todo.objects.filter(ease=1)
        medium = Todo.objects.filter(ease=2)
        hard = Todo.objects.filter(ease=3)
        bucket_list = [priority_now, hard, medium, easy]
        priority_now = Todo.objects.filter(priority=4).order_by('ease')

        drug = Medication.objects.filter(name=drug_name)
        post_peak_medium = drug.post_peak_medium_start
        post_peak_easy = drug.post_peak_easy_start
        today = datetime.date.today()
        start_time = datetime.datetime(today.year, today.month, today.day, 9)

        for bucket in bucket_list:
            events_list = []
            priority_dict = {}

            for event in bucket:
                priority_dict['description'] = event.description
                priority_dict['title'] = event.title
                priority_dict['start'] = start_time
                priority_dict['end'] = start_time + datetime.timedelta(hours=event.duration)

                events_list.append(dict(priority_dict))
                start_time = start_time + datetime.timedelta(hours=event.duration)

        return events_list
