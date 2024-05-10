# app/views.py
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
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


# 发送验证码
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
                "id": user.id,
                "email": user.email,
                "nickname": user.nickname,
                "password": user.password,
                "created_at": user.created_at
            }
            return Response(data_schema(status.HTTP_201_CREATED, "用户注册成功", response_data),
                            status=status.HTTP_201_CREATED)
        return Response(data_schema(status.HTTP_400_BAD_REQUEST, "验证码不正确", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# 用户登录 - 接受用户提供的用户名或邮箱和密码，验证用户身份并返回 JWT Token。
class LoginView(APIView):
    authentication_classes = []  # 登录无需身份认证

    def post(self, request, *args, **kwargs):
        # 使用登录序列化器验证输入的数据
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # 生成 JWT Token
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(access),
                'id': user.id,
                'nickname': user.nickname,
                'email': user.email
            }

            return Response(data_schema(status.HTTP_200_OK, '登录成功', response_data),
                            status=status.HTTP_200_OK)
        return Response(data_schema(status.HTTP_400_BAD_REQUEST, '登录失败', serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

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
        user = self.request.user  # Assuming user is logged in and verified
        instance = self.get_object()

        # Check if the requesting user is allowed to delete this user
        if user != instance and not user.is_superuser:
            return Response(data_schema(status.HTTP_403_FORBIDDEN, "无权限删除此用户"),
                            status=status.HTTP_403_FORBIDDEN)

        try:
            with transaction.atomic():
                # Delete associated EmailVerification record
                EmailVerification.objects.filter(email=instance.email).delete()
                # Delete the User instance
                self.perform_destroy(instance)
            return Response(data_schema(status.HTTP_204_NO_CONTENT, "成功注销用户"),
                            status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(data_schema(status.HTTP_404_NOT_FOUND, "用户不存在"),
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, f"删除用户失败: {str(e)}"),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """根据 id 获取单个用户的详细信息"""
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
        id = kwargs.get('id')
        user = User.objects.filter(id=id).first()
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
        id = kwargs.get('id')
        user = User.objects.filter(id=id).first()
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
