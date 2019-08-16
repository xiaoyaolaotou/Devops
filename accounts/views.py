from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, QueryDict
from django.views.generic import View, ListView, TemplateView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionDenied, PermissionRequiredMixin
from django.contrib.auth.models import User, Group, Permission, ContentType
from pure_pagination.mixins import PaginationMixin
from django.utils.decorators import method_decorator



#自定义模块
from accounts import forms
from accounts.mixins import PermissionRequried


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


class UserInfoView(LoginRequiredMixin, PermissionRequried, PaginationMixin, ListView):
    """展示用户信息"""
    model = User
    login_url = "/login/"
    template_name = "users/users.html"
    context_object_name = "username"
    paginate_by = 10
    keyword = ''
    permission_required = "auth.view_user"


    def get_queryset(self):
        """用户查询"""
        queryset = super(UserInfoView, self).get_queryset()
        self.keyword = self.request.GET.get("keyword", '').strip()
        if self.keyword:
            queryset = queryset.filter(username__icontains=self.keyword)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """回显查询"""
        context = super(UserInfoView, self).get_context_data(object_list=None, **kwargs)
        context["keyword"] = self.keyword
        context["group_dd"] = Group.objects.all()
        return context

    #@method_decorator(permission_required("auth.view_user", login_url="/error/"))
    def get(self, request, *args, **kwargs):
        return super(UserInfoView, self).get(request, *args, **kwargs)




    def delete(self, request):
        """删除用户信息"""
        ret = {"status": 0}

        data = QueryDict(request.body).get("uid") #获取ajax传过来的数据

        try:
            if  request.user.has_perm('auth.delete_user'):
                User.objects.filter(pk=data).delete()
            else:
                ret["status"] = 1
                ret["errmsg"] = "你没有删除用户的权限"
        except User.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "用户不存在"
        return JsonResponse(ret)

    def put(self, request):
        """修改用户状态"""

        ret={"status": 0}

        data = QueryDict(request.body).get("uid", "")

        try:
            if request.user.has_perm("auth.change_user"):
                user_obj = User.objects.filter(pk=data).first()
                if user_obj.is_active:
                    user_obj.is_active = False
                else:
                    user_obj.is_active = True
                user_obj.save()
            else:
                ret["status"] = 1
                ret["errmsg"] = "你没有修改用户状态的权限"
        except User.DoesNotExist:
            ret['status'] = 1
            ret["errmsg"] = "用户不存在"

        return JsonResponse(ret)

    def post(self, request):
        """将用户添加至指定组"""
        ret = {"status": 0}
        uid = request.POST.get("uid", '')
        gid = request.POST.get("gid", "")

        try:
            user_obj = User.objects.get(pk=uid)
        except user_obj.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "用户不存在"
            return JsonResponse(ret)

        try:
            group_obj = Group.objects.get(pk=gid)
        except group_obj.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "用户组不存在"
            return JsonResponse(ret)

        if user_obj in group_obj.user_set.all():
            ret["status"] = 1
            ret["errmsg"] = "用户已存在该组"
            return JsonResponse(ret)
        else:
            user_obj.groups.add(group_obj)

        return JsonResponse(ret)


class UserCreateUserView(LoginRequiredMixin ,View):
    """添加用户"""

    def get(self, request):
        obj = forms.RegisterCreateUser()
        return render(request, "users/createuser.html", {"obj": obj})

    def post(self, request):
        """创建用户"""

        obj = forms.RegisterCreateUser(request.POST)
        if obj.is_valid():
            username = obj.cleaned_data.get('username')
            password = obj.cleaned_data.get('password')
            re_password = obj.cleaned_data.get('re_password')
            email = obj.cleaned_data.get('email')
            userre = User.objects.create_user(username=username, password=password, email=email)

            if userre:
                return HttpResponseRedirect(reverse("accounts:userlist"))

            else:
                return  render(request, 'users/createuser.html', {'obj': obj})

        else:
            return render(request, 'users/createuser.html', {'obj': obj})

        obj = forms.RegisterCreateUser()
        return render(request, 'users/createuser.html', {'obj': obj})


class GroupListView(LoginRequiredMixin, PaginationMixin, ListView):
    """用户组管理"""
    model = Group
    paginate_by = 10
    context_object_name = "group"
    login_url = "/login/"
    template_name = "users/group/grouplist.html"


class GroupCreateView(LoginRequiredMixin, View):
    """创建组"""

    def post(self, request):
        ret = {"status": 0}
        data = request.POST.get("name", None)
        if not data:
            ret["status"] = 1
            ret["errmsg"] = "组名不能为空"
            return JsonResponse(ret)
        else:
            try:
                g = Group()
                g.name = data
                g.save()
            except Exception as e:
                ret["status"] = 1
                ret["errmsg"] = "用户组已存在"

        return JsonResponse(ret)


