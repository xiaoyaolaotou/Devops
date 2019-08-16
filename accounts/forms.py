#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/8/5 0005 上午 10:37
__Author__ = '村长'

from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields,widgets


class LoginForm(forms.Form):
    """后端验证帐号密码"""

    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class RegisterCreateUser(forms.Form):
    """创建用户"""
    username = fields.CharField(required=True,
                                label="用户名:",
                                widget=widgets.TextInput(attrs={'class': 'form-control'}),
                                min_length=5, max_length=32, error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名不能少于3个字符',
            'max_length': '用户名不能大于32个字符',

        })

    password = fields.CharField(required=True,
                                label="密码:",
                                widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                                min_length=5, max_length=10, error_messages={
            'required': '密码不能为空',
            'min_length': '密码不能少于3个字符',
            'max_length': '密码不能大于10个字符'
        })

    re_password = fields.CharField(required=True,
                                   label="再次输入密码:",
                                   widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                                   min_length=5, max_length=10, error_messages={
            'required': '密码不能为空',
        })

    email = fields.EmailField(required=True,
                              label="邮箱:",
                              widget=widgets.EmailInput(attrs={'class': 'form-control'}),
                              error_messages={
                                  'required': '邮箱不能为空',
                                  'invalid': '请输入正确的邮箱格式'
                              })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        users = User.objects.filter(username=username).first()
        if users:
            raise ValidationError("用户已存在")

        return username


    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_obj = User.objects.filter(email=email).first()
        if email_obj:
            raise  ValidationError("用户邮箱已存在")

        return email

    def clean(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("re_password")

        if password1 and password2 and password1 != password2:
            self.add_error('re_password', '两次密码不一致')
            return None
        else:
            return self.cleaned_data


class ChangeUserPwd(forms.Form):
    """修改密码"""
    password = fields.CharField(required=True,
                                label="密码:",
                                widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                                min_length=5, max_length=10, error_messages={
            'required': '密码不能为空',
            'min_length': '密码不能少于5个字符',
            'max_length': '密码不能大于10个字符'
        })

    re_password = fields.CharField(required=True,
                                   label="再次输入密码:",
                                   widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                                   min_length=5, max_length=10, error_messages={
            'required': '密码不能为空',
        })


    def clean(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("re_password")

        if password1 and password2 and password1 != password2:
            self.add_error('re_password', '两次密码不一致')
            return None
        else:
            return self.cleaned_data
