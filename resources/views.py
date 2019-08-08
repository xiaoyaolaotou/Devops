#内置模块
import datetime

#第三方模块
from django.shortcuts import render, reverse
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect, QueryDict
from django.views.generic import View
from resources import models

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








