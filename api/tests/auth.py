from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from api.models.user import User, UserManager
from api.serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from api.views import RegistrationView, LoginView, UserView
import json

class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

        self.user_data = {
            'email': 'davidfisher24@gmail.com',
            'password': 'password',
            'username': 'davidfisher24'
        }

        self.user = User.objects.create(**self.user_data)

    def test_registration_viewset_creates_user(self):
        view = RegistrationView.as_view()
        data = {
            'email': 'user@gmail.com',
            'password': 'password',
            'username': 'newUser'
        }
        request = self.factory.post('/api/auth/register', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(set(response.data.keys()), set(['email', 'username', 'token', 'refresh_token']))

    def test_registration_viewset_errors_with_missing_email(self):
        view = RegistrationView.as_view()
        data = {
            'password': 'password',
            'username': 'newUser2'
        }
        request = self.factory.post('/api/auth/register', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['email']))

    def test_registration_viewset_errors_with_invalid_email(self):
        view = RegistrationView.as_view()
        data = {
            'email': 'user2gmail.com',
            'password': 'password',
            'username': 'newUser2'
        }
        request = self.factory.post('/api/auth/register', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['email']))

    def test_registration_viewset_errors_with_missing_username(self):
        view = RegistrationView.as_view()
        data = {
            'email': 'user2@gmail.com',
            'password': 'password',
        }
        request = self.factory.post('/api/auth/register', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['username']))

    def test_registration_viewset_errors_with_missing_password(self):
        view = RegistrationView.as_view()
        data = {
            'email': 'user2@gmail.com',
            'username': 'userNoPassword'
        }
        request = self.factory.post('/api/auth/register', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['password']))

    def test_registration_viewset_errors_with_duplicate_email(self):
        view = RegistrationView.as_view()
        data = {
            'email': 'davidfisher24@gmail.com',
            'username': 'duplicate-user',
            'password': 'password'
        }
        request = self.factory.post('/api/auth/register', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['email']))

    def test_registration_viewset_errors_with_duplicate_username(self):
        view = RegistrationView.as_view()
        data = {
            'email': 'davidfisher23@gmail.com',
            'username': 'davidfisher24',
            'password': 'password'
        }
        request = self.factory.post('/api/auth/register', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['username']))

    def test_login_viewset_logins_user(self):
        view = LoginView.as_view()
        data = {
            'email': 'davidfisher24@gmail.com',
            'username': 'password'
        }
        request = self.factory.post('/api/auth/login', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data.keys()), set(['email', 'username', 'token', 'refresh_token']))
