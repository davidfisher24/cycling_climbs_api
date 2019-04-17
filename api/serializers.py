# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from api.models import Climb,Peak,User
from django.contrib.auth import authenticate

class PeakListSerializer(GeoFeatureModelSerializer):
	class Meta:
		model = Peak
		geo_field = "location"
		fields = ('id', 'name', 'location',)

class PeakOneSerializer(serializers.ModelSerializer):

    class RelatedClimbsSerializer(GeoFeatureModelSerializer):
        class Meta:
            model = Climb
            geo_field = "path"
            fields = ('id', 'name', 'path', 'extent')

    climbs = RelatedClimbsSerializer(many=True, read_only=True)

    class Meta:
        model = Peak
        fields = ('id', 'name', 'location', 'climbs')


class ClimbListSerializer(serializers.ModelSerializer):

	class RelatedPeakSerializer(GeoFeatureModelSerializer):
		class Meta:
			model = Peak
			geo_field = "location"
			fields = ('id', 'name', 'location')

	peak = RelatedPeakSerializer(many=False, read_only=True)

	class Meta:
		model = Climb
		fields = ('id', 'name', 'peak')


class ClimbOneSerializer(GeoFeatureModelSerializer):
	class Meta:
		model = Climb
		geo_field = "path"
		fields = ('id', 'name', 'path', 'altitude', 'extent', 'gradient', 'gain', 
			'distance', 'center')

class AltimeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climb
        geo_field = "path"
        fields = ('id', 'name', 'waypoints', 'altitude', 'extent', 'gradient', 'gain', 
            'distance', 'center')

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