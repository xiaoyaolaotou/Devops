import datetime

from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import HttpResponse, JsonResponse,QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionDenied, PermissionRequiredMixin
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

#自定义模块
from assets import models


class IndexVew(LoginRequiredMixin, View):
    """访问首页"""
    login_url = "/login/"
    def get(self, request, *args, **kwargs):
        object_list = models.Assets.objects.all().order_by("-id")
        count = models.Assets.objects.count() #主机总数
        count_user = User.objects.all().count() # 用户数
        vmware = models.Assets.objects.filter(server_type__icontains="VMware Virtual Platform").count() #VM虚拟机总数
        kvm = models.Assets.objects.filter(server_type__icontains="kvm").count() #KVM虚拟机总数

        """处理分页"""
        try:
            page_num = request.GET.get('page', 1)  # 获取URL上第几页
        except:
            page_num = 1  # 如果出错默认page等一1

        paginator = Paginator(object_list, 10)  # 每页显示多少条
        page_obj = paginator.page(page_num)
        object_list = page_obj.object_list  # 当前页面的所有对象列表

        search = request.GET.get("search_username", None) #处理搜索功能
        if search:
            object_list = object_list.filter(hostname=search)
        return render(request, "assets/assets.html", {"object_list":object_list, 'page_obj':page_obj, "total": count, "count_user": count_user, "vm": vmware, "kvm":kvm})


    def delete(self, request):
        """删除资产信息"""
        ret = {"status": 0}

        data = QueryDict(request.body)

        host_id = data.get('id', None)
        try:
            host_obj = models.Assets.objects.get(pk=host_id).delete()

        except host_obj.DoesNotExist:
            ret["status"] = 1
            ret["errmsg"] = "资产不存在"
            return JsonResponse(ret)

        return JsonResponse(ret)


class CollectHostInfo(View):
    """资产收集"""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CollectHostInfo, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        data = request.POST.dict()

        try:
            obj = models.Assets.objects.get(uuid=data["uuid"])
            if obj:
                models.Assets.objects.filter(uuid=data["uuid"]).update(**data, update_time=datetime.datetime.now())

        except models.Assets.DoesNotExist:
            models.Assets.objects.create(**data)

        return HttpResponse("")


class  Test(View):
    def get(self, request):

        return render(request, "index.html")



