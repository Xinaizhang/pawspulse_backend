from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from app import models
from rest_framework import status

from .serializers import *
from .models import *


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """创建用户"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # 构建返回数据格式
            data = {
                "code": status.HTTP_201_CREATED,
                "message": "用户注册成功",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            return Response({"code": status.HTTP_400_BAD_REQUEST, "message": "Invalid input", "data": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"code": status.HTTP_409_CONFLICT, "message": "Conflict", "data": "用户信息已存在"},
                            status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response(
                {"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "Internal Server Error", "data": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """删除用户"""
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except User.DoesNotExist:
            return Response({"message": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)  # 返回未找到资源错误信息
        except Exception as e:
            return Response({"message": "删除用户失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # 返回其他未知错误信息

        # 构建返回数据格式
        data = {
            "code": status.HTTP_204_NO_CONTENT,
            "message": "成功注销用户",
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        """根据 user_id 获取单个用户的详细信息"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = {
                "code": status.HTTP_200_OK,
                "message": "成功获取用户信息",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)  # 用户不存在错误信息
        except Exception as e:
            return Response({"message": "获取用户信息失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # 其他未知错误信息


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        # 1. 获取用户提交的用户名和密码
        print(request.data)
        phoneNumber = request.data.get("phoneNumber")
        password = request.data.get("password")

        # 2. 数据库校验用户名和密码
        user_object = models.User.objects.filter(phoneNumber=phoneNumber, password=password).first()
        if not user_object:
            return Response({"status": False, "message": "用户名或密码错误"})

        # 3. 若校验正确，则生成token
        token = str
        return Response("post")
