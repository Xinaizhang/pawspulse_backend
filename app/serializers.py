from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'phone_number', 'email', 'nickname', 'avatar', 'address', 'password_hash', 'created_at']

    def create(self, validated_data):
        user_instance = User.objects.create(**validated_data)
        return user_instance
