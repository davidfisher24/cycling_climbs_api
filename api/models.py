# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import jwt
import math
from datetime import datetime, timedelta

#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.gis.geos import GEOSGeometry, LineString, Point
from django.conf import settings

class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        print(settings.SECRET_KEY)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class Peak(models.Model):
    name = models.CharField(max_length=200)
    location = models.PointField()
    created_at = models.DateTimeField(auto_now_add=True)

class Climb(models.Model):
    name = models.CharField(max_length=200)
    peak = models.ForeignKey(
        Peak, related_name='climbs', on_delete=models.CASCADE)
    path = models.LineStringField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def altitude(self):
        return self.path[-1][2]

    @property
    def extent(self):
        return self.path.extent

    @property
    def gradient(self):
        return ((self.path[-1][2] - self.path[0][2]) / self.path.length) /1000

    @property
    def gain(self):
        return self.path[-1][2] - self.path[0][2]

    @property
    def distance(self):
        return self.path.length * 100

    @property
    def center(self):
        return json.loads(self.path.centroid.geojson)

    @property
    def waypoints(self):
        points = []
        for x in range(0,math.ceil(self.path.length * 1000) + 1):
            point = {}
            point["type"] = "Feature"
            point["geometry"] = json.loads(self.path.interpolate(x/1000).geojson)
            distance = self.path.length * 100 if (math.ceil(self.path.length * 1000)) == x else x/10
            point["properties"] = {}
            point["properties"]["distance"] = distance
            
            if x != 0:
                divider = (distance - points[x-1]["properties"]["distance"]) * 100
                point["properties"]["gain"] = point["geometry"]["coordinates"][2] - points[x-1]["geometry"]["coordinates"][2]
                point["properties"]["gradient"] = (point["geometry"]["coordinates"][2] - points[x-1]["geometry"]["coordinates"][2]) / divider
            else:
                point["properties"]["gain"] = 0
                point["properties"]["gradient"] = 0

            if point["properties"]["distance"] >= 1:
                divider = (distance - points[x-10]["properties"]["distance"]) * 10
                point["properties"]["kmGradient"] = (point["geometry"]["coordinates"][2] - points[x-10]["geometry"]["coordinates"][2]) / divider
            else:
                point["properties"]["kmGradient"] = None

            points.append(point)

        return {
            "type": "FeatureCollection",
            "features": points,
        }
    
    

def __str__(self):
        return '%s %s' % (self.name)

