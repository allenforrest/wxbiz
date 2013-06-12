#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-22
Description: 数据库连接管理
Others:
Key Class&Method List:
    1. DBConnection: 数据库连接的基类
    2. DBQuery: 数据库操作的基类
History:
1. Date:
   Author:
   Modification:
"""

import hashlib

import threading
from .error import DBConnectError, DBQueryError

ROOT_TRANS = None

class _DBConnectionList:
    """
    Class: _DBConnectionList
    Description: 存放一组数据库连接的类
    Base: 
    Others:
    """
    def __init__(self, conn_info, create_func, max_connections):
        """
        Method: __init__
        Description: 对象构造函数
        Parameter: 
            conn_info: 连接信息(用户名密码等)
            create_func: 创建数据库连接的回调函数
            max_connections: 最大连接数
        Return:
        Others:
        """
        
        self.conn_info = conn_info
        self.max_connections = max_connections
        self.create_func = create_func
        self.conns = []
        
    def close(self):
        """
        Method: close
        Description: 关闭这一组所有的连接
        Parameter: 
        Return:
        Others:
        """
        for con in self.conns:
            try:
                con.close()
            except:
                pass

        self.conns = []

    def init(self):
        """
        Method: init
        Description: 根据最大连接数初始化所有的连接
        Parameter: 
        Return:
        Others:
        """
        for i in xrange(self.max_connections):
            self.conns.append(self.create_func(self.conn_info))

    def get_connection(self):
        """
        Method: get_connection
        Description: 得到一个可用的连接
        Parameters:
        Return:
        Others:
        """
        conn_info = self.conn_info
        max_connections = self.max_connections
        connection = None
        conns = self.conns
    
        # check existed connections if closed
        for conn in conns:
            if conn.used is None or conn.used is False:
                connection = conn
                break
            elif conn.is_closed():
                conn.reconnect(conn_info)
                connection = conn
                break
                
        if connection is None:
            if len(conns) < max_connections:
                # unused connection remains
                connection = self.create_func(conn_info)
                self.conns.append(connection)
            else:
                # unavailable connection
                raise DBConnectError('connection pool was full.max=%d' % max_connections)

        connection.used = True
        return connection

            
class DBConnectionPool():
    """
    Class: DBConnectionPool
    Description: 数据库连接池管理
    """

    def __init__(self):
        """
        Method: __init__
        Description: 连接池初始化
        Parameters:
        """

        self._lock = threading.RLock()        
        self._conn_info = {}

    def get_connection_num(self, alias):
        """
        Method: get_connection_num
        Description: 得到连接数
        """
        with self._lock:
            con_list = self._conn_info.get(alias)
            if con_list is None:
                return 0
                
            return len(con_list.conns)
        
    
    def create_connection(self, alias, conn_info, create_func, max_connections = 10):
        """
        Method: create_connection
        Description: 创建所有连接
        Parameters:
            alias: 连接别名
            conn_info: 连接信息
            max_connections: 最大连接数
        """
        with self._lock:
            con_list = _DBConnectionList(conn_info, create_func, max_connections)
            #con_list.init()
            self._conn_info[alias] = con_list
        
   
    def release_connection(self, connection):
        """
        Method: release_connection
        Description: 释放数据库连接
        Parameters:
            1. conn_info 数据库连接信息
            2. connection 需要释放的连接
        """
        with self._lock:
            for con_list in self._conn_info.itervalues():
                if connection in con_list.conns:
                    connection.used = False
                    break

    def get_connection(self, alias, transaction = True):
        """
        Method: get_connection
        Description: 得到一个可用的连接
        Parameters:
            alias: 连接别名
            transaction: 是否是事务,默认是True
        """
        
        with self._lock:
            con_list = self._conn_info.get(alias)
            if con_list is None:
                return None

            connection = con_list.get_connection()
            connection.transaction = transaction
            
            return connection

    def close(self):
        for con_list in self._conn_info.itervalues():
            con_list.close()

        self._conn_info.clear()
        
class DBConnectionInfo:
    """
    Class: DBConnectionInfo
    Description: 数据库连接信息
    """
    def __init__(self, *args, **kargs):
        """
        Method: __init__
        Description: 数据库连接信息初始化
        """
        self.info = kargs.copy()     
        self.set_key()
        
    def set_info(self, conn_info):
        self.info.update(conn_info)
        self.set_key()

    def set_key(self, key = None):
        if key is None:
            # Calculate hash string of confiration
            hash_str = ''.join([str(x) for x in self.info.values()])
            self.key = hashlib.md5(hash_str).hexdigest()
        else:
            self.key = key

class DBConnection:
    """
    Class: DBConnection
    Description: 数据库连接的基类
    Base:
    Others:
    """

    def __init__(self, conn_info):
        self.used = False
        self._connection = None
        self._query_list = []
        self.transaction = False
        self.reconnect(conn_info)

    def reconnect(self, conn_info):
        """
        Method: connect
        Description: 数据库再连接
        Parameters:
            1. conn_info: 数据库连接信息
        """
        
            
        try:
            if self._connection is not None:
                self._connection.close()
                self._connection = None
                
            self.connect(conn_info)
        except Exception as e:
            raise DBConnectError(e)

    def connect(self, conn_info):
        """
        Method: connect
        Description: 数据库连接接口，由子类负责实现
        Parameters:
            1. conn_info: 数据库连接信息
        """

        raise NotImplementedError('Class %s does not implement connect(self, user, password, sid, host, port, **kw)' % self.__class__)

    def get_active_query(self):
        """
        Method:    get_active_query
        Description: 获取一个查询接口
        Parameter: 无
        Return: DBQuery的实例
        Others:
        """

        query = self.get_query()
        self._query_list.append(query)
        return query

    def get_query(self):
        """
        Method:    get_query
        Description: 获取一个查询接口
        Parameter: 无
        Return: DBQuery的实例
        Others:
        """
        
        raise NotImplementedError('Class %s does not implement get_query(self)' % self.__class__)

    def __del__(self):
        """
        Method: __del__
        Description: 对象删除
        Parameter: 无
        Return: 
        Others: 
        """

        self.close()

    def is_closed(self):
        """
        Method:    close
        Description: 检查数据库连接关闭
        Return:
        Others:
        """
        if self._connection is None:
            return True
        else:
            return False

    def close(self):
        """
        Method:    close
        Description: 关闭数据库连接
        Return:
        Others:
        """

        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def begin(self, name):
        """
        Method:    begin
        Description: 启动事务
        Parameter:
            1. name: 事务的名字
        Return:
        Others:
        """

        raise NotImplementedError('Class %s does not implement begin(self)' % self.__class__)

    def commit(self, name):
        """
        Method:    commit_trans
        Description: 提交事务
        Parameter:
            1. name: 事务的名字
        Return:
        Others:
        """

        raise NotImplementedError('Class %s does not implement commit(self)' % self.__class__)


    def rollback(self, name):
        """
        Method:    rollback
        Description: 回滚事务
        Parameter:
            1. name: 事务的名字
        Return:
        Others:
        """

        raise NotImplementedError('Class %s does not implement rollback(self)' % self.__class__)

        
    def get_dbms_type(self):
        """
        Method:    get_dbms_type
        Description: 获取数据库系统的名称(oracle、sqlite等)
        Parameter: 无
        Return: 数据库系统的名称
        Others:
        """

        return "unknown"


    def __enter__(self):
        """
        Method: __enter__
        Description: WITH进入处理
        Parameter:
        Return:
        Others: 没有处理
        """
        if self.transaction is True:
            self.begin()
            
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Method: __exit__
        Description: WITH退出处理
        Parameter:
        Return:
        Others: 设置连接状态为可用
        """
        if self.transaction is True:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()

        self.used = False
        for query in self._query_list:
            query.close()

