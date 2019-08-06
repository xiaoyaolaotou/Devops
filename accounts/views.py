from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionDenied, PermissionRequiredMixin
from django.contrib.auth.models import User

#自定义模块
from accounts import forms


class LoginView(View):
    """用户登录"""

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        res = {"status" : 0}

        login_form = forms.LoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    res['next_url'] = '/'
                else:
                    res['status'] = 1
                    res['errmsg'] = "用户被禁用"
            else:
                res["status"] = 1
                res["errmsg"] = "用户名密码错误"
        else:
            res["status"] = 1
            res["errmsg"] = "用户名或密码不能为空"

        return JsonResponse(res,safe=True)


class LogoutView(View):
    """退出登录"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("accounts:login"))


class UserInfoView(View):
    """展示用户信息"""
    def get(self, request):
        username = User.objects.all()
        return render(request, "users/users.html", locals())
