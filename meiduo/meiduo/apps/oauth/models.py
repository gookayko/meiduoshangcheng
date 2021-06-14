from django.db import models
from utils.models import BaseModel


class QQUser(BaseModel):
    # QQ帐号在QQ的唯一标识
    openid = models.CharField(max_length=128)
    # 关联本网站的用户
    user = models.ForeignKey('users.User')


    class Meta:
        db_table = 'tb_oauth_qq'