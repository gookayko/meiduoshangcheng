import random

from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms.tasks import send_sms_code
from utils.ytx_sdk.sendSMS import CCP
from . import constans

# 链接redis
from django_redis import get_redis_connection

class SMSCodeView(APIView):
    # 发送短信验证码
    def get(self,request,mobile):
        # 获取redis的链接
        redis_cli = get_redis_connection('sms_code')
        #1.判断60s内是否向手机发过短信
        # 如发过,抛出异常
        if redis_cli.get('sms_flag_'+mobile):
            raise serializers.ValidationError('此手机在60s秒内已发送过验证码')
        #2.如果未发送短信
        #2.1 获取随机的6位数
        code = random.randint(100000,999999)

        #2.2 保存到redis中  验证码  发送的标记
        # redis_cli.setex('sms_code_'+mobile,300,code)
        # redis_cli.setex('sms_flag_' + mobile, 60, 1)
        # 优化：pipeline
        # 减少与redis数据库交互的次数,现在只交互一次，之前交互两次
        redis_pipeline=redis_cli.pipeline()
        redis_pipeline.setex('sms_code_'+mobile,constans.SMS_CODE_EXPIRES,code)
        redis_pipeline.setex('sms_flag_' + mobile, constans.SMS_FLAG_EXPIRES, 1)
        redis_pipeline.execute()

        #2.3 发短信 云通信
        # CCP.sendTemplateSMS(mobile,code,constans.SMS_CODE_EXPIRES/constans.SMS_FLAG_EXPIRES,1)
        # print(code)
        # 调用celery任务，执行耗时代码
        send_sms_code.delay(mobile,code,constans.SMS_CODE_EXPIRES/60,1)
        #3.响应
        return Response({'message':'OK'})





