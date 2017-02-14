"""Todo url paths."""

from django.conf.urls import url
from todo.views import(
    AddTodo, EditTodo, ListTodo, DetailTodo
)

urlpatterns = [
    url(r'^(?P<pk>\d+)/edit/$', EditTodo.as_view(), name='edit_todo'),
    url(r'^(?P<todo_id>\d+)', DetailTodo.as_view(), name='show_todo'),
    url(r'^add/$', AddTodo.as_view(), name='add_todo'),
    url(r'^$', ListTodo.as_view(), name='list_todo'),
]
