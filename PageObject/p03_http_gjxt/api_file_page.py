import os
import re
from Base.basePath import BasePath as BP
from Base.baseAutoHttp import BaseApi
from Base.baselogger import Logger

logger = Logger("api_file_page.py").getLogger()


class ApiFile(BaseApi):

    def __init__(self):
        super(ApiFile, self).__init__("03文件上传下载接口信息")

    def add_folder(self, name, description):
        """
        文件夹新增
        :return:
        """
        change_data = {
            "name": name,
            "description": description
        }
        res = self.request_base('add_folder', change_data=change_data)
        return res.text

    def select_folder(self):
        """
        查询文件夹
        :return:
        """
        res = self.request_base('select_folder')
        re_info = re.findall('%2Fdocument_library%2Fview&_20_folderId=(.*?)">(.*?)</a>', res.text)
        return re_info

    def assert_add_folder(self, name):
        """
        断言文件夹新增
        :return:
        """
        re_info = self.select_folder()
        print(re_info)
        assert name in str(re_info), "断言新增文件夹失败"
        logger.info("断言新增文件夹成功")

    def delete_folder(self, name):
        """
        文件夹删除
        :return:
        """
        res = self.select_folder()
        folder_id = None
        for i in res:
            if name in i:
                folder_id = i[0]
        change_data = {
            "folderId": folder_id
        }
        result = self.request_base('delete_folder', change_data)
        return result.text

    def assert_delete_folder(self, name):
        """
        删除文件夹断言
        :return:
        """
        res = self.select_folder()
        assert name not in str(res), "断言删除文件夹失败"
        logger.info("断言删除文件夹成功")

    def upload_file(self, file_name, rename, description):
        """
        文件上传
        :return:
        """
        folder_id = self.select_folder()[0][0]
        change_data = {
            "title": rename,
            "description": description,
            "folderId": folder_id
        }
        file_path = os.path.join(BP.DATA_TEMP_DIR, file_name)
        files = {
            "_20_file": (file_name, open(file_path, 'r', encoding='utf-8'), 'text/plain'),
        }
        res = self.request_base('file_upload', change_data=change_data, files=files)
        return res.text

    def assert_upload_file(self, text, rename):
        """
        断言上传页面验证
        :return:
        """
        name = re.findall('id="_20_title" name="_20_title" style="width: 350px; " type="text" value="(.*?)"', text)[0]
        assert name == rename, "断言文件上传失败"
        logger.info("断言文件上传成功")

    def select_file(self, rename):
        """文件查询"""
        folder_id = self.select_folder()[0][0]
        change_data = {
            "keywords": rename.split('.')[0],
            "FolderId": folder_id
        }
        res = self.request_base("select_file", change_data=change_data)
        return res.text

    def download_file(self, res, rename):
        """文档下载"""
        res = re.findall('&_20_folderId=(.*?)&_20_name=(.*?)">', res)[0]
        change_data = {
            "FolderId": res[0],
            "name": res[1]
        }
        res = self.request_base("down_file", change_data=change_data)
        file_path = os.path.join(BP.DATA_TEMP_DIR, rename)
        with open(file_path, 'wb') as f:
            f.write(res.content)

    def assert_download_file(self, rename):
        """
        断言文件下载是否成功
        :return:
        """
        file_path = os.path.join(BP.DATA_TEMP_DIR, rename)
        assert os.path.exists(file_path),"断言文档下载失败"
        logger.info("断言文档下载成功")


if __name__ == '__main__':
    from PageObject.p03_http_gjxt.api_login_page import LoginPage

    lp = LoginPage()
    res = lp.login(username='test01', password='1111')
    lp.assert_login_ok(res, '测试比对样品 - 稿件管理')
    api = ApiFile()
    # result = api.add_folder("aaa", "bbb")
    # api.add_folder('aaa')
    # res = api.upload_file('upload_file.txt','新文件','测试文件')
    # api.assert_upload_file(res,'新文件')
    res = api.select_file('10086')
    api.download_file(res, 'temp.txt')
    api.assert_download_file('temp.txt')
