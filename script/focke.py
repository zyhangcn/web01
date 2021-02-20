import multiprocessing
import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management.settings')
django.setup()

from customer.models import Customer
from project.models import Project

a1 = (1976, 1, 1, 0, 0, 0, 0, 0, 0)
a2 = (1990, 12, 31, 23, 59, 59, 0, 0, 0)
a3 = (2000, 1, 1, 1, 1, 1, 1, 1, 1)
start = time.mktime(a1)
end = time.mktime(a2)
end2 = time.mktime(a3)


def create_fake_user(num):
    for i in range(num):
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


        try:
            user = Customer.objects.create(username=username, age=age, professional=professional
                                           , province=province, city=city, join_time=start_time
                                           )
            user.save()
        except Exception as e:
            print(e)


def create_fake_project(num):
    instroduce_list = [chr(random.randint(25000, 29000)) for i in range(1000)]
    for i in range(num):
        introduce = ''.join(random.choices(instroduce_list, k=40))
        project_name = ''.join([chr(random.randint(28000, 29000)) for i in range(2)]) + '管理'
        t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
        date_touple = time.localtime(t)  # 将时间戳生成时间元组
        start_time = time.strftime("%Y-%m-%d", date_touple)
        End = random.randint(end, end2)
        end_time_touple = time.localtime(End)
        end_time = time.strftime("%Y-%m-%d", end_time_touple)
        project = Project.objects.create(project_name=project_name,
                                         start_time=start_time, end_time=end_time,
                                         introduce=introduce, user=76)
        project.save()


import time
import random
from multiprocessing import Process

if __name__ == '__main__':
    # create_fake_user(750000)
    # create_fake_project(20)
    for i in range(11):
        t = Process(target=create_fake_user,args=(200000,))
        t.start()
