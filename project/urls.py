from django.urls import path, include
from django.urls import re_path

from . import views

from rest_framework.routers import SimpleRouter

rounter = SimpleRouter(trailing_slash=False)

rounter.register("kk", views.Project_listsa, basename="users")

urlpatterns = [
    path(r"projectlist/",
         views.ProjectList.as_view()),
    re_path(r"projectlist/(?P<pk>[0-9]+)/",
            views.ProjectDetail.as_view()),
    re_path(r"project/(?P<pk>[0-9]+)/user/(?P<customer_id>[0-9]+)/",
            views.ProjectRelationUser.as_view()),
    path("addCustomer/", views.ProjectAddUser),
    path("deleteCustomer/", views.ProjectDeleteCustomer),
    path("", include(rounter.urls))
]

