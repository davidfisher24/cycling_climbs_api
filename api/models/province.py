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
import base64
import json

class Province(models.Model):
    name = models.CharField(max_length=200)
    population = models.IntegerField()
    region = models.IntegerField()
    area = models.MultiPolygonField()
    
