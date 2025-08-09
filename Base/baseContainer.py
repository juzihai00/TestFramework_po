class GlobalManager(object):
    """
    用来数据传递，管理全局的变量
    """
    # 实现单例模式的参数
    _instance = None
    # 一个私有的字典
    _globaldict = {}

    def __new__(cls):
        # 如果还没有实例存在
        if cls._instance is None:
            # 创建新实例
            cls._instance = super(GlobalManager, cls).__new__(cls)
            # 可以在这里初始化实例变量
            cls._instance._initialized = False
        return cls._instance

    def set_value(self, name, value):
        """
        给字典globaldict添加数据
        """
        self._globaldict[name] = value

    def get_value(self, name):
        """
        获取字典键为name的值
        """
        try:
            return self._globaldict.get(name)
        except KeyError:
            print('获取的变量{}不存在'.format(name))
            return None

if __name__ == '__main__':
    g1 = GlobalManager()
    g1.set_value('a', 'value1')
    g2 = GlobalManager()
    print(g2.get_value('a'))