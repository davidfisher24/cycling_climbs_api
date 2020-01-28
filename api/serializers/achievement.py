# -*- coding: utf-8 -*-
from rest_framework import serializers
from api.models import Achievement

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'climb', 'user', 'time', 'date', 'created_at')
