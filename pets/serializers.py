from rest_framework import serializers
from .models import *
from app.serializers import UserSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nickname', 'phone_number', 'avatar', 'address', 'background', 'created_at',
                  'signature']


class PetSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    species_name_cn = serializers.CharField(source='species.species_name_cn', read_only=True)
    species_name_cn_input = serializers.CharField(write_only=True, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Pet
        fields = ['user_id', 'pet_id', 'pet_name', 'pet_type', 'species_name_cn', 'species_name_cn_input', 'sex',
                  'birth_date', 'weight', 'qr_code', 'avatar', 'sterilization', 'user']

    # 新增宠物序列器
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        species_name_cn_input = validated_data.pop('species_name_cn_input')
        user = User.objects.get(id=user_id)
        species = Pet_encyclopedia.objects.get(species_name_cn=species_name_cn_input)
        pet = Pet.objects.create(user=user, species=species, **validated_data)
        return pet

    # 更新宠物序列器
    def update(self, instance, validated_data):
        if 'species_name_cn_input' in validated_data:
            species_name_cn_input = validated_data.pop('species_name_cn_input')
            instance.species = Pet_encyclopedia.objects.get(species_name_cn=species_name_cn_input)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# 宠物百科序列化器
class PetEncyclopediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet_encyclopedia
        fields = ['species_id', 'pet_type', 'species_name', 'species_name_cn', 'characteristic', 'care_instruction']


# 宠物护理日记序列化器
class PetCareDiarySerializer(serializers.ModelSerializer):
    pet_id = serializers.IntegerField(write_only=True)
    pet = PetSerializer(read_only=True)

    class Meta:
        model = Pet_care_diary
        fields = ['diary_id', 'pet_id', 'content', 'weight', 'pet', 'diary_date']

    # 新增宠物护理日记序列器
    def create(self, validated_data):
        pet_id = validated_data.pop('pet_id')
        pet = Pet.objects.get(pet_id=pet_id)
        diary = Pet_care_diary.objects.create(pet=pet, **validated_data)
        return diary

# class PetListSerializer(serializers.ModelSerializer):
#     """ 宠物列表序列化器 """
#     user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.user_id')
#
#     class Meta:
#         model = Pet
#         fields = '__all__'
#
#
# class PetDetailSerializer(serializers.ModelSerializer):
#     """ 宠物序列化器 """
#     user = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Pet
#         fields = '__all__'
#
#
# class PetCreateSerializer(serializers.ModelSerializer):
#     """ 创建宠物序列化器 """
#     user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
#
#     class Meta:
#         model = Pet
#         fields = ['pet_name', 'pet_type', 'species_id', 'user_id', 'sex', 'age', 'weight', 'qr_code']
#
#     def create(self, validated_data):
#         # 用户已经通过 user_id 字段验证并从 User 模型中获取
#         return Pet.objects.create(**validated_data)
#
#
# class PetUpdateSerializer(serializers.ModelSerializer):
#     """ 更新宠物序列化器 """
#
#     class Meta:
#         model = Pet
#         fields = ['pet_name', 'pet_type', 'species_id', 'sex', 'age', 'weight', 'qr_code']
#         read_only_fields = ['qr_code']  # 假设qr_code在创建后不可更改
#
#     def update(self, instance, validated_data):
#         # 这里你可以添加任何特定的更新逻辑
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance
