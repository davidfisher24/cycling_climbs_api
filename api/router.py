# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter
import api.views as views

router = DefaultRouter()
router.register(r'climb', views.ClimbViewSet)
router.register(r'province', views.ProvinceViewSet)
router.register(r'review', views.ReviewViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'achievement', views.AchievementViewSet)
router.register(r'bookmark', views.BookmarkViewSet)
router.register(r'photo', views.PhotoViewSet)
router.register(r'user', views.UserViewSet)