import hashlib
import time
import collections

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from customer.models import Token
from customer.models import User


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


# @api_view(['POST', ])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    hash_password = hashlib.sha1(password.encode("utf-8")).hexdigest()
    user = User.objects.filter(username=username, password=hash_password, is_delete=False).first()
    if not user:
        return Response({"msg": "用户名或密码不对!"}, status=status.HTTP_200_OK)
    # 删除原有的Token
    # old_token = Token.objects.filter(user_id=user.id)
    # old_token.delete()
    # # 创建新的Token
    # token = get_token_code(username)
    # Token.objects.update_or_create(token=token, user=user)
    request.session['user_id'] = user.id
    # return Response(headers={"token": token}, status=status.HTTP_200_OK)


@api_view()
def login_out(requset):
    user_id = requset.session.get('user_id')
    if user_id is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token = Token.objects.filter(user_id=user_id)
    token.delete()
    del requset.session['user_id']
    return JsonResponse({"message": "登出成功"})


class Test(APIView):

    def __get__(self, instance, owner):
        print(instance)
