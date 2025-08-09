import re

from Base.baseAutoHttp import BaseApi
from Base.baselogger import Logger

logger = Logger("api_login_page.py").getLogger()

class LoginPage(BaseApi):

    def __init__(self):
        super().__init__("01登录页面接口信息")

    def login(self,username,password):
        """
        登录功能
        :return:
        """
        self.request_base("home_api")
        change_data = {
            "_58_login": username,
            "_58_password" : password
        }
        res = self.request_base("login_api",change_data=change_data)
        return res.text

    def assert_login_ok(self,res,title):
        """
        断言登录成功
        :return:
        """
        page_title = re.findall("<title>(.*?)</title>",res)[0]
        assert page_title == title,"断言登陆验证失败"
        logger.info('断言登陆成功')

if __name__ == '__main__':
    login = LoginPage()
    res = login.login("test01","1111")
    print(res)
    login.assert_login_ok(res,"测试比对样品 - 稿件管理")
