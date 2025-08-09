from time import sleep
import os
import pyautogui
from selenium.webdriver.common.by import By
from Base.baseAutoWeb import BaseWeb

from Base.baselogger import Logger

logger = Logger('web_file_page.py').getLogger()


class FilePage(BaseWeb):

    def __init__(self):
        super().__init__('03文件上传下载元素信息')

    def add_folder(self, name, description):
        """
        新增文件夹
        :return:
        """
        logger.info('新增文件夹开始')
        self.click("file/file_page")
        self.click("file/add_btn")
        self.clear("file/folder_name")
        self.send_keys("file/folder_name", text=name)
        self.clear("file/folder_desc")
        self.send_keys("file/folder_desc", text=description)
        self.click("file/save_folder")
        logger.info('新增文件夹结束')

    # def selfct_folder(self, name):
    #     """
    #     查询文件夹
    #     :param name:
    #     :return:
    #     """
    #     logger.info('查询文件夹开始')
    #     self.click("file/file_page")
    #     self.clear("file/select_file")
    #     self.send_keys("file/select_file", text=name)
    #     self.click("file/select_btn")
    #     sleep(3)
    #     logger.info('查询文件夹结束')

    def assert_folder_add(self, name):
        """
        断言增加文件夹成功
        :return:
        """
        assert self.get_text("file/first_name") == name, "断言新增文件夹失败"
        logger.info('断言新增文件夹成功')

    def delete_folder(self):
        """
        删除文件夹
        :return:
        """
        logger.info('删除文件夹开始')
        self.click("file/file_page")
        self.click("file/first_del")
        self.is_alert().accept()
        logger.info('删除文件夹结束')

    def assert_folder_delete(self):
        """
        断言文件夹删除成功
        :return:
        """
        assert self.get_text("file/msg_success") == "您的请求执行成功。", "断言删除文件夹失败"
        logger.info('断言删除文件夹成功')

    def upload_file(self, file_path, rename, description):
        """
        上传文件
        :return:
        """
        logger.info('上传文件开始')
        self.click("file/file_page")
        self.click("file/first_name")
        self.click("file/upload_btn")
        self.switch_iframe("file/iframe_file")
        self.send_keys("file/input_file", text=file_path)
        self.send_keys("file/rename_file", text=rename)
        self.send_keys("file/desc_file", text=description)
        self.click("file/sub_file")
        self.switch_iframe_out()
        logger.info('上传文件结束')

    def assert_upload_file(self, rename, description):
        """
        断言文件上传成功
        :return:
        """
        file_info = self.get_text("file/first_file")
        assert file_info.split('\n')[0] == rename, "断言文件上传失败"
        assert file_info.split('\n')[1] == description, "断言文件上传失败"
        logger.info('文件断言上传成功')

    def download_file(self):
        """
        文件下载
        :return:
        """
        logger.info('文件下载开始')
        self.click("file/first_file")
        sleep(1)
        pyautogui.hotkey("alt", "s")
        sleep(1)
        logger.info('文件下载结束')

    def assert_download_file(self, rename):
        """
        断言文件下载成功
        :return:
        """
        download_path = r'C:\Users\ckz\Downloads'
        path = os.path.join(download_path, rename)
        is_ext = os.path.exists(path)
        assert is_ext, "断言文件下载失败"
        logger.info('断言文件下载成功')


if __name__ == '__main__':
    from selenium import webdriver
    from Base.baseContainer import GlobalManager
    from PageObject.p02_web_gjxt.web_login_page import LoginPage
    from Base.basePath import BasePath as BP

    driver = webdriver.Edge()
    gm = GlobalManager()
    gm.set_value("driver", driver)
    lp = LoginPage()
    lp.login("test01", '1111')
    fp = FilePage()
    fp.add_folder("文件夹1", "测试文件夹")
    # fp.add_folder("文件夹2","测试文件夹")
    # fp.assert_file_add("文件夹1")
    # fp.assert_file_add("文件夹2")
    file_path = os.path.join(BP.DATA_TEMP_DIR, 'upload_file.txt')
    print(file_path)
    fp.upload_file(file_path=file_path, rename='测试文件夹',
                   description="文件描述")
    fp.assert_upload_file(rename="测试文件夹.txt", description="文件描述")
    fp.download_file()
    fp.assert_download_file("测试文件夹.txt")
