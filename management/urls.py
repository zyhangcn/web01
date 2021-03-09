"""management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, register_converter, re_path
from django.urls import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from . import view
from project import views as ProView
from . import urlrounter
from te.views import Alist

info = openapi.Info(
    title="WebTest",
    default_version="1.0.0",
    description="WebTest接口文档",
)

schema_view = get_schema_view(
    info,
    public=True,
)

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('customer.urls')),
    path('project/', include('project.urls')),
    path("login/", view.login),
    path("register/", view.register),
    path("login_out/", view.login_out),
    path("kks", view.skk),
    path("doc/", include_docs_urls(title="文档")),
    path("Atest", Alist.as_view({'get': "list", "post": "partial_update"})),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
