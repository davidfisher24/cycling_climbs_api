from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from api.models import User
from api.serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from api.views import RegistrationView, LoginView, UserView
import json

class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

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
        self.assertEqual(set(response.data.keys()), set(['email', 'username', 'token']))

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
