#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-20
Description: 本文件中实现了mit中数据库管理的类
Others:      
Key Class&Method List: 
             1. MitDbMgr: mit中数据库管理的类
History: 
1. Date:
   Author:
   Modification:
"""


from dba import sqlitedb
try:
    from dba import oradb
except:
    # oracle的数据库不存在
    oradb = None
    
class MitDbMgr:
    """
    Class: MitDbMgr
    Description: mit中数据库管理的类
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
            _active_db: 当前活动的数据连接
            _db_con_map: 所有的数据库连接(名称:数据库连接)
        """

        self._active_db = None
        self._db_con_map = {}

    def get_db_con(self, name): 
        """
        Method:    get_db_con
        Description: 根据名称获取数据库连接
        Parameter: 
            name: 数据库连接的名称
        Return: 
            None: 指定的数据库连接不存在
            非None: 数据库连接
        Others: 
        """

        return self._db_con_map.get(name)
        
    def open_sqlite(self, name, db_file):
        """
        Method:    open_sqlite
        Description: 打开一个sqlite数据库
        Parameter: 
            name: 数据库连接的名称
            db_file: 数据库文件路径(可以是 :memory:)
        Return: 
        Others: 
        """

        self.close_db(name)
        
        con = sqlitedb.Connection(sqlitedb.ConnectionInfo(db_file = db_file))  
        self._db_con_map[name] = con

        if self._active_db is None:
            self._active_db = con

    def open_oracle(self, name, host, port, username, password, db, sysdba):
        """
        Method:    open_oracle
        Description: 打开Oracle数据库连接
        Parameter: 
            name: 
            host: 
            user: 
            pwd: 
        Return: 
        Others: 
        """

        self.close_db(name)
        
        conn_info = oradb.ConnectionInfo(
                        host = host,
                        port = port,
                        username = username,
                        password = password,
                        db= db,
                        sysdba = sysdba
                        )
        
        con = oradb.Connection(conn_info)   
        
        self._db_con_map[name] = con

        if self._active_db is None:
            self._active_db = con
            
    def close_db(self, name):
        """
        Method:    close_db
        Description: 关闭数据库连接
        Parameter: 
            name: 被关闭的数据库连接的名称
        Return: 
        Others: 
        """

        con = self._db_con_map.pop(name, None)

        if con is not None:      
            con.close()

        if con is self._active_db:
            self._active_db = None


    def close_all(self):
        """
        Method:    close_all
        Description: 关闭所有的数据库连接
        Parameter: 无
        Return: 
        Others: 
        """

        for name, con in self._db_con_map.iteritems():
            con.close()

        self._db_con_map.clear()        
        self._active_db = None
        
    def set_active_db(self, name):
        """
        Method:    set_active_db
        Description: 将指定的数据库连接设置为活动的数据库连接
        Parameter: 
            name: 数据库连接的名称
        Return: 
        Others: 
        """

        
        con = self._db_con_map.get(name)

        # 如果con为None，这self._active_db也被设置为None
        self._active_db = con
        
    def get_active_db(self):
        """
        Method:    get_active_db
        Description: 获取当前活动的数据库连接
        Parameter: 无
        Return: 当前活动的数据库连接
        Others: 
        """

        return self._active_db
        
        