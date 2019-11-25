# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from api.models import Climb,User,Province,Review,Photo
from django.contrib.auth import authenticate
from django.contrib.gis.measure import Distance  

class AltimeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climb
        geo_field = "path"
        fields = ('id', 'name', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center', 'kilometers', 'area')

class ClimbListSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Climb
        geo_field = "location"
        fields= ('id','name','location')

class ClimbOneSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Climb
        geo_field = "path"
        fields = ('id', 'name', 'path', 'location', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center', 'peak_name', 'climb_name')
        extra_kwargs = {
            'peak_name': {'write_only': True},
            'climb_name': {'write_only': True}
        }  

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'name')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id','text','score','user','created_at','updated_at','climb')

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id','path','fileType','fileSize','text','user','created_at', 'climb')

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)
        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
            
        instance.save()

        return instance