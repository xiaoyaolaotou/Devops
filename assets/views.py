# 内部模块
import datetime

# 第三方模块
from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import HttpResponse, JsonResponse,QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionDenied, PermissionRequiredMixin
from django.db.models import Q
from django.contrib.auth.models import User
from pure_pagination.mixins import PaginationMixin
from django.db.models import Q

#自定义模块
from assets import models


class IndexVew(LoginRequiredMixin, PaginationMixin, ListView):
    """首页"""
    model = models.Assets
    login_url = "/login/"
    paginate_by = 10
    template_name = "assets/assets.html"
    keyword = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexVew, self).get_context_data()
        context["count"] = models.Assets.objects.count()
        context["count_user"] = User.objects.all().count()
        context["vmware"] = models.Assets.objects.filter(server_type__icontains="VMware Virtual Platform").count()  # VM虚拟机总数
        context["kvm"] = models.Assets.objects.filter(server_type__icontains="kvm").count()  # KVM虚拟机总数
        context["keyword"] = self.keyword
        return context

    def get_queryset(self):
        """处理搜索"""
        queryset = super(IndexVew, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(hostname__icontains=self.keyword) | Q(private_ip__icontains=self.keyword))

        return queryset

    def delete(self, request):
        # 删除资产信息
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





