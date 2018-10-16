#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models import Sum
from django.core.cache import cache
from blog.models import Article
from readlike.models import ReadDetail
from readlike.utils import days_read_data, today_hot, yesterday_hot
from .forms import loginForm, regForm

def month_hot_article():
    today = timezone.now().date()
    date = timezone.now().date() - datetime.timedelta(days=30)
    hot_articles = Article.objects.filter(read_detail__date__lt=today, read_detail__date__gte=date)\
        .values('id', 'title')\
        .annotate(read_num_sum=Sum('read_detail__read_num'))\
        .order_by('-read_num_sum')
    return hot_articles[:7]

def week_hot_article():
    today = timezone.now().date()
    date = timezone.now().date() - datetime.timedelta(days=7)
    hot_articles = Article.objects.filter(read_detail__date__lt=today, read_detail__date__gte=date)\
        .values('id', 'title')\
        .annotate(read_num_sum=Sum('read_detail__read_num'))\
        .order_by('-read_num_sum')
    return hot_articles[:7]

def home(request):
    article_content_type = ContentType.objects.get_for_model(Article)
    days, readdetails = days_read_data(article_content_type)
    today_hot_data = today_hot(article_content_type)
    yesterday_hot_data = yesterday_hot(article_content_type)

    # 每小时获取一次本周热门
    week_hot_articles = cache.get_or_set('week_hot_articles', week_hot_article(), 3600)

    # 每天获取一次本月热门
    month_hot_articles = cache.get_or_set('month_hot_articles', month_hot_article(), 86400)

    context = {}

    context["days"] = days
    context["readdetails"] = readdetails
    context["articles"] = Article.objects.all()
    context["articles_count"] = Article.objects.all().count()
    context["today_hot"] = today_hot_data
    context["yesterday_hot"] = yesterday_hot_data
    context["week_hot"] = week_hot_articles
    context["month_hot"] = month_hot_articles
    return render(request, "home.html", context)

def login(request):
    '''
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', '/')
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message':'用户名或密码不正确', 'redirect_to': referer})
    '''
    if request.method == "POST":
        login_form = loginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        user=request.user
        if user.is_authenticated:
            return redirect(request.GET.get('from', reverse('home')))
        else:
            login_form = loginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == "POST":
        reg_form = regForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = regForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))
