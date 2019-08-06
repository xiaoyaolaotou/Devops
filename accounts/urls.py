#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/8/5 0005 上午 10:14
__Author__ = '村长'
from django.urls import path, re_path
from accounts import views

app_name = 'accounts'

urlpatterns = [

    re_path(r'^login/$', views.LoginView.as_view(), name="login"),
    re_path(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    re_path(r'^userlist/$', views.UserInfoView.as_view(), name="userlist"),

]
