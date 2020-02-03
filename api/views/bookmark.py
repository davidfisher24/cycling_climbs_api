# -*- coding: utf-8 -*-
from .viewBase import DefaultViewSet
from api.models import Bookmark
from api.serializers import BookmarkSerializer

class BookmarkViewSet(DefaultViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    key_options = ['user','climb']
    page_size = 20
