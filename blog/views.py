from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import Article, ArticleType
from readlike.utils import read_num_add_up
from comment.models import Comment
from myaccount.models import UserProfile

# Create your views here.

def article_common(request, articles_all):
    context = {}
    page_num = int(request.GET.get('page', 1))  # 获取 url 的页面参数（GET请求）
    articles_paginator = Paginator(articles_all, 10)
    articles = articles_paginator.page(page_num)
    page_list = [x for x in range(max(1, page_num - 2), min(articles_paginator.num_pages + 1, page_num + 3))]
    if page_num < (articles_paginator.num_pages - 2):
        page_list += ['...', articles_paginator.num_pages]
    if page_num > 3:
        page_list = [1, '...'] + page_list
    types = ArticleType.objects.annotate(article_count=Count('article'))
    context["page_list"] = page_list
    context["page_num"] = page_num
    context["articles"] = articles
    context["types"] = types
    dates_dict = {}
    dates = Article.objects.dates('created_time', 'month', order='DESC')
    for date in dates:
        dates_dict[date] = Article.objects.filter(created_time__year=date.year, created_time__month=date.month).count()
    context["dates"] =dates_dict
    return context

def article_list(request):
    articles_all = Article.objects.all()
    return render(request, "blog/article_list.html", article_common(request, articles_all))

def article_type(request, type_pk):
    need_type = get_object_or_404(ArticleType, id=type_pk)
    articles_all = Article.objects.filter(article_type=need_type)

    context = article_common(request, articles_all)
    context["type"] = need_type
    return render(request, "blog/article_type.html", context)

def article_date(request, year, month):
    articles_all = Article.objects.filter(created_time__year=year, created_time__month=month)

    context = article_common(request, articles_all)
    context["date"] = "{}年{}月".format(year, month)
    return render(request, "blog/article_date.html", context)

def article_detail(request, article_pk):
    context = {}
    article = get_object_or_404(Article, id=article_pk)

    read_cookie_key = read_num_add_up(request, article)

    article_content_type = ContentType.objects.get_for_model(article)
    comments = Comment.objects.filter(content_type=article_content_type, object_id=article.pk)

    context["article_pre"] = Article.objects.filter(created_time__lt=article.created_time).first()
    context["article_next"] = Article.objects.filter(created_time__gt=article.created_time).last()
    context["article"] = article
    context["user"] = request.user
    context["comments"] = comments
    response = render(request, "blog/article_detail.html", context)
    response.set_cookie(read_cookie_key, True, max_age=600) # 阅读 cookie 标记
    return response