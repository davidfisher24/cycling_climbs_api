# -*- coding: utf-8 -*-
from rest_framework import authentication, permissions, viewsets, pagination, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action 
import api.backends as backends
import api.serializers as serializers

class DefaultsMixin(object):
	authentication_classes = (
		authentication.BasicAuthentication,
		backends.JWTAuthentication
	)
	permission_classes = (
		permissions.IsAuthenticated,
	)

class DefaultPaginator(pagination.LimitOffsetPagination):
    def __init__(self):
        super(DefaultPaginator, self).__init__()

    def setPageSize(self,size):
        if (size is not None):
            self.default_limit = size

class DefaultViewSet(DefaultsMixin, viewsets.ModelViewSet):
    serializers = {}
    query_options = []
    key_options = []
    pagination_class = DefaultPaginator
    page_size = None

    def get_serializer_class(self):
        if self.action in self.serializers:
            return self.serializers[self.action]
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        if self.pagination_class != None:
            self.pagination_class.setPageSize(self.pagination_class,self.page_size)
        return super().list(request)

    @action(detail=False)
    def me(self, request, *args, **kwargs):
        if (request.user.id == None):
            raise exceptions.PermissionDenied('User not authorized to edit this instance')
        self.pagination_class.setPageSize(self.pagination_class,self.page_size)
        queryset = self.get_queryset()
        self.queryset = queryset.filter(user=request.user.id)
        print(self.get_queryset)
        return super().list(request)

    def create(self, request, *args, **kwargs):
        instance = request.data
        instance['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if (instance.user.id != request.user.id):
            raise exceptions.PermissionDenied('User not authorized to edit this instance')
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (instance.user.id != request.user.id):
            raise exceptions.PermissionDenied('User not authorized to remove this instance')
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = super().get_queryset()
        options = {}

        for key in self.request.query_params:
            if (key in self.query_options):
                options[key + "__unaccent__icontains"] = self.request.query_params[key]
            if (key in self.key_options):
                options[key] = int(self.request.query_params[key])

        return qs.filter(**options)
