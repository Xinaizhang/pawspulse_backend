from django.db import IntegrityError, DatabaseError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.views import APIView

from .serializers import *
from .models import *


def data_schema(code, message, data=None):
    return {
        "code": code,
        "message": message,
        "data": data
    }


# B01 - 新增宠物
class PetCreateView(APIView):
    def post(self, request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data_schema(code=200, message="Pet created successfully", data=serializer.data),
                            status=status.HTTP_201_CREATED)
        return Response(data_schema(code=400, message="Invalid data", data=serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# B02 - 删除宠物
class PetDeleteView(APIView):
    def delete(self, request, pet_id):
        try:
            pet = Pet.objects.get(pet_id=pet_id)
            pet.delete()
            return Response(data_schema(code=200, message="Pet deleted successfully"), status=status.HTTP_200_OK)
        except Pet.DoesNotExist:
            return Response(data_schema(code=404, message="Pet not found"), status=status.HTTP_404_NOT_FOUND)


# 修改宠物信息
class PetUpdateView(APIView):
    def put(self, request, pet_id):
        try:
            pet = Pet.objects.get(pet_id=pet_id)
        except Pet.DoesNotExist:
            return Response(data_schema(code=404, message="Pet not found"), status=status.HTTP_404_NOT_FOUND)

        serializer = PetSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            updated_pet = serializer.save()
            response_data = serializer.data
            response_data['species_name_cn'] = updated_pet.species.species_name_cn
            return Response(data_schema(code=200, message="Pet updated successfully", data=response_data),
                            status=status.HTTP_200_OK)
        return Response(data_schema(code=400, message="Invalid data", data=serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# B04 - 获取用户的所有宠物
class UserPetsView(APIView):
    def get(self, request, user_id):
        pets = Pet.objects.filter(user_id=user_id)
        if pets.exists():
            serializer = PetSerializer(pets, many=True)
            return Response(data_schema(code=200, message="Pets retrieved successfully", data=serializer.data),
                            status=status.HTTP_200_OK)
        else:
            return Response(data_schema(code=404, message="No pets found for this user"),
                            status=status.HTTP_404_NOT_FOUND)


# B05 - 获取宠物详情
class PetDetailView(APIView):
    def get(self, request, pet_id):
        try:
            pet = Pet.objects.get(pet_id=pet_id)
            serializer = PetSerializer(pet)
            return Response(data_schema(code=200, message="Pet retrieved successfully", data=serializer.data),
                            status=status.HTTP_200_OK)
        except Pet.DoesNotExist:
            return Response(data_schema(code=404, message="Pet not found"), status=status.HTTP_404_NOT_FOUND)


# B06 - 获取宠物百科信息
class PetEncyclopediaView(APIView):
    def get(self, request, species_id):
        try:
            species = Pet_encyclopedia.objects.get(species_id=species_id)
            serializer = PetEncyclopediaSerializer(species)
            return Response(
                data_schema(code=200, message="Pet encyclopedia retrieved successfully", data=serializer.data),
                status=status.HTTP_200_OK)
        except Pet_encyclopedia.DoesNotExist:
            return Response(data_schema(code=404, message="Pet encyclopedia not found"),
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data_schema(code=500, message="An error occurred", data=str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# B07 - 新增宠物护理日记
class PetCareDiaryCreateView(APIView):
    def post(self, request):
        serializer = PetCareDiarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data_schema(code=200, message="Pet care diary created successfully", data=serializer.data),
                            status=status.HTTP_201_CREATED)
        return Response(data_schema(code=400, message="Invalid data", data=serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# B08 - 修改宠物护理日记
class PetCareDiaryUpdateView(APIView):
    def put(self, request, diary_id):
        try:
            diary = Pet_care_diary.objects.get(diary_id=diary_id)
        except Pet_care_diary.DoesNotExist:
            return Response(data_schema(code=404, message="Pet care diary not found"), status=status.HTTP_404_NOT_FOUND)

        serializer = PetCareDiarySerializer(diary, data=request.data, partial=True)
        if serializer.is_valid():
            updated_diary = serializer.save()
            return Response(data_schema(code=200, message="Pet care diary updated successfully", data=serializer.data),
                            status=status.HTTP_200_OK)
        return Response(data_schema(code=400, message="Invalid data", data=serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# B09 - 删除宠物护理日记
class PetCareDiaryDeleteView(APIView):
    def delete(self, request, diary_id):
        try:
            diary = Pet_care_diary.objects.get(diary_id=diary_id)
            diary.delete()
            return Response(data_schema(code=200, message="Pet care diary deleted successfully"),
                            status=status.HTTP_200_OK)
        except Pet_care_diary.DoesNotExist:
            return Response(data_schema(code=404, message="Pet care diary not found"), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data_schema(code=500, message="An error occurred", data=str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# B10 - 获取某宠物的所有护理日记
class PetCareDiaryListView(APIView):
    def get(self, request, pet_id):
        diaries = Pet_care_diary.objects.filter(pet_id=pet_id)
        if diaries.exists():
            serializer = PetCareDiarySerializer(diaries, many=True)
            return Response(
                data_schema(code=200, message="Pet care diaries retrieved successfully", data=serializer.data),
                status=status.HTTP_200_OK)
        else:
            return Response(data_schema(code=404, message="No pet care diaries found for this pet"),
                            status=status.HTTP_404_NOT_FOUND)
