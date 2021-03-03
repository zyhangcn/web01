from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(read_only=True,
                                         source="project.project_name")

    def validate_age(self, value):
        if value < 0 or value > 120:
            raise serializers.ValidationError("年龄范围不合法")
        return value

    def validate_province(self, value):
        if value not in ["北京", "上海"]:
            raise serializers.ValidationError("省份不在列表中")
        return value

    def validate_city(self, value):
        if value not in ["北京", "上海"]:
            raise serializers.ValidationError("城市不在列表中")
        return value

    def validate(self, attrs):
        print(attrs)
        print(type(attrs))
        return attrs

    def create(self, validated_data):
        print(validated_data)
        instance =Customer.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)
        return instance

    class Meta:
        model = Customer
        fields = ("username",
                  "age",
                  "professional",
                  "province",
                  "city",
                  "join_time",
                  "update_time",
                  "project_name")


class CustomerUpdateSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(read_only=True,
                                         source="project.project_name")
    username = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = ("username",
                  "age",
                  "professional",
                  "province",
                  "city",
                  "project_name")

    def validate_province(self, value):
        if value not in ["北京", "上海"]:
            raise serializers.ValidationError("省份不在列表中")
        return value

    def validate_city(self, value):
        if value not in ["北京", "上海"]:
            raise serializers.ValidationError("城市不在列表中")
        return value
