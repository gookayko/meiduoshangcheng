from rest_framework import serializers
import re
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings


# # ModelSerializer=》有模型类优先使用该类型
# # Serializer=》
# class CreateUserSerializer(serializers.Serializer):
#     # don not receive value from client
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(
#         min_length=5,
#         max_length=20,
#         error_messages={
#         'min_length':'用户名为5-20个字符',
#         'max_length':'用户名为5-20个字符'
#         }
#     )
#     password = serializers.CharField(
#         write_only=True,
#         min_length=8,
#         max_length=20,
#         error_messages={
#             'min_length':'密码为8-20个字符',
#             'max_length':'密码为8-20个字符'
#         }
#     )
#     mobile = serializers.CharField()
#     password2 = serializers.CharField(write_only=True)
#     sms_code = serializers.CharField(write_only=True)
#     # allow		是否同意用户协议
#     allow = serializers.CharField(write_only=True)
#
#     def validate_username(self, value):
#         if User.objects.filter(username=value).count()>0:
#             raise serializers.ValidationError('用户名存在')
#         return value
#
#
#
#
#     def validate_mobile(self,value):
#         if not re.matech('^1[3-9]\d{9}$',value):
#             raise serializers.ValidationError('手机号格式不正确')
#         return value
#
#
#
#     def validate_allow(self,value):
#         if not value:
#             raise serializers.ValidationError('必须同意协议')
#         return value
#
#
#
#     def validate(self,attrs):
#         # 短信验证码   where is 'verify_codes'
#         redis_cli = get_redis_connection('verify_codes')
#         key = 'sms_code_' + attrs.get('mobile')
#         # bytes
#         sms_code_redis = redis_cli.get(key)
#         if not sms_code_redis:
#             raise serializers.ValidationError('验证码已经过期')
#         redis_cli.delete(key)
#         # bytes==>string
#         sms_code_redis = sms_code_redis.decode()
#         sms_code_request = attrs.get('sms_code')
#         if sms_code_redis != sms_code_request:
#             raise serializers.ValidationError('验证码错误')
#
#         pwd1 = attrs.get('password')
#         pwd2 = attrs.get('password2')
#         if pwd1 != pwd2:
#             raise serializers.ValidationError('两次输入的密码不一致')
#
#         return attrs
#
#
#
#
#
#     def create(self,validated_data):
#         user=User()
#         user.username=validated_data.get('username')
#         user.mobile=validated_data.get('mobile')
#         user.password=validated_data.get('password')
#         user.set_password(validated_data.get('password'))
#         user.save()
#
#
#         return user
from users.models import User


class CreateUserSerializer(serializers.Serializer):
    # I定义属性
    # read_only 不接收客户端的数据 只向客户端输出
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        min_length=5,
        max_length=20,
        error_messages={
            'min_length':'用户名请输入5-20个字符',
            'max_length':'用户名请输入5-20个字符',
        }

    )


    password = serializers.CharField(
        min_length=8,
        max_length=20,
        error_messages={
            'min_length': '密码请输入5-20个字符',
            'max_length': '密码请输入5-20个字符'
        },
        write_only = True
    )


    password2 = serializers.CharField(
        min_length=8,
        max_length=20,
        error_messages={
            'min_length': '密码请输入5-20个字符',
            'max_length': '密码请输入5-20个字符',
        },
        # 只接收客户端数据 不向客户端输出数据
        write_only=True
    )
    sms_code = serializers.IntegerField(write_only=True)
    mobile = serializers.IntegerField()
    allow = serializers.BooleanField(write_only=True)
    token=serializers.CharField(read_only=True)




    # II验证
    # 1.验证用户名是否重复
    def validate_username(self,value):
        count=User.objects.filter(username=value).count()
        if count>0:
            raise serializers.ValidationError('该用户名已经注册')
        return value



    # 2.多属性判断  密码
    def validate(self,attrs):
        # 判断两个密码是否一致
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('两个密码不一致')


    # 3.短信验证码是否正确
        #1.获取请求报文中的短信验证码 手机号
        sms_code_request = attrs.get('sms_code')
        mobile = attrs.get('mobile')
        #2.获取redis中的短信验证码
        redis_cli=get_redis_connection('sms_code')
        sms_code_redis = redis_cli.get('sms_code'+mobile)
        #3.判断是否过期
        if sms_code_redis is None:
            raise serializers.ValidationError('短信验证码已经过期')
        #4.强制立即过期
        redis_cli.delete('sms_code'+mobile)
        #5.判断两个验证码是否相等
        if int(sms_code_request)!=int(sms_code_redis):
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    #4. 手机号码匹配
    def validate_mobile(self,value):
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$',value):
            raise serializers.ValidationError('手机号码格式错误')
        # 验证手机号是否重复
        count = User.objects.filter(mobile=value).count()
        if count>0:
            raise serializers.ValidationError('手机号码已经注册')
        return value

    # 5.用户协议
    def validated_allow(self,value):
        # 是否同意协议
        if not value:
            raise serializers.ValidationError('请先阅读协议并同意')
        return value


    # III保存
    def create(self,validated_data):
        user=User()
        user.username=validated_data.get('username')
        # 密码需要加密，故用该方法，不用下面的直接给密码赋值用法
        user.set_password(validated_data.get('password'))
        user.mobile=validated_data.get('mobile')
        user.save()
        # user=User.objects.create(
        #     username=validated_data.get('user_name'),
        #     password=validated_data.get('password'),
        #     mobile=validated_data.get('mobile')
        # )
        # user.password=



        # 需要生成token
        jwt_payload_handler=api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler=api_settings.JWT_ENCODE_HANDLER
        payload=jwt_payload_handler(user)
        # 通过token可以获得header.payload.signature
        token=jwt_encode_handler(payload)


        # 将token输出到客户端
        # 为user对象添加属性
        user.token=token


        return user

