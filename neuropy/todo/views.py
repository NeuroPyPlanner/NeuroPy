from django.shortcuts import render

class AddTodo(PermissionRequiredMixin, CreateView):
    """Add todo."""

    login_url = reverse_lazy('login')
    permission_required = "imager_images.add_todo"

    model = todo
    template_name = "imager_images/add_todo.html"

    fields = ['title', 'description', 'date', 'duration', 'ease', 'priority', 'owner']
    success_url = reverse_lazy('todo')

    def form_valid(self, form):
        """Form validation for adding a todo."""
        form.instance.user = self.request.user
        return super(Addtodo, self).form_valid(form)


class EditTodo(PermissionRequiredMixin, UpdateView):
    """Edit todo."""

    permission_required = "imager_images.change_todo"

    model = todo
    template_name = "imager_images/add_todo.html"

    fields = ['title', 'description', 'date', 'duration', 'ease', 'priority']
    success_url = reverse_lazy('library')
