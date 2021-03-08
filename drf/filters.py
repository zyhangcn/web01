import operator
from functools import reduce
from datetime import datetime, timedelta

from django.core import exceptions
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from rest_framework.filters import BaseFilterBackend


class RangeFilter(BaseFilterBackend):
    # 查询的值
    search_params = ['begin', 'end']
    # 搜索的字段
    filter_column = 'filterColumn'

    def get_search_terms(self, request, search_params):
        params = [get_value(request, search_param) for search_param in search_params]
        if not all(params):
            return ['', '']
        params[0] = datetime.strptime(params[0], "%Y-%m-%d")
        params[1] = datetime.strptime(params[1], "%Y-%m-%d") + timedelta(days=1)

        return params

    def filter_queryset(self, request, queryset, view):
        params = self.get_search_terms(request, self.search_params)
        if not all(params):
            return queryset
        try:
            queryset = queryset.filter(join_time__range=params)
        except exceptions.ValidationError:
            return queryset
        return queryset
        # start_time = get_value(request, "start_time")
        # if start_time:
        #     queryset = queryset.filter(join_time__gte=start_time)
        # end_time = request.query_params.get("end_time")
        # if end_time:
        #     queryset = queryset.filter(join_time__lte=end_time)
        # return queryset


class SearchFilter(BaseFilterBackend):
    # 查询的值
    search_param = 'word'
    # 搜索的字段
    filter_column = 'filterColumn'

    def filter_queryset(self, request, queryset, view):
        search_value = get_value(request, self.search_param)
        filter_column = get_value(request, self.filter_column)

        search_fields = getattr(view, 'search_fields', [])
        fields_map = getattr(view, 'fields_map', {})
        if search_value:
            if filter_column and (filter_column in search_fields):
                # 查询特定的字段
                fields = [filter_column]
            else:
                # 查询全部字段
                fields = search_fields
            # 构造查询模式
            orm_lookups = [
                LOOKUP_SEP.join([fields_map.get(field, field), 'contains'])
                for field in fields
            ]
            # 生成查询条件
            queries = [
                models.Q(**{orm_lookup: search_value}) for orm_lookup in orm_lookups
            ]
            queryset = queryset.filter(reduce(operator.or_, queries))
        # if project_name is not None:
        #     # todo : 项目名字不存在 ·ID报错
        #     project = Project.objects.filter(project_name=project_name).first()
        #     if project is not None:
        #         queryset = queryset.filter(project=project)
        return queryset


def get_value(request, search_param):
    """
    筛选器获取get请求参数
    """
    value = request.query_params.get(search_param, "")
    value = value.replace("\x00", "").strip()
    return value
