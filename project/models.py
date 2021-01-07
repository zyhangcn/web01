from django.db import models


class Project(models.Model):
    '''
         项目表
    '''
    project_name = models.CharField(max_length=128)
    start_time = models.DateField()
    end_time = models.DateField()
    customer_num = models.IntegerField(default=0)
    introduce = models.TextField(null=False)
    is_delete = models.BooleanField(default=False)
    # 项目的拥有者
    user = models.IntegerField(default=None)
