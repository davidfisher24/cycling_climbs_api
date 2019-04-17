# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter
import api.views as views

router = DefaultRouter()
router.register(r'peak', views.PeakViewSet)
router.register(r'climb', views.ClimbViewSet)
router.register(r'altimeter', views.AltimeterViewSet)