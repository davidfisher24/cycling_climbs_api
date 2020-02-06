from django.test import TestCase
from datetime import date
from django.core.serializers import register_serializer
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from api.models import Climb, User, Comment
from api.serializers import CommentSerializer
from api.views import CommentViewSet
import json

class CommentTestCase(TestCase):
    register_serializer('yml', 'django.core.serializers.pyyaml')
    fixtures = [
        'api/tests/fixtures/user.yml',
        'api/tests/fixtures/climb.yml',
        'api/tests/fixtures/comment.yml'
    ]

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_comment_viewset_list_route(self):
        request = self.factory.get('/api/comment')
        view = CommentViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),3)

    def test_comment_viewset_list_route_filters_by_climb(self):
        request = self.factory.get('/api/comment?climb=1')
        view = CommentViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),2)

    def test_comment_viewset_list_route_filters_by_user(self):
        request = self.factory.get('/api/comment?user=1')
        view = CommentViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),2)

    def test_comment_viewset_list_route_for_auth_user(self):
        request = self.factory.get('/api/comment/me')
        view = CommentViewSet.as_view(actions={'get': 'me'})
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(len(response.data['results']),2)

    def test_comment_viewset_list_route_for_auth_user_with_auth_error(self):
        request = self.factory.get('/api/comment/me')
        view = CommentViewSet.as_view(actions={'get': 'me'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_comment_viewset_retrieve_route(self):
        request = self.factory.get('/api/comment')
        view = CommentViewSet.as_view(actions={'get': 'retrieve'})
        response = view(request,pk=1)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(set(response.data.keys()), set(['id', 'climb', 'user', 'text', 'title', 'created_at']))
        self.assertEqual(response.data['climb'],3)

    def test_comment_viewset_create_route(self):
        view = CommentViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
            'title': "Hello World",
            'text': "Hello World"
        }
        request = self.factory.post('/api/comment', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['climb'],1)

    def test_comment_viewset_create_route_with_undefined_required_data(self):
        view = CommentViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
            'title': "Hello World",
        }
        request = self.factory.post('/api/comment', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['text']))

    def test_comment_viewset_fails_to_create_if_no_user_is_authenticated(self):
        view = CommentViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
            'title': "Hello World",
            'text': "Hello World"
        }
        request = self.factory.post('/api/comment', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 401)
    
    
    def test_comment_viewset_update_route_updates_data(self):
        view = CommentViewSet.as_view(actions={'put': 'update'})
        data = {
            'text': 'Lorem Ipsum is simply dummy text'
        }
        request = self.factory.put('/api/comment', data=data)
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['text'],'Lorem Ipsum is simply dummy text')
        self.assertEqual(response.data['climb'],3)

    def test_comment_viewset_update_route_fails_to_update_if_no_user_autenticated(self):
        view = CommentViewSet.as_view(actions={'put': 'update'})
        data = {
            'text': 'Lorem Ipsum is simply dummy text'
        }
        request = self.factory.put('/api/comment', data=data)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_comment_viewset_update_route_fails_to_update_if_wrong_user_autenticated(self):
        view = CommentViewSet.as_view(actions={'put': 'update'})
        data = {
            'text': 'Lorem Ipsum is simply dummy text'
        }
        request = self.factory.put('/api/comment', data=data)
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)

        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 

    
    def test_comment_viewset_destroy_route(self):
        view = CommentViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/comment')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 204) 

    def test_comment_viewset_delete_route_fails_if_no_user_autenticated(self):
        view = CommentViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/comment')
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_comment_viewset_update_route_fails_if_wrong_user_autenticated(self):
        view = CommentViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/comment')
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 
    