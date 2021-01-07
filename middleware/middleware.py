import logging

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

from rest_framework import status
from customer.models import Token

logger = logging.getLogger("projectlog")


class LoginAuthToken(MiddlewareMixin):

    def process_request(self, request):
        White_list = ['/login/',
                      '/register/']
        if request.get_full_path() in White_list:
            pass
        else:
            token = request.headers.get('token')
            if token is None:
                logger.info("没有传token")
                return JsonResponse({"message": '当前用户未登录'}, status=status.HTTP_200_OK)
            server_token = Token.objects.filter(token=token).first()
            if server_token is None:
                logger.info("非法请求")
                return JsonResponse({"message": '当前用户未登录'}, status=status.HTTP_400_BAD_REQUEST)
            if request.session.get('user_id') != server_token.user_id:
                request.session['user_id'] = server_token.user_id
