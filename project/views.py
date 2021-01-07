import logging

from django.db.models import F
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

import const
from .models import Project
from .serializer import (
    ProjectDetailSerializer, ProjectOperUser, ProjectListSerializer
)
from permission.permission import MyPermission
from customer.models import User, Customer
from permission.myauth import MyAuth
from common.utils import my_get_paginated_response as paginated_response
from drf.filters import SearchFilter

log = logging.getLogger(name='projectlog')


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all().filter(is_delete=False)
    serializer_class = ProjectListSerializer
    authentication_classes = (MyAuth,)
    permission_classes = (MyPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ['project_name']

    my_get_paginated_response = paginated_response

    def list(self, request, *args, **kwargs):
        # print(request.auth)
        # 认证令牌 token的值
        # print(request.authenticators)
        # 认证类
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.my_get_paginated_response(page)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update({"user": request.session['user_id']})
        self.perform_create(serializer)
        log.info("项目创建成功")
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().filter(is_delete=False)
    serializer_class = ProjectDetailSerializer
    authentication_classes = (MyAuth,)
    permission_classes = (MyPermission,)

    def destroy(self, request, *args, **kwargs):
        # 删除项目
        project_id = kwargs.get("pk")
        instance = self.get_object()
        User.objects.filter(project_id=project_id).update(project_id=None)
        instance.is_delete = True
        instance.user_num = 0
        instance.save()
        log.info("项目删除成功")
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@authentication_classes([MyAuth])
@permission_classes([MyPermission])
def ProjectAddUser(request):
    projectid = request.data.get("projectid")
    try:
        instance = Project.objects.get(pk=projectid)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if instance.customer_num >= const.PROJECT_USER_MAX_NUM:
        log.info("当前项目人数以达上限")
        return Response({"message": "当前项目人数以达上限"}, status=status.HTTP_202_ACCEPTED)

    customerid = request.data.get("customerid")
    try:
        customer = Customer.objects.get(pk=customerid)
    except Customer.DoesNotExist:
        log.info("当前用户不存在")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if customer.project_id:
        log.info("当前用户已经被分配，不能添加")
        return Response({"message": "当前用户已经被分配"}, status=status.HTTP_202_ACCEPTED)
    instance.customer_num = F('customer_num') + 1
    customer.project_id = instance.id
    customer.save()
    instance.save()
    log.info("项目添加用户成功")
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['DELETE'])
@authentication_classes([MyAuth])
@permission_classes([MyPermission])
def ProjectDeleteCustomer(request):
    projectid = request.data.get('projectid')
    try:
        instance = Project.objects.get(pk=projectid)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    customerid = request.data.get("customerid")
    try:
        customer = Customer.objects.filter(project_id=projectid).get(pk=customerid)
    except Customer.DoesNotExist:
        log.warning("非法请求")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    instance.customer_num = F('customer_num') - 1
    customer.project_id = None
    customer.save()
    instance.save()
    log.info("项目删除用户成功")
    return Response(status=status.HTTP_200_OK)


class ProjectRelationUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().filter(is_delete=False)
    serializer_class = ProjectOperUser
    authentication_classes = (MyAuth,)
    permission_classes = (MyPermission,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_num >= const.PROJECT_USER_MAX_NUM:
            log.info("当前项目人数以达上限")
            return Response({"message": "当前项目人数以达上限"}, status=status.HTTP_202_ACCEPTED)

        customer_id = kwargs.get("customer_id")
        try:
            customer = Customer.objects.get(pk=customer_id)
        except User.DoesNotExist:
            log.info("查找用户不存在")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if customer.project_id:
            log.info("当前用户已经被分配，不能添加")
            return Response({"message": "当前用户已经被分配"}, status=status.HTTP_202_ACCEPTED)

        instance.update(user_num=F('user_num') + 1)
        customer.project_id = instance.id
        customer.save()
        log.info("项目添加用户成功")
        return Response({"message": "用户添加成功"}, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        user_id = kwargs.get("customer_id", 0)
        try:
            user = User.objects.filter(project_id=instance.id).get(pk=user_id)
        except User.DoesNotExist:
            log.warning("非法请求")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        instance.update(user_num=F('user_num') - 1)
        user.project_id = None
        user.save()
        log.info("项目删除用户成功")
        return Response({"message": "用户删除成功"}, status=status.HTTP_202_ACCEPTED)
