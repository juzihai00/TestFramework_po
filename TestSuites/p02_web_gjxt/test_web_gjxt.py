import pytest
import os
from Base.basePath import BasePath as BP
from Base.baseData import DataDriver
from PageObject.p02_web_gjxt.web_article_page import ArticlePage
from PageObject.p02_web_gjxt.web_file_page import FilePage
from PageObject.p02_web_gjxt.web_login_page import LoginPage


class TestCase1:
    """
    web自动化-稿件管理系统-登录功能模块
    """

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('01登录功能'))
    def test_login_case1(self, driver, case_data):
        """
        WEB自动化测试用例-用户登录测试
        :return:
        """
        lp = LoginPage()
        lp.login(case_data['username'], case_data['password'])
        lp.assert_login_ok(case_data['flag'])


class TestCase2:
    """
    web自动化-稿件管理系统-稿件管理功能模块
    """

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('02稿件新增'))
    def test_article_case1(self, driver, init_login, case_data):
        """
        web自动化-稿件增加
        :return:
        """
        ap = ArticlePage()
        ap.add_article(case_data['title'], case_data['content'])
        ap.assert_article_add(case_data['title'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('03稿件删除'))
    def test_article_case2(self, driver, init_login, case_data):
        """
        web自动化-稿件删除
        :return:
        """
        ap = ArticlePage()
        ap.add_article(case_data['title'], case_data['content'])
        ap.delete_article()
        ap.assert_article_delete(case_data['title'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('04稿件修改'))
    def test_article_case3(self, driver, delete_article, case_data):
        """
        web自动化-稿件修改
        :return:
        """
        ap = ArticlePage()
        ap.edit_article(case_data['title'], case_data['content'])
        ap.assert_article_edit(case_data['title'])

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('05稿件查询'))
    def test_article_case4(self, driver, init_login, case_data):
        """
        web自动化-稿件查询
        :return:
        """
        ap = ArticlePage()
        ap.select_article(case_data['title'])
        ap.assert_article_select(case_data['title'])


class TestCase3:
    """
    web自动化-稿件管理系统-稿件管理功能模块
    """
    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('06文件夹新增和删除'))
    def test_file_case1(self, driver, init_login, case_data):
        """
        web自动化-新增和删除文件夹
        :return:
        """
        fp =FilePage()
        fp.add_folder(case_data['name'], case_data['description'])
        fp.assert_folder_add(case_data['name'])
        fp.delete_folder()
        fp.assert_folder_delete()

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('07文件上传'))
    def test_file_case2(self, driver, init_login, case_data):
        """
        web自动化-新增文件
        :return:
        """
        fp = FilePage()
        fp.add_folder(name='测试文件夹', description='这是一个测试文件夹')
        file_path = os.path.join(BP.DATA_TEMP_DIR, case_data['file_path'])
        fp.upload_file(file_path, case_data['rename'],case_data['description'])
        fp.assert_upload_file(case_data['rename'], case_data['description'])
        fp.delete_folder()

    @pytest.mark.parametrize('case_data', DataDriver().get_case_data('07文件上传'))
    def test_file_case3(self, driver, init_login, case_data):
        """
        web自动化-下载文件
        :return:
        """
        fp = FilePage()
        fp.add_folder(name='测试文件夹', description='这是一个测试文件夹')
        file_path = os.path.join(BP.DATA_TEMP_DIR, case_data['file_path'])
        fp.upload_file(file_path, case_data['rename'], case_data['description'])
        fp.assert_upload_file(case_data['rename'], case_data['description'])
        fp.download_file()
        fp.assert_download_file(case_data['rename'])
        fp.delete_folder()