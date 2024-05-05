# app/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *


class EmailVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)  # 添加格式验证

    class Meta:
        model = EmailVerification
        fields = ['email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    verification_code = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'nickname', 'password', 'verification_code']

    def validate(self, data):
        try:
            email_verification = EmailVerification.objects.get(email=data['email'])
            if email_verification.verification_code != data['verification_code']:
                raise serializers.ValidationError("验证码不正确")
            if email_verification.is_verified:
                raise serializers.ValidationError("该邮箱已被注册")
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("邮箱不存在或未申请验证码")
        return data

    def create(self, validated_data):
        validated_data.pop('verification_code')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password_hash = make_password(password)
        user.save()
        return user


# def generate_verification_code(length=6):
#     import random
#     return ''.join(random.choices('0123456789', k=length))
#
#
# def send_verification_code_email(email, code):
#     from django.core.mail import send_mail
#     subject = '欢迎注册PawsPulse账号'
#     message = f'欢迎使用邮箱注册PawsPulse账号，账号的验证码为：{code}。\n注意，请不要轻易将此验证码告知他人。若此内容非您操作，请忽视此条信息。'
#     send_mail(
#         subject,
#         message,
#         'zhangxinai_02@163.com',  # 替换为你的网易邮箱地址
#         [email],
#         fail_silently=False,
#     )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'phone_number', 'email', 'nickname', 'avatar', 'background', 'address', 'password_hash',
                  'created_at']

    def create(self, validated_data):
        user_instance = User.objects.create(**validated_data)
        return user_instance

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.background = validated_data.get('background', instance.background)
        instance.save()
        return instance
