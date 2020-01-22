# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString, Point
import math
import json
from .user import User

class Climb(models.Model):
    climb_name = models.CharField(max_length=200, null=True)
    peak_name = models.CharField(max_length=200, null=True)
    location = models.PointField(null=True)
    start = models.PointField(null=True)
    summit = models.PointField(null=True)
    path = models.LineStringField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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

        for x in range(0,math.ceil(self.path.length * 1000) + 1):
            distance = self.path.length * 100 if (math.ceil(self.path.length * 1000)) == x else x/10
            altitude = json.loads(self.path.interpolate(x/1000).geojson)['coordinates'][2]
            area.append({
                'altitude': altitude,
                'distance': distance,
                'x': distance,
                'y': altitude - baseY,
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
    
