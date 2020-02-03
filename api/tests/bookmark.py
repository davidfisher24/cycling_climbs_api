from django.test import TestCase
from datetime import date
from django.core.serializers import register_serializer
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from api.models import Climb, User, Bookmark
from api.serializers import BookmarkSerializer
from api.views import BookmarkViewSet
import json

class BookmarkTestCase(TestCase):
    register_serializer('yml', 'django.core.serializers.pyyaml')
    fixtures = [
        'api/tests/fixtures/user.yml',
        'api/tests/fixtures/climb.yml',
        'api/tests/fixtures/bookmark.yml'
    ]

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_bookmark_viewset_list_route(self):
        request = self.factory.get('/api/bookmark')
        view = BookmarkViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),4)

    def test_bookmark_viewset_list_route_fills_climb_data(self):
        request = self.factory.get('/api/bookmark')
        view = BookmarkViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        climb = response.data['results'][0]['climb']
        self.assertEqual(set(climb.keys()), set(['id', 'name', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center']))

    def test_bookmark_viewset_list_route_filters_by_climb(self):
        request = self.factory.get('/api/bookmark?climb=1')
        view = BookmarkViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),2)

    def test_bookmark_viewset_list_route_filters_by_user(self):
        request = self.factory.get('/api/bookmark?user=1')
        view = BookmarkViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),2)

    def test_bookmark_viewset_list_route_for_auth_user(self):
        request = self.factory.get('/api/bookmark/me')
        view = BookmarkViewSet.as_view(actions={'get': 'me'})
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(len(response.data['results']),2)

    def test_bookmark_viewset_list_route_for_auth_user_with_auth_error(self):
        request = self.factory.get('/api/bookmark/me')
        view = BookmarkViewSet.as_view(actions={'get': 'me'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_bookmark_viewset_retrieve_route(self):
        request = self.factory.get('/api/bookmark')
        view = BookmarkViewSet.as_view(actions={'get': 'retrieve'})
        response = view(request,pk=1)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(set(response.data.keys()), set(['id', 'climb', 'user', 'created_at']))
        self.assertEqual(response.data['user'],1)

    def test_bookmark_viewset_create_route(self):
        view = BookmarkViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 3,
        }
        request = self.factory.post('/api/bookmark', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['climb'],3)

    def test_bookmark_viewset_fails_to_create_if_data_is_a_duplicate(self):
        view = BookmarkViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
        }
        request = self.factory.post('/api/bookmark', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_booomark_viewset_fails_to_create_if_no_user_is_authenticated(self):
        view = BookmarkViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
        }
        request = self.factory.post('/api/bookmark', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 401)
    
    def test_bookmark_viewset_destroy_route(self):
        view = BookmarkViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/bookmark')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 204) 

    def test_bookmark_viewset_delete_route_fails_if_no_user_autenticated(self):
        view = BookmarkViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/bookmark')
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_bookmark_viewset_update_route_fails_if_wrong_user_autenticated(self):
        view = BookmarkViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/bookmark')
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 
    