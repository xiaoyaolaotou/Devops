#! /usr/bin/env python
# encoding: utf-8
# @Time :2019/9/3 0003 下午 1:33
__Author__ = '村长'

import json
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client, models


class TencentYun_api:
    def __init__(self,secretid, secretkey):
        """
        实例化KEY认证
        :param secretid:
        :param secretkey:
        """
        try:
            self.cred = credential.Credential(secretid, secretkey)
        except TencentCloudSDKException as e:
            print(e)

    def get_describe_instances(self, region):
        """
        请求cvm实例
        :param region:
        :return:
        """

        try:

            client = cvm_client.CvmClient(self.cred, region)
            req = models.DescribeInstancesRequest()
            res = client.DescribeInstances(req)
            data_json = json.loads(res.to_json_string())
            return data_json
        except TencentCloudSDKException as e:
            return e



