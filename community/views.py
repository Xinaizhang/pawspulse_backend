from django.db import IntegrityError, DatabaseError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .serializers import *


def data_schema(code, message, data=None):
    return {
        "code": code,
        "message": message,
        "data": data
    }


class PostViewSet(viewsets.ViewSet):
    authentication_classes = []

    def list(self, request):
        """ 返回帖子列表 """
        try:
            queryset = Post.objects.all()
            serializer = PostListSerializer(queryset, many=True)
            return Response(data_schema(status.HTTP_200_OK, "Posts retrieved successfully", serializer.data),
                            status.HTTP_200_OK)
        except Exception as e:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)),
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """ 根据post_id返回帖子详情 """
        try:
            if pk is None:
                raise ParseError("Post ID is required")

            post = Post.objects.get(post_id=pk)
            serializer = PostDetailSerializer(post)
            return Response(data_schema(status.HTTP_200_OK, "Post retrieved successfully", serializer.data),
                            status.HTTP_200_OK)
        except Post.DoesNotExist as e:
            return Response(data_schema(status.HTTP_404_NOT_FOUND, "Post not found", str(e)),
                            status=status.HTTP_404_NOT_FOUND)
        except ParseError as e:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "ParseError", str(e)),
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "An error occurred", str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """ 用户发布帖子 """
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                post = serializer.save()  # 尝试保存帖子到数据库
                return Response(data_schema(status.HTTP_201_CREATED, "Post created successfully"),
                                status=status.HTTP_201_CREATED)
            except (IntegrityError, DatabaseError) as e:
                # 处理数据库错误
                return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database error: {str(e)}"),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                # 处理其他类型的错误
                return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, f"An error occurred: {str(e)}"),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "Invalid data", str(serializer.errors)),
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ 根据post_id删除帖子 """
        try:
            if pk is None:
                raise ParseError("Post ID is required")

            # 尝试从数据库中获取要删除的帖子对象
            try:
                post = Post.objects.get(post_id=pk)
            except ObjectDoesNotExist as e:
                # 如果不存在对应post_id的帖子，返回404 Not Found
                return Response(data_schema(status.HTTP_404_NOT_FOUND, "Post not found", str(e)),
                                status=status.HTTP_404_NOT_FOUND)

            # 删除帖子对象
            post.delete()

            # 返回成功删除的响应
            return Response(data_schema(status.HTTP_204_NO_CONTENT, "Post deleted successfully"),
                            status=status.HTTP_204_NO_CONTENT)

        except ParseError as e:
            # 如果post_id参数缺失，返回400 Bad Request
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, str(e)),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # 其他类型的异常统一返回500 Internal Server Error
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error", str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def posts_by_user(self, request, user_id=None):
        """ 根据user_id返回某用户发布的所有帖子 """
        try:
            if user_id is None:
                raise ParseError("User ID is required")

            # 尝试从数据库中获取指定用户发布的所有帖子
            posts = Post.objects.filter(user_id=user_id)

            # 序列化帖子数据
            serializer = PostListSerializer(posts, many=True)

            # 返回成功的响应
            return Response(data_schema(status.HTTP_200_OK, "User's posts retrieved successfully", serializer.data),
                            status=status.HTTP_200_OK)

        except ParseError as e:
            # 如果user_id参数缺失，返回400 Bad Request
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, str(e)),
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # 其他类型的异常统一返回500 Internal Server Error
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error", str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
