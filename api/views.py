# -*- coding: utf-8 -*-
from rest_framework import permissions, status, pagination
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.decorators import action
from api.viewBase import DefaultViewSet, DefaultsMixin
import api.models as models
import api.serializers as serializers
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.gis.geos import Point, Polygon, LineString
from django.contrib.gis.measure import Distance  
from magic import from_file
import time

from rest_framework import viewsets

class AltimeterViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Climb.objects.all()
    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, pk):
        climb = models.Climb.objects.get(pk=pk)
        serializer = serializers.AltimeterSerializer(climb)
        return Response(serializer.data)

    def list(self, request):
        options = {}
        for key in (request.GET):
            options[key] = request.GET.get(key)

        queryset = models.Climb.objects.filter(**options)
        serializer = serializers.AltimeterSerializer(queryset, many=True)
        return Response(serializer.data)

class ClimbViewSet(DefaultViewSet):
    queryset = models.Climb.objects.all()
    serializer_class = serializers.ClimbOneSerializer
    serializers = {
        'list': serializers.ClimbListSerializer,
    }
    query_options = ['climb_name','peak_name']

    def convertGeom(self):
        path = LineString(self.request.data['path'])
        self.request.data['path'] = path
        self.request.data['start'] = Point(path[0])
        self.request.data['location'] = Point(path[0])
        self.request.data['summit'] = Point(path[-1])

    def create(self,request,*args,**kwargs):
        self.convertGeom()
        return super().create(self.request,*args,**kwargs)

    def update(self,request,*args,**kwargs):
        if ('path' in request.data):
            self.convertGeom()
        return super().update(self.request,*args,**kwargs)

    @action(detail=False)
    def inarea(self, request, *args, **kwargs):
        ne = request.GET['ne'].split(',')
        sw = request.GET['sw'].split(',')
        bbox = (sw[0], ne[0], sw[1], ne[1])
        geom = Polygon.from_bbox(bbox)
        self.queryset = models.Climb.objects.filter(location__contained=geom)
        return super().list(request)

    @action(detail=False)
    def nearby(self,request, *args, **kwargs):
        location = request.GET['location'].split(',')
        radius = request.GET['distance']
        lat = location[0]
        lng = location[1]
        point = Point(float(lng), float(lat))
        self.queryset = models.Climb.objects.filter(location__distance_lt=(point, Distance(km=radius)))
        return super().list(request)

    @action(detail=False)
    def province(self,request,*args, **kwargs):
        provId = int(request.GET['id'])
        province = models.Province.objects.get(pk=provId)
        self.queryset = models.Climb.objects.filter(path__within=province.area)
        return super().list(request)

class ProvinceViewSet(DefaultViewSet):
    queryset = models.Province.objects.all()
    serializer_class = serializers.ProvinceSerializer
    page_size = 10

class ReviewViewSet(DefaultViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    key_options = ['user','climb']
    page_size = 20

class PhotoViewSet(DefaultViewSet):
    queryset = models.Photo.objects.all()
    serializer_class = serializers.PhotoSerializer
    page_size = 20

    def create(self,request,*args,**kwargs):
        fs = FileSystemStorage()
        timeFileName = time.strftime("%Y%m%d-%H%M%S")
        path = 'assets/'+str(request.data['climb'])+'/photos/'+timeFileName
        fs.save(path,request.FILES['photo'])
        
        request.data._mutable = True
        request.data['path'] = path
        request.data['fileSize'] = request.FILES['photo'].size
        request.data['fileType'] = from_file(path, mime=True)

        return super().create(request)

class RegistrationView(DefaultsMixin, APIView):
	queryset = models.User.objects.all()
	permission_classes = (permissions.AllowAny,)
	serializer_class = serializers.RegistrationSerializer

	def post(self, request):
		user = request.data
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(DefaultsMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(DefaultsMixin, APIView):
    serializer_class = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.data

        serializer = self.serializer_class(
            request.user, data=user, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

class ImageView(APIView):
    def get(self, request, format=None):
        with open('./assets'+request.path,'rb') as fh:
            return HttpResponse(fh.read(), content_type='image')
