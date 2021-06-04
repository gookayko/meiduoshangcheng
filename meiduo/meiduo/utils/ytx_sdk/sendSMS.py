from .CCPRestSDK import REST


class CCP:
    @classmethod
    def sendTemplateSMS(cls, mobile, code,expires, template_id):
        # 主帐号
        accountSid = '8aaf070866235bc501662845f1100536'

        # 主帐号Token
        accountToken = '9c7188bd7d6045309fc85c647b7969ca'

        # 应用Id
        appId = '8aaf070866235bc501662845f16e053d'

        # 请求地址，格式如下，不需要写http://
        serverIP = 'app.cloopen.com'

        # 请求端口
        serverPort = '8883'

        # REST版本号
        softVersion = '2013-12-26'

        # 发送模板短信
        # @param to 手机号码
        # @param datas 内容数据 格式为列表 例如：[验证码，以分为单位的有效时间]
        # @param $tempId 模板Id

        # 初始化REST SDK
        rest = REST(serverIP, serverPort, softVersion)
        rest.setAccount(accountSid, accountToken)
        rest.setAppId(appId)

        result = rest.sendTemplateSMS(mobile, [str(code),str(expires)], template_id)
        return result.get('statusCode')
