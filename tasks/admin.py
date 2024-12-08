from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'due_date', 'priority')
    list_filter = ('status', 'due_date', 'priority')
    search_fields = ('title', 'description')