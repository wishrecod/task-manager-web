from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Создание групп пользователей"

    def handle(self, *args, **kwargs):
        # Создаем группы
        admin_group, created_admin = Group.objects.get_or_create(name='Администратор')
        user_group, created_user = Group.objects.get_or_create(name='Обычный пользователь')

        if created_admin:
            self.stdout.write(self.style.SUCCESS('Группа "Администратор" успешно создана!'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Администратор" уже существует.'))

        if created_user:
            self.stdout.write(self.style.SUCCESS('Группа "Обычный пользователь" успешно создана!'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Обычный пользователь" уже существует.'))

        self.stdout.write(self.style.SUCCESS("Группы успешно обработаны!"))
