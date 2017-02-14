"""Views allowing the user to interact with their own todo items."""

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from todo.models import Todo
from django import forms
from userprofile.models import Profile


class AddTodo(LoginRequiredMixin, CreateView):
    """Add todo."""

    login_url = reverse_lazy('login')
    login_required = True

    model = Todo
    template_name = "todo/add_todo.html"

    class AddForm(forms.Form):
        """Tweak the add todo form to include a SelectDateWidget."""

        title = forms.CharField()
        description = forms.TextField()
        date = forms.DateField(widget=forms.SelectDateWidget())
        duration = forms.PositiveIntegerField()
        ease = forms.PositiveIntegerField()
        priority = forms.PositiveIntegerField()

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

    class EditForm(forms.Form):
        """Tweak the edit todo form to include a SelectDateWidget."""

        title = forms.CharField()
        description = forms.TextField()
        date = forms.DateField(widget=forms.SelectDateWidget())
        duration = forms.PositiveIntegerField()
        ease = forms.PositiveIntegerField()
        priority = forms.PositiveIntegerField()

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


class DetailTodo(LoginRequiredMixin, TemplateView):
    """Allow user to view details on a specific todo list item."""

    login_url = reverse_lazy('login')
    login_required = True

    template_name = "todo/detail_todo.html"

    def get_context_data(self):
        """Return a specific todo list itme attached to the logged in user."""
        todo_item = Todo.objects.get(id=self.kwargs['todo_id'])
        if todo_item.owner.user.username == self.request.user.username:
            return {'todo': todo_item}
        return HttpResponseForbidden('Unauthorized')
