# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter
import api.views as views

router = DefaultRouter()
router.register(r'altimeter', views.AltimeterViewSet)
router.register(r'climb', views.ClimbViewSet)
router.register(r'province', views.ProvinceViewSet)
router.register(r'review', views.ReviewViewSet)
router.register(r'photo', views.PhotoViewSet)