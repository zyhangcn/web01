from django.db import models

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
