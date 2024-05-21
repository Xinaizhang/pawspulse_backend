"""
URL configuration for pawspulse_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from community.views import PostViewSet

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [path('admin/', admin.site.urls),
               # app中的urls
               path('app/', include('app.urls')),
               # pets中的urls'
               path('pets/', include('pets.urls')),
               path('', include(router.urls)),
               path('posts/user/<int:user_id>/', PostViewSet.as_view({'get': 'posts_by_user'}), name='user_posts'),

               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 用于提供媒体文件
