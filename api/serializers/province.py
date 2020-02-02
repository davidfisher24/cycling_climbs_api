# -*- coding: utf-8 -*-
from rest_framework import serializers
from api.models import Province, Region

class RegionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Region
		fields = ('id', 'name')

class ProvinceSerializer(serializers.ModelSerializer):
	region = RegionSerializer()

	class Meta:
		model = Province
		fields = ('id', 'name', 'region')
		depth = 1

