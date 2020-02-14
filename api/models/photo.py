# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.gis.db import models
from .user import User
from .climb import Climb


class Photo(models.Model):
    path = models.CharField(max_length=200)
    fileType = models.CharField(max_length=50)
    fileSize = models.IntegerField()
    text = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    climb = models.ForeignKey(Climb, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def url(self):
        return settings.BASE_URL + self.path

class PhotoFlag(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
