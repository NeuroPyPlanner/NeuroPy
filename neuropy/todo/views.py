"""Views allowing the user to interact with their own todo items."""

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from todo.models import Todo
from userprofile.models import Profile


class AddTodo(LoginRequiredMixin, CreateView):
    """Add todo."""

    login_url = reverse_lazy('login')
    login_required = True

    model = Todo
    template_name = "todo/add_todo.html"

    fields = [
        'title', 'description', 'date', 'duration', 'ease', 'priority'
    ]
    success_url = reverse_lazy('todo:list_todo')

    def form_valid(self, form):
        """Form should update the photographer to the user."""
        self.object = form.save(commit=False)
        self.object.owner = Profile.objects.get(user=self.request.user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EditTodo(PermissionRequiredMixin, UpdateView):
    """Edit todo."""

    permission_required = "todo.change_todo"

    model = Todo
    template_name = "todo/add_todo.html"

    fields = ['title', 'description', 'date', 'duration', 'ease', 'priority']
    success_url = reverse_lazy('todo:list_todo')


class ListTodo(LoginRequiredMixin, ListView):
    """Lists the todo items attached to a specific user."""

    login_url = reverse_lazy('login')

    template_name = "todo/list_todo.html"

    def get_context_data(self):
        """Return a dict of all todos, filtering out todos belonging to other users."""
        owned_todos = []
        todo_items = Todo.objects.all()
        for item in todo_items:
            if Todo.owner.user.username == self.request.user.username:
                owned_todos.append(item)
        return {'todos': owned_todos}


class DetailTodo(LoginRequiredMixin, TemplateView):
    """Allow user to view details on a specific todo list item."""

    login_url = reverse_lazy('login')

    template_name = "todo/detail_todo.html"

    def get_context_data(self):
        """Return a specific todo list itme attached to the logged in user."""
        todo_item = Todo.objects.get(id=self.kwargs['todo_id'])
        if todo_item.owner.user.username == self.request.user.username:
            return {'todo': todo_item}
        return HttpResponseForbidden('Unauthorized')
