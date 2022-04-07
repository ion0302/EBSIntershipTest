import random
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
            for i in range(total):
                TimeLog.objects.create(started_at=timezone.now() - timedelta(hours=i),
                                       duration=timedelta(minutes=random.randint(20, 1000)),
                                       task_id=random.choice(tasks_id),
                                       user_id=random.choice(users_id))
            self.stdout.write(self.style.SUCCESS('Successfully added timelogs'))
