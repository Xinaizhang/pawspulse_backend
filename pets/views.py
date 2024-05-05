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


class PetViewSet(viewsets.ViewSet):
    authentication_classes = []

    def retrieve(self, request, pk=None):
        """ 根据 pet_id 返回宠物信息 """
        try:
            if pk is None:
                raise ParseError("Pet ID is required")

            pet = Pet.objects.get(pet_id=pk)
            serializer = PetDetailSerializer(pet)
            return Response(data_schema(status.HTTP_200_OK, "Pet retrieved successfully", serializer.data),
                            status.HTTP_200_OK)
        except Pet.DoesNotExist as e:
            return Response(data_schema(status.HTTP_404_NOT_FOUND, "Pet not found", str(e)),
                            status=status.HTTP_404_NOT_FOUND)
        except ParseError as e:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "ParseError", str(e)),
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "An error occurred", str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """ 新增宠物 """

        serializer = PetCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pet = serializer.save()  # 尝试保存宠物到数据库
                return Response(data_schema(status.HTTP_201_CREATED, "Pet created successfully"),
                                status=status.HTTP_201_CREATED)
            except (IntegrityError, DatabaseError) as e:
                return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "参数不正确", str(serializer.errors)),
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ 删除宠物 """
        try:
            if pk is None:
                raise ParseError("Pet ID is required")

            pet = Pet.objects.get(pet_id=pk)
            pet.delete()
            return Response(data_schema(status.HTTP_204_NO_CONTENT, "Pet deleted successfully"),
                            status.HTTP_204_NO_CONTENT)
        except Pet.DoesNotExist as e:
            return Response(data_schema(status.HTTP_404_NOT_FOUND, "Pet not found", str(e)),
                            status=status.HTTP_404_NOT_FOUND)
        except ParseError as e:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "ParseError", str(e)),
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "An error occurred", str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """更新宠物信息"""
        if pk is None:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "Pet ID is required"),
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            pet = Pet.objects.get(pet_id=pk)  # 获取宠物实例
        except Pet.DoesNotExist:
            return Response(data_schema(status.HTTP_404_NOT_FOUND, "Pet not found"),
                            status=status.HTTP_404_NOT_FOUND)

        serializer = PetUpdateSerializer(pet, data=request.data, partial=True)  # 使用 PetUpdateSerializer，并允许部分更新
        if serializer.is_valid():
            try:
                updated_pet = serializer.save()  # 保存更新
                return Response(data_schema(status.HTTP_200_OK, "Pet updated successfully", serializer.data),
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "An error occurred", str(e)),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "Invalid parameters", serializer.errors),
                            status=status.HTTP_400_BAD_REQUEST)

    def pet_by_user(self, request, user_id=None):
        """ 根据user_id返回用户的所有宠物 """
        if user_id is None:
            return Response(data_schema(status.HTTP_400_BAD_REQUEST, "User ID is required"),
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            pets = Pet.objects.filter(user_id=user_id)  # 获取指定用户的所有宠物
            serializer = PetListSerializer(pets, many=True)
            return Response(data_schema(status.HTTP_200_OK, "Pets retrieved successfully", serializer.data),
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data_schema(status.HTTP_500_INTERNAL_SERVER_ERROR, "An error occurred", str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
