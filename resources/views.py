#第三方模块
from django.shortcuts import render, reverse
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.views.generic import View
from resources import models

#自定义模块
from resources import forms


class RessourcessIndexView(View):

    def get(self, request):
        """获取业务线"""

        object_list = models.Bussiness.objects.all()

        return render(request, "resources/resources.html", locals())

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
        # obj = forms.CreateBussiness()
        # return render(request, "resources/resources_add.html", locals())




