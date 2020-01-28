from django.test import TestCase
from django.core.serializers import register_serializer
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from api.models.user import User, UserManager
from api.serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from api.views import RegistrationView, LoginView, RefreshView, ForgotPasswordView, ResetPasswordView
import json

class AuthTestCase(TestCase):

    register_serializer('yml', 'django.core.serializers.pyyaml')
    fixtures = [
        'api/tests/fixtures/user.yml'
    ]

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_registration_viewset_creates_user(self):
        view = RegistrationView.as_view()
        data = {
            'email': 'newuser@email.com',
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
            'email': 'user2email.com',
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
            'email': 'user2@email.com',
            'password': 'password',
        }
        request = self.factory.post('/api/auth/register', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['username']))

    def test_registration_viewset_errors_with_missing_password(self):
        view = RegistrationView.as_view()
        data = {
            'email': 'user2@email.com',
            'username': 'userNoPassword'
        }
        request = self.factory.post('/api/auth/register', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['password']))

    def test_registration_viewset_errors_with_duplicate_email(self):
        view = RegistrationView.as_view()
        data = {
            'email': 'testuser1@email.com',
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
            'email': 'testusercopy@email.com',
            'username': 'testuser1',
            'password': 'password'
        }
        request = self.factory.post('/api/auth/register', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['username']))

    def test_login_viewset_logins_user(self):
        view = LoginView.as_view()
        data = {
            'email': 'testuser1@email.com',
            'password': 'password'
        }
        request = self.factory.post('/api/auth/login', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data.keys()), set(['email', 'username', 'token', 'refresh_token']))

    def test_login_viewset_fails_with_incorrect_password(self):
        view = LoginView.as_view()
        data = {
            'email': 'testuser1@email.com',
            'password': 'fake-password'
        }
        request = self.factory.post('/api/auth/login', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_refresh_viewset_refreshes_users_token(self):
        view = RefreshView.as_view()
        data = {
            'refresh_token': "b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTgwMjM1MjI0fQ.WF2NjpSJOYrIZ9dBK_eClBXi0VX9zxCVpkPCZ61NRXo'",
        }
        request = self.factory.post('/api/auth/refresh', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data.keys()), set(['email', 'username', 'token', 'refresh_token']))
        self.assertEqual(response.data['email'], 'testuser1@email.com')

    def test_refresh_viewset_fails_with_incorrect_refresh_token(self):
        view = RefreshView.as_view()
        data = {
            'refresh_token': 'a-nonsense-string'
        }
        request = self.factory.post('/api/auth/refresh', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_forgot_password_viewset_sets_refresh_token(self):
        view = ForgotPasswordView.as_view()
        data = {
            'email': "testuser2@email.com",
        }
        request = self.factory.post('/api/auth/forgot-password', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        user_model = User.objects.get(id=2)
        self.assertIsNotNone(user_model.reset_password_token)

    def test_forgot_password_viewset_fails_with_invalid_email(self):
        view = ForgotPasswordView.as_view()
        data = {
            'email': "testuserXXX@email.com",
        }
        request = self.factory.post('/api/auth/forgot-password', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_reset_password_viewset_sets_new_password(self):
        forgotPasswordView = ForgotPasswordView.as_view()
        requestTokenData = { 'email': "testuser1@email.com" }
        requestToken = self.factory.post('/api/auth/forgot-password', data=requestTokenData, format='json')
        forgotPasswordView(requestToken)
        user_model = User.objects.get(id=1)
        token = user_model.reset_password_token

        view = ResetPasswordView.as_view()
        url = "/api/auth/reset-password?id={}&token={}".format(1, token)
        data = {
            'password': "new-password",
        }
        request = self.factory.post(url, data=data, format='json')

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data.keys()), set(['email', 'username', 'token', 'refresh_token']))
        user_model = User.objects.get(id=1)
        self.assertIsNone(user_model.reset_password_token)

    def test_reset_password_viewset_fails_with_no_password_passed(self):
        forgotPasswordView = ForgotPasswordView.as_view()
        requestTokenData = { 'email': "testuser1@email.com" }
        requestToken = self.factory.post('/api/auth/forgot-password', data=requestTokenData, format='json')
        forgotPasswordView(requestToken)
        user_model = User.objects.get(id=1)
        token = user_model.reset_password_token

        view = ResetPasswordView.as_view()
        url = "/api/auth/reset-password?id={}&token={}".format(1, token)
        request = self.factory.post(url, data={}, format='json')

        response = view(request)
        self.assertEqual(response.status_code, 400)


    def test_reset_password_viewset_fails_with_invalid_token_data(self):
        view = ResetPasswordView.as_view()
        url = "/api/auth/reset-password?id={}&token={}".format(2, "nothing")
        data = {
            'password': "new-password",
        }
        request = self.factory.post(url, data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)

