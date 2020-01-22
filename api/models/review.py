# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from .user import User
from .climb import Climb


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

