from rest_framework import serializers
from .models import *
from app.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """ 评论序列化器 """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'user', 'content', 'created_at', 'parent']


class PostListSerializer(serializers.ModelSerializer):
    """ 帖子列表序列化器 """
    user = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ['post_id', 'user', 'title', 'content', 'picture_url', 'tags', 'likes_count', 'comments_count',
                  'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    """ 帖子详情序列化器 """
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['post_id', 'user', 'title', 'content', 'picture_url', 'tags', 'likes_count', 'comments_count',
                  'created_at', 'comments']


class PostCreateSerializer(serializers.ModelSerializer):
    """ 创建帖子序列化器 """
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'picture_url', 'tags', 'user_id']  # 添加 user_id 字段

    def create(self, validated_data):
        # 用户已经通过 user_id 字段验证并从 User 模型中获取
        return Post.objects.create(**validated_data)
