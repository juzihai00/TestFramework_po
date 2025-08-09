import os
import sys
from platform import system

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 根目录
sys.path.append(PROJECT_ROOT)
import pytest
from Base.basePath import BasePath as BP
from Base.utils import read_config_ini, file_all_dele
from Base.baseContainer import GlobalManager
from Base.baseSendEmail import HandleEmail

config = read_config_ini(BP.CONFIG_FILE)
gm = GlobalManager()
gm.set_value('CONFIG_INFO', config)
gm.set_value("DATA_DRIVER_PATH", os.path.join(BP.DATA_DRIVER_DIR, config['项目运行设置']['DATA_DRIVER_TYPE']))


def run_main():
    """
    运行入口函数
    :return:
    """
    run_config = gm.get_value('CONFIG_INFO')['项目运行设置']
    test_case = os.path.join(BP.TEST_SUIT_DIR, run_config['TEST_PROJECT'])
    if run_config['REPORT_TYPE'] == 'ALLURE':
        pytest.main(['-v', '--alluredir={}'.format(BP.ALLURE_RESULT_DIR), test_case])
        os.system('allure generate {} -o {} --clean'.format(BP.ALLURE_RESULT_DIR, BP.ALLURE_REPORT_DIR))
        file_all_dele(BP.ALLURE_RESULT_DIR)
    elif run_config['REPORT_TYPE'] == 'HTML':
        repost_path = os.path.join(BP.REPORTS_HTML_DIR, 'auto_reports.html')
        pytest.main(['-v', '--html={}'.format(repost_path), '--self-contained-html', test_case])
    elif run_config['REPORT_TYPE'] == 'XML':
        repost_path = os.path.join(BP.REPORTS_XML_DIR, 'auto_reports.xml')
        pytest.main(['-v', '--junitxml={}'.format(repost_path), test_case])
    else:
        print("暂未支持此报告类型：{}".format(run_config['REPORT_TYPE']))
    if run_config['IS_EMAIL'] == 'yes':
        el = HandleEmail()
        text = '本邮件由系统自动发出，无需回复！\n各位同事，大家好，以下为本次测试报告!'
        el.send_public_email(text, file_type=run_config['REPORT_TYPE'])
        print("邮件发送成功：{}".format(run_config['REPORT_TYPE']))


if __name__ == '__main__':
    run_main()
