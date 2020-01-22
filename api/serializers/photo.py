# -*- coding: utf-8 -*-
from rest_framework import serializers
from api.models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id','path','fileType','fileSize','text','user','created_at', 'climb')

