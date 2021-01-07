from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path("userlist/", views.CustomerList.as_view()),
    re_path("userlist/(?P<pk>[0-9]+)", views.CustomerDetail.as_view(), name="track-detail")
]
