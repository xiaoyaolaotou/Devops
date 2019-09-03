#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/9/3 0003 下午 3:03
__Author__ = '村长'

from django.urls import path, re_path
from cloud.tencent import views

app_name = 'cloud'

urlpatterns = [
        re_path('^tencent_list/$', views.TencentCmdbListView.as_view(), name="tencent_list"),
    ]





