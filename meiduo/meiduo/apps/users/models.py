from django.db import models

# Create your models here.
# 导入diango系统自定义的字段
from django.contrib.auth.models import AbstractUser
# 继承系统定义的字段
class User(AbstractUser):
    # 默认拥有用户名 密码 邮箱 字段等属性
    # 自定义扩展属性
    mobile=models.CharField(max_length=128,unique=True)

    class Meta:
        db_table = 'tb_users'
#在settings中替换更新 新加入的字段属性

