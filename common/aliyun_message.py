# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import json
import os
import sys

from typing import List

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        """
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = f'xxxxxx.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def main(
            phone_number, code
    ):
        client = Sample.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='xxxxxx',
            template_code='xxxxx',
            phone_numbers=phone_number,
            template_param=json.dumps({"code": code})
        )
        runtime = util_models.RuntimeOptions()

        # 复制代码运行请自行打印 API 的返回值
        client.send_sms_with_options(send_sms_request, runtime)


@staticmethod
async def main_async(
        args: List[str],
) -> None:
    client = Sample.create_client()
    send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
        sign_name='我的AI学院在线教育网站',
        template_code='SMS_462045617',
        phone_numbers='13250345097',
        template_param='{"code":"1234"}'
    )
    runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        await client.send_sms_with_options_async(send_sms_request, runtime)
    except Exception as error:
        # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
        # 错误 message
        print(error.message)
        # 诊断地址
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)

# if __name__ == '__main__':
#     Sample.main("13250345097","22236")
