#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = "myaccount"
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/ajax/avatar', views.ajax_avatar_upload, name='ajax_avatar_upload'),
]