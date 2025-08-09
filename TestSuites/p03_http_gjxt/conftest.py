import pytest

from PageObject.p03_http_gjxt.api_article_page import ApiArticle
from PageObject.p03_http_gjxt.api_file_page import ApiFile
from PageObject.p03_http_gjxt.api_login_page import LoginPage

@pytest.fixture(scope="function")
def init_login():
    lp = LoginPage()
    lp.login(username='test01', password='1111')

@pytest.fixture(scope="function")
def article_add_delete_edit(request):
    # 这里直接拿到测试用例里面的值
    case_data = request.param
    aa = ApiArticle()
    aa.add_article(case_data['title'],"内容1")
    yield case_data
    aa.delete_article(case_data['edit_title'])


@pytest.fixture(scope="function")
def article_add_delete(request):
    case_data = request.param
    aa = ApiArticle()
    aa.add_article(case_data['title'], case_data['content'])
    aa.assert_add_article(case_data['title'])
    yield case_data
    aa.delete_article(case_data['title'])
    aa.assert_delete_article(case_data['title'])


@pytest.fixture(scope="function")
def add_delete_folder():
    """
    文件夹新增和删除前置
    :return:
    """
    af = ApiFile()
    af.add_folder("文件夹1", "内容1")
    yield
    af.delete_folder("文件夹1")


@pytest.fixture(scope="function")
def upload_file():
    """
    文件上传前置
    :return:
    """
    af = ApiFile()
    af.upload_file('upload_file.txt','test1','content1')