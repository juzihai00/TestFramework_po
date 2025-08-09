#!/usr/bin/python
# -*- coding:utf-8 -*-
import base64
import pytest
from io import BytesIO
from Base.utils import *
from Base.basePath import BasePath as BP
from Base.baseContainer import GlobalManager
from Base.baseYaml import write_yaml

#初始化配置
insert_js_html = False
gm = GlobalManager()
config = read_config_ini(BP.CONFIG_FILE)
gm.set_value('CONFIG_INFO',config)


def pytest_addoption(parser):
    '''添加命令行参数--browser、--host'''
    parser.addoption(
        "--browser", action="store", default=config['WEB自动化配置']['browser'], help="browser option: firefox or chrome or ie"
             )
    # 添加host参数，设置默认测试环境地址
    parser.addoption(
        "--host", action="store", default=config['项目运行设置']['test_url'], help="test host->http://10.11.1.171:8888"
    )




@pytest.fixture(scope='session')
def host(request):
    '''全局host参数'''
    return request.config.getoption("--host")


@pytest.fixture(scope='function')
def driver(request):
    """创建并返回浏览器实例"""
    name = request.config.getoption("--browser")
    print(f"正在启动浏览器: {name}")

    try:
        from selenium import webdriver

        # 创建浏览器实例
        if name == "firefox":
            driver_instance = webdriver.Firefox()
        elif name == "chrome":
            driver_instance = webdriver.Chrome()
        elif name == "ie":
            driver_instance = webdriver.Ie()
        elif name == "edge":
            driver_instance = webdriver.Edge()
        elif name == "chromeheadless":
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            driver_instance = webdriver.Chrome(options=chrome_options)
            driver_instance.set_window_size(width=1920, height=1080)
        else:
            # 默认使用 Chrome
            driver_instance = webdriver.Chrome()

        # 设置隐式等待
        driver_instance.implicitly_wait(5)

        # 设置到全局管理器
        GlobalManager().set_value('driver', driver_instance)

        # 返回驱动实例
        yield driver_instance

        # 测试结束后清理
        print("测试结束，关闭浏览器")
        driver_instance.quit()

    except ImportError as e:
        pytest.fail(f"未安装selenium: {str(e)}")
    except Exception as e:
        pytest.fail(f"启动webdriver发生错误: {str(e)}")


def _capture_screenshot_sel():
    driver = GlobalManager().get_value('driver')
    if not driver:
        pytest.exit('driver 获取为空')
    driver.get_screenshot_as_file(BP.SCREENSHOT_PIC)
    return driver.get_screenshot_as_base64()


def _capture_screenshot_pil():
    try:
        from PIL import ImageGrab
        output_buffer = BytesIO()
        img = ImageGrab.grab()
        img.save(BP.SCREENSHOT_PIC)
        img.save(output_buffer, "png")
        bytes_value = output_buffer.getvalue()
        output_buffer.close()
        return base64.b64encode(bytes_value).decode()
    except ImportError:
        pytest.exit('未安装PIL')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """当测试失败的时候，自动截图，展示到html报告中"""
    outcome = yield
    pytest_html = item.config.pluginmanager.getplugin('html')
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):  # 失败截图
            if config['项目运行设置']['AUTO_TYPE'] == 'WEB':
                screen_img = _capture_screenshot_sel()
            elif config['项目运行设置']['AUTO_TYPE'] == 'CLIENT':
                screen_img = _capture_screenshot_pil()
            else:
                screen_img = None
            file_name = report.nodeid.replace("::", "_") + ".png"
            if config['项目运行设置']['REPORT_TYPE'] == 'HTML' and screen_img:
                if file_name:
                    html = '<div><img src="Data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                           'onclick="lookimg(this.src)" align="right"/></div>' % screen_img
                    script = '''
                    <script>
                        function lookimg(str)
                        {
                            var newwin=window.open();
                            newwin.document.write("<img src="+str+" />");
                        }
                    </script>
                    '''
                    extra.append(pytest_html.extras.html(html))
                    if not insert_js_html:
                        extra.append(pytest_html.extras.html(script))
            elif config['项目运行设置']['REPORT_TYPE'] == 'ALLURE':
                import allure
                with allure.step('添加失败截图...'):
                    allure.attach.file(BP.SCREENSHOT_PIC, "失败截图", allure.attachment_type.PNG)
    report.extra = extra
    report.description = str(item.function.__doc__)


def pytest_collection_modifyitems(session, config, items):
    '''收集用例后修改'''
    if '--co' in config.invocation_params.args:
        testcases = {}
        for item in items:
            case_class_name = '::'.join(item.nodeid.split("::")[0:2])
            case_name = item.nodeid.split("::")[-1]
            if not testcases.get(case_class_name, None):
                testcases[case_class_name] = {}
            if not testcases[case_class_name].get('comment', None):
                testcases[case_class_name]['comment'] = item.cls.__doc__
            testcases[case_class_name][case_name] = item.function.__doc__
        tempcases_path = BP.TEMPCASES
        write_yaml(tempcases_path, testcases)





if __name__ == '__main__':
    # 在 conftest.py 文件底部添加
    print("conftest.py 已加载！可用的 fixture 包括:", dir())




