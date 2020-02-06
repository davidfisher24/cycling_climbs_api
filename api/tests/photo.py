from django.test import TestCase
from datetime import date
from django.core.serializers import register_serializer
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from api.models import Climb, User, Photo
from api.serializers import PhotoSerializer
from api.views import PhotoViewSet
import json
from django.core.files import File

class PhotoTestCase(TestCase):
    register_serializer('yml', 'django.core.serializers.pyyaml')
    fixtures = [
        'api/tests/fixtures/user.yml',
        'api/tests/fixtures/climb.yml',
        'api/tests/fixtures/photo.yml'
    ]

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.image_url = '/home/david/Sites/cycling_climbs_api/api/tests/fixtures/image.jpeg'
        self.pdf_url = '/home/david/Sites/cycling_climbs_api/api/tests/fixtures/image.pdf'

    def test_photo_viewset_list_route(self):
        request = self.factory.get('/api/photo')
        view = PhotoViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),9)

    def test_photo_viewset_list_route_filters_by_climb(self):
        request = self.factory.get('/api/photo?climb=1')
        view = PhotoViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),5)

    def test_photo_viewset_list_route_filters_by_user(self):
        request = self.factory.get('/api/photo?user=1')
        view = PhotoViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),7)

    def test_photo_viewset_list_route_filters_by_user_and_climb(self):
        request = self.factory.get('/api/photo?user=1&climb=1')
        view = PhotoViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(len(response.data['results']),4)

    def test_photo_viewset_list_route_for_auth_user(self):
        request = self.factory.get('/api/photo/me')
        view = PhotoViewSet.as_view(actions={'get': 'me'})
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(len(response.data['results']),7)

    def test_photo_viewset_list_route_for_auth_user_with_auth_error(self):
        request = self.factory.get('/api/photo/me')
        view = PhotoViewSet.as_view(actions={'get': 'me'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_photo_viewset_retrieve_route(self):
        request = self.factory.get('/api/photo')
        view = PhotoViewSet.as_view(actions={'get': 'retrieve'})
        response = view(request,pk=1)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(set(response.data.keys()), set(['id', 'climb', 'user', 'text', 'path', 'fileType', 'fileSize', 'created_at']))
        self.assertEqual(response.data['climb'],1)


    def test_photo_viewset_create_route(self):
        view = PhotoViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
        }
        request = self.factory.post('/api/photo/', data=data, format='multipart')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)

        with File(open(self.image_url, "rb")) as f:
            request.FILES['photo'] = f
            response = view(request)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['climb'],1)
            self.assertEqual(set(response.data.keys()), set(['id', 'climb', 'user', 'text', 'path', 'fileType', 'fileSize', 'created_at']))

    def test_photo_viewset_create_route_fails_with_wrong_file_type(self):
        view = PhotoViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
        }
        request = self.factory.post('/api/photo/', data=data, format='multipart')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)

        with File(open(self.pdf_url, "rb")) as f:
            request.FILES['photo'] = f
            response = view(request)
            self.assertEqual(response.status_code, 406)
            self.assertEqual(response.data['detail'], "Image can only be jpeg or png")

    def test_photo_viewset_create_route_fails_with_missing_file(self):
        view = PhotoViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb': 1,
        }
        request = self.factory.post('/api/photo/', data=data, format='multipart')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.data['detail'], "No photo was attached to the request")

    def test_photo_viewset_fails_to_create_if_no_user_is_authenticated(self):
        view = PhotoViewSet.as_view(actions={'post': 'create'})
        data = {
            'file': 'image.jpeg',
            'climb': 1,
        }
        request = self.factory.post('/api/photo', data=data, format='multipart')
        response = view(request)
        self.assertEqual(response.status_code, 401)
    
    
    def test_photo_viewset_update_route_updates_data(self):
        view = PhotoViewSet.as_view(actions={'put': 'update'})
        data = {
            'text': 'some text',
        }
        request = self.factory.put('/api/photo', data=data)
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['text'],'some text')
        self.assertEqual(response.data['climb'],1)

    def test_photo_viewset_update_route_fails_to_update_if_no_user_autenticated(self):
        view = PhotoViewSet.as_view(actions={'put': 'update'})
        data = {
            'text': 'some text',
        }
        request = self.factory.put('/api/photo', data=data)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_photo_viewset_update_route_fails_to_update_if_wrong_user_autenticated(self):
        view = PhotoViewSet.as_view(actions={'put': 'update'})
        data = {
            'text': 'some text',
        }
        request = self.factory.put('/api/photo', data=data)
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)

        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 

    
    def test_photo_viewset_destroy_route(self):
        view = PhotoViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/photo')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 204) 

    def test_photo_viewset_delete_route_fails_if_no_user_autenticated(self):
        view = PhotoViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/photo')
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_photo_viewset_update_route_fails_if_wrong_user_autenticated(self):
        view = PhotoViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/photo')
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 
    