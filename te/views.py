from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import ASerializer, A


class PartialUpdateModelMixin:
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class Alist(PartialUpdateModelMixin, ModelViewSet):
    queryset = A.objects.all()
    serializers = {
        'default': ASerializer,
        "post": ASerializer
    }

    def get_serializer_class(self):
        # print(self.action)
        return self.serializers.get(self.action, self.serializers["default"])