class GroupDeleteView(LoginRequiredMixin, View):
    """删除组"""
    def delete(self, request):
        ret = {"status": 0}

        data = QueryDict(request.body).get("gid", None)

        try:
            g = Group.objects.get(pk=data)
            if g.user_set.all():
                ret["status"] = 1
                ret["errmsg"] = "组内存在用户,不能删除该组"
                return JsonResponse(ret)
            else:
                Group.objects.get(pk=data).delete()
        except Group.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "组不存在"

        return JsonResponse(ret)

class GroupGrouplistView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        """展示用户组内成员"""

        gid = request.GET.get("gid", None)
        g = Group.objects.get(pk=gid)
        g_obj = g.user_set.all()

        return render(request, "users/group/group_user.html", {"group_user": g_obj, "g": g})

    def delete(self, request):
        """删除组内成员"""
        ret = {"status": 0}

        uid = QueryDict(request.body).get("uid", None)
        gid = QueryDict(request.body).get("gid", None)

        try:
            user_obj = User.objects.get(pk=uid)
            group_obj = Group.objects.get(pk=gid)
            group_obj.user_set.remove(user_obj)
        except user_obj.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "用户不存在"

        except group_obj.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "用户组不存在"

        except Exception as e:
            ret["errmsg"] = e.args

        return JsonResponse(ret)


class ModifyGroupPermissionList(LoginRequiredMixin, ListView):
    """查看组权限"""
    template_name = "users/group/modify_group_permissions.html"
    model = ContentType

    def get_context_data(self, **kwargs):
        context = super(ModifyGroupPermissionList, self).get_context_data(**kwargs)
        context["contenttypes"] = ContentType.objects.all()
        context["group"] = self.request.GET.get("gid")
        context["group_permissions"] = self.get_group_permission(self.request.GET.get("gid"))
        return context

    def get_group_permission(self, groupid):
        """获取组权限"""
        try:
            group_obj = Group.objects.get(pk=groupid)
            return [p.id for p in group_obj.permissions.all()]
        except Group.DoesNotExist:
            return HttpResponse("用户组不存在")



    def post(self, request):
        permission_id_list = request.POST.getlist("permission", [])
        groupid = request.POST.get("groupid", 0)
        try:
            group_obj = Group.objects.get(pk=groupid)
        except Group.DoesNotExist:
            return HttpResponse("操作失败, 没有该组")
        if len(permission_id_list) > 0:
            permission_obj = Permission.objects.filter(id__in=permission_id_list)
            group_obj.permissions.set(permission_obj)
        else:
            group_obj.permissions.clear() #如果传过来没有值, 则表示清空权限
        # return HttpResponse("修改成功")
        return HttpResponseRedirect(reverse("accounts:grouplist"))



class UserChangePwd(LoginRequiredMixin, View):
    """修改用户密码"""
    def get(self, request,):
        form = forms.ChangeUserPwd()
        uid = request.GET.get("id")
        try:
            u = User.objects.get(pk=uid)
            return render(request, "users/changepassword.html", {"form":form, "u":u, "uid":uid})
        except Exception as e:
            return HttpResponse("有错误,返回重新设置密码")


    def post(self, request):
        uid = request.POST.get("uid", 0)
        form = forms.ChangeUserPwd(request.POST)
        ret = {'status': "false", 'error': None, 'data': None}

        if form.is_valid():
            password = form.cleaned_data.get("password")
            re_password = form.cleaned_data.get("re_password")

            try:
                username = User.objects.get(pk=uid)
                if username:
                    username.set_password(password)
                    username.save()
                    return HttpResponseRedirect(reverse("accounts:userlist"))
                else:
                    return render(request, "users/changepassword.html", locals())
            except Exception as e:
                return HttpResponseRedirect(reverse("accounts:changepasswd"))
        else:
            return render(request, "users/changepassword.html", locals())

        form = forms.ChangeUserPwd()
        return render(request, "users/changepassword.html", locals())


class PermissionViewView(LoginRequiredMixin, ListView):
    """查看用户组权限"""
    login_url = "/login/"
    model = Permission
    template_name = "users/group/group_view_user_permissions.html"
    context_object_name = "group_permission"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super(PermissionViewView, self).get_context_data(object_list=None, **kwargs)
        context["group_permissions"] = self.get_group_permission(self.request.GET.get("id"))

        return context

    def get_group_permission(self, gid):
        """获取组权限"""
        try:
            groupid = Group.objects.get(pk=gid)
            print(groupid.permissions.all())
            return [p for p in groupid.permissions.all()]
        except:
            return HttpResponse("没有")



















