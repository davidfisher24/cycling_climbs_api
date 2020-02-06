# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .user import User
from .climb import Climb


class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    climb = models.ForeignKey(Climb, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "climb"),)

class ReviewFlag(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

