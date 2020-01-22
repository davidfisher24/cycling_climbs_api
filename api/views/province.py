# -*- coding: utf-8 -*-
from .viewBase import DefaultViewSet
from api.models import Province
from api.serializers import ProvinceSerializer

class ProvinceViewSet(DefaultViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    page_size = 10
