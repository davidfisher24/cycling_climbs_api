# -*- coding: utf-8 -*-
from rest_framework import permissions, serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Func, Q
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point, Polygon, LineString
from django.contrib.gis.measure import Distance  
from .viewBase import DefaultViewSet, DefaultsMixin
from api.models import Climb, Province
from api.serializers import ClimbOneSerializer, ClimbListSerializer

class Unaccent(Func):
    function = 'unaccent'
    template = '%(function)s(%(expressions)s)'

class ClimbViewSet(DefaultViewSet):
    queryset = Climb.objects.all()
    serializer_class = ClimbListSerializer
    pagination_class = None

    def get_object(self):
        obj_id = self.kwargs.get('pk')
        try:
            return Climb.objects.get(pk=obj_id)
        except Climb.DoesNotExist:
            raise NotFound("Climb not found.")

    def get_queryset(self):
        queryset = super().get_queryset()

        location = self.request.query_params.get('location')
        distance = self.request.query_params.get('distance', 25)
        bbox = self.request.query_params.get('bbox')
        search = self.request.query_params.get('search')

        if not (location or bbox or search):
            raise serializers.ValidationError("At least one of 'location', 'bbox', or 'search' is required.")

        # http://localhost:8000/api/climb?search=Leon
        if search:
              queryset = queryset.annotate(
                unaccented_climb_name=Unaccent('climb_name'),
                unaccented_peak_name=Unaccent('peak_name')
            ).filter(
                Q(unaccented_climb_name__icontains=search.lower()) |
                Q(unaccented_peak_name__icontains=search.lower())
            )

        # http://localhost:8000/api/climb?location=37.18817,-3.60667&distance=25
        if location:
            lat, lng = map(float, location.split(','))
            point = Point(lng, lat)
            queryset = queryset.filter(location__distance_lt=(point, Distance(km=float(distance))))

        # http://localhost:8000/api/climb?bbox=36.9048387,-4.3367416,37.18817,-3.60667
        if bbox:
            try:
                bbox_coords = list(map(float, bbox.split(',')))
                if len(bbox_coords) != 4:
                    raise serializers.ValidationError("Invalid 'bbox' coordinates provided. 4 coordinates must be provided.")
                sw_lat, sw_lng, ne_lat, ne_lng = bbox_coords
                geom = Polygon.from_bbox((sw_lng, sw_lat, ne_lng, ne_lat))
                queryset = queryset.filter(location__contained=geom)
            except (ValueError, IndexError):
                raise serializers.ValidationError("Invalid 'bbox' coordinates provided.")

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ClimbOneSerializer(instance)
        return Response(serializer.data)

    def create(self,request,*args,**kwargs):
        self.convertGeom()
        return super().create(self.request,*args,**kwargs)

    def update(self,request,*args,**kwargs):
        if ('path' in request.data):
            self.convertGeom()
        return super().update(self.request,*args,**kwargs)

    def convertGeom(self):
        path = LineString(self.request.data['path'])
        self.request.data['path'] = path
        self.request.data['start'] = Point(path[0])
        self.request.data['location'] = Point(path[0])
        self.request.data['summit'] = Point(path[-1])
