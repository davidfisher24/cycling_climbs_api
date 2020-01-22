# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from .user import User
from .climb import Climb

class Comment(models.Model):
    text = models.TextField()
    title = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    climb = models.ForeignKey(Climb, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommentFlag(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

