# app - models.py
from django.db import models
from django.utils import timezone


# 邮箱验证码模型
class EmailVerification(models.Model):
    email = models.EmailField(max_length=254, unique=True, verbose_name="邮箱地址")
    verification_code = models.CharField(max_length=6, verbose_name="验证码")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_verified = models.BooleanField(default=False, verbose_name="是否验证")


# 用户模型
class User(models.Model):
    # 用户唯一标识
    user_id = models.AutoField(primary_key=True)
    # 电话号码，唯一约束
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="电话号码")
    # 邮箱地址，可为空，唯一约束
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True, verbose_name="邮箱地址")
    # 用户昵称
    nickname = models.CharField(max_length=50, verbose_name="用户昵称")
    # 用户头像
    avatar = models.ImageField(upload_to='user_avatars/', blank=True, null=True, verbose_name="用户头像")
    # 地址
    address = models.CharField(max_length=255, verbose_name="地址")
    # 密码散列值
    password_hash = models.CharField(max_length=128, verbose_name="密码散列值")
    # 账户创建日期，默认为当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="账户创建日期")
    # 添加一个背景图片字段
    background = models.ImageField(upload_to='user_backgrounds/', blank=True, null=True, verbose_name="背景图片")


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
