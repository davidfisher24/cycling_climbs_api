# -*- coding: utf-8 -*-
from .viewBase import DefaultViewSet
from api.models import Photo
from api.serializers import PhotoSerializer
from django.core.files.storage import FileSystemStorage
from magic import from_file
from rest_framework.exceptions import NotAcceptable
import time


class PhotoViewSet(DefaultViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    page_size = 20
    key_options = ['user','climb']

    def create(self,request,*args,**kwargs):
        fs = FileSystemStorage()
        timeFileName = time.strftime("%Y%m%d-%H%M%S")
        path = 'assets/'+str(request.data['climb'])+'/photos/'+timeFileName

        filepath = request.FILES['photo'] if 'photo' in request.FILES else False

        if filepath == False:
            raise NotAcceptable(
                detail="No photo was attached to the request"
            )

        if str(filepath).split('.')[-1] not in ['jpeg', 'jpg', 'png']:
            raise NotAcceptable(
                detail="Image can only be jpeg or png"
            )


        fs.save(path,request.FILES['photo'])
        request.data._mutable = True
        request.data['path'] = path
        request.data['fileSize'] = request.FILES['photo'].size
        request.data['fileType'] = from_file(path, mime=True)
        return super().create(request)


