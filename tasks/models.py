from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_status_color(self):
        """Возвращает цвет на основе статуса задачи."""
        if self.status == 'completed':
            return 'green' 
        elif self.status == 'in_progress':
            return 'yellow'  
        elif self.status == 'new':
            return 'red' 
        return 'black'  # По умолчанию

    def get_status_display_text(self):
        """Возвращает текстовое представление статуса с учетом выбора."""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
