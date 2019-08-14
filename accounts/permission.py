#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/8/14 0014 上午 9:37
__Author__ = '村长'

from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import Permission, ContentType
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render



class PermissionListView(LoginRequiredMixin, PaginationMixin, ListView):
    """展示权限列表"""
    model = Permission
    template_name = "users/permission/permission_list.html"
    context_object_name = 'permission'
    paginate_by = 10
    login_url = "/login/"
    keyword = ''


    def get_queryset(self):
        """查询数据表名称与codename名称"""
        queryset = super(PermissionListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(content_type__model__icontains=self.keyword) | Q(codename__icontains=self.keyword))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """回显查询"""
        context = super(PermissionListView,self).get_context_data(object_list=None, **kwargs)
        context["keyword"] = self.keyword
        return context


class PermissionCreateView(LoginRequiredMixin, TemplateView):
    """展示用户创建权限页面"""
    template_name = "users/permission/add_permission.html"

    def get_context_data(self, **kwargs):
        context = super(PermissionCreateView, self).get_context_data(**kwargs)
        context["contenttypes"] = ContentType.objects.all()
        return context

    def post(self, request):
        """创建权限"""
        content_type_id = request.POST.get('content_type', '')
        codename = request.POST.get('codename', '')
        name = request.POST.get('name', '')

        try:
            content_type = ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            return HttpResponse("模型不存在")

        if not codename or codename.find(" ")>=0:
            return HttpResponse("codename不能有空格")

        try:
            Permission.objects.create(codename=codename, content_type=content_type, name=name)
        except Exception as e:
            return HttpResponse(e.args)
        return redirect("/success/")








