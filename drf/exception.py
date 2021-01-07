# -*- coding: UTF-8 -*-
# @Date ：2020/7/7 5:19 下午
from django.http import Http404
from rest_framework.views import set_rollback
from rest_framework import exceptions, status
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied

from .utils import generate_fields


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()
    elif isinstance(exc, exceptions.NotAuthenticated):
        exc.status_code = status.HTTP_401_UNAUTHORIZED

    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {"message": exc.detail}

        if isinstance(exc, exceptions.ValidationError):
            fields = generate_fields(data)
            data = {"message": "字段校验失败", "fields": fields}
            exc.status_code = 422
        set_rollback()
        return Response(data, status=exc.status_code)

    return None
