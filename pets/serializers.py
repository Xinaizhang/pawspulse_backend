from rest_framework import serializers
from .models import *
from app.serializers import UserSerializer


class PetListSerializer(serializers.ModelSerializer):
    """ 宠物列表序列化器 """
    user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.user_id')

    class Meta:
        model = Pet
        fields = '__all__'


class PetDetailSerializer(serializers.ModelSerializer):
    """ 宠物序列化器 """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Pet
        fields = '__all__'


class PetCreateSerializer(serializers.ModelSerializer):
    """ 创建宠物序列化器 """
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = Pet
        fields = ['pet_name', 'pet_type', 'species_id', 'user_id', 'sex', 'age', 'weight', 'qr_code']

    def create(self, validated_data):
        # 用户已经通过 user_id 字段验证并从 User 模型中获取
        return Pet.objects.create(**validated_data)


class PetUpdateSerializer(serializers.ModelSerializer):
    """ 更新宠物序列化器 """

    class Meta:
        model = Pet
        fields = ['pet_name', 'pet_type', 'species_id', 'sex', 'age', 'weight', 'qr_code']
        read_only_fields = ['qr_code']  # 假设qr_code在创建后不可更改

    def update(self, instance, validated_data):
        # 这里你可以添加任何特定的更新逻辑
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
