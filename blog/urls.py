#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    #http://localhost:8000/blog/
    path('<int:article_pk>', views.article_detail, name="article_detail"),
    #http://localhost:8000/blog/1.html
    path('type<int:type_pk>', views.article_type, name="article_type"),
    path('year<int:year>/month<int:month>', views.article_date, name="article_date"),
]
