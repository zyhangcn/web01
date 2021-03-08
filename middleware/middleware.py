import json
import logging
import time

from django.http import JsonResponse
from django.urls import resolve, Resolver404
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.response import Response

from customer.models import Token

logger = logging.getLogger("access")


class LoginAuthToken(MiddlewareMixin):

    def process_request(self, request):
        White_list = ['/login/',
                      '/register/']
        request.start_time = time.time()
        if request.get_full_path() in White_list:
            pass
        else:
            token = request.headers.get('token')
            if token is None:
                logger.info("没有传token")
                return JsonResponse(data={},status=status.HTTP_200_OK)
            server_token = Token.objects.filter(token=token).first()
            if server_token is None:
                logger.info("非法请求")
                return JsonResponse(data={},status=status.HTTP_400_BAD_REQUEST)
            if request.session.get('user_id') != server_token.user_id:
                request.session['user_id'] = server_token.user_id

    def process_response(self, request, response):
        if self._should_log_route(request):
            headers = {
                k: v for k, v in request.META.items() if k.startswith("HTTP_")
            }
            log_data = {
                "request_headers": headers,
                "request_method": request.method.upper(),
                "request_path": request.get_full_path(),
                "status_code": response.status_code,
                "run_time": time.time() - request.start_time,
            }

            logger.debug(
                "AccessInfo:\n{}".format(json.dumps(log_data, indent=2))
            )
        return response

    def _should_log_route(self, request):
        """
        是否是路由中的，存在则打印日志，不存在就忽略
        """
        urlconf = getattr(request, "urlconf", None)

        try:
            resolve(request.path, urlconf=urlconf)
        except Resolver404:
            return False
        return True
