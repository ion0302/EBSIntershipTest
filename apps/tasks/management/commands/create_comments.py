import random
from itertools import islice

from faker import Faker

from django.core.management.base import BaseCommand

from apps.tasks.models import Task, Comment


class Command(BaseCommand):
    help = 'Create random commentaries'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of comments to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        tasks_id = list(Task.objects.values_list('id', flat=True))

        if tasks_id:
            batch_size = total
            objs = (Comment(task_id=random.choice(tasks_id),
                            text=fake.text()) for i in range(total))
            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                Comment.objects.bulk_create(batch, batch_size)

            self.stdout.write(self.style.SUCCESS('Successfully added comments'))
