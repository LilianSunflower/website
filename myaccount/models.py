from django.db import models # 模型的类
from django.contrib.auth.models import User # 和 User 外链
import uuid # 生成身份辨识 id
import os #操作头像的图片文件

# Create your models here.

# 用户的文件目录设置
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid1().hex[:10], ext)
    # 头像文件用身份标识命名
    sub_folder = 'file'
    if ext.lower() in ["jpg","png", "gif"]:
        sub_folder = "avatar"
    if ext.lower() in ["pdf", "docx"]:
        sub_folder = "document"
    return os.path.join(str(instance.user.id), sub_folder, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') # 外链
    nickname = models.CharField(max_length=20) # 昵称
    uid = models.UUIDField(unique=True, default=uuid.uuid1, editable=False) # 用了根据全球时间戳随机生成的身份标识字符串
    avatar = models.ImageField(upload_to=user_directory_path, default=os.path.join("avatar","default.jpg"), verbose_name="头像")
    sex = models.CharField(max_length=20, default="保密")
    birth = models.DateTimeField("birth date", blank=True, null=True)
    address = models.CharField(max_length=200, default="未知")
    org = models.CharField('Organization', max_length=128, blank=True)
    job = models.CharField('Job', max_length=128, blank=True)
    join_date = models.DateTimeField("join date", blank=True, null=True, auto_now_add=True)
    mod_date = models.DateTimeField("Mod date", blank=True, auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)