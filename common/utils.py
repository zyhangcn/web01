from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        print(self.page)
        return Response(OrderedDict([
            ("page", {
                "current": self.page.number,  # 显示当前的页码
                "size": self.page.paginator.per_page,  # 每页显示的数量
                "total": self.page.paginator.count  # 总共多少页
            }),
            ('records', data)
        ]))
