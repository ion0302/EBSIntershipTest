import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.tasks.models import Task, Timer, Comment, TimeLog
from apps.tasks.serializers import TaskListSerializer, TaskSerializer, CommentSerializer


class TaskTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.user = User.objects.create(username='string@mail.com', email='string@mail.com', password='string')

        # User.objects.create(username='lorem2@mail.com', email='lorem2@mail.com', password='string2')

        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=f'Bearer {refresh.access_token}')

    def tearDown(self) -> None:
        super().tearDown()

    def create_user(self):
        return User.objects.create(username='string2@mail.com', email='string2@mail.com', password='string2')

    def create_task(self):
        return Task.objects.create(title='Task', description='task', assigned_to=self.user, created_by=self.user)

    def create_comment(self, task):
        return Comment.objects.create(text='Text', task=task)

    # def test_get_tasks(self):
    #     instance = self.create_task()
    #     response = self.client.get(reverse('tasks-list'))
    #     self.assertEqual(200, response.status_code)
    #
    #     response = self.client.get(reverse('tasks-detail', args=[instance.id]))
    #     self.assertEqual(200, response.status_code)

    # def test_create_tasks(self):
    #     data = {
    #         "title": "string",
    #         "description": "string",
    #         "assigned_to": 1
    #
    #     }
    #
    #     response = self.client.post('/api/tasks/', data, 'json')
    #     self.assertEqual(201, response.status_code)
    #     self.assertEqual(1, Task.objects.count())
    #
    # def test_top_20_tasks(self):
    #     response = self.client.get('/api/tasks/top-20/')
    #     self.assertEqual(200, response.status_code)
    #
    # def test_update_tasks(self):
    #     instance = self.create_task()
    #     data = {
    #         "title": "string",
    #         "description": "string"
    #     }
    #     url = reverse('tasks-detail', args=[instance.id])
    #     response = self.client.put(url, data, 'json')
    #     self.assertEqual(200, response.status_code)
    #
    #     queryset = Task.objects.get(id=instance.id)
    #     self.assertEqual(TaskSerializer(queryset).data, json.loads(response.content))
    #
    # def test_partial_update_tasks(self):
    #     instance = self.create_task()
    #     data = {
    #         "title": "string",
    #     }
    #     url = reverse('tasks-detail', args=[instance.id])
    #
    #     response = self.client.patch(url, data, 'json')
    #     self.assertEqual(200, response.status_code)
    #
    #     task = Task.objects.get(id=instance.id)
    #     self.assertEqual('string', task.title)
    #
    # def test_delete_tasks(self):
    #     instance = self.create_task()
    #     url = reverse('tasks-detail', args=[instance.id])
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(204, response.status_code)
    #     self.assertEqual(0, Task.objects.count())
    #
    # def test_assign_to_tasks(self):
    #     user2 = self.create_user()
    #     task = self.create_task()
    #     url = f'/api/tasks/{task.id}/assign-to/'
    #     data = {
    #         "assigned_to": user2.id
    #     }
    #     response = self.client.post(url, data, 'json')
    #     self.assertEqual(200, response.status_code)
    #
    #     task = Task.objects.get(id=task.id)
    #     self.assertEqual(task.assigned_to, user2)



    def test_create_tasks(self):
        data = {
            "title": "string",
            "description": "string",
            "assigned_to": 1

        }

        response = self.client.post('/api/tasks/', data, 'json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, Task.objects.count())


    def test_comments_tasks(self):
        pass
        # task = self.create_task()
        # self.create_comment(task)
        #
        # url = f'/api/tasks/{task.id}/comments/'
        # response = self.client.get(url)
        # self.assertEqual(200, response.status_code)

        # comments = Comment.objects.filter(task=task)
        # self.assertEqual(CommentSerializer(comments, many=True).data, json.loads(response.content))


