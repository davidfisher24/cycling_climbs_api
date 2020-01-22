# -*- coding: utf-8 -*-
from .viewBase import DefaultViewSet
from api.models import Review
from api.serializers import ReviewSerializer

class ReviewViewSet(DefaultViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    key_options = ['user','climb']
    page_size = 20