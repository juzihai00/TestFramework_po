from Base.baseAutoWeb import BaseWeb
from Base.baseContainer import GlobalManager
from Base.baselogger import Logger
from Base.utils import read_config_ini
from Base.basePath import BasePath as BP

logger = Logger("web_login_page.py").getLogger()
config = read_config_ini(BP.CONFIG_FILE)


class LoginPage(BaseWeb):

    def __init__(self):
        super().__init__('01登录页面元素信息')

    def login(self,username,password):
        """
        稿件系统登录
        :return:
        """
        logger.info('稿件系统登录开始')
        self.get_url(config['项目运行设置']['TEST_URL'])
        # 输入用户名
        self.clear('login/username')
        self.send_keys('login/username', text=username)
        # 输入密码
        self.clear('login/password')
        self.send_keys('login/password', text=password)
        # 点击登录
        self.click('login/loginbtn')
        logger.info('稿件系统登陆结束')


    def assert_login_ok(self,flag):
        """
        登录成功断言
        :param flag:
        :return:
        """
        if flag == 1:
            assert  self.get_title() == '测试比对样品 - 稿件管理','断言失败'
            logger.info('登陆成功')
            assert self.get_text('login/welcome') == 'Welcome test01!','断言失败'
            logger.info('登陆成功')
        elif flag == 2:
            assert self.get_title() == '测试比对样品 - 登录', '断言失败'
            logger.info('验证登陆失败成功')
        elif flag == 3:
            assert self.get_title() == '测试比对样品 - 登录', '断言失败'
            logger.info('验证登陆失败成功')


if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Edge()
    gm = GlobalManager()
    gm.set_value("driver",driver)
    res = LoginPage()
    res.login('test01','1111')
    LoginPage().assert_login_ok(1)
