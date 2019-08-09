#内置模块
import datetime
import os
import time
import xlwt

#第三方模块
from django.shortcuts import render, reverse
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect, QueryDict
from django.views.generic import View
from resources import models
from django.conf import settings

#自定义模块
from resources import forms


class RessourcessIndexView(View):

    def get(self, request):
        """获取业务线"""

        object_list = models.Bussiness.objects.all().order_by("-id")

        return render(request, "resources/resources.html", locals())

    def delete(self, request):
        """删除业务线"""
        ret = {"status": 0}

        data = QueryDict(request.body)
        bid = data.get("bid", None)
        try:
            obj = models.Bussiness.objects.get(pk=bid).delete()
        except Exception as e:
            ret["status"] = 1
            ret["errmsg"] = "该业务线不存在"

        return JsonResponse(ret)

class RessourcessaddView(View):

    def get(self, request):
        obj = forms.CreateBussiness()
        return render(request,"resources/resources_add.html",locals())

    def post(self, request):
        obj = forms.CreateBussiness(request.POST)
        if obj.is_valid():
            success = models.Bussiness.objects.create(**obj.cleaned_data)
            if success:
                return HttpResponseRedirect(reverse("resources:resource_list"))
        else:
            return render(request, "resources/resources_add.html", locals())



class RessourcessModifyView(View):
    """更新业务线"""

    def get(self, request, *args, **kwargs):
        """获取历史相应的数据"""
        nid = request.GET.get('id', None)

        update = models.Bussiness.objects.filter(id=nid).first()
        obj = forms.CreateBussiness(initial={
            "virIP":update.virIP,
            "application":update.application,
            "port":update.port,
            "component":update.component,
            "principal":update.principal,
            "business_chooics":update.business_chooics,
            "note":update.note
        })

        return render(request, "resources/resources_update.html", {'obj':obj})

    def post(self, request):
        """更新相应的历史数据"""
        bid = request.GET.get("id")
        obj = forms.CreateBussiness(request.POST)

        if obj.is_valid():
            virIP = obj.cleaned_data.get("virIP")
            application = obj.cleaned_data.get("application")
            port = obj.cleaned_data.get("port")
            component = obj.cleaned_data.get("component")
            principal = obj.cleaned_data.get("principal")
            note = obj.cleaned_data.get("note")
            business_chooics = obj.cleaned_data.get("business_chooics")

            try:
                update = models.Bussiness.objects.filter(pk=bid).update(
                    virIP = virIP,
                    application = application,
                    port = port,
                    component = component,
                    principal = principal,
                    note = note,
                    business_chooics = business_chooics,
                    uptime = datetime.datetime.now()
                )
                if update:
                    return HttpResponseRedirect(reverse("resources:resource_list"))
            except Exception as e:
                return HttpResponseRedirect(reverse("resources:resource_modify"))
        else:
            return render(request,"resources/resources_update.html", locals())




class RessourcessUploadView(View):
    """业务线导出"""
    def get(self, request):

        db = models.Bussiness.objects.all()
        response = HttpResponse(content_type='application/vnd.ms-excel')

        bt = ['业务ip', '业务名称', '业务端口', '业务用途', '业务线', '上线时间', '更新时间', '负责人', '备注']

        wb = xlwt.Workbook(encoding='utf-8')
        sh = wb.add_sheet("详情")
        dateFormat = xlwt.XFStyle()
        dateFormat.num_format_str = 'yyyy/mm/dd'

        for i in range(len(bt)):
            sh.write(0, i, bt[i])

        for i in range(len(db)):
            sh.write(i + 1, 0, db[i].virIP)
            sh.write(i + 1, 1, db[i].application)
            sh.write(i + 1, 2, db[i].port)
            sh.write(i + 1, 3, db[i].component)
            sh.write(i + 1, 4, db[i].business_chooics)
            sh.write(i + 1, 5, db[i].ctime.strftime('%Y-%m-%d %H:%M:%S'))
            sh.write(i + 1, 6, db[i].uptime.strftime('%Y-%m-%d %H:%M:%S'))
            sh.write(i + 1, 7, db[i].note)
            sh.write(i + 1, 8, db[i].principal)
        response['Content-Disposition'] = 'attachment; filename=reources' + time.strftime('%Y%m%d', time.localtime(
            time.time())) + '.xls'
        wb.save(response)

        return response


# def RessourcessUploadView(request):
#
#     buss = request.FILES.get('bussiness', None)
#     if buss:
#
#         path = os.path.join(settings.BASE_DIR,'resources','media', 'upload', str(time.time()))
#         flandler = open(path, "wb")
#         for chunk in buss.chunks():
#             flandler.write(buss.read())
#         flandler.close()
#     return HttpResponse(buss.read())






