from django.test import TestCase
from customer.models import Customer
import multiprocessing
import os
import sys
import time
import random
from django.test import Client


a1 = (1976, 1, 1, 0, 0, 0, 0, 0, 0)
a2 = (1990, 12, 31, 23, 59, 59, 0, 0, 0)
a3 = (2000, 1, 1, 1, 1, 1, 1, 1, 1)
start = time.mktime(a1)
end = time.mktime(a2)
end2 = time.mktime(a3)
username = ''.join([chr(random.randint(25000, 29000)) for i in range(3)])
age = random.randint(0, 110)
professional = random.choice(["海员", "经纪人", "建筑师", "建筑工人", "教练", "记者",
                              "剧作家", "教育家", "教授", "经理"])
province = random.choice(["河北省", "山西省", "辽宁省", "吉林省", "黑龙江省", "江苏省",
                          "浙江省", "安徽省", "福建省", "江西省", "山东省", "台湾省", "河南省"])
city = random.choice(["石家庄市", "保定市", "唐山市", "邯郸市", "邢台市", "衡水市",
                      "鹿泉市", "秦皇岛市", "南宫市", "任丘市", "辛集市",
                      "黄骅市", "遵化市", "张家口市", "沙河市", "冀州市",
                      "泊头市", "安国市", "双滦区", "高碑店市"])
t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
date_touple = time.localtime(t)  # 将时间戳生成时间元组
start_time = time.strftime("%Y-%m-%d", date_touple)


class CustomerTest(TestCase):
    def setUp(self) -> None:
        Customer.objects.create(username=username, age=age, professional=professional
                                , province=province, city=city, join_time=start_time)


def add():
    print("asdasd","kklkl")