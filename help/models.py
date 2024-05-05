from django.db import models
from pets.models import Pet
from app.models import User


# Create your models here.

# 互助模型
class Help(models.Model):
    # 互助帖子的唯一标识
    help_id = models.AutoField(primary_key=True)
    # 需要帮助的宠物ID
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="需要帮助的宠物ID")
    # 发布互助的用户
    requester = models.ForeignKey(User, related_name='help_requests', on_delete=models.CASCADE,
                                  verbose_name="发布互助的用户")
    # 提供帮助的用户
    provider = models.ForeignKey(User, related_name='help_provided', on_delete=models.CASCADE,
                                 verbose_name="提供帮助的用户")
    # 互助状态（0-待接取 1-进行中 2-已完成）
    status = models.IntegerField(default=0, verbose_name="互助状态")
    # 互助详情
    detail = models.TextField(verbose_name="互助详情")
    # 佣金
    cost = models.CharField(max_length=255, verbose_name="佣金")
    # 互助标签
    tags = models.CharField(max_length=50, verbose_name="标签", blank=True, null=True)
