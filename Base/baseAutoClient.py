import os
import pyperclip
import pyautogui
from time import sleep
from Base.baseData import BaseData
from Base.basePath import BasePath as BP
from Base.baselogger import Logger

logger = Logger('baseAutoClient').getLogger()


class GuiBase(BaseData):

    def __init__(self):
        super().__init__()
        self.duration = float(self.config['客户端自动化配置']['duration'])
        self.interval = float(self.config['客户端自动化配置']['interval'])
        self.minSearchTime = float(self.config['客户端自动化配置']['minSearchTime'])
        self.confidence = float(self.config['客户端自动化配置']['confidence'])
        self.grayscale = bool(self.config['客户端自动化配置']['grayscale'])

    def _is_file_exist(self, el):
        """
        判断文件是否存在并返回完整路径
        :return:完整路径
        """
        abs_path = self.api_path.get(el)
        if not abs_path:
            raise FileNotFoundError("el:{}不存在，请检查文件名或者配置文件".format(el))
        return abs_path

    def is_exist(self, el, search_time=None):
        """
        检查图片是否出现在屏幕上
        :return:并返回一个点
        """
        pic_path = self._is_file_exist(el)
        if not search_time:
            search_time = self.minSearchTime
        coordinate = pyautogui.locateOnScreen(pic_path, minSearchTime=search_time, confidence=self.confidence,
                                              grayscale=self.grayscale)
        if coordinate:
            logger.debug("查找对象{}存在".format(el.split('.')[0]))
            return pyautogui.center(coordinate)
        logger.debug("查找对象{}不存在".format(el.split('.')[0]))
        return None

    def _error_record(self, name, type_pic):
        """
        错误截图
        :return:
        """
        pyautogui.screenshot(os.path.join(BP.SCREENSHOTS_DIR, 'name'))
        logger.error("类型：{}，查找图片 {} 位置，当前屏幕无此内容，已截图".format(type_pic, name))
        raise pyautogui.ImageNotFoundException

    def click_picture(self, el, search_time=None, clicks_num=1, button='left', isclick=True):
        """
        图片点击
        :param el:
        :return:
        """
        pos_x_y = self.is_exist(el, search_time)
        if not pos_x_y:
            self._error_record(el, 'click_picture')
        pyautogui.moveTo(pos_x_y, duration=self.duration)
        if isclick:
            pyautogui.click(pos_x_y, clicks=clicks_num, interval=self.interval, button=button, duration=self.duration)
        logger.debug('移动到图片{}位置{}，点击：{}成功'.format(el, isclick, pos_x_y))

    def rel_click_picture(self, el, rel_x=0, rel_y=0, search_time=None, clicks_num=1, button='left', isclick=True):
        """
        相对位置点击,根据检测到的文字偏移到右侧文本框
        :return:
        """
        pos_x_y = self.is_exist(el, search_time)
        if not pos_x_y:
            self._error_record(el, 'rel_click_picture')
        pyautogui.moveTo(pos_x_y, duration=self.duration)
        pyautogui.moveRel(rel_x, rel_y, duration=self.duration)
        if isclick:
            # 这里是已经移动到文本框，可以直接点击
            pyautogui.click(clicks=clicks_num, interval=self.interval, button=button, duration=self.duration)
        logger.debug("查找图片{}，位置{}，便宜{}，点击{}，成功".format(el, pos_x_y, (rel_x, rel_y), isclick))

    def click(self, pos_x=None, pos_y=None, clicks_num=1, button='left'):
        """
        鼠标的绝对位置点击
        :return:
        """
        pyautogui.click(pos_x, pos_y, clicks=clicks_num, interval=self.interval, button=button, duration=self.duration)
        logger.debug("鼠标在坐标{}，{} 点击{}键{}次".format(pos_x, pos_y, button, clicks_num))

    def rel_click(self, rel_x=0, rel_y=0, clicks_num=1, button='left'):
        """
        鼠标的相对位置点击
        :return:
        """
        pyautogui.move(rel_x, rel_y, duration=self.duration)
        pyautogui.click(clicks=clicks_num, button=button, interval=self.interval)
        logger.debug("鼠标在相对坐标{}，{} 点击{}键{}次".format(rel_x, rel_y, button, clicks_num))

    def move_to(self, pos_x, pos_y, rel=False):
        """
        鼠标移动，包括相对和绝对移动
        :return:
        """
        if rel:
            pyautogui.moveRel(pos_x, pos_y, duration=self.duration)
            logger.debug("鼠标偏移{}，{}".format(pos_x, pos_y))
        else:
            pyautogui.moveTo(pos_x, pos_y, duration=self.duration)
            logger.debug("鼠标移动到{}，{}".format(pos_x, pos_y))

    def drag_to(self, pos_x, pos_y, button='left', rel=False):
        """
        鼠标的绝对和相对位置拖拽
        :return:
        """
        if rel:
            pyautogui.dragRel(pos_x, pos_y, duration=self.duration, button=button)
            logger.debug("鼠标相对拖拽{}，{}".format(pos_x, pos_y))
        else:
            pyautogui.dragTo(pos_x, pos_y, duration=self.duration, button=button)
            logger.debug("鼠标拖拽{}，{}".format(pos_x, pos_y))

    def scroll_to(self, amount_to_scroll, moveToX=None, moveToY=None):
        """
        鼠标的滑轮滚动
        :return:
        """
        pyautogui.scroll(clicks=amount_to_scroll, x=moveToX, y=moveToY)
        logger.debug("鼠标在{}位置移动{}值".format((moveToX, moveToY), amount_to_scroll))

    def type(self, text):
        """
        键盘输入长文本，英文
        :return:
        """
        pyautogui.typewrite(message=text, interval=self.interval)
        logger.debug("文本框输入{}".format(text))

    def input_string(self, text, clear=False):
        """
        输入中文
        :return:
        """
        pyperclip.copy(text)
        if not clear:
            pyautogui.hotkey('ctrl', 'v')
        logger.debug("文本框输入中文{}".format(text))

    def press(self, key):
        """
        实现键盘单个按键
        :return:
        """
        pyautogui.press(key)
        logger.debug("按下键盘按键{}".format(key))

    def hotkey(self, *keys):
        """
        实现键盘的组合键
        :return:
        """
        pyautogui.hotkey(*keys)
        logger.debug("执行快捷键{}".format(keys))


if __name__ == '__main__':
    gui = GuiBase()
    # gui.rel_click_picture('qq1',rel_y=-400,search_time=10,clicks_num=3)
    # gui.click(20, 20)
    # gui.rel_click(40, 40)
    # gui.move_to(1000,1000,rel=True)
    sleep(3)
    # gui.scroll_to(1000)
    # gui.type("<UNK>asdafafasdw")
    # gui.input_string("你好")
    # gui.press('enter')
    gui.hotkey('win', 'm')
