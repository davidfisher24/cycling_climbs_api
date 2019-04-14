# -*- coding: utf-8 -*-
from rest_framework import authentication, permissions, viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
import django_filters.rest_framework
import api.models as models
import api.serializers as serializers

from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import Distance  

from math import sqrt, pi, log, sin


class DefaultsMixin(object):
	authentication_classes = (
		#authentication.BasicAuthentication,
		#authentication.TokenAuthentication,
	)
	permission_classes = (
		#permissions.IsAuthenticated,
	)
	paginate_by = 25
	paginate_by_param = 'page_size'
	max_paginate_by = 100
	filter_backends = (
		django_filters.rest_framework.DjangoFilterBackend,
        #filters.SearchFilter,
        #filters.OrderingFilter,
    )

class PeakViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
	queryset = models.Peak.objects.all()

	def retrieve(self, request, pk):
		peak = models.Peak.objects.get(pk=pk)
		serializer = serializers.PeakOneSerializer(peak)
		return Response(serializer.data)

	def list(self,request):
		if request.GET.get('ne') and request.GET.get('sw'):
			ne = request.GET['ne'].split(',')
			sw = request.GET['sw'].split(',')
			xmin=sw[1]
			ymin=sw[0]
			xmax=ne[1]
			ymax=ne[0]
			bbox = (xmin, ymin, xmax, ymax)
			geom = Polygon.from_bbox(bbox)
			queryset = models.Peak.objects.filter(location__contained=geom)
		elif request.GET.get('location') and request.GET.get('distance'):
			loc = request.GET['location'].split(',')
			lat = loc[0]
			lng = loc[1]
			point = Point(float(lng), float(lat))
			radius = request.GET['distance']
			queryset = models.Peak.objects.filter(location__distance_lt=(point, Distance(km=radius)))
		else :
			options = {}
			for key in (request.GET):
				options[key] = request.GET.get(key)
			queryset = models.Peak.objects.filter(**options); 
		
		serializer = serializers.PeakListSerializer(queryset, many=True)
		return Response(serializer.data)


class ClimbViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
	queryset = models.Climb.objects.all()

	def retrieve(self, request, pk):
		climb = models.Climb.objects.get(pk=pk)
		serializer = serializers.ClimbOneSerializer(climb)
		return Response(serializer.data)

	def list(self, request):
		queryset = models.Climb.objects.all()
		serializer = serializers.ClimbListSerializer(queryset, many=True)
		filterset_fields = ('name','peak')
		return Response(serializer.data)
		

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

class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
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

        return Response(serializer.data, status=status.HTTP_200_OK)