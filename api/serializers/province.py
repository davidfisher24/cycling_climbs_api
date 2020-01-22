# -*- coding: utf-8 -*-
from rest_framework import serializers
from api.models import Province

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name')
