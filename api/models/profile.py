# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString, Point
from django_countries.fields import CountryField
from .user import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    country = CountryField(null=True)
    nationality = CountryField(null=True)
    location = models.PointField(null=True)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, null=True)
    profile_picture_path = models.CharField(max_length=200, null=True)

    @property
    def full_name(self):
        return (self.first_name if self.first_name else '') + ' ' + (self.last_name if self.last_name else '')

    @property
    def profile_picture_url(self):
        return (settings.BASE_URL + self.profile_picture_path) if self.profile_picture_path else None

