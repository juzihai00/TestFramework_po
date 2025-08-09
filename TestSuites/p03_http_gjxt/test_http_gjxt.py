import pytest

from Base.baseData import DataDriver
from PageObject.p03_http_gjxt.api_article_page import ApiArticle
from PageObject.p03_http_gjxt.api_file_page import ApiFile
from PageObject.p03_http_gjxt.api_login_page import LoginPage


class TestApiCase:
    """
    接口自动化-稿件管理系统-登录功能模块
    """

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('01稿件系统登录'))
    def test_http_case01(self, case_data):
        """
        接口自动化用例-用户登录测试
        :return:
        """
        lp = LoginPage()
        res = lp.login(case_data['username'], case_data['password'])
        lp.assert_login_ok(res, case_data["title"])


class TestApiCase2:
    """
    接口自动化-稿件管理系统-新增稿件功能模块
    """

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('02稿件新增'))
    def test_http_case01(self, init_login, case_data):
        """
        接口自动化用例-稿件增加测试
        :return:
        """
        aa = ApiArticle()
        aa.add_article(case_data['title'], case_data['content'])
        aa.assert_add_article(case_data['title'])

    @pytest.mark.usefixtures('init_login')
    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('03稿件删除'))
    def test_http_case02(self, case_data):
        """
        接口自动化用例-稿件删除测试
        :return:
         """
        aa = ApiArticle()
        aa.add_article(case_data['title'], case_data['content'])
        aa.assert_add_article(case_data['title'])
        aa.delete_article(case_data['title'])
        aa.assert_delete_article(case_data['title'])

    @pytest.mark.usefixtures('init_login')
    # 这里因为conftest里的前置后置函数也用到了数据驱动，所以将函数名传过来
    @pytest.mark.parametrize('article_add_delete_edit', DataDriver().get_case_data('04稿件修改'), indirect=True)
    def test_http_case03(self, article_add_delete_edit):
        """
        接口自动化用例-稿件编辑测试
        :return:
        """
        aa = ApiArticle()
        aa.edit_article(article_add_delete_edit['title'], article_add_delete_edit['edit_title'],
                        article_add_delete_edit['content'])
        aa.assert_edit_article(article_add_delete_edit['edit_title'])

    @pytest.mark.parametrize('article_add_delete', DataDriver().get_case_data('05稿件查询'), indirect=True)
    def test_http_case04(self, init_login, article_add_delete):
        """
        接口自动化用例-稿件查询测试
        :return:
        """
        aa = ApiArticle()
        res = aa.select_article(article_add_delete['title'])
        aa.assert_select_article(res, article_add_delete['title'])
        aa.assert_select_article(res, article_add_delete['title'])


class TestApiCase3:
    """
    接口自动化-稿件管理系统-文件上传下载功能模块
    """

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('06文件夹新增和删除'))
    def test_file_case1(self, init_login, case_data):
        """
        接口自动化用例-文件夹上传和删除测试
        :return:
        """
        af = ApiFile()
        af.add_folder(case_data['name'], case_data['description'])
        af.assert_add_folder(case_data['name'])
        af.delete_folder(case_data['name'])
        af.assert_delete_folder(case_data['name'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('07文件上传'))
    def test_file_case2(self, init_login, add_delete_folder, case_data):
        """
        接口自动化用例-文件上传
        :return:
        """
        af = ApiFile()
        res = af.upload_file(case_data['file_name'], case_data['rename'], case_data['description'])
        af.assert_upload_file(res, case_data['rename'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('08文件下载'))
    def test_file_case3(self, init_login, add_delete_folder,upload_file, case_data):
        """
        接口自动化用例-文件下载
        :return:
        """
        af = ApiFile()
        res = af.select_file(case_data['name'])
        af.download_file(res, case_data['new_name'])
        af.assert_download_file(case_data['new_name'])
