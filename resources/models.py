from django.db import models

class Bussiness(models.Model):
    """业务线"""

    business_type = (
        (0, "---请选择---"),
        (1, "O2M300"),
        (2, "O2M500"),
        (3, "O2M800"),
        (4, "IM800"),
        (5, "供应链")
    )

    business_chooics = models.IntegerField(choices=business_type)
    virIP = models.GenericIPAddressField(verbose_name="业务IP",db_index=True) #一台机器有多个业务,可以重复
    application = models.CharField(max_length=200, verbose_name="业务名称", db_index=True)
    port = models.IntegerField(verbose_name='应用端口', null=True, default="")
    component = models.CharField(verbose_name='组件用途', max_length=100)
    principal = models.CharField(verbose_name='开发负责人', max_length=32)
    ctime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    uptime = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    note = models.CharField(verbose_name='备注', max_length=100, null=True)

    class Meta:
        db_table = "bussiness"


    def __str__(self):
        return self.virIP








