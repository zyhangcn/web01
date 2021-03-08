from django.urls import path, include
from django.urls import re_path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)

router.register("", views.CustomerList)
urlpatterns = [path("userlist/", include(router.urls))]
# urlpatterns = [
#     re_path("userlist/(?P<pk>[0-9]+)", views.CustomerList.as_view()),
#     re_path("userlist/(?P<pk>[0-9]+)", views.CustomerDetail.as_view(), name="track-detail")
# ]
