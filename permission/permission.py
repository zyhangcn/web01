import logging

from rest_framework.permissions import BasePermission

import const
from utility.cache import rds
from customer.models import User

logger = logging.getLogger("projectlog")


class MyPermission(BasePermission):
    message = '用户权限验证失败'

    def has_permission(self, request, view):
        if request.method in ["POST", 'PUT', 'DELETE']:
            if request.user.identify == const.ADMIN or request.user.identify == const.MEMBER:
                return True
            else:
                return False
        else:
            return True

    def has_object_permission(self, request, view, obj):

        if request.user.identify == const.ADMIN:
            return True
        else:
            if request.user.id == obj.user and request.method == 'DELETE':
                logger.info("没有操作权限")
                return False
            else:
                print(request.method)
                return True

        # if request.method in ["PUT"]:
        #     if request.user.identify == const.ADMIN:
        #         return True
        #     if request.user.id == obj.user:
        #         return True
        #     else:
        #
        #         return False
        # elif request.method == 'DELETE' and request.user.identify == const.ADMIN:
        #
        # return True
