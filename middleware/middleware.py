import json
import logging
import time
import datetime

from django.http import JsonResponse
from django.urls import resolve, Resolver404
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse

from customer.models import Token
from utility.cache import rds

logger = logging.getLogger("access")


class LoginAuthToken(MiddlewareMixin):

    def process_request(self, request):
        White_list = ['/login/',
                      '/register/']
        request.start_time = time.time()
        print(dir(request))
        token = request.headers.get('token')
        rds_user_id = rds.get(token)
        if request.get_full_path() in White_list:
            if rds_user_id is not None:
                return JsonResponse({"LL": "yijingdengl"})
        else:
            if token is None:
                logger.info("没有传token")
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            if rds_user_id is None:
                logger.info("非法请求")
                obj_token = Token.objects.get(pk=token)
                now_time = datetime.datetime.now()
                delat = (now_time - obj_token.created_time).seconds
                if obj_token.count() != 0 and delat < 10:
                    pass
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

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
