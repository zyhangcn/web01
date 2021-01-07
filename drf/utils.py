# -*- coding: UTF-8 -*-
# @Date ：2020/8/7 6:02 下午
import re
from collections import defaultdict


def invalid_template(v):
    template = {"code": "invalid", "message": str(v)}
    return template


def exception_str_detail(fields: dict, field: str, exception):
    fields[field].append(invalid_template(exception))


def exception_dict_detail(fields: dict, field: str, exception_dict: dict):
    for child_field, exception in exception_dict.items():
        if exception:
            mid_field = ".".join([str(field), str(child_field)])
            if isinstance(exception, list):
                exception_list_detail(fields, mid_field, exception)
            elif isinstance(exception, dict):
                exception_dict_detail(fields, mid_field, exception)
            else:
                exception_str_detail(fields, mid_field, exception)


def exception_list_detail(fields: dict, field: str, exception_list: list):
    length = len(exception_list)
    for num in range(length):
        exception = exception_list[num]
        if exception:
            if isinstance(exception, list):
                exception_list_detail(fields, field, exception)
            elif isinstance(exception, dict):
                field = ".".join([field, str(num)])
                exception_dict_detail(fields, field, exception)
            else:
                exception_str_detail(fields, field, exception)


def generate_fields(data):
    fields = defaultdict(list)
    for field, multi_exception in data.items():
        assert isinstance(multi_exception, (list, dict))

        if isinstance(multi_exception, list):
            exception_list_detail(fields, field, multi_exception)
        elif isinstance(multi_exception, dict):
            exception_dict_detail(fields, field, multi_exception)

    return fields


# def make_markdown_table(array: list):
#     """把数组转为markdown格式的字符串
#     :array: [['title', 'value'], ['asd', '1']]
#     """
#     array.insert(0, ["值", "描述"])
#     markdown = "\n" + str("| ")
#
#     for e in array[0]:
#         to_add = " " + str(e) + str(" |")
#         markdown += to_add
#     markdown += "\n"
#
#     markdown += "|"
#     for i in range(len(array[0])):
#         markdown += str("-------------- | ")
#     markdown += "\n"
#
#     for entry in array[1:]:
#         markdown += str("| ")
#         for e in entry:
#             to_add = str(e) + str(" | ")
#             markdown += to_add
#         markdown += "\n"
#
#     return markdown + "\n"
#
#
# def make_markdown_description(data):
#     return "\n".join("* `{}` - {}".format(k, v) for k, v in data)
#
#
# def get_value(request, search_param):
#     """
#     筛选器获取get请求参数
#     """
#     value = request.query_params.get(search_param, "")
#     value = value.replace("\x00", "").strip()
#     return value
