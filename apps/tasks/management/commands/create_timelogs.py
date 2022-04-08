import random
from itertools import islice

from datetime import timedelta

from django.contrib.auth.models import User

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.tasks.models import Task, TimeLog


class Command(BaseCommand):
    help = 'Create random timelogs'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of timelogs to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        users_id = list(User.objects.values_list('id', flat=True))
        tasks_id = list(Task.objects.values_list('id', flat=True))
        if users_id and tasks_id:
            batch_size = total
            objs = (TimeLog(task_id=random.choice(tasks_id),
                            user_id=random.choice(users_id),
                            started_at=timezone.now()-timedelta(hours=i),
                            duration=timedelta(minutes=random.randint(20, 1000))) for i in range(total))
            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                TimeLog.objects.bulk_create(batch, batch_size)

            self.stdout.write(self.style.SUCCESS('Successfully added timelogs'))
