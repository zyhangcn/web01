from rest_framework.response import Response


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
