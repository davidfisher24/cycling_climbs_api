# -*- coding: utf-8 -*-
import csv
import os
from django.core.management.base import BaseCommand, CommandError

from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import GEOSGeometry
from api.models import Province
import json

class Command(BaseCommand):
    help = 'adds spanish provinces from static csv'

    def handle(self, *args, **options):

        file = "/home/david/Sites/cycling_climbs_api/data/spain_provinces.geojson"
        

        with open(file, 'r') as jsonFile:
            featureCollection = json.loads(jsonFile.read())
            for feature in featureCollection["features"]:

                area = GEOSGeometry(str(feature["geometry"]))

                province = Province()
                province.area = area
                province.name = feature["properties"]["name"]
                province.region = int(feature["properties"]["region"])
                province.population = int(feature["properties"]["poblacion_"])
                province.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported from the file provinces'))