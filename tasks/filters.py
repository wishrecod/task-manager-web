import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    due_date_min = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')
    due_date_max = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')

    class Meta:
        model = Task
        fields = ['status', 'category', 'due_date_min', 'due_date_max']
