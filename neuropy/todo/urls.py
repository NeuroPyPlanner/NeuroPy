"""Todo url paths."""
from django.conf.urls import url
from todo.views import(
    AddTodo, EditTodo, ListTodo, DetailTodo
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^(?P<pk>\d+)/edit/$', login_required(EditTodo.as_view()), name='edit_todo'),
    url(r'^(?P<todo_id>\d+)', login_required(DetailTodo.as_view()), name='show_todo'),
    url(r'^add/$', login_required(AddTodo.as_view()), name='add_todo'),
    url(r'^$', login_required(ListTodo.as_view()), name='list_todo'),
]
