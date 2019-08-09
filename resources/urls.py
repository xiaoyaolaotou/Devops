#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/8/6 0006 下午 5:53
__Author__ = '村长'

from django.urls import path, re_path, include
from resources import views

app_name = 'resources'

urlpatterns = [
    re_path('^bussiness/', include([
        re_path(r'^list/$', views.RessourcessIndexView.as_view(), name="resource_list"),
        re_path(r'^add/$', views.RessourcessaddView.as_view(), name="resource_add"),
        re_path(r'^modify/$', views.RessourcessModifyView.as_view(), name="resource_modify"),
        re_path(r'^upload/$', views.RessourcessUploadView.as_view(), name="resource_upload"),
        # re_path(r'^upload/$', views.RessourcessUploadView, name="resource_upload"),
    ])),

]