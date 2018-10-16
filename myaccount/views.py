from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import ProfileForm, AvatarUploadForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import uuid
from django.http import JsonResponse
from django.urls import reverse
from PIL import Image
import os
import json

# Create your views here.
@login_required
def profile(request):
    user = request.user
    return render(request, 'myaccount/profile.html', {'user':user})

@login_required
def ajax_avatar_upload(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['avatar_file'] # 获取上传图片
            data = request.POST['avatar_data'] # 获取 ajax 返回图片坐标

            if img.size/1024 >700:
                return JsonResponse({"message": "图片尺寸应小于 900×1200 像素，请重新上传。",})

            current_avatar = user_profile.avatar
            cropped_avatar = crop_image(current_avatar, img, data, user.id)
            user_profile.avatar = cropped_avatar # 将图片路径修改到当前用户数据库
            user_profile.save()

            # 向前端返回一个 json, result 值是图片路径
            data = {"result": user_profile.avatar.url,}
            return JsonResponse(data)

        else:
            return JsonResponse({"msg":"请重新上传。只能上传图片"})

    return HttpResponseRedirect(reverse('myaccount:profile'))

def crop_image(current_avatar, file, data, uid):
    # 随机生成新的图片名，自定义路径。
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid1().hex[:10], ext)
    cropped_avatar = os.path.join(str(uid), "avatar", file_name)
    # 相对根目录路径
    file_path = os.path.join("media", str(uid), "avatar", file_name)

    # 获取 Ajax 发送的裁剪参数 data, 先用 json 解析。
    coords = json.loads(data)
    t_x = int(coords['x'])
    t_y = int(coords['y'])
    t_width = t_x + int(coords['width'])
    t_height = t_y + int(coords['height'])
    t_rotate = coords['rotate']

    # 裁剪图片，压缩尺寸为 400*400.
    img = Image.open(file)
    #print(type(img.crop((t_x, t_y, t_width, t_height)))

    crop_im = img.crop((t_x, t_y, t_width, t_height)).resize((400, 400), Image.ANTIALIAS).rotate(t_rotate)

    directory = os.path.dirname(file_path)
    if os.path.exists(directory):
        crop_im.save(file_path)
    else:
        os.makedirs(directory)
        crop_im.save(file_path)

    # 如果头像不是默认头像，删除老头像图片，节省空间
    if not current_avatar == os.path.join("avatar", "default.jpg"):
        current_avatar_path = os.path.join("media", str(uid), "avatar", os.path.basename(current_avatar.url))
        os.remove(current_avatar_path)

    return cropped_avatar