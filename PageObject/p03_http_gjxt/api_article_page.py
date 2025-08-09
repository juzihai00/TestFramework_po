import re

import select

from Base.baseAutoHttp import BaseApi
from Base.baselogger import Logger

logger = Logger("api_article_page.py").getLogger()

class ApiArticle(BaseApi):

    def __init__(self):
        super(ApiArticle,self).__init__("02稿件管理接口信息")

    def add_article(self,title,content):
        """
        稿件新增
        :return:
        """
        change_data = {
            "title":title,
            "content":content
        }
        res = self.request_base('add_api',change_data=change_data)
        return res.text

    def select_article(self,title=''):
        """
        查询稿件
        :return:
        """
        change_data = {
            "title":title,
        }
        res = self.request_base('select_api',change_data=change_data)
        res_info = re.findall('_15_version=1.0">(.*?)</a>',res.text)[:7]
        return res_info

    def assert_select_article(self,res,title):
        """
        断言查询稿件-res:查询数据
        :return:
        """
        assert res[1] == title  ,"断言稿件查询失败"
        logger.info("断言稿件查询成功")

    def assert_add_article(self,title):
        """
        页面断言增加稿件是否成功
        :return:
        """
        res_info = self.select_article(title=title)
        assert res_info[1] == title,"断言增加稿件失败"
        logger.info("断言稿件新增成功")
        assert res_info[3] == "不批准","断言增加稿件失败"
        logger.info("断言稿件新增成功")

    def delete_article(self,title):
        """
        稿件删除
        :return:
        """
        id = self.select_article(title=title)[0]
        change_data = {
            "_15_deleteArticleIds": "{}_version_1.0".format(id),
            "_15_rowIds":"{}_version_1.0".format(id)
        }
        res = self.request_base('delete_api',change_data=change_data)
        return res.text

    def assert_delete_article(self,title):
        """
        断言稿件删除成功
        :return:
        """
        first_info = self.select_article(title=title)
        assert first_info == [],"断言稿件删除失败"
        logger.info("断言稿件删除成功")

    def edit_article(self,title,edit_title,content):
        """
        稿件编辑
        :return:
        """
        id = self.select_article(title=title)[0]
        change_data = {
            "title":edit_title,
            "content":content,
            "articleId":id,
            "deleteArticleIds":"{}_version_1.0".format(id),
            "expireArticleIds":"{}_version_1.0".format(id)
        }
        res = self.request_base('edit_api',change_data=change_data)
        return res.text

    def assert_edit_article(self,title):
        """
        断言稿件编辑成功
        :return:
        """
        res_info = self.select_article(title=title)
        print(res_info)
        assert res_info[1] == title,"断言编辑稿件失败"
        logger.info("断言编辑稿件成功")
        assert res_info[3] == "不批准","断言编辑稿件失败"
        logger.info("断言编辑稿件成功")

if __name__ == '__main__':
    from PageObject.p03_http_gjxt.api_login_page import LoginPage
    lp = LoginPage()
    lp.login(username='test01',password='1111')
    aa = ApiArticle()
    # result = aa.add_article("测试稿件","测试内容")
    res = aa.select_article(title="333")
    aa.assert_select_article(res,"333")
    # aa.edit_article("测试稿件","测试稿件111","测试内哦那个")
    # aa.assert_edit_article("测试稿件111")