# -*- coding: utf-8 -*-
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from .viewBase import DefaultViewSet, DefaultsMixin
from api.models import User
from api.serializers import RegistrationSerializer, LoginSerializer, RefreshSerializer, ResetPasswordSerializer
import json

class RegistrationView(DefaultsMixin, APIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(DefaultsMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class VerifyView(DefaultsMixin, APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        user = request.data
        if user:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class RefreshView(DefaultsMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        json_data = json.loads(request.body)
        context = {"refresh_token": json_data['refresh_token']}
        serializer = RefreshSerializer(data=self.request.data, context=context)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForgotPasswordView(DefaultsMixin, APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        json_data = json.loads(request.body)
        try:
            user = User.objects.get(email=json_data['email'])
        except User.DoesNotExist:
            raise ValidationError("A user with this email was not found")
        
        token = user.set_reset_password_token()
        # SEND THE RESET PASSWORD EMAIL HERE
        return Response(status=status.HTTP_200_OK)

class ResetPasswordView(DefaultsMixin, APIView):
    permission_classes = (permissions.AllowAny,)

    def get_context_data(self, **kwargs):
        user_id = kwargs['user_id']
        token = kwargs['token']
    
    def post(self, request):
        json_data = json.loads(request.body)
        context = {}
        context = {
            "user_id":  request.GET['id'],
            "reset_token":  request.GET['token']
        }
        serializer = ResetPasswordSerializer(data=json.loads(request.body), context=context)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)