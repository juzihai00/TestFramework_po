import pymysql
import sqlite3
from Base.baselogger import Logger
from Base.utils import read_config_ini

logger = Logger('dbbase.py').getLogger()

class MysqlHelp:
    """
    mysql数据库封装类
    """
    def __init__(self,host,user,passwd,port,database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = int(port)
        self.db = database
        self.connection = None

    def create_connection(self):
        """
        创建链接
        :return:
        """
        self.connection = pymysql.connect(host=self.host,
                                          user=self.user,
                                          passwd=self.passwd,
                                          port=self.port,
                                          db=self.db,
                                          charset='utf8')

    def mysql_db_select(self,sql):
        """
        数据库查询操作
        :return:
        """
        try:
            self.create_connection()
            logger.info("建立链接ok")
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logger.error(e)
        finally:
            self.connection.close()

    def mysql_db_operate(self,sql):
        """
        增删该数据库操作
        :return:
        """
        try:
            self.create_connection()
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                # 提交数据库事务
                self.connection.commit()
        except Exception as e:
            # 数据库事务回滚
            self.connection.rollback()
        finally:
            self.connection.close()


class Sqlite3Tools:
    """
    Sqlite3数据库封装类
    """
    def __init__(self,database = ''):
        self.database = database
        self.connection = None

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def create_connection(self):
        """
        创建链接
        :return:
        """
        self.connection = sqlite3.connect(self.database)
        self.connection.row_factory = self.dict_factory

    def sqlite3_db_select(self,sql):
        """
        数据库查询
        :param sql:
        :return:
        """
        try:
            self.create_connection()
            cur = self.connection.cursor().execute(sql)
            result = cur.fetchall()
            return result
        except Exception as e:
            print("查询错误{}".format(e))
        finally:
            self.connection.close()

    def sqlite3_db_operate(self,sql):
        """
        数据库增删改
        :param sql:
        :return:
        """
        try:
            self.create_connection()
            self.connection.cursor().execute(sql)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
        finally:
            self.connection.close()

if __name__ == '__main__':
    from  Base.basePath import BasePath as BP
    dbInfo = read_config_ini(BP.CONFIG_FILE)['数据库连接配置']
    db = MysqlHelp(host=dbInfo['host'], user=dbInfo['user'], passwd=dbInfo['passwd'], port=dbInfo['port'],
                   database=dbInfo['database'])
    res = db.mysql_db_select("select title,content,approved from journalartile order by createDate desc limit 1")[0]
    print(res)
    # pymysql.connect(host=dbInfo['host'], user=dbInfo['user'], passwd=dbInfo['passwd'], port=int(dbInfo['port']),
    #                database=dbInfo['database'],charset='utf8')