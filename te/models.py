from django.db import models
from django.db.models import Lookup

from rest_framework.serializers import ModelSerializer


# Create your models here.


class A(models.Model):
    username = models.CharField(max_length=32)
    age = models.IntegerField()
    sex = models.BooleanField(default=True)
    introduce = models.TextField()

    class Meta:
        app_label = 'project'


class ASerializer(ModelSerializer):

    def create(self, validated_data):
        instance = A.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        return instance

    class Meta:
        model = A
        fields = [
            'username',
            'age',
            'sex',
            'introduce'
        ]


# 自建查询器
class NotEuql(Lookup):
    lookup_name = "ne"

    def as_sql(self, compiler, connection):
        print("compiler", compiler)
        print("connection", connection)
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        print(lhs_params)
        print("lhs_params + rhs_params", rhs_params)
        print(params)
        print('%s <> %s' % (lhs, rhs), params)
        return '%s <> %s' % (lhs, rhs), params


from django.db.models import Field

Field.register_lookup(NotEuql)
# print(A.objects.filter(username__ne="aa"))
