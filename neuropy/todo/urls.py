"""Todo url paths."""

from django.conf.urls import url
from todo.views import(
    AddTodo, EditTodo, ListTodo, DetailTodo, ScheduleView, CreateScheduleView
)
from oauth2client.contrib.django_util import decorators

urlpatterns = [
    url(r'calendar/$', decorators.oauth_enabled(ScheduleView.as_view()), name='schedule'),
    url(r'^(?P<pk>\d+)/edit/$', EditTodo.as_view(), name='edit_todo'),
    url(r'^(?P<pk>\d+)', DetailTodo.as_view(), name='show_todo'),
    url(r'^add/$', AddTodo.as_view(), name='add_todo'),
    url(r'^$', ListTodo.as_view(), name='list_todo'),
    url(r'^schedule/$', CreateScheduleView.as_view(), name="create_sched"),
]
