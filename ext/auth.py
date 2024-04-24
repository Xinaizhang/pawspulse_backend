from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from app import models


class QueryParamsAuthentication(BaseAuthentication):
    class MyAuthentication(BaseAuthentication):
        def authenticate(self, request):
            # 去做用户认证
            # 1.读取请求传递的token
            # 2.校验合法性
            # 3.认证成功 -> 返回元组(11,22) request.User request.auth
            #   认证失败 -> 抛出异常，返回错误信息
            #   返回None -> 交给下一个认证类处理
            token = request.query_params.get("token")
            if token:
                return token, 'userId'

            raise AuthenticationFailed({"code": 1001, "error": "认证失败"})

    def authenticate(self, request):
        token = request.query_params.get("token")
        if token:
            return token, 'userId'

        raise AuthenticationFailed({"code": 1001, "error": "认证失败"})

    def authenticate_header(self, request):
        return "APP"


class HeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")

        if token:
            return token, 'userId'

        raise AuthenticationFailed({"code": 1001, "error": "认证失败"})

    def authenticate_header(self, request):
        return "APP"


class NoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        raise AuthenticationFailed({"code": 1001, "error": "认证失败"})

    def authenticate_header(self, request):
        return "APP"
