# app/views.py
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *


# 定义通用的数据响应格式
def data_schema(code, message, data=None):
    return {
        "code": code,
        "message": message,
        "data": data
    }


def generate_verification_code(length=6):
    import random
    return ''.join(random.choices('0123456789', k=length))


def send_verification_code_email(email, code):
    from django.core.mail import send_mail
    subject = '欢迎注册PawsPulse账号'
    message = f'您的验证码为：{code}。\n请勿告知他人。'
    send_mail(subject, message, 'zhangxinai_02@163.com', [email], fail_silently=False)


class EmailVerificationView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                return Response(data_schema(status.HTTP_400_BAD_REQUEST, "该邮箱已被注册"),
                                status=status.HTTP_400_BAD_REQUEST)

            code = generate_verification_code()
            email_verification, created = EmailVerification.objects.update_or_create(
                email=email,
                defaults={'verification_code': code, 'is_verified': False}
            )
            send_verification_code_email(email, code)
            return Response(data_schema(status.HTTP_200_OK, "验证码已发送，请查收", email), status=status.HTTP_200_OK)
        return Response(
            data_schema(status.HTTP_400_BAD_REQUEST, "邮箱无效或已被注册，请重新输入邮箱", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST)


# 用户注册 - 接受用户提供的邮箱、验证码、昵称和密码，验证验证码并注册用户。
class UserRegistrationView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # 更新邮箱验证状态
            EmailVerification.objects.filter(email=user.email).update(is_verified=True)
            response_data = {
                "user_id": user.user_id,
                "email": user.email,
                "nickname": user.nickname,
                "password_hash": user.password_hash,
                "created_at": user.created_at
            }
            return Response(data_schema(status.HTTP_201_CREATED, "用户注册成功", response_data),
                            status=status.HTTP_201_CREATED)
        return Response(data_schema(status.HTTP_400_BAD_REQUEST, "验证码不正确", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# 用户提交注册信息
# class UserRegistrationView(APIView):
#     authentication_classes = []
#
#     def post(self, request, *args, **kwargs):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             response_data = {
#                 "user_id": user.user_id,
#                 "email": user.email,
#                 "nickname": user.nickname,
#                 "password_hash": user.password_hash,
#                 "created_at": user.created_at
#             }
#             return Response(data_schema(status.HTTP_201_CREATED, "用户注册成功，请查收邮箱验证码", response_data),
#                             status=status.HTTP_201_CREATED)
#         return Response(data_schema(status.HTTP_400_BAD_REQUEST, "数据无效", serializer.errors),
#                         status=status.HTTP_400_BAD_REQUEST)
#
#
# # 验证邮箱验证码
# class VerifyCodeView(APIView):
#     authentication_classes = []
#
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         verification_code = request.data.get('verification_code')
#
#         # 从数据库中获取用户
#         user = get_object_or_404(User, email=email)
#
#         # 检查验证码
#         if user.verification_code == verification_code:
#             user.verification_code = None  # 清除验证码
#             user.save()
#             return Response({
#                 "code": status.HTTP_200_OK,
#                 "message": "验证码验证成功，用户已激活",
#                 "data": {
#                     "user_id": user.user_id,
#                     "email": user.email,
#                     "nickname": user.nickname,
#                     "created_at": user.created_at,
#                 }
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 "code": status.HTTP_400_BAD_REQUEST,
#                 "message": "验证码错误或已过期",
#                 "data": None
#             }, status=status.HTTP_400_BAD_REQUEST)


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
            return Response(data_schema(status.HTTP_201_CREATED, "用户注册成功", serializer.data),
                            status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "Invalid input", str(e)),
                            status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(data_schema(status.HTTP_409_CONFLICT, "Conflict", "用户信息已存在"),
                            status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error", str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """删除用户"""
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(data_schema(status.HTTP_204_NO_CONTENT, "成功注销用户"),
                            status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(data_schema(status.HTTP_404_NOT_FOUND, "用户不存在"),
                            status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "删除用户失败"),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """根据 user_id 获取单个用户的详细信息"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(data_schema(status.HTTP_200_OK, "成功获取用户信息", serializer.data),
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data_schema(status.HTTP_404_NOT_FOUND, "用户不存在"),
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "获取用户信息失败", str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadAvatarView(APIView):
    authentication_classes = []
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return Response(data_schema(status.HTTP_404_NOT_FOUND, "用户不存在"),
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data_schema(status.HTTP_200_OK, "头像上传成功", serializer.data),
                            status=status.HTTP_200_OK)
        else:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "数据无效", serializer.errors),
                            status=status.HTTP_400_BAD_REQUEST)


class UploadBackgroundView(APIView):
    authentication_classes = []
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return Response(data_schema(status.HTTP_404_NOT_FOUND, "用户不存在"),
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data_schema(status.HTTP_200_OK, "背景图上传成功", serializer.data),
                            status=status.HTTP_200_OK)
        else:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "数据无效", serializer.errors),
                            status=status.HTTP_400_BAD_REQUEST)
