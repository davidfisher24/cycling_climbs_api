# -*- coding: utf-8 -*-
import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString, Point
from api.models import Climb

class Command(BaseCommand):
    help = 'Adds climbs from data/climbs folder'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        folder = options['path'][0]
        count = 0

        for file in os.listdir(folder):
            jsonData = json.loads(open(folder + '/' + file,'r').read())

            if len(jsonData['path']) > 1:

                climb = Climb()
                climb.id = file.split('.')[0]
                climb.climb_name = jsonData['name']
                climb.peak_name = jsonData['mountain']

                path = []
                for val in jsonData['path']:
                    point = Point(val[0], val[1], val[2])
                    path.append(point)

                linepath = LineString(path)
                climb.path = linepath

                climb.location = Point(jsonData['path'][0][0], jsonData['path'][0][1], jsonData['path'][0][2])
                climb.start = Point(jsonData['path'][0][0], jsonData['path'][0][1], jsonData['path'][0][2])
                climb.summit = Point(jsonData['path'][-1][0], jsonData['path'][-1][1], jsonData['path'][-1][2])

                climb.save()
                ++count

        self.stdout.write(self.style.SUCCESS('Successfully imported climbs'))
            