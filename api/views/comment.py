# -*- coding: utf-8 -*-
from .viewBase import DefaultViewSet
from api.models import Comment
from api.serializers import CommentSerializer

class CommentViewSet(DefaultViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    key_options = ['user','climb']
    page_size = 20


