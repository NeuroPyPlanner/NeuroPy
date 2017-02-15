"""Todo model for admin."""

from django.contrib import admin
from todo.models import Todo


# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    """Display list for admin."""

    list_display = ("title", "description", "date")

admin.site.register(Todo, TodoAdmin)
