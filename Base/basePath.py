import os


class BasePath(object):
    """
    该类用于获取项目内的所有文件夹路径
    """

    # 自动获取项目的绝对路径
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 配置文件config的路径,以及配置文件.ini的路径
    CONFIG_DIR = os.path.join(PROJECT_ROOT, 'Config')
    CONFIG_FILE = os.path.join(CONFIG_DIR, '配置文件.ini')
    # 通过数据data的路径，获取datadriver，dataelement，temp的路径
    DATA_DIR = os.path.join(PROJECT_ROOT, 'Data')
    DATA_DRIVER_DIR = os.path.join(DATA_DIR, 'DataDriver')
    DATA_ELEMENT_DIR = os.path.join(DATA_DIR, 'DataElement')
    DATA_TEMP_DIR = os.path.join(DATA_DIR, 'Temp')
    # Temp下的截图文件夹路径
    SCREENSHOTS_DIR = os.path.join(DATA_TEMP_DIR, 'Screenshots')
    SCREENSHOT_PIC = os.path.join(SCREENSHOTS_DIR, 'error-screenshot.png')
    # 浏览器驱动driver的路径
    DRIVER_DIR = os.path.join(PROJECT_ROOT, 'Driver')
    # 日志文件log的路径
    LOG_DIR = os.path.join(PROJECT_ROOT, 'Log')
    # 测试报告的路径，以及allure，html，xml的路径
    REPORTS_DIR = os.path.join(PROJECT_ROOT, 'Reports')
    REPORTS_ALLURE_DIR = os.path.join(REPORTS_DIR, 'ALLURE')
    # 这里是allure报告测试报告原始数据和测试报告的路径
    ALLURE_REPORT_DIR = os.path.join(REPORTS_ALLURE_DIR, 'Report')
    ALLURE_RESULT_DIR = os.path.join(REPORTS_ALLURE_DIR, 'Result')
    REPORTS_HTML_DIR = os.path.join(REPORTS_DIR, 'HTML')
    REPORTS_XML_DIR = os.path.join(REPORTS_DIR, 'XML')
    # testsuit用来存放测试用例
    TEST_SUIT_DIR= os.path.join(PROJECT_ROOT, 'TestSuites')
    # testcases存放要运行的测试用例，tempcase存放所有的测试用例
    TESTCASES = os.path.join(DATA_TEMP_DIR, 'testcases.yaml')
    TEMPCASES = os.path.join(DATA_TEMP_DIR, 'tempcases.yaml')


if __name__ == '__main__':
    print(BasePath.CONFIG_DIR)
    print(BasePath.REPORTS_XML_DIR)
