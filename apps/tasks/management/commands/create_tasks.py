import random
from itertools import islice

from faker import Faker

from django.contrib.auth.models import User

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from apps.tasks.models import Task


class Command(BaseCommand):
    help = 'Create random tasks'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of tasks to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        users_id = list(User.objects.values_list('id', flat=True))
        if users_id:
            batch_size = total
            objs = (Task(title=fake.name(),
                         description=fake.text(),
                         assigned_to_id=random.choice(users_id),
                         created_by_id=random.choice(users_id)) for i in range(total))
            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                Task.objects.bulk_create(batch, batch_size)

            self.stdout.write(self.style.SUCCESS('Successfully added tasks'))
