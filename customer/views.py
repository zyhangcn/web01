import logging

from django.db.models import F
from rest_framework.filters import OrderingFilter
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Customer
from .serializer import CustomerSerializer
from .serializer import CustomerUpdateSerializer
from drf.filters import (RangeFilter, SearchFilter)

logger = logging.getLogger("projectlog")


class CustomerList(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer]
    queryset = Customer.objects.all().filter(is_delete=False)
    # permission_classes =
    serializer_class = CustomerSerializer
    filter_backends = (RangeFilter, SearchFilter, OrderingFilter)
    # 过滤器类
    search_fields = ['username', 'project_name']
    # todo 如果我想查询的用户名和职业名字有重复的结果会怎么样
    fields_map = {
        'project_name': 'project__project_name'
    }
    ordering_fields = ['age', 'username']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        logger.info("查询成功")
        return Response(serializer.data)



    def perform_create(self, serializer):
        serializer.save()
        logger.info("用户创建成功")


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all().filter(is_delete=False)
    serializer_class = CustomerUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 减少该用户所在项目的用户人数
        if instance.project_id is not None:
            instance.project.customer_num = F('customer_num') - 1
            instance.project.save()
        # 修改删除状态
        instance.is_delete = True
        instance.project_id = None
        instance.save()
        logger.info("用户删除成功")
        return Response(status=status.HTTP_204_NO_CONTENT)
