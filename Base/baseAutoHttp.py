from urllib.parse import urljoin

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from Base.baseData import BaseData
from Base.baselogger import Logger

logger = Logger("baseAutoHttp.py").getLogger()

class BaseApi(BaseData):
    """
    接口自动化基类
    """
    # 实例化一个会话保持器，保存cookie
    session = requests.session()

    def __init__(self,yaml_name):
        super().__init__(yaml_name)
        self.time_out = 10

    def request_base(self,api_name,change_data=None,**kwargs):
        """
        实现通用的接口请求
        :return:
        """
        try:
            logger.info('【{}:{}接口调用开始】'.format(self.yaml_name, api_name))
            yaml_data = self.get_element_data(change_data)[api_name]
            yaml_data['url'] = urljoin(self.run_config['TEST_URL'], yaml_data['url'])
            # res = requests.request(**yaml_data)
            # logger.info("现在开始打印响应报文")
            # print(res.text)
            logger.info('获取【{}】文件【{}】接口请求数据：{}'.format(self.yaml_name, api_name, yaml_data))
            logger.info('接口的请求方式：{}'.format(yaml_data['method']))
            logger.info('接口的请求地址：{}'.format(yaml_data['url']))
            if 'data' in yaml_data.keys():
                logger.info('接口的请求体：{}'.format(yaml_data['data']))
            elif 'json' in yaml_data.keys():
                logger.info('接口的请求体：{}'.format(yaml_data['json']))
            urllib3.disable_warnings(InsecureRequestWarning)
            # 这一句为request调用api
            res = BaseApi.session.request(**yaml_data, **kwargs)
            logger.info('接口的响应时间：{}'.format(res.elapsed.total_seconds()))
            logger.debug('POST-接口的响应码：{}'.format(res.status_code))
            logger.debug('POST-接口的响应体：{}'.format(res.text))
            logger.info('【{}:{}接口调用结束】'.format(self.yaml_name, api_name))
            return res
        except Exception as e:
            logger.error("接口请求 {}".format(e))
            return None


if __name__ == '__main__':
    # bd = BaseData("01登录页面接口信息")
    # res = bd.get_element_data().get("login_api")
    # print(res)
    ba = BaseApi(yaml_name="01登录页面接口信息")
    result = ba.request_base('login_api')
    print(result)