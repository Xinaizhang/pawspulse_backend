from django.db import models
from app.models import User


# 论坛帖子模型
class Post(models.Model):
    # 帖子的唯一标识
    post_id = models.AutoField(primary_key=True)
    # 发布帖子的用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID")
    # 帖子标题
    title = models.CharField(max_length=255, verbose_name="标题")
    # 帖子内容
    content = models.TextField(verbose_name="内容")
    # 帖子图片URL，存储为JSON格式
    picture_url = models.JSONField(verbose_name="图片URL", blank=True, null=True)
    # 帖子标签
    tags = models.CharField(max_length=50, verbose_name="标签", blank=True, null=True)
    # 点赞数
    likes_count = models.PositiveIntegerField(default=0, verbose_name="点赞数")
    # 评论数
    comments_count = models.PositiveIntegerField(default=0, verbose_name="评论数")
    # 帖子创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="帖子创建时间")


class Comment(models.Model):
    # 评论的唯一标识
    comment_id = models.AutoField(primary_key=True)
    # 评论内容
    content = models.TextField(verbose_name="内容")
    # 评论所属的帖子
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, verbose_name="帖子ID")
    # 发表评论的用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID")
    # 评论创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论创建时间")
    # 父评论，允许为空，用于实现评论回复
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE,
                               verbose_name="父评论ID")


class Like(models.Model):
    # 点赞的唯一标识
    like_id = models.AutoField(primary_key=True)
    # 点赞的用户
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID")
    # 点赞的帖子
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="帖子ID", blank=True, null=True)
    # 点赞创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="点赞创建时间")

    # 联合约束-保证一个用户只能对一个帖子点赞一次
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like_post')
        ]
        print(constraints)
