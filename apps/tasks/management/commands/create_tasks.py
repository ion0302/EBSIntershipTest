import random

from django.contrib.auth.models import User

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from apps.tasks.models import Task


class Command(BaseCommand):
    help = 'Create random tasks'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of tasks to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        users_id = list(User.objects.values_list('id', flat=True))
        if users_id:
            for i in range(total):
                Task.objects.create(title=get_random_string(length=15),
                                    description=get_random_string(length=200),
                                    created_by_id=random.choice(users_id),
                                    assigned_to_id=random.choice(users_id),
                                    is_completed=random.choice([True, False]))
            self.stdout.write(self.style.SUCCESS('Successfully added tasks'))
