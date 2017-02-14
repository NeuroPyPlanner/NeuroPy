"""Views allowing the user to interact with their own todo items."""

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from todo.models import Todo


class AddTodo(PermissionRequiredMixin, CreateView):
    """Add todo."""

    login_url = reverse_lazy('login')
    permission_required = "imager_images.add_todo"

    model = Todo
    template_name = "imager_images/add_todo.html"

    fields = [
        'title', 'description', 'date', 'duration', 'ease', 'priority', 'owner'
    ]
    success_url = reverse_lazy('todo:list_todos')

    def form_valid(self, form):
        """Form validation for adding a todo."""
        form.instance.user = self.request.user
        return super(AddTodo, self).form_valid(form)


class EditTodo(PermissionRequiredMixin, UpdateView):
    """Edit todo."""

    permission_required = "imager_images.change_todo"

    model = Todo
    template_name = "imager_images/add_todo.html"

    fields = ['title', 'description', 'date', 'duration', 'ease', 'priority']
    success_url = reverse_lazy('todo:list_todos')


class ListTodo(LoginRequiredMixin, ListView):
    """Lists the todo items attached to a specific user."""

    login_url = reverse_lazy('login')

    template_name = "todo/list_todo.html"

    def get_context_data(self):
        owned_todos = []
        todo_items = Todo.objects.all()
        for item in todo_items:
            if todo.owner.user.username == self.request.user.username:
                owned_todos.append(item)
        return {'todos': owned_todos}
