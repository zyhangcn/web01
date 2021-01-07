from django.urls import path
from django.urls import re_path

from . import views

urlpatterns = [
    path(r"projectlist/",
         views.ProjectList.as_view()),
    re_path(r"projectlist/(?P<pk>[0-9]+)/",
            views.ProjectDetail.as_view()),
    re_path(r"project/(?P<pk>[0-9]+)/user/(?P<customer_id>[0-9]+)/",
            views.ProjectRelationUser.as_view()),
    path("addCustomer/", views.ProjectAddUser),
    path("deleteCustomer/", views.ProjectDeleteCustomer)
]
