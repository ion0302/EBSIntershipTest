from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


# class UserTests(TestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create(username='lorem@mail.com', email='lorem@mail.com', password='string')
#
#         User.objects.create(username='lorem2@mail.com', email='lorem2@mail.com', password='string2')
#
#         refresh = RefreshToken.for_user(self.user)
#         self.client.force_authenticate(user=self.user, token=f'Bearer {refresh.acces_token}')
#
#     def test_user_register(self):
#
#         self.client = APIClient()
#         data = {
#             "first_name": "test",
#             "last_name": "test",
#             "email": "test@example.com",
#             "password": "test"
#         }
#
#         response = self.client.post('/users/register', data, 'json')
#         self.assertEqual(status.HTTP_201_CREATED, response.status_code)
