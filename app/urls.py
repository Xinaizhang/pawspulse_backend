# app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send_verification_code/', EmailVerificationView.as_view(), name='send-verification-code'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),  # 登录路径

    path('upload-avatar/<int:user_id>/', UploadAvatarView.as_view(), name='upload-avatar'),
    path('upload-background/<int:user_id>/', UploadBackgroundView.as_view(), name='upload-background'),
]
