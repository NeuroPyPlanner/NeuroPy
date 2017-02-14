"""Todo url paths."""
from django.conf.urls import url, include
from imager_images.models import Todo
from imager_images.views import AddTodo, EditTodo
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^todo/(?P<pk>\d+)/edit/$', EditTodo.as_view(), name='edit_todo'),
    url(r'^todo/(?P<todo_id>\d+)', TodoView.as_view(), name='show_todo'),
    url(r'^todo/add/$', AddTodo.as_view(), name='add_todo'),
    url(r'^todos/$', TodoCollectionView.as_view(), name='list_todos'),
    url(r'', include('two_factor.urls', 'two_factor')),
]
