import logging

from rest_framework.permissions import BasePermission

logger = logging.getLogger("projectlog")


class MyPermission(BasePermission):
    message = '用户权限验证失败'

    def has_permission(self, request, view):
        if request.method in ["POST", 'PUT', 'DELETE']:
            if request.user.identify == 2 or request.user.identify == 0:
                return True
            else:
                return False
        else:
            return True

    def has_object_permission(self, request, view, obj):

        if request.method in ["PUT", "DELETE"]:
            if request.user.identify == 2:
                return True
            if request.user.id == obj.user:
                return True
            else:
                logger.info("没有操作权限")
                return False
        return True
