from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class UsersTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(username='string@mail.com', email='string@mail.com', password='string')
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user, token=f'Bearer {refresh.access_token}')

    def tearDown(self) -> None:
        super().tearDown()

    def test_users_list(self):
        url = '/api/users/list/'
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

    def test_users_register(self):
        url = '/api/users/register/'
        data = {
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "password": "string"
        }
        response = self.client.post(url, data, 'json')
        self.assertEqual(200, response.status_code)

    def test_users_last_month_logs(self):
        url = '/api/users/list/last-month-logs/'
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)