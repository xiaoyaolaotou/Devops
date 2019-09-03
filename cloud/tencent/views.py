#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/9/3 0003 下午 2:50
__Author__ = '村长'
#三方模块
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from django.conf import settings

#自定义模块
from util.tencentyun_api import TencentYun_api


class TencentCmdbListView(LoginRequiredMixin, PaginationMixin, TemplateView):
    login_url = '/login/'
    paginate_by = 15
    region = ['ap-chengdu','ap-chongqing']
    template_name = 'tencent/tencent_list.html'
    keybord = ''

    def get_context_data(self, **kwargs):
        context= super(TencentCmdbListView, self).get_context_data(**kwargs)
        tencent = TencentYun_api(settings.SECRETID, settings.SECRETKEY)
        context = {}
        context_list = []

        for region in settings.REGION:
            context_list.append(tencent.get_describe_instances(region))
            context['tencent'] = context_list
        print(context_list)

        return context




