from django.db import models
from pets.models import Pet
from app.models import User


# 互助信息模型
class Help(models.Model):
    # 互助帖子的唯一标识
    help_id = models.AutoField(primary_key=True)
    # 需要帮助的宠物ID，关联宠物模型
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name="需要帮助的宠物ID")
    # 发布互助的用户
    requester = models.ForeignKey(User, related_name='help_requests', on_delete=models.CASCADE,
                                  verbose_name="发布互助的用户")
    # 互助标题
    title = models.CharField(max_length=255, verbose_name="互助标题")
    # 互助详情
    detail = models.TextField(verbose_name="互助详情")
    # 互助状态（0-待接取，1-进行中，2-已完成）
    status = models.IntegerField(default=0, verbose_name="互助状态")
    # 互助标签
    tags = models.CharField(max_length=50, verbose_name="标签", blank=True, null=True)
    # 互助创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 互助更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")


# 互助申请模型
class HelpApplication(models.Model):
    # 申请的唯一标识
    application_id = models.AutoField(primary_key=True)
    # 对应的互助信息
    help = models.ForeignKey(Help, related_name='applications', on_delete=models.CASCADE, verbose_name="互助信息")
    # 申请互助的用户
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="申请用户")
    # 申请状态（0-待审核，1-通过，2-不通过）
    status = models.IntegerField(default=0, verbose_name="申请状态")
    # 申请创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")


# 互助评价模型
class HelpReview(models.Model):
    # 评价的唯一标识
    review_id = models.AutoField(primary_key=True)
    # 对应的互助信息
    help = models.ForeignKey(Help, related_name='reviews', on_delete=models.CASCADE, verbose_name="互助信息")
    # 发表评价的用户
    reviewer = models.ForeignKey(User, related_name='reviews_made', on_delete=models.CASCADE, verbose_name="评价者")
    # 被评价的用户
    reviewee = models.ForeignKey(User, related_name='reviews_received', on_delete=models.CASCADE,
                                 verbose_name="被评价者")
    # 评价内容
    content = models.TextField(verbose_name="评价内容")
    # 评价时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评价时间")
