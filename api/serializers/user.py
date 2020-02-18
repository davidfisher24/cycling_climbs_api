# -*- coding: utf-8 -*-
from rest_framework import serializers
from api.models import User, Profile
from django_countries.serializer_fields import CountryField
from rest_framework_gis.serializers import GeometryField
from django.contrib.gis.geos import Point

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    country = CountryField(required=False)
    nationality = CountryField(required=False)
    birthdate = serializers.DateField(required=False)
    location = GeometryField(required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'full_name', 'country', 'nationality', 'birthdate', 'location', 'profile_picture_url')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('email', 'username', 'profile',)


class UserUpdateSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=False)
    username = serializers.CharField(max_length=255, required=False)
    profile = ProfileSerializer(required=False)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=False
    )


    def validate(self, data):
        user_id = self.context.get('user_id', None)
        user = User.objects.get(id=user_id)
        password = data.pop('password', None)
        profile = data.pop('profile', None)
        try:
            for key, value in data.items():
                setattr(user, key, value)
            if password is not None:
                user.set_password(password)
            if profile is not None:
                profile_instance = Profile.objects.get_or_create(user=user)[0]
                self.update_profile(profile_instance,profile)
            user.save()
        except Exception as e:
            raise serializers.ValidationError(e)
        return user


    def update_profile(self, profile, data):
        for key, value in data.items():
            setattr(profile, key, value)
        return profile.save()
