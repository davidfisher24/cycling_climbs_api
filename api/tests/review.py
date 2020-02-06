from django.test import TestCase
from datetime import date
from django.core.serializers import register_serializer
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from api.models import Climb, User, Review
from api.serializers import ReviewSerializer
from api.views import ReviewViewSet
import json

class ReviewTestCase(TestCase):
    register_serializer('yml', 'django.core.serializers.pyyaml')
    fixtures = [
        'api/tests/fixtures/user.yml',
        'api/tests/fixtures/climb.yml',
        'api/tests/fixtures/review.yml'
    ]

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_review_viewset_list_route(self):
        request = self.factory.get('/api/review')
        view = ReviewViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),5)

    def test_review_viewset_list_route_filters_by_climb(self):
        request = self.factory.get('/api/review?climb=1')
        view = ReviewViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),2)

    def test_review_viewset_list_route_filters_by_user(self):
        request = self.factory.get('/api/review?user=1')
        view = ReviewViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),2)

    def test_review_viewset_list_route_for_auth_user(self):
        request = self.factory.get('/api/review/me')
        view = ReviewViewSet.as_view(actions={'get': 'me'})
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(len(response.data['results']),2)

    def test_review_viewset_list_route_for_auth_user_with_auth_error(self):
        request = self.factory.get('/api/review/me')
        view = ReviewViewSet.as_view(actions={'get': 'me'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_review_viewset_retrieve_route(self):
        request = self.factory.get('/api/review')
        view = ReviewViewSet.as_view(actions={'get': 'retrieve'})
        response = view(request,pk=1)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(set(response.data.keys()), set(['id', 'climb', 'user', 'text', 'score', 'created_at', 'updated_at']))
        self.assertEqual(response.data['climb'],1)

    def test_review_viewset_create_route(self):
        view = ReviewViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 3,
            'score': 4,
            'text': "Review"
        }
        request = self.factory.post('/api/review', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['climb'],3)
        self.assertEqual(response.data['score'],4)

    def test_review_viewset_create_route_with_invalid_data(self):
        view = ReviewViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 3,
            'score': 8,
            'text': "Review"
        }
        request = self.factory.post('/api/review', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['score']))

    def test_review_viewset_create_route_with_invalid_repeat_data(self):
        view = ReviewViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
            'score': 2,
            'text': "Review"
        }
        request = self.factory.post('/api/review', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_review_viewset_fails_to_create_if_no_user_is_authenticated(self):
        view = ReviewViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 3,
            'score': 4,
            'text': "Review"
        }
        request = self.factory.post('/api/review', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 401)
    
    
    def test_review_viewset_update_route_updates_data(self):
        view = ReviewViewSet.as_view(actions={'put': 'update'})
        data = {
            'score': 4,
        }
        request = self.factory.put('/api/review', data=data)
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['score'],4)
        self.assertEqual(response.data['climb'],1)

    def test_review_viewset_update_route_fails_to_update_if_no_user_autenticated(self):
        view = ReviewViewSet.as_view(actions={'put': 'update'})
        data = {
            'score': 4,
        }
        request = self.factory.put('/api/review', data=data)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_review_viewset_update_route_fails_to_update_if_wrong_user_autenticated(self):
        view = ReviewViewSet.as_view(actions={'put': 'update'})
        data = {
            'score': 4,
        }
        request = self.factory.put('/api/review', data=data)
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)

        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 

    
    def test_review_viewset_destroy_route(self):
        view = ReviewViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/review')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 204) 

    def test_review_viewset_delete_route_fails_if_no_user_autenticated(self):
        view = ReviewViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/review')
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_review_viewset_update_route_fails_if_wrong_user_autenticated(self):
        view = ReviewViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/review')
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 
    