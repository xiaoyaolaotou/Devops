#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/8/6 0006 上午 9:16
__Author__ = '村长'
from django.urls import path, re_path, include
from assets import views

app_name = 'assets'

urlpatterns = [
    re_path('^$', views.IndexVew.as_view(), name="index"),
    re_path('collect', views.CollectHostInfo.as_view(), name="collect"),
    re_path('api/v1/cmdb/collect', views.CollectHostInfo.as_view(), name="collect"),

]