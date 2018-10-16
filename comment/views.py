from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Comment

# Create your views here.
def update_comment(request):
    referer = request.META.get('HTTP_REFERER', '/')
    user = request.user
    if not user.is_authenticated:
        return render(request, 'error.html', {'message': '请先登录！', 'redirect_to': referer})

    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request, 'error.html', {'message': '评论内容不能为空！', 'redirect_to': referer})

    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
    except Exception as e:
        return render(request, 'error.html', {'message': '评论对象不存在！', 'redirect_to': referer})


    comment = Comment() # 实例化评论
    comment.user = user
    comment.text = text
    comment.content_object = model_class.objects.get(id=object_id)
    comment.save()


    return redirect(referer)