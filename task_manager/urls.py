from django.contrib import admin
from django.urls import path, include
from tasks.views import signup
from tasks import views as task_views
from tasks.views import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('', task_views.task_list, name='task_list'),
    path('tasks/create/', task_views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', task_views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', task_views.task_delete, name='task_delete'),
    path('api/tasks/', TaskListCreateAPIView.as_view(), name='api_task_list_create'),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='api_task_detail'),
]