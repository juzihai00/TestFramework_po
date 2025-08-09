from configparser import RawConfigParser
import zipfile
import os

def read_config_ini(config_path):
    """
    读取配置文件.ini
    """
    config = RawConfigParser()
    config.read(config_path, encoding='utf-8')
    # 这里返回的是一个字典对象
    return config

def make_zip(local_path,pname):
    """
    将local_path打包成压缩包，并命名为pname
    """
    zipf = zipfile.ZipFile(pname, 'w', zipfile.ZIP_DEFLATED)
    pre_len = len(os.path.dirname(local_path))
    for parent, dirnames, filenames in os.walk(local_path):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            zipf.write(pathfile, arcname)
    zipf.close()
    return pname

def file_all_dele(path):
    """
    删除所有文件
    :return:
    """
    for filename in os.listdir(path):
        os.unlink(os.path.join(path, filename))

if __name__ == '__main__':
    from Base.basePath import BasePath
    import os

    result = read_config_ini(os.path.join(BasePath.CONFIG_DIR, '配置文件.ini'))
    # 用字典的方式即可得到具体参数配置，但参数均为str格式，后续使用要进行处理
    print(result['客户端自动化配置']['duration'])
