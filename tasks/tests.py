from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task
from django.contrib.auth.models import Group


class TaskAPITestCase(TestCase):
    def setUp(self):
        # Создаём пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

        # Создаём тестовые задачи
        self.task1 = Task.objects.create(
            user=self.user, 
            title='Test Task 1', 
            description='Description 1', 
            priority=1, 
            status='new'
        )
        self.task2 = Task.objects.create(
            user=self.user, 
            title='Test Task 2', 
            description='Description 2', 
            priority=2, 
            status='completed'
        )

        # URL-адреса
        self.list_url = '/api/tasks/'
        self.detail_url = f'/api/tasks/{self.task1.id}/'

    def test_list_tasks(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task(self):
        data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'priority': 3,
            'status': 'in_progress',
            'category': 'Work'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_retrieve_task(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task 1')

    def test_update_task(self):
        data = {'title': 'Updated Task'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')

    def test_delete_task(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_filter_by_status(self):
        response = self.client.get(self.list_url, {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task 2')

    def test_search_by_title(self):
        response = self.client.get(self.list_url, {'search': 'Task 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task 1')


class UserRoleTestCase(TestCase):
    def setUp(self):
        # Явно создаём группы в тестовой базе данных
        self.admin_group, _ = Group.objects.get_or_create(name='Администратор')
        self.user_group, _ = Group.objects.get_or_create(name='Обычный пользователь')

        # Создаем администратора и пользователя
        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.user = User.objects.create_user(username='user', password='userpass')

        # Назначаем роли
        self.admin_user.groups.add(self.admin_group)
        self.user.groups.add(self.user_group)

        # API клиент
        self.client = APIClient()

    def test_admin_access(self):
        # Авторизация администратора
        self.client.login(username='admin', password='adminpass')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_access(self):
        # Авторизация обычного пользователя
        self.client.login(username='user', password='userpass')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # У пользователя пока нет задач




