# app - models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# 邮箱验证码模型
class EmailVerification(models.Model):
    email = models.EmailField(max_length=254, unique=True, verbose_name="邮箱地址")
    verification_code = models.CharField(max_length=6, verbose_name="验证码")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_verified = models.BooleanField(default=False, verbose_name="是否验证")


# 用户模型
# class User(models.Model):
#     # 用户唯一标识
#     user_id = models.AutoField(primary_key=True)
#     # 电话号码，唯一约束
#     phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="电话号码")
#     # 邮箱地址，可为空，唯一约束
#     email = models.EmailField(max_length=254, unique=True, blank=True, null=True, verbose_name="邮箱地址")
#     # 用户昵称
#     nickname = models.CharField(max_length=50, verbose_name="用户昵称")
#     # 用户头像
#     avatar = models.ImageField(upload_to='user_avatars/', blank=True, null=True, verbose_name="用户头像")
#     # 地址
#     address = models.CharField(max_length=255, verbose_name="地址")
#     # 密码散列值
#     password_hash = models.CharField(max_length=128, verbose_name="密码散列值")
#     # 账户创建日期，默认为当前时间
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="账户创建日期")
#     # 添加一个背景图片字段
#     background = models.ImageField(upload_to='user_backgrounds/', blank=True, null=True, verbose_name="背景图片")
#
#     # 调用check_password方法
#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password_hash)


# 自定义用户管理器
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # 将 `id` 设为主键
    email = models.EmailField(unique=True, blank=True, null=True)
    nickname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    avatar = models.ImageField(upload_to='user_avatars/', blank=True, null=True)
    address = models.CharField(max_length=255)
    background = models.ImageField(upload_to='user_backgrounds/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # 个性签名
    signature = models.CharField(max_length=255)

    # 添加字段以便与 Django 默认模型兼容
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 自定义用户管理器
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.email or 'Anonymous User'


# 关注关系模型
class User_follows(models.Model):
    # 关注关系的唯一标识
    follow_id = models.AutoField(primary_key=True)
    # 关注者ID
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name="关注者ID")
    # 被关注者ID
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name="被关注者ID")


# 用户消息模型
class User_message(models.Model):
    # 用户消息的唯一标识
    message_id = models.AutoField(primary_key=True)
    # 接收者ID
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',
                                 verbose_name="接收者ID")
    # 发送者ID
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="发送者ID")
    # 消息内容
    message_content = models.TextField(verbose_name="消息内容")
    # 发送时间
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="发送时间")


# 系统通知模型
class Notification(models.Model):
    # 系统通知的唯一标识
    notification_id = models.AutoField(primary_key=True)
    # 接收用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="接收用户")
    # 消息内容
    message = models.TextField(verbose_name="消息内容")
