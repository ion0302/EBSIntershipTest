import json
import time

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.tasks.models import Task, Timer, Comment, TimeLog
from apps.tasks.serializers import TaskSerializer, CommentSerializer, TimeLogSerializer


def create_user():
    return User.objects.create(username='string2@mail.com', email='string2@mail.com', password='string2')

class TaskTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(username='string@mail.com', email='string@mail.com', password='string')
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=f'Bearer {refresh.access_token}')

    def tearDown(self) -> None:
        super().tearDown()

    def create_task(self):
        return Task.objects.create(title='Task', description='task', assigned_to=self.user, created_by=self.user)

    def create_comment(self, task):
        return Comment.objects.create(text='Text', task=task)

    def create_timelog(self, task):
        return TimeLog.objects.create(started_at="2022-03-30T11:52:14Z", duration="00:30:00", user=self.user, task=task)

    def test_get_tasks(self):
        instance = self.create_task()
        response = self.client.get(reverse('tasks-list'))
        self.assertEqual(200, response.status_code)

        response = self.client.get(reverse('tasks-detail', args=[instance.id]))
        self.assertEqual(200, response.status_code)

    def test_create_tasks(self):
        data = {
            "title": "string",
            "description": "string",
            "assigned_to": 1

        }

        response = self.client.post('/api/tasks/', data, 'json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Task.objects.count())

    def test_top_20_tasks(self):
        response = self.client.get('/api/tasks/top-20/')
        self.assertEqual(200, response.status_code)

    def test_update_tasks(self):
        instance = self.create_task()
        data = {
            "title": "string",
            "description": "string"
        }
        url = reverse('tasks-detail', args=[instance.id])
        response = self.client.put(url, data, 'json')
        self.assertEqual(200, response.status_code)

        queryset = Task.objects.get(id=instance.id)
        self.assertEqual(TaskSerializer(queryset).data, json.loads(response.content))

    def test_partial_update_tasks(self):
        instance = self.create_task()
        data = {
            "title": "string",
        }
        url = reverse('tasks-detail', args=[instance.id])

        response = self.client.patch(url, data, 'json')
        self.assertEqual(200, response.status_code)

        task = Task.objects.get(id=instance.id)
        self.assertEqual('string', task.title)

    def test_delete_tasks(self):
        instance = self.create_task()
        url = reverse('tasks-detail', args=[instance.id])
        response = self.client.delete(url)

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Task.objects.count())

    def test_tasks_assign_to(self):
        user2 = create_user()
        task = self.create_task()
        url = f'/api/tasks/{task.id}/assign-to/'
        data = {
            "assigned_to": user2.id
        }
        response = self.client.post(url, data, 'json')
        self.assertEqual(200, response.status_code)
        task = Task.objects.get(id=task.id)
        self.assertEqual(task.assigned_to, user2)

    def test_tasks_comments(self):
        task = self.create_task()
        self.create_comment(task)

        url = f'/api/tasks/{task.id}/comments/'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        comments = Comment.objects.filter(task=task)
        self.assertEqual(CommentSerializer(comments, many=True).data, json.loads(response.content))

    def test_tasks_complete(self):
        task = self.create_task()
        url = f'/api/tasks/{task.id}/complete/'
        response = self.client.post(url)
        self.assertEqual(200, response.status_code)

        task = Task.objects.get(id=task.id)
        status_after = task.is_completed
        self.assertEqual(True, status_after)

    def test_tasks_logs(self):
        task = self.create_task()
        self.create_timelog(task)
        url = f'/api/tasks/{task.id}/logs/'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        logs = TimeLog.objects.filter(task=task)
        self.assertEqual(TimeLogSerializer(logs, many=True).data, json.loads(response.content))

    def test_tasks_timer(self):
        task = self.create_task()
        url = f'/api/tasks/{task.id}/timer_start/'
        response = self.client.post(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, Timer.objects.count())

        timer = Timer.objects.get(id=1)
        self.assertEqual(True, timer.is_started)

        time.sleep(1)

        url = f'/api/tasks/{task.id}/timer_stop/'
        response = self.client.post(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, TimeLog.objects.count())


class CommentsTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(username='string@mail.com', email='string@mail.com', password='string')
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=f'Bearer {refresh.access_token}')

    def tearDown(self) -> None:
        super().tearDown()

    def create_task(self):
        return Task.objects.create(title='Task', description='task', assigned_to=self.user, created_by=self.user)

    def create_comment(self, task):
        return Comment.objects.create(text='Text', task=task)

    def test_get_comments(self):
        task = self.create_task()
        instance = self.create_comment(task)

        url = reverse('comments-list')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        url = reverse('comments-detail', args=[instance.id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_create_comment(self):
        task = self.create_task()
        data = {
            "text": "string",
            "task": task.id
        }
        response = self.client.post('/api/comments/', data, 'json')

        self.assertEqual(201, response.status_code)

    def test_update_comments(self):
        task = self.create_task()
        instance = self.create_comment(task)
        url = f'/api/comments/{instance.id}/'
        data = {
            "text": "string",
            "task": task.id,
        }
        response = self.client.put(url, data, 'json')
        self.assertEqual(200, response.status_code)

        data = {
            "text": "string",
        }
        response = self.client.patch(url, data, 'json')
        self.assertEqual(200, response.status_code)

    def test_delete_comment(self):
        task = self.create_task()
        instance = self.create_comment(task)
        url = f'/api/comments/{instance.id}/'
        response = self.client.delete(url)

        self.assertEqual(204, response.status_code)


class TimeLogsTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(username='string@mail.com', email='string@mail.com', password='string')
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=f'Bearer {refresh.access_token}')

    def tearDown(self) -> None:
        super().tearDown()

    def create_task(self):
        return Task.objects.create(title='Task', description='task', assigned_to=self.user, created_by=self.user)

    def create_timelog(self, task):
        return TimeLog.objects.create(started_at="2022-03-31T14:13:14.576Z", duration="00:00:17.7", user=self.user,
                                      task=task)

    def test_get_timelogs(self):
        task = self.create_task()
        instance = self.create_timelog(task)
        url = reverse('timelogs-list')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        url = reverse('timelogs-detail', args=[instance.id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_create_timelogs(self):
        task = self.create_task()
        data = {
            "started_at": "2022-03-31T14:13:14.576Z",
            "duration": 0,
            "task": task.id
        }
        response = self.client.post('/api/timelogs/', data, 'json')
        self.assertEqual(201, response.status_code)

    def test_update_timelogs(self):
        task = self.create_task()
        instance = self.create_timelog(task)
        url = f'/api/timelogs/{instance.id}/'
        data = {
            "started_at": "2022-03-31T14:13:14.576Z",
            "duration": 0,
            "task": task.id
        }
        response = self.client.put(url, data, 'json')
        self.assertEqual(200, response.status_code)

        data = {
            "started_at": "2022-03-31T14:13:14.576Z",
        }
        response = self.client.patch(url, data, 'json')
        self.assertEqual(200, response.status_code)

    def test_delete_timelog(self):
        task = self.create_task()
        instance = self.create_timelog(task)
        url = f'/api/timelogs/{instance.id}/'
        response = self.client.delete(url)

        self.assertEqual(204, response.status_code)