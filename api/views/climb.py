# -*- coding: utf-8 -*-
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from django.contrib.gis.geos import Point, Polygon, LineString
from django.contrib.gis.measure import Distance  
from .viewBase import DefaultViewSet, DefaultsMixin
from api.models import Climb, Province
from api.serializers import ClimbOneSerializer, ClimbListSerializer, AltimeterSerializer

class AltimeterViewSet(DefaultsMixin, ReadOnlyModelViewSet):
    queryset = Climb.objects.all()
    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, pk):
        climb = Climb.objects.get(pk=pk)
        serializer = AltimeterSerializer(climb)
        return Response(serializer.data)

    def list(self, request):
        options = {}
        for key in (request.GET):
            options[key] = request.GET.get(key)

        queryset = models.Climb.objects.filter(**options)
        serializer = AltimeterSerializer(queryset, many=True)
        return Response(serializer.data)

class ClimbViewSet(DefaultViewSet):
    queryset = Climb.objects.all()
    serializer_class = ClimbOneSerializer
    serializers = {
        'list': ClimbListSerializer,
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
        self.queryset = Climb.objects.filter(location__contained=geom)
        return super().list(request)

    @action(detail=False)
    def nearby(self,request, *args, **kwargs):
        location = request.GET['location'].split(',')
        radius = request.GET['distance']
        lat = location[0]
        lng = location[1]
        point = Point(float(lng), float(lat))
        self.queryset = Climb.objects.filter(location__distance_lt=(point, Distance(km=radius)))
        return super().list(request)

    @action(detail=False)
    def province(self,request,*args, **kwargs):
        provId = int(request.GET['id'])
        province = Province.objects.get(pk=provId)
        self.queryset = Climb.objects.filter(path__within=province.area)
        return super().list(request)