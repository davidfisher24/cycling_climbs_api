# -*- coding: utf-8 -*-
from .viewBase import DefaultViewSet
from api.models import Achievement
from api.serializers import AchievementSerializer

class AchievementViewSet(DefaultViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    key_options = ['user','climb', 'time', 'date']
    page_size = 20
