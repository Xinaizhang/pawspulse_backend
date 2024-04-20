from django.shortcuts import render, HttpResponse
from django.contrib.auth.hashers import make_password


# Create your views here.
def index(request):
    return HttpResponse("欢迎使用")


# 登录
def signin(request):
    return HttpResponse("登录")


from app.models import user


def orm(request):
    # 测试ORM操作表中的数据
    user.objects.create(email="mingyu@example.com",
                        nickname="mingyu",
                        phoneNumber="1234567899",
                        passwordHash=make_password("2333"),
                        )

    return HttpResponse("成功")
