# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from .viewBase import DefaultsMixin
from api.models import User
from api.serializers import UserSerializer

class UserView(DefaultsMixin, APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.data

        serializer = self.serializer_class(
            request.user, data=user, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()