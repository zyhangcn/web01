from django.db import models

from project.models import Project


class Customer(models.Model):
    '''
        客户表
    '''
    username = models.CharField(max_length=64, unique=True, null=False)
    age = models.IntegerField()
    professional = models.CharField(max_length=64)
    province = models.CharField(max_length=32, null=False)
    city = models.CharField(max_length=32, null=False)
    join_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    project = models.ForeignKey(Project, null=True,
                                on_delete=models.DO_NOTHING,
                                default=None,
                                related_name="users_set")

    # 用户默认值为None、不属于任何一个项目、

    class Meta:
        ordering = ['username', 'age']


class Token(models.Model):
    '''
        token 登录认证表
    '''
    token = models.CharField(max_length=200,
                             primary_key=True)
    created_time = models.DateField(auto_now_add=True)
    user = models.OneToOneField(to="customer.User",
                                on_delete=models.DO_NOTHING)


class User(models.Model):
    """
        用户登录表
    """
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    identify = models.SmallIntegerField(choices=(
        (0, "普通用户"), (2, "管理员"), (4, "超级管理员")
    ), default=0)
    # 0 普通用户 2 admin 4 superadmin
    is_delete = models.BooleanField(default=False)
