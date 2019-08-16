# 内部模块
import datetime
import time

# 第三方模块
import xlwt
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
            if request.user.has_perm("assets:delete_assets"):
                host_obj = models.Assets.objects.get(pk=host_id).delete()
            else:
                ret["status"] = 1
                ret["errmsg"] = "没有该删除权限, 滚!"

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


class ErrorView(View):
    """没有权限提示页面"""
    def get(self, request):
        return render(request, 'error.html')

class SuccessView(View):
    def get(self, request):
        return render(request, "success.html")


class CollectHostExport(LoginRequiredMixin, View):
    def get(self, request):
        """业务线导出"""

        db = models.Assets.objects.all()
        response = HttpResponse(content_type='application/vnd.ms-excel')

        bt = ['主机名', 'IP地址', 'cpu', '内存', '磁盘', '主机类型', '系统', '创建日期', '更新日期']

        wb = xlwt.Workbook(encoding='utf-8')
        sh = wb.add_sheet("详情")
        dateFormat = xlwt.XFStyle()
        dateFormat.num_format_str = 'yyyy/mm/dd'

        for i in range(len(bt)):
            sh.write(0, i, bt[i])

        for i in range(len(db)):
            sh.write(i + 1, 0, db[i].hostname)
            sh.write(i + 1, 1, db[i].private_ip)
            sh.write(i + 1, 2, db[i].cpu)
            sh.write(i + 1, 3, db[i].server_mem)
            sh.write(i + 1, 4, db[i].disk)
            sh.write(i + 1, 5, db[i].server_type)
            sh.write(i + 1, 6, db[i].os)
            sh.write(i + 1, 7, db[i].create_time.strftime('%Y-%m-%d %H:%M:%S'))
            sh.write(i + 1, 8, db[i].update_time.strftime('%Y-%m-%d %H:%M:%S'))

        response['Content-Disposition'] = 'attachment; filename=assets' + time.strftime('%Y%m%d', time.localtime(
            time.time())) + '.xls'
        wb.save(response)

        return response




