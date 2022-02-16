from django.conf import settings
from django.test import TestCase

from authapp.models import User
from django.test.client import Client


class UserTestCase(TestCase):
    username = 'django'
    email = 'django@mail.ru'
    password = 'geekbrains'

    new_user_data = {
        'username': 'django1',
        'first_name': 'django1',
        'last_name': 'django1',
        'email': 'django1@mail.ru',
        'password1': 'geekbrains1',
        'password2': 'geekbrains1',
        'age': 18,
    }

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 302)

    def test_register(self):
        response = self.client.post('/auth/register/', data=self.new_user_data)
        print(response.status_code)

        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username=self.new_user_data['username'])
        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{user.email}/{user.activation_key}/"

        response = self.client.get(activation_url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(user.is_active)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def tearDown(self) -> None:
        pass
