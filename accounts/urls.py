#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/8/5 0005 上午 10:14
__Author__ = '村长'
from django.urls import path, re_path, include
from accounts import views
from accounts import permission

app_name = 'accounts'

urlpatterns = [

    re_path(r'^login/$', views.LoginView.as_view(), name="login"),
    re_path(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    re_path(r'^userlist/$', views.UserInfoView.as_view(), name="userlist"),
    re_path(r'^createuser/$', views.UserCreateUserView.as_view(), name="createuser"),

    re_path(r'^group/', include([
        re_path(r'^$', views.GroupListView.as_view(), name="grouplist"),
        re_path(r'^create/$', views.GroupCreateView.as_view(), name="groupcreate"),
        re_path(r'^delete/$', views.GroupDeleteView.as_view(), name="groupdelete"),
        re_path(r'^grouplist/$', views.GroupGrouplistView.as_view(), name="group_userlist"),
        re_path(r'permission/', include([
            re_path(r'^modify/$' ,views.ModifyGroupPermissionList.as_view(), name="group_permission_modify")
        ])),
    ])),

    re_path(r'^permission/', include([
        re_path(r'^list/$', permission.PermissionListView.as_view(), name='permission_list'),
        re_path(r'^add/$', permission.PermissionCreateView.as_view(), name='permission_add')
    ])),

]
