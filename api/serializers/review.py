# -*- coding: utf-8 -*-
from rest_framework import serializers
from api.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id','text','score','user','created_at','updated_at','climb')