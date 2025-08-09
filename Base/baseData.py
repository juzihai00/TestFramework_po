import os
import yaml
from string import Template
from Base.baseExcel import ExcelRead
from Base.basePath import BasePath as BP
from Base.baseContainer import GlobalManager
from Base.baseYaml import read_yaml
from Base.baselogger import Logger
from Base.utils import read_config_ini

logger = Logger('baseData.py').getLogger()


def init_file_path(pic_path):
    """
    遍历文件夹下的所有yaml文件，并存入字典。注：子文件夹下的yaml不可读取
    """
    path = {}
    # 返回三元组列表：(当前目录路径, 子目录列表, 文件列表)
    path_lists = list(os.walk(pic_path))

    for dir_tuple in path_lists:
        # 正确解包三元组
        current_dir, sub_dirs, file_list = dir_tuple

        # 只处理文件列表
        for file_name in file_list:
            # 获取文件名（不含扩展名）
            base_name = os.path.splitext(file_name)[0]
            # 构建完整路径
            full_path = os.path.join(current_dir, file_name)
            path[base_name] = full_path

    return path


def is_file_exist(file_path, yaml_name):
    """
    判断文件夹下有没有所要的文件名
    file_path: 这里是init_file_path函数返回的字典
    """
    abs_path = file_path.get(yaml_name)
    if not abs_path:
        raise FileNotFoundError(f"el:{yaml_name}不存在检查文件名或检查配置文件TEST_PROJECT")
    return abs_path


class BaseData(object):
    """
    逻辑层数据读取-获取dataelement数据
    """

    def __init__(self, yaml_name=None):
        self.gm = GlobalManager()
        self.yaml_name = yaml_name
        self.config = read_config_ini(BP.CONFIG_FILE)
        self.run_config = self.config['项目运行设置']
        self.api_path = init_file_path(os.path.join(BP.DATA_ELEMENT_DIR, self.run_config['TEST_PROJECT']))
        if not self.run_config['AUTO_TYPE'] == 'CLIENT':
            self.abs_path = is_file_exist(self.api_path, self.yaml_name)

    def get_element_data(self, change_data=None):
        """
        读取数据，判断是否要数据替换
        """
        # 这里要数据替换将change_data替换到$后
        if change_data:
            with open(self.abs_path, 'r', encoding='utf-8') as f:
                cfg = f.read()
                content = Template(cfg).safe_substitute(**change_data)
                return yaml.load(content, Loader=yaml.FullLoader)
        else:
            return read_yaml(self.abs_path)


class DataDriver:
    """
    读取测试用例数据的信息
    """

    def __init__(self):
        self.gm = GlobalManager()
        self.config = read_config_ini(BP.CONFIG_FILE)

    def get_case_data(self, yaml_name):
        """
        获取测试数据驱动-这里yaml-name只是一个名称
        """
        data_type = self.config['项目运行设置']['DATA_DRIVER_TYPE']
        abs_path = init_file_path(
            os.path.join(BP.DATA_DRIVER_DIR, data_type, self.config['项目运行设置']['TEST_PROJECT']))
        data_path = is_file_exist(abs_path, yaml_name)
        if data_type == 'YamlDriver':
            return read_yaml(data_path)
        elif data_type == 'ExcelDriver':
            return ExcelRead(data_path).dict_date()
        return None


if __name__ == '__main__':
    path = os.path.join(BP.DATA_ELEMENT_DIR, 'project02')
    res1 = init_file_path(path)
    res2 = is_file_exist(res1,'Web元素信息-登录')
    bd = BaseData('Web元素信息-登录')
    print(bd.get_element_data())
