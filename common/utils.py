from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ("page", {
                "current": self.page.number,  # 显示当前的页码
                "size": self.page.paginator.per_page,  # 每页显示的数量
                "total": self.page.paginator.num_pages  # 总共多少页
            }),
            ('records', data)
        ]))


def my_get_paginated_response(self, page):
    # 对序列化分页器进行封装
    serializer = self.get_serializer(page, many=True)
    assert self.paginator is not None
    self.paginator.get_paginated_response(serializer.data)

    data = {
        "records": serializer.data,
        "page": {
            "current": self.paginator.page.number,
            "size": self.paginator.page.paginator.count,
            "total": self.paginator.page.paginator.num_pages
        }
    }
    return Response(data)
