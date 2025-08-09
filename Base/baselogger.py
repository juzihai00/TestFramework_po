import logging
import time
import os
from Base.basePath import BasePath as BP
from Base.utils import read_config_ini

# 拿到日志打印配置文件的信息
config = read_config_ini(BP.CONFIG_FILE)['日志打印配置']
# 获取当前时间作为日志文件的名称
rq = time.strftime('%Y%m%d_%H%M%S', time.localtime()) + '.log'


class Logger(object):
    """
    该类用于配置logger，以及获取logger对象
    """

    def __init__(self, name):
        self.name = name
        # 创建日志对象
        self.logger = logging.getLogger(self.name)
        # 配置全局的日志级别
        self.logger.setLevel(config['level'])
        # 创建控制台日志对象
        self.streamHandler = logging.StreamHandler()
        # 创建文件日志对象,并传入日志文件的名称,写入方式（a为追加），文件编码格式
        self.fileHandler = logging.FileHandler(os.path.join(BP.LOG_DIR, rq), mode='a', encoding='utf-8')
        # 设置日志打印格式
        self.formatter = logging.Formatter(config['formatter'])
        # 为控制台和日志文件设置日志打印格式
        self.streamHandler.setFormatter(self.formatter)
        self.fileHandler.setFormatter(self.formatter)
        # 配置控制台和文件的日志级别
        self.streamHandler.setLevel(config['stream_handler_level'])
        self.fileHandler.setLevel(config['file_handler_level'])
        # 将控制台和文件对象添加到logger对象中
        self.logger.addHandler(self.streamHandler)
        self.logger.addHandler(self.fileHandler)

    def getLogger(self):
        return self.logger


if __name__ == '__main__':
    logger = Logger('baselogger.py').getLogger()
    # print(logger)
    # print(config['level'])
    # print(os.path.join(BP.LOG_DIR, rq))

    logger.info("这里是info级别的信息")
