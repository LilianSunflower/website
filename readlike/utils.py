#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail

def read_num_add_up(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "{}_{}_readnum".format(ct.model, obj.pk)

    if not request.COOKIES.get(key):
        # 总阅读数加一
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当日阅读数加一
        today = timezone.now().date()
        readdetail, created = ReadDetail.objects.get_or_create(date=today, content_type=ct, object_id=obj.pk)
        readdetail.read_num += 1
        readdetail.save()
    return key

def days_read_data(content_type):
    today = timezone.now().date()
    days = []
    readdetails = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        read_detail = ReadDetail.objects.filter(content_type=content_type, date=date)
        read_agg = read_detail.aggregate(read_num_sum=Sum('read_num'))
        readdetails.append(read_agg['read_num_sum'] or 0)
        days.append(date.strftime('%m/%d'))
    return days, readdetails

def today_hot(content_type):
    today = timezone.now().date()
    hot_data = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return hot_data[:7]

def yesterday_hot(content_type):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    hot_data = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return hot_data[:7]