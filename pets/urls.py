# pets/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('create_pet/', PetCreateView.as_view(), name='create_pet'),
    path('delete_pet/<int:pet_id>/', PetDeleteView.as_view(), name='delete_pet'),
    path('update_pet/<int:pet_id>/', PetUpdateView.as_view(), name='update_pet'),
    path('user_pets/<int:user_id>/', UserPetsView.as_view(), name='user_pets'),
    path('pet_detail/<int:pet_id>/', PetDetailView.as_view(), name='pet_detail'),
    path('get_pet_encyclopedia/<int:species_id>', PetEncyclopediaView.as_view(), name='get_pet_encyclopedia'),
    path('create_diary/', PetCareDiaryCreateView.as_view(), name='create_pet_care_diary'),
    path('update_diary/<int:diary_id>/', PetCareDiaryUpdateView.as_view(), name='update_pet_care_diary'),
    path('delete_diary/<int:diary_id>/', PetCareDiaryDeleteView.as_view(), name='delete_pet_care_diary'),
    path('pet_diaries/<int:pet_id>/', PetCareDiaryListView.as_view(), name='pet_diaries'),
]
