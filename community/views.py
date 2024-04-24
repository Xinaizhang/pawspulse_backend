from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.core.exceptions import ValidationError

from .models import *
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
            return Response(data_schema(status.HTTP_200_OK, "Posts retrieved successfully", serializer.data))
        except Exception as e:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)))

    def retrieve(self, request, pk=None):
        """ 根据post_id返回帖子详情 """
        try:
            if pk is None:
                raise ParseError("Post ID is required")

            post = Post.objects.get(post_id=pk)
            serializer = PostDetailSerializer(post)
            return Response(data_schema(status.HTTP_200_OK, "Post retrieved successfully", serializer.data))
        except Post.DoesNotExist:
            return Response(data_schema(status.HTTP_404_NOT_FOUND, "Post not found"))
        except ParseError as e:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, str(e)))
        except Exception as e:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "An error occurred: " + str(e)))
