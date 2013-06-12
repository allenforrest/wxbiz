#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-22
Description: Sqlite数据库管理
Others:
Key Class&Method List:
    1. SqliteConnection: Sqlite数据库连接
History:
1. Date:
   Author:
   Modification:
"""
import sqlite3

from .base import DBConnection, DBConnectionInfo, DBQuery
from .base import ROOT_TRANS

def create_connection(conn_info):
    """
    Method: create_connection
    Description: 数据库连接创建回调函数
    """
    return Connection(conn_info)

class ConnectionInfo(DBConnectionInfo):
    """
    Class: ConnectionInfo
    Description: sqlite 数据库连接信息
    """
    def __init__(self, *args, **kargs):
        """
        Method: __init__
        Description: 数据库连接信息初始化
        """
        info = {
                'db_file': ':memory:'
                }
            
        info.update(kargs)         
        
        DBConnectionInfo.__init__(self, *args, **info)



class Connection(DBConnection):
    """
    Class: Connection
    Description: Sqlite数据库连接
    Base: DBConnection
    Others:
    """

    def connect(self, conn_info):
        """
        Method: connect
        Description: 数据库连接接口，由子类负责实现
        Parameters:
            1. conn_info: 数据库连接信息
        """
        self._connection = sqlite3.connect(conn_info.info["db_file"]
                                    , isolation_level=None
                                    , check_same_thread = False)
                                    
        self._connection.text_factory = str
        

    def get_query(self):
        """
        Method:    get_query
        Description: 获取一个查询接口
        Parameter: 无
        Return: DBQuery的实例
        Others:
        """

        return Query(self)

    def begin(self, name = ROOT_TRANS):
        """
        Method:    begin
        Description: 启动事务
        Parameter:
            1. name: 事务的名字
        Return:
        Others:
        """
        query = self.get_query()
        if name == ROOT_TRANS:        
            query.execute("begin;")
        else:
            query.execute("SAVEPOINT %s;" % name)

    def commit(self, name = ROOT_TRANS):
        """
        Method:    commit_trans
        Description: 提交事务
        Parameter:
            1. name: 事务的名字
        Return:
        Others:
        """
        
        if name == ROOT_TRANS:        
            self._connection.commit()
        else:
            query = self.get_query()
            query.execute("RELEASE SAVEPOINT %s;" % name)

    def rollback(self, name = ROOT_TRANS):
        """
        Method:    rollback
        Description: 回滚事务
        Parameter:
            1. name: 事务的名字
        Return:
        Others:
        """

        if name == ROOT_TRANS:        
            self._connection.rollback()
        else:
            query = self.get_query()
            query.execute("ROLLBACK TO SAVEPOINT %s;" % name)

        
    def get_dbms_type(self):
        """
        Method:    get_dbms_type
        Description: 获取数据库系统的名称(oracle、sqlite等)
        Parameter: 无
        Return: 数据库系统的名称
        Others:
        """

        return "sqlite"

    
    
class Query(DBQuery):
    """
    Class: Query
    Description: 数据库操作类
    Base: DBQuery
    Others:
    """

    def __init__(self, connection):
        """
        Method: __init__
        Description: Query类初始化
        Parameter: 
            connection: 数据库连接
        Return: 
        Others: 
        """
        self._cursor = None
        
        DBQuery.__init__(self, connection)
       
        self._cursor = self._connection._connection.cursor()
        
    def select(self, sql, *args, **dw):
        """
        Method:    select
        Description: 执行select语句，返回查询结果
        Parameter:
            sql: SQL语句
            *args: 传递给数据库接口的参数
            **dw: 传递给数据库接口的参数
        Return: 查询结果
        Others:
        """

        self._cursor.execute(sql, *args, **dw)        
        rst = self._cursor.fetchall()
        return rst

    def execute(self, sql, *args, **dw):
        """
        Method:    execute
        Description: 执行修改类的SQL语句
        Parameter:
            sql: SQL语句
            *args: 传递给数据库接口的参数
            **dw: 传递给数据库接口的参数
        Return:
        Others:
        """

        self._cursor.execute(sql, *args, **dw)

    def executemany(self, sql, seq_of_parameters):
        """
        Method:    executemany
        Description: 批量执行SQL
        Parameter:
            sql: SQL语句
            seq_of_parameters: 与SQL语句配套的序列
        Return:
        Others:
        """

        self._cursor.executemany(sql, seq_of_parameters)

    def executescript(self, sql_script):
        """
        Method:    executescript
        Description: 执行一段SQL脚本
        Parameter:
            sql_script: 一段SQL脚本
        Return:
        Others:
        """

        self._cursor.executescript(sql_script)

    def close(self):
        """
        Method:    close
        Description: 关闭当前查询
        Parameter:
        Return:
        Others:
        """

        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

