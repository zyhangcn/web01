from rest_framework import serializers
from rest_framework.validators import UniqueForDateValidator

from .models import Project
from customer.models import Customer


class ProjectListSerializer(serializers.ModelSerializer):
    introduce = serializers.CharField(write_only=True)

    def validate(self, attr):
        request = self.context["request"]

        if attr.get("end_time") < attr.get("start_time"):
            raise serializers.ValidationError("开始时间应该小于结束时间")
        else:
            return attr

    class Meta:
        model = Project
        fields = ("project_name",
                  "start_time",
                  "end_time",
                  "customer_num",
                  "introduce")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("username", 'age')


class ProjectDetailSerializer(serializers.ModelSerializer):
    users_set = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ("project_name",
                  "introduce",
                  "users_set")


class ProjectOperUser(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("project_name",
                  "start_time",
                  "end_time",
                  "customer_num")
