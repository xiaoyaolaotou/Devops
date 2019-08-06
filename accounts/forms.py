#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/8/5 0005 上午 10:37
__Author__ = '村长'

from django import forms

class LoginForm(forms.Form):
    """后端验证帐号密码"""

    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


