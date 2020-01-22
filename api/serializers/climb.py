# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from api.models import Climb

class AltimeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climb
        geo_field = "path"
        fields = ('id', 'name', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center', 'kilometers', 'area')

class ClimbListSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Climb
        geo_field = "location"
        fields= ('id','name','location')

class ClimbOneSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Climb
        geo_field = "path"
        fields = ('id', 'name', 'path', 'location', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center', 'peak_name', 'climb_name')
        extra_kwargs = {
            'peak_name': {'write_only': True},
            'climb_name': {'write_only': True}
        }