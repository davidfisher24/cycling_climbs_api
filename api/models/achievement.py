# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.gis.db import models
from .user import User
from .climb import Climb

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    climb = models.ForeignKey(Climb, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    time = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
