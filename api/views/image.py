# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from django.http import HttpResponse

class ImageView(APIView):
    def get(self, request, format=None):
        with open('.'+request.path,'rb') as fh:
            return HttpResponse(fh.read(), content_type='image')
