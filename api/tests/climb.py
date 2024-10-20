from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from django.contrib.gis.geos import LineString, Point
from api.models import Climb, User
from api.serializers import ClimbListSerializer, ClimbOneSerializer
from api.views import ClimbViewSet
from django.core.serializers import register_serializer
import json
from unittest import skip

class ClimbTestCase(TestCase):
    register_serializer('yml', 'django.core.serializers.pyyaml')
    fixtures = [
        'api/tests/fixtures/user.yml',
        'api/tests/fixtures/climb.yml'
    ]

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

        self.test_climb = Climb.objects.get(id=1)
        self.listSerializer = ClimbListSerializer(instance=self.test_climb)
        self.oneSerializer = ClimbOneSerializer(instance=self.test_climb)
 
    def test_climb_peak_name(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.peak_name, "Santillana")

    def test_climb_virtual_name(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.name, "Santillana por Ohanes")

    def test_climb_virtual_altitude(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.altitude, 1358.0)

    def test_climb_virtual_extent(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.extent, (-2.754625, 37.005069, -2.718852, 37.090495))

    def test_climb_virtual_gradient(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.gradient, 4.910263399292802)

    def test_climb_virtual_gain(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.gain, 887.0)

    def test_climb_virtual_distance(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.distance, 18.064204053243856)

    def test_climb_virtual_center(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(climb.center, {
            "type": "Point",
            "coordinates": [
                -2.731412423189668, 
                37.04294132621043
            ]
        })

    def test_climb_virtual_altimeter(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(len(climb.altimeter),20)
        self.assertEqual(climb.altimeter[1], {
            "altitude": 512.0,
            "distance": 1.0,
            "kmGradient": 4.1
        })
        self.assertEqual(climb.altimeter[19],{
            "altitude": 1358.0,
            "distance": 18.064204053243856,
            "kmGradient": 2.887914419236268
        })

    def test_climb_virtual_area(self):
        climb = Climb.objects.get(pk=1)
        self.assertEqual(len(climb.area),182)
        self.assertEqual(climb.area[0],{
            'altitude': 471.0, 
            'distance': 0.0, 
            'x': 0.0, 
            'y': 0.0
        })
        self.assertEqual(climb.area[-1],{
            "altitude": 1358.0,
            "distance": 18.064204053243856,
            "x": 18.064204053243856,
            "y": 887.0
        })

    def test_list_serializer_contains_expected_geo_fields(self):
        data = self.listSerializer.data
        self.assertEqual(set(data.keys()), set(['id','type','geometry','properties']))

    def test_list_serializer_contains_geojson_point(self):
        data = self.listSerializer.data
        self.assertEqual(data['geometry']['coordinates'],[-2.719262, 37.005069, 471.0])
        self.assertEqual(data['geometry']['type'], 'Point')

    def test_one_serializer_contains_expected_geo_fields(self):
        data = self.oneSerializer.data
        self.assertEqual(set(data.keys()), set(['id','type','geometry','properties']))

    def test_properties_contains_expected_in_one_serializer(self):
        data = self.oneSerializer.data
        self.assertEqual(set(data['properties'].keys()), set(['name', 'location', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center', 'area', 'altimeter']))

    def test_one_serializer_contains_geojson_point(self):
        data = self.oneSerializer.data
        self.assertEqual(data['geometry']['type'], 'LineString')
        self.assertEqual(len(data['geometry']['coordinates']),670)

    def test_climb_viewset_list_route_with_search_query(self):
        request = self.factory.get('/api/climb?search=santillana')
        view = ClimbViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['type'],"FeatureCollection")
        self.assertEqual(len(response.data['features']),1)

    def test_climb_viewset_list_route_with_location_query(self):
        request = self.factory.get('/api/climb?location=37.0904287,-2.730939&distance=25')
        view = ClimbViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['type'],"FeatureCollection")
        self.assertEqual(len(response.data['features']),2)

    def test_climb_viewset_list_route_with_bbox_query(self):
        request = self.factory.get('/api/climb?bbox=36.984455,-2.813873,37.109271,-2.519989')
        view = ClimbViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['type'],"FeatureCollection")
        self.assertEqual(len(response.data['features']),1)

    def test_climb_viewset_list_route_without_query(self):
        request = self.factory.get('/api/climb')
        view = ClimbViewSet.as_view(actions={'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 400) 
        self.assertEqual(response.data['errors'][0], "At least one of 'location', 'bbox', or 'search' is required.")
    
    def test_climb_viewset_retrieve_route(self):
        request = self.factory.get('/api/climb')
        view = ClimbViewSet.as_view(actions={'get': 'retrieve'})
        response = view(request,pk=1)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(set(response.data.keys()), set(['id','type','geometry','properties']))

    @skip('Not yet implemented')
    def test_climb_viewset_create_route(self):
        view = ClimbViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb_name': 'Climb',
            'peak_name': 'The Top',
            'path':  [[0, 0, 10], [0.5, 0.5, 50], [1, 1, 100], [1.5, 1.5, 150]],
            'start': [0,0,10],
            'location': [0,0,10],
            'summit': [1.5,1.5,150]
        }
        request = self.factory.post('/api/climb', data=data, format='json')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['properties']["name"],"The Top por Climb")

    def test_climb_viewset_fails_to_create_if_no_user_is_authenticated(self):
        view = ClimbViewSet.as_view(actions={'post': 'create'})
        data = {
            'climb_name': 'Climb',
            'peak_name': 'The Top',
            'path': [(0,0,10),(0.5,0.5,50),(1,1,100),(1.5,1.5,150)],
            'start': [0,0,10],
            'location': [0,0,10],
            'summit': [1.5,1.5,150]
        }
        request = self.factory.post('/api/climb', data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 401)
    
    @skip('Not yet implemented')
    def test_climb_viewset_update_route_updates_data(self):
        view = ClimbViewSet.as_view(actions={'put': 'update'})
        data = {
            'climb_name':"Ohanes pueblo", 
            'peak_name':"Santillia de Almeria",
        }
        request = self.factory.put('/api/climb', data=data)
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data['properties']['name'],'Santillia de Almeria por Ohanes pueblo')

    def test_climb_viewset_update_route_fails_to_update_if_no_user_autenticated(self):
        view = ClimbViewSet.as_view(actions={'put': 'update'})
        data = {
            'climb_name':"Ohanes pueblo", 
            'peak_name':"Santillia de Almeria",
        }
        request = self.factory.put('/api/climb', data=data)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_climb_viewset_update_route_fails_to_update_if_wrong_user_autenticated(self):
        view = ClimbViewSet.as_view(actions={'put': 'update'})
        data = {
            'climb_name':"Ohanes pueblo", 
            'peak_name':"Santillia de Almeria",
        }
        request = self.factory.put('/api/climb', data=data)
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)

        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 

    
    def test_climb_viewset_destroy_route(self):
        view = ClimbViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/climb')
        auth_user = User.objects.get(id=1)
        force_authenticate(request,user=auth_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 204) 

    def test_climb_viewset_delete_route_fails_if_no_user_autenticated(self):
        view = ClimbViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/climb')
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 401) 

    def test_climb_viewset_update_route_fails_if_wrong_user_autenticated(self):
        view = ClimbViewSet.as_view(actions={'delete': 'destroy'})
        request = self.factory.delete('/api/climb')
        wrong_user = User.objects.get(id=2)
        force_authenticate(request,user=wrong_user)
        response = view(request, pk=1, format='json')
        self.assertEqual(response.status_code, 403) 
    