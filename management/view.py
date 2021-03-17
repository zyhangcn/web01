import datetime
import hashlib
import time
import collections
from urllib.parse import urljoin, urlsplit, parse_qs, urlencode, urlunsplit

import requests
from django.conf import settings
from django.contrib import auth
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.decorators import api_view, schema, permission_classes

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


from django.contrib.auth import authenticate, login


def get_redirect_url(request):
    redirect_to = request.query_params.get('next') or request.META.get("HTTP_REFERER")
    url_is_safe = url_has_allowed_host_and_scheme(
        redirect_to,
        allowed_hosts={request.get_host(), "oauth.devops.hypers.cc", "haa.devops.hypers.cc"},
        require_https=request.is_secure()
    )
    redirect_to = redirect_to if url_is_safe else settings.LOGIN_REDIRECT_URL
    return redirect_to


def set_query_parameter(url, param_name, param_value):
    """Given a URL, set or replace a query parameter and return the
    modified URL.

    >>> set_query_parameter('http://example.com?foo=bar&biz=baz', 'foo', 'stuff')
    'http://example.com?foo=stuff&biz=baz'

    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))


def build_scheme_host(scheme, host):
    return f"{scheme}://{host}"


from xml.etree import ElementTree as ET


def cas_login_handle(request, ticket, service, cas_url):
    url = urljoin(cas_url, "proxyValidate")
    url = set_query_parameter(url, "ticket", ticket)
    url = set_query_parameter(url, "service", service)
    try:
        response = requests.get(url, verify=False)
    except requests.RequestException:
        pass
    else:
        tree = ET.fromstring(response.text)
        if tree[0].tag.endswith('authenticationSuccess'):
            email = tree[0][0].text
            login_time = datetime.datetime.strptime(
                tree[0][1][2].text.rstrip("[Etc/UTC]"),
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ) + datetime.timedelta(hours=8)  # 在cas那边登录的utc时间
            try:
                user = User.objects.get(email=email)
                if user.is_active:
                    login(request, user)  # 设置session
                    # 设置session过期时间，有效时间为在cas登录后加2小时
                    expiry_seconds = ((login_time + datetime.timedelta(hours=2)) - datetime.datetime.now()).seconds
                    data = dict(session_key=request.session.session_key, email=user.email)
                    cache.set(f"CAS:{ticket}", data, expiry_seconds)
                    request.session.set_expiry(expiry_seconds)
                    print(f"CAS Login Success: {ticket}")
                    return
                else:
                    raise PermissionDenied('用户未授权或授权被取消，请重新授权')
            except User.DoesNotExist:
                raise PermissionDenied('用户未授权或授权被取消，请重新授权')

    raise AuthenticationFailed()


@api_view(['GET', ])
@permission_classes([])
def django_login(request):
    redirect_to = get_redirect_url(request)
    if request.user.is_authenticated:
        return redirect(redirect_to)
    print(request.user)
    print(request.user.__class__)
    ticket = request.query_params.get("ticket")
    cas_url = urljoin(build_scheme_host(request.scheme, "127.0.0.1:8081"), "/")
    print(cas_url)
    service = set_query_parameter(
        urljoin(
            build_scheme_host(request.scheme, "zyh:8000"), reverse("login")
        ),
        "next",
        redirect_to,
    )
    print(service)
    if ticket:
        cas_login_handle(request, ticket, service, cas_url)
        return redirect(redirect_to)

    redirect_to = set_query_parameter(urljoin(cas_url, "login"), "service", service)
    print(redirect_to)
    return redirect(redirect_to)


@api_view(['GET'])
def django_out(request):
    auth.logout(request)
    redirect_to = get_redirect_url(request)
    return Response("asd")


@api_view(['GET'])
def kks(request):
    return Response("klkalskdlklasd")
