from Base.baseAutoWeb import BaseWeb
from Base.baseContainer import GlobalManager
from Base.baselogger import Logger
from time import sleep

from ExtTools.dbbase import MysqlHelp
from PageObject.p02_web_gjxt.web_login_page import LoginPage

logger = Logger('web_article_page.py').getLogger()

class ArticlePage(BaseWeb):

    def __init__(self):
        super().__init__('02稿件管理元素信息')

    def add_article(self,text,content):
        """
        稿件新增
        :return:
        """
        logger.info('稿件新增开始')
        self.click("article/add_article_btn")
        self.send_keys("article/title",text=text)
        self.switch_iframe("article/add_iframe")
        self.send_keys("article/add_iframe",text=content)
        self.switch_iframe_out()
        self.click("article/save")
        self.click("article/select_btn")
        logger.info('稿件新增结束')

    def assert_article_add(self,title):
        """
        断言稿件增加成功
        :return:
        """
        assert self.get_text("article/first") == title, "【断言】稿件新增失败"
        logger.info('稿件新增验证成功')
        assert self.get_text("article/state") == "不批准", "【断言】稿件新增失败"
        logger.info('稿件新增验证成功')

    def assert_add_database(self):
        """
        稿件新增数据库断言--------该函数有问题，暂未实现
        :return:
        """
        dbInfo = self.config['数据库连接配置']
        db = MysqlHelp(host=dbInfo['host'],
                       user=dbInfo['user'],
                       passwd=dbInfo['passwd'],
                       port=dbInfo['port'],
                       database=dbInfo['database'],)
        res = db.mysql_db_select("select title,content,approved from journalartile order by createDate desc limit 1")[0]


    def delete_article(self):
        """
        稿件删除
        :return:
        """
        logger.info('稿件删除开始')
        self.click("article/find_all_article")
        self.click("article/check")
        self.click("article/delete_btn")
        self.is_alert().accept()
        logger.info('稿件删除结束')

    def assert_article_delete(self,title):
        """
        删除稿件页面断言
        :return:
        """
        assert self.get_text("article/first") != title, "断言稿件删除失败"
        logger.info('断言稿件删除成功')

    def edit_article(self,text,content):
        """
        稿件修改
        :return:
        """
        logger.info('稿件修改开始')
        self.click("article/find_all_article")
        # sleep(1)
        self.click("article/first_article")
        # sleep(1)
        self.clear("article/title")
        # sleep(1)
        self.send_keys("article/title",text=text)
        self.switch_iframe("article/add_iframe")
        # sleep(1)
        # 这里可能是网站的原因，导致iframe框不能使用clear
        # self.clear("article/add_iframe")
        # sleep(1)
        self.send_keys("article/add_iframe",text=content)
        self.switch_iframe_out()
        self.click("article/save")
        logger.info('稿件修改结束')


    def assert_article_edit(self,title):
        """
        断言稿件增加成功
        :return:
        """
        assert self.get_text("article/first") == title, "【断言】稿件修改失败"
        logger.info('稿件修改验证成功')
        assert self.get_text("article/state") == "不批准", "【断言】稿件修改失败"
        logger.info('稿件修改验证成功')

    def select_article(self,title):
        """
        稿件查询方法
        :return:
        """
        logger.info('查询稿件开始')
        self.clear("article/select_input")
        self.send_keys("article/select_input",text=title)
        self.click("article/select_btn")
        logger.info('稿件查询结束')

    def assert_article_select(self,title):
        """
        断言稿件查询成功
        :param title:
        :return:
        """
        assert self.get_text("article/first") == title, "断言稿件查询失败"
        logger.info('断言稿件查询成功')




if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Edge()
    gm = GlobalManager()
    gm.set_value("driver", driver)
    lp = LoginPage()
    lp.login("test01",'1111')
    res = ArticlePage()
    # res.add_article("测试标题1","666")
    res.select_article("111")
    res.assert_article_select("111")




