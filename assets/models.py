from django.db import models


class Assets(models.Model):
    """资产表"""

    CHOICE_VM_STATUS = (
        (0, '在线'),
        (1, '下线'),
    )

    hostname            =  models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name="主机名")
    private_ip          =  models.GenericIPAddressField(verbose_name="内网IP")
    mac_address         =  models.CharField(max_length=32, unique=True, verbose_name="mac地址")
    cpu                 =  models.IntegerField(verbose_name="CPU")
    server_mem          =  models.CharField(verbose_name="内存总大小", max_length=32,default="")
    disk                =  models.CharField(max_length=100, verbose_name="磁盘")
    manufacturers       =  models.CharField(max_length=100, verbose_name="制造商")
    server_type         =  models.CharField(max_length=32, verbose_name="服务器类型")
    st                  =  models.CharField(max_length=120, verbose_name="序列号")
    uuid                =  models.CharField(max_length=100, verbose_name="uuid")
    manufacture_data    =  models.CharField(max_length=32, verbose_name="生产日期")
    os                  =  models.CharField(max_length=32, verbose_name="操作系统")
    vm_status           =  models.IntegerField(choices=CHOICE_VM_STATUS, verbose_name="状态")
    create_time         =  models.DateTimeField(auto_now_add=True, verbose_name="创建日期")
    update_time         =  models.DateTimeField(auto_now=True, verbose_name="更新日期")

    class Meta:
        db_table = "assets"
        verbose_name = "资产"
        verbose_name_plural = verbose_name