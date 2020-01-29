from django.test import TestCase
from django.core.serializers import register_serializer
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from api.models import Climb, User, Achievement
from api.serializers import AchievementSerializer
from api.views import AchievementViewSet
import json

class AchievementTestCase(TestCase):
    register_serializer('yml', 'django.core.serializers.pyyaml')
    fixtures = [
        'api/tests/fixtures/user.yml',
        'api/tests/fixtures/climb.yml',
        'api/tests/fixtures/achievement.yml'
    ]

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_achievement_viewset_list_route(self):
        request = self.factory.get('/api/achievement')
        view = AchievementViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),6)

    def test_achievement_viewset_list_route_filters_by_climb(self):
        request = self.factory.get('/api/achievement?climb=1')
        view = AchievementViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),2)

    def test_achievement_viewset_list_route_filters_by_user(self):
        request = self.factory.get('/api/achievement?user=1')
        view = AchievementViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),4)
    
    def test_climb_viewset_retrieve_route(self):
        request = self.factory.get('/api/achievement')
        view = AchievementViewSet.as_view(actions={'get': 'retrieve'})
        response = view(request,pk=1)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(set(response.data.keys()), set(['id', 'climb', 'user', 'time', 'date', 'created_at']))
        self.assertEqual(response.data['climb'],1)

    def test_climb_viewset_create_route(self):
        view = AchievementViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
            'time': 3600,
            'date': "2019-02-12"
        }
        request = self.factory.post('/api/achievement', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['climb'],1)

    def test_climb_viewset_create_route_with_undefined_required_data(self):
        view = AchievementViewSet.as_view(actions={'post': 'create'})
        data = {
            'time': 3600,
            'date': "2019-02-12"
        }
        request = self.factory.post('/api/achievement', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data['errors'].keys()), set(['climb']))

    def test_climb_viewset_create_route_with_undefined_non_required_data(self):
        view = AchievementViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
        }
        request = self.factory.post('/api/achievement', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['climb'],1)
        self.assertEqual(response.data['time'],None)
        #self.assertEqual(response.data['date'],None)

    def test_climb_viewset_fails_to_create_if_no_user_is_authenticated(self):
        view = AchievementViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
            'time': 3600,
            'date': "2019-02-12"
        }
        request = self.factory.post('/api/achievement', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 401)
    
    
    def test_climb_viewset_update_route_updates_data(self):
        view = AchievementViewSet.as_view(actions={'put': 'update'})
        data = {
            'time': 1000
        }
        request = self.factory.put('/api/achievement', data=data)
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['time'],1000)
        self.assertEqual(response.data['climb'],1)

    def test_climb_viewset_update_route_fails_to_update_if_no_user_autenticated(self):
        view = AchievementViewSet.as_view(actions={'put': 'update'})
        data = {
            'time': 1000
        }
        request = self.factory.put('/api/achievement', data=data)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_climb_viewset_update_route_fails_to_update_if_wrong_user_autenticated(self):
        view = AchievementViewSet.as_view(actions={'put': 'update'})
        data = {
            'time': 1000
        }
        request = self.factory.put('/api/achievement', data=data)
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)

        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 

    
    def test_climb_viewset_destroy_route(self):
        view = AchievementViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/achievement')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 204) 

    def test_climb_viewset_delete_route_fails_if_no_user_autenticated(self):
        view = AchievementViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/achievement')
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_climb_viewset_update_route_fails_if_wrong_user_autenticated(self):
        view = AchievementViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/achievement')
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 
    