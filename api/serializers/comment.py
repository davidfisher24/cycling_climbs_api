# -*- coding: utf-8 -*-
from rest_framework import serializers
from api.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','title','text','user','created_at', 'climb')

