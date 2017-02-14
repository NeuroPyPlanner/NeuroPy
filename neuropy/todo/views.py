"""Views allowing the user to interact with their own todo items."""

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        # PermissionRequiredMixin,
                                        UserPassesTestMixin,
                                        )
from todo.models import Todo
from todo.forms import TodoForm
from userprofile.models import Profile
from django.shortcuts import get_object_or_404


class AddTodo(LoginRequiredMixin, CreateView):
    """Add todo."""

    login_url = reverse_lazy('login')
    login_required = True

    model = Todo
    template_name = "todo/add_todo.html"

    form_class = TodoForm

    success_url = reverse_lazy('todo:list_todo')

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
    template_name = "todo/add_todo.html"

    form_class = TodoForm

    success_url = reverse_lazy('todo:list_todo')


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
