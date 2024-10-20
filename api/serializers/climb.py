# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from api.models import Climb

class ClimbListSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Climb
        geo_field = "location"
        fields= ('id','name','location', 'altitude', 'gradient', 'gain', 'distance')

class ClimbOneSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Climb
        geo_field = "path"
        fields = ('id', 'name', 'path', 'location', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center', 'peak_name', 'climb_name', 'altimeter', 'area')
        extra_kwargs = {
            'peak_name': {'write_only': True},
            'climb_name': {'write_only': True}
        }