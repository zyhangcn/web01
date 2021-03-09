import hashlib
import time
import collections

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, schema
from django.views import View
from rest_framework.schemas import AutoSchema

from utility.cache import rds
from customer.models import Token
from customer.models import User
from customer.models import Customer


def get_token_code(username):
    timestamp = str(time.time())
    m = hashlib.md5(username.encode("utf-8"))

    m.update(timestamp.encode("utf-8"))
    return m.hexdigest()


@api_view(['POST', ])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    hash_password = hashlib.sha1(password.encode("utf-8"))
    hash_password = hash_password.hexdigest()
    user = User.objects.create(username=username, password=hash_password)
    user.save()
    return Response({"message": '注册成功'}, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    hash_password = hashlib.sha1(password.encode("utf-8")).hexdigest()
    user = User.objects.filter(username=username, password=hash_password, is_delete=False).first()
    if not user:
        return Response({"msg": "用户名或密码不对!"}, status=status.HTTP_200_OK)
    token = get_token_code(username)
    rds.set(token, user.id, ex=10000)
    Token.objects.create(token=token, user=user.id)
    return Response(headers={"token": token}, status=status.HTTP_200_OK)


@api_view()
def login_out(request):
    token = request.headers.get('token')
    rds.delete(token)
    return Response()


def skk(request, year=3333):
    return redirect(Customer.objects.get(pk=1))
    # return JsonResponse({"dasd":"asdas"})
