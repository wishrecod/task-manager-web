from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Task
from .forms import TaskForm
from .serializers import TaskSerializer
from django.views.generic.edit import CreateView  # Для RegisterView
from django.contrib.auth.models import User, Group  # User и Group
from rest_framework.permissions import IsAuthenticated, BasePermission  # Кастомные разрешения
from rest_framework import generics
from .filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority']
    ordering = ['due_date']  # По умолчанию задачи будут упорядочены по дате выполнения

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    




class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save()
        group, created = Group.objects.get_or_create(name='Обычный пользователь')
        user.groups.add(group)
        return super().form_valid(form)
    


class IsAdminOrOwner(BasePermission):
    """
    Кастомный класс разрешений: администратор или владелец объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Администраторы имеют полный доступ
        if request.user.groups.filter(name='Администратор').exists():
            return True
        # Обычные пользователи могут управлять только своими задачами
        return obj.user == request.user


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        # Администраторы видят все задачи
        if self.request.user.groups.filter(name='Администратор').exists():
            return Task.objects.all()
        # Обычные пользователи видят только свои задачи
        return Task.objects.filter(user=self.request.user)