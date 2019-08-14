#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/8/14 0014 下午 2:32
__Author__ = '村长'

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect

class PermissionRequried(PermissionRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():  #如果当前用户没有登录权限
            return redirect("/error/")
            # return self.handle_no_permission()
        return super(PermissionRequried, self).dispatch(request, *args, **kwargs)








