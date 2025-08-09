#!/usr/bin/python
# -*- coding:utf-8 -*-

import yaml
import os


def read_yaml(yaml_path):
    """
    读取yaml文件内容
    realPath: 文件的真实绝对路径
    """
    if not os.path.isfile(yaml_path):
        raise FileNotFoundError("文件路径不存在，请检查路径是否正确：%s" % yaml_path)
    # open方法打开直接读出来
    with open(yaml_path, 'r', encoding='utf-8') as f:
        cfg = f.read()
    content = yaml.load(cfg,Loader=yaml.FullLoader)
    # 用load方法转字典
    return content


def write_yaml(yaml_path, write_data):
    """
    写入yaml文件单组数据
    """
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data=write_data, stream=f, allow_unicode=True)


if __name__ == '__main__':
    path = r'D:\code\python_code\TestFramework_po\Data\DataDriver\YamlDriver\project02\Yaml数据驱动-登录.yaml'
    data = read_yaml(path)
    print(data)

