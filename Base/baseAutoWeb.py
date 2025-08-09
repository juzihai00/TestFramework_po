from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from Base.baseContainer import GlobalManager
from Base.baselogger import Logger
from Base.baseData import BaseData
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = Logger("baseAutoWeb.py").getLogger()


class BaseWeb(BaseData):
    """
    web自动化基类
    """

    def __init__(self, yaml_name):
        super().__init__(yaml_name)
        self.driver = self.gm.get_value('driver')
        self.time = 0.5
        self.time_out = 10

    def get_locate_data(self, locator, change_data=None):
        """
        获取元素数据
        locator参数写法是login/password
        :return:
        """
        res = self.get_element_data(change_data=change_data)
        # 将整个数据分割开，["login","password"]
        items = locator.split('/')
        locator_data = tuple(res[items[0]][items[1]])
        return locator_data

    def find_element(self, locator, change_data=None):
        """
        单个元素定位方法,支持数据动态替换
        :return:元素对象
        """
        try:
            locator_data = self.get_locate_data(locator, change_data)
            if not isinstance(locator_data, tuple):
                logger.error("locator参数类型错误，必须传入列表或元组类型：loc = ['id','value1']")
            logger.debug("正在定位元素信息：定位方式->{},value值->{}".format(locator_data[0], locator_data[1]))
            ele = WebDriverWait(self.driver, self.time_out, self.time).until(EC.presence_of_element_located(locator_data))
            logger.debug("元素定位成功{}".format(locator_data))
            return ele
        except Exception as e:
            logger.error("未定位到元素", locator)
            raise e

    def find_elements(self, locator, change_data=None):
        """
        多个元素定位方法,支持数据动态替换
        :return:元素对象
        """
        try:
            locator_data = self.get_locate_data(locator, change_data)
            if not isinstance(locator_data, tuple):
                logger.error("locator参数类型错误，必须传入列表或元组类型：loc = ['id','value1']")
            logger.debug("正在定位元素信息：定位方式->{},value值->{}".format(locator_data[0], locator_data[1]))
            ele = WebDriverWait(self.driver, self.time_out, self.time).until(
                EC.presence_of_all_elements_located(locator))
            logger.debug("元素定位成功{}".format(locator_data))
            return ele
        except Exception as e:
            logger.error("未定位到元素", locator)
            raise e

    def get_url(self, url):
        """
        打开浏览器，最大化窗口
        :return:
        """
        self.driver.get(url)
        self.driver.maximize_window()
        logger.debug("浏览器访问请求地址：{}".format(url))

    def click(self, locator, change_data=None):
        """
        点击元素
        :return:
        """
        try:
            ele = self.find_element(locator=locator, change_data=change_data)
            ele.click()
            logger.debug("点击按钮成功{}".format(locator))
        except Exception as e:
            logger.debug("点击按钮失败{}".format(locator))
            raise e

    def clear(self, locator, change_data=None):
        """
        清空输入框
        :return:
        """
        try:
            ele = self.find_element(locator=locator, change_data=change_data)
            ele.clear()
            logger.debug("输入框{}清空成功".format(locator))
        except Exception as e:
            logger.debug("输入框{}清空失败".format(locator))
            raise e

    def send_keys(self, locator, change_data=None, text=''):
        """
        输入文本信息
        :param locator:
        :param change_data:
        :param text:
        :return:
        """
        try:
            ele = self.find_element(locator=locator, change_data=change_data)
            ele.send_keys(text)
            logger.debug("输入文本{}成功".format(locator))
        except Exception as e:
            logger.debug("输入文本{}失败".format(locator))
            raise e

    def get_title(self):
        """
        获取浏览器当前页面的title
        :return:
        """
        try:
            title = self.driver.title
            logger.debug("获取title {} 成功".format(title))
            return title
        except Exception as e:
            logger.debug("获取title失败")
            raise e

    def get_text(self, locator, change_data=None):
        """
        获取元素的文本值
        :return:
        """
        try:
            content = self.find_element(locator=locator, change_data=change_data).text
            logger.debug("获取文本 {} 成功".format(content))
            return content
        except Exception as e:
            logger.debug("获取文本失败")
            raise e

    def get_attribute(self, locator, name, change_data=None):
        """
        获取元素的属性值
        :param locator:
        :param change_data:
        :param name:属性的名称
        :return:
        """
        try:
            element = self.find_element(locator=locator, change_data=change_data)
            attribute = element.get_attribute(name)
            logger.debug("获取属性 {} 成功".format(attribute))
            return attribute
        except Exception as e:
            logger.debug("获取属性失败")
            raise e

    def is_selected(self, locator, change_data=None):
        """
        判断元素是否被选择
        :param locator:
        :param change_data:
        :return:
        """
        ele = self.find_element(locator=locator, change_data=change_data)
        r = ele.is_selected()
        return r

    def is_title(self, _title=''):
        """
        判断页面标题是否为所需标题
        :param _title:
        :return:
        """
        try:
            result = WebDriverWait(self.driver, self.time_out, self.time).until(EC.title_is(_title))
            return result
        except Exception as e:
            return False

    def is_title_contains(self, _title=''):
        """
        判断标题是都被包含在当前页面标题内
        :param _title:
        :return:
        """
        try:
            result = WebDriverWait(self.driver, self.time_out, self.time).until(EC.title_contains(_title))
            return result
        except Exception as e:
            return False

    def is_text_in_element(self, locator, _text='', change_data=None):
        """
        判断文本值是否符合预期
        :param locator:
        :param _text:
        :param change_data:
        :return:
        """
        try:
            locator = self.find_element(locator=locator, change_data=change_data)
            result = WebDriverWait(self.driver, self.time_out, self.time).until(
                EC.text_to_be_present_in_element(locator=locator, text_=_text))
            return result
        except Exception as e:
            return False

    def is_value_in_element(self, locator, _value='', change_data=None):
        """
        判断元素的属性值是否符合预期
        :param locator:
        :param _value:
        :param change_data:
        :return:
        """
        try:
            locator = self.find_element(locator=locator, change_data=change_data)
            result = WebDriverWait(self.driver, self.time_out, self.time).until(
                EC.text_to_be_present_in_element_value(locator=locator, text_=_value))
            return result
        except Exception as e:
            return False

    def is_alert(self, timeout=3):
        """
        判断当前页面是否有弹窗
        :param timeout:
        :return:
        """
        try:
            result = WebDriverWait(self.driver, self.time_out, self.time).until(EC.alert_is_present())
            return result
        except Exception as e:
            return False

    def mouse_move_to(self, locator, change_data=None):
        """
        鼠标悬停
        :return:
        """
        element = self.find_element(locator=locator, change_data=change_data)
        ActionChains(self.driver).move_to_element(element).perform()
        logger.info("鼠标在 {} 元素悬停".format(locator))

    def mouse_drag_to(self, locator, xoffset, yoffset, change_data=None):
        """
        鼠标拖拽到某一坐标
        :return:
        """
        element = self.find_element(locator=locator, change_data=change_data)
        ActionChains(self.driver).drag_and_drop_by_offset(element, xoffset, yoffset)
        logger.info("鼠标在 {} 元素拖拽 {}，{}".format(locator, xoffset, yoffset))

    def js_focus_element(self, locator, change_data=None):
        """
        滑轮到某一元素
        :return:
        """
        target = self.find_element(locator=locator, change_data=change_data)
        # arguments[0].scrollIntoView()将鼠标滑轮滑动到target位置上
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        logger.info("聚焦元素 {}".format(locator))

    def js_scroll_end(self, x=0):
        """
        滚动到底部
        :param x:
        :return:
        """
        js = "window.scrollTo(%s,document.body.scrollHeight);".format(x)
        self.driver.execute_script(js)
        logger.info("鼠标滑轮滚动到底部")

    def js_scroll_top(self):
        """
        滚动到顶部
        :return:
        """
        js = "window.scrollTo(0,0);"
        self.driver.execute_script(js)
        logger.info("鼠标滑轮滚动到顶部")

    def keyboard_send_keys_to(self, locator, key, text, change_data=None):
        """
        模拟键盘输入文本
        :return:
        """
        element = self.find_element(locator=locator, change_data=change_data)
        ActionChains(self.driver).send_keys_to_element(element, text).perform()
        logger.info("键盘在 {} 位置输入： {}".format(locator, text))

    def get_alert_text(self):
        """
        获取弹窗文本
        :return:
        """
        confirm = self.driver.switch_to.alert
        logger.info("获取弹窗文本： {}".format(confirm))
        return confirm.text

    def alert_accept(self):
        """
        弹窗点击确认
        :return:
        """
        confirm = self.driver.switch_to.alert
        confirm.accept()
        logger.info("弹窗点击确认")

    def alert_dismiss(self):
        """
        弹窗点击取消
        :return:
        """
        confirm = self.driver.switch_to.alert
        confirm.dismiss()
        logger.info("弹窗点击取消")

    def alert_input(self, text):
        """
        弹窗输入文本
        :param text:
        :return:
        """
        prompt = self.driver.switch_to.alert
        prompt.send_keys(text)
        logger.info("弹窗输入文本值：{}".format(text))

    def select_by_index(self, locator, index=0, change_data=None):
        """
        通过索引选择下拉框，index=0，代表默认选择第一项
        :return:
        """
        element = self.find_element(locator=locator, change_data=change_data)
        Select(element).select_by_index(index)
        logger.info("选择 {} 位置的下拉列表的下拉项索引".format(locator, index))

    def select_by_value(self, locator, value, change_data=None):
        """
        通过value属性选择下拉框
        :return:
        """
        element = self.find_element(locator=locator, change_data=change_data)
        Select(element).select_by_value(value)
        logger.info("选择 {} 位置的下拉列表的下拉项值".format(locator, value))

    def select_by_text(self, locator, text, change_data=None):
        """
        通过文本值选择下拉框
        :return:
        """
        element = self.find_element(locator=locator, change_data=change_data)
        Select(element).select_by_visible_text(text)
        logger.info("选择 {} 位置的下拉列表的下拉项文本".format(locator, text))

    def switch_iframe(self, locator, change_data=None):
        """
        切换iframe表单
        :return:
        """
        try:
            id_index_locator = self.find_element(locator=locator, change_data=change_data)
            self.driver.switch_to.frame(id_index_locator)
            # if isinstance(id_index_locator, int):
            #     self.driver.switch_to.frame(id_index_locator)
            # elif isinstance(id_index_locator, str):
            #     self.driver.switch_to.frame(id_index_locator)
            # elif isinstance(id_index_locator, tuple) or isinstance(id_index_locator, list):
            #     ele = self.find_element(locator=locator)
            #     self.driver.switch_to.frame(ele)
            # else:
            #     self.driver.switch_to.frame(id_index_locator)
            logger.info("iframe切换为 {}".format(locator))
        except Exception as e:
            logger.error("iframe切换异常 {}".format(locator, e))

    def switch_iframe_out(self):
        """
        从iframe表单内切换到最外层
        :return:
        """
        try:
            self.driver.switch_to.default_content()
            logger.info("iframe切换到最外层成功")
        except Exception as e:
            logger.error("iframe切换到最外层失败 {}".format(e))

    def switch_iframe_up(self):
        """
        切换iframe到上一层
        :return:
        """
        try:
            self.driver.switch_to.parent_frame()
            logger.info("iframe切换到上一层成功")
        except Exception as e:
            logger.error("iframe切换到上一层失败 {}".format(e))

    def get_handles(self):
        """
        获取当前所有窗口的id
        :return:
        """
        try:
            handles = self.driver.window_handles
            logger.info("获取到所有的handles {}".format(handles))
            return handles
        except Exception as e:
            logger.error("获取所有的handles失败 {}".format(e))

    def switch_handle(self, index=-1):
        """
        切换窗口到index=-1，这里代表切换到最新打开的窗口，因为最新打开的窗口id出现在列表最后面
        """
        try:
            handle_list = self.driver.window_handles
            self.driver.switch_to.window(handle_list[index])
            logger.info("切换handle成功 {}".format(index))
        except Exception as e:
            logger.error("切换handles失败 {}".format(e))


if __name__ == '__main__':
    from selenium import webdriver
    from time import sleep
    driver = webdriver.Edge()
    gm = GlobalManager()
    gm.set_value("driver", driver)
    web = BaseWeb(yaml_name='01登录页面元素信息')
    res = BaseWeb(yaml_name='03文件上传下载元素信息')
    web.get_url(url='http://127.0.0.1/')
    web.find_element('login/username').send_keys('test01')
    web.find_element('login/password').send_keys('1111')
    web.find_element('login/loginbtn').click()
    res.find_element('file/file_page').click()
    sleep(2)

