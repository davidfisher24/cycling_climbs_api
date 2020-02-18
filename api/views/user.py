# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from .viewBase import DefaultsMixin, DefaultViewSet
from api.models import User
from api.serializers import UserSerializer, UserUpdateSerializer
from rest_framework.decorators import action 
from rest_framework.response import Response
from rest_framework import status
import json

class UserViewSet(DefaultViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    key_options = ['username', 'password']
    page_size = 20

    @action(detail=False, methods=['get','post'])
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            if (request.user.id == None):
                raise exceptions.PermissionDenied('User not authorized to edit this instance')
            return Response(self.serializer_class(request.user).data)
        else:
            return self.update_user(request, *args, **kwargs)

    def update_user(self, request, *args, **kwargs):
        context = {
            "user_id":  request.user.id,
        }
        serializer = UserUpdateSerializer(data=json.loads(request.body), context=context)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
