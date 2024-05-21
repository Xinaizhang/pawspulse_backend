# app/serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *


# 邮箱验证码序列化器
class EmailVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)  # 添加格式验证

    class Meta:
        model = EmailVerification
        fields = ['email']


# 用户注册序列化器
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
        user.set_password(password)
        user.save()
        return user


# 登录序列化器
class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # 用户名或邮箱字段
    password = serializers.CharField()  # 密码字段

    def validate(self, data):
        identifier = data['identifier']
        password = data['password']

        # 查找用户，可通过昵称或邮箱登录
        user = User.objects.filter(email=identifier).first() or User.objects.filter(nickname=identifier).first()

        if not user:
            raise serializers.ValidationError('用户不存在')

        # 验证密码是否匹配
        if not user.check_password(password):
            raise serializers.ValidationError('密码错误')

        data['user'] = user
        return data


# 用户序列化器
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email', 'nickname', 'avatar', 'background', 'address', 'password',
                  'created_at', 'signature']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.signature = validated_data.get('signature', instance.signature)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.background = validated_data.get('background', instance.background)

        # Update the password only if it's provided
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance