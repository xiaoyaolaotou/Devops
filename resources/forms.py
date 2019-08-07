#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/8/7 0007 下午 2:21
__Author__ = '村长'

from resources import models
from django import forms
from django.forms import fields, widgets
from django.core.exceptions import ValidationError


class CreateBussiness(forms.Form):
    """业务验证"""

    business_chooics = fields.ChoiceField(
        choices = models.Bussiness.business_type,
        label="业务线",
        required=True,
        error_messages={
          "required": "此选项必填"
        },
        widget = widgets.Select(attrs={'class':'form-control'})
    )

    virIP = fields.GenericIPAddressField(
        required=True,
        label="业务IP",
        widget=widgets.TextInput(attrs={'class':'form-control'}),
        error_messages={
            'required' : "此项不能为空",
            'invalid': '请输入正确的IP格式'
        }
    )

    application = fields.CharField(
        required=True,
        label="业务名称",
        widget=widgets.TextInput(attrs={'class':'form-control'}),
        error_messages={
            'required': "此项不能为空",
        }
    )

    port = fields.IntegerField(
        required=False,
        label="业务端口",
        widget=widgets.TextInput(attrs={'class':'form-control'}),
        error_messages={
            'invalid': '请输入正确的端口格式'
        }
    )

    component = fields.CharField(
        required=True,
        label="业务用途",
        min_length=5,
        max_length=20,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': '此项不能为空',
            'min_length': '不能少于5个字符',
            'max_length': '不能超过20个字符'
        }
    )

    principal = fields.CharField(
        required=True,
        label="负责人",
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': '此项不能为空',
        }
    )

    note = fields.CharField(required=False,
                            label="备注",
                            max_length="10",
                            widget=widgets.TextInput(attrs={'class': 'form-control'}),
                            error_messages={
                                "max_length" : "最大不超过10个字符"
                            }
                            )

    #
    def clean_business_chooics(self):
        value = self.cleaned_data.get('business_chooics')
        if value == '0':
            raise ValidationError("请选择!")
        return value