class DBQuery():
    """
    Class: DBQuery
    Description: 数据库操作接口
    Base:
    Others:
    """

    def __init__(self, connection):
        """
        Method: __init__
        Description: 查询类的初始化
        Parameter: 
            connection: 数据库连接
        Return: 
        Others: 
        """
        self._connection = None
        
        if isinstance(connection, DBConnection):
            self._connection = connection
        elif isinstance(connection, DBConnectionPool):
            self._connection = connection.get_connection()
        else:
            raise DBQueryError('Not supported parameter type. :%r' % connection)

    def __enter__(self):
        """
        Method: __enter__
        Description: WITH进入处理
        Parameter:
        Return:
        Others: 没有处理
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Method: __exit__
        Description: WITH退出处理
        Parameter:
        Return:
        Others: 关闭Query，Cursor对象
        """
        self.close()

    def __del__(self):
        """
        Method: __del__
        Description: 析构处理
        Parameter:
        Return:
        Others: 关闭Query，Cursor对象
        """
        self.close()

    def select_cursor(self, sql, *args, **dw):
        """
        Method:    select
        Description: 执行select语句，返回查询结果
        Parameter:
            sql: SQL语句
            *args: 传递给数据库接口的参数
            **dw: 传递给数据库接口的参数
        Return: 查询游标
        Others:
        """

        raise NotImplementedError('Class %s does not implement select(self, sql, *args, **dw)' % self.__class__)

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

        raise NotImplementedError('Class %s does not implement select(self, sql, *args, **dw)' % self.__class__)

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

        raise NotImplementedError('Class %s does not implement execute(self, sql, *args, **dw)' % self.__class__)

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

        raise NotImplementedError('Class %s does not implement executemany(self, sql, seq_of_parameters)' % self.__class__)

    def executescript(self, sql_script):
        """
        Method:    executescript
        Description: 执行一段SQL脚本
        Parameter:
            sql_script: 一段SQL脚本
        Return:
        Others:
        """

        raise NotImplementedError('Class %s does not implement executescript(self, sql_script)' % self.__class__)

    def close(self):
        """
        Method:    close
        Description: 关闭当前查询
        Parameter:
        Return:
        Others:
        """

        raise NotImplementedError('Class %s does not implement close(self)' % self.__class__)

    def get_conn(self):
        return self._connection
        
