# -*- coding: utf-8 -*-
from datetime import date
from django.contrib.gis.db import models
from .user import User
from .climb import Climb

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    climb = models.ForeignKey(Climb, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "climb"),)
