# -*- coding: UTF-8 -*-
# @Date ：2020/8/13 1:57 下午
from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

User = get_user_model()


class SessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = getattr(request._request, "user", None)
        print(user.is_authenticated)
        if not user or not user.is_active:
            return None
        return (user, None)


class OAuthAuthentication(BaseAuthentication):
    # 网关登录验证 直接使用此Authentication
    auth_header = "HTTP_X_AUTH_USER"

    def authenticate(self, request):
        email = request.META.get(self.auth_header, "")
        if not email:
            return None
        return self.authenticate_credentials(email, request)

    def authenticate_credentials(self, email, request=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.NotAuthenticated()

        return user, None
