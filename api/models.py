# -*- coding: utf-8 -*-
import json
import jwt
from datetime import datetime, timedelta
from django.contrib.gis.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.contrib.gis.geos import LineString, Point
from django.conf import settings

import math
import functools 

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
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

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class Province(models.Model):
    name = models.CharField(max_length=200)
    population = models.IntegerField()
    region = models.IntegerField()
    area = models.MultiPolygonField()

class Climb(models.Model):
    climb_name = models.CharField(max_length=200, null=True)
    peak_name = models.CharField(max_length=200, null=True)
    location = models.PointField(null=True)
    start = models.PointField(null=True)
    summit = models.PointField(null=True)
    path = models.LineStringField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return ' '.join([self.peak_name, "por", self.climb_name])

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
    def area(self):
        area = []
        baseY = self.path[0][2]
        accumX = 0

        for i in range(0,len(self.path)):
            currentPoint = self.path[i]
            prevPoint = self.path[i - 1] if i > 0 else None
            distance = Point(currentPoint[0],currentPoint[1]).distance(Point(prevPoint[0],prevPoint[1])) * 100 if i > 0 else 0
            accumX += distance
            area.append({
                'altitude': currentPoint[2],
                'distance': accumX,
                'x': accumX,
                'y': currentPoint[2] - baseY,
            })

        return area

    @property
    def kilometers(self):
        points = []
        kilometers = []
        indexLimit = math.ceil(self.path.length * 1000) + 1
        for x in range(0,indexLimit):

            point = {}
            distance = self.path.length * 100 if (math.ceil(self.path.length * 1000)) == x else x/10
            point["altitude"] = json.loads(self.path.interpolate(x/1000).geojson)['coordinates'][2]
            point["distance"] = distance
            points.append(point)

            if x%10 == 0 or x == indexLimit - 1:
                divider = (distance - points[x-10]["distance"]) * 10 if x !=0 else None
                point['kmGradient'] = (point['altitude'] - points[x-10]['altitude']) / divider if x != 0 else 0
                kilometers.append(point)

        return kilometers
    
class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    climb = models.ForeignKey(Climb, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReviewFlag(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Photo(models.Model):
    path = models.CharField(max_length=200)
    fileType = models.CharField(max_length=50)
    fileSize = models.IntegerField()
    text = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    climb = models.ForeignKey(Climb, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class PhotoFlag(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
