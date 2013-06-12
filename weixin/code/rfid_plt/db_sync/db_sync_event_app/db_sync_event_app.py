#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: DbSync APP，负责数据库的同步
Others:
Key Class&Method List:
    1. DBSyncApp
History:
1. Date:2013-03-23
   Author:ACP2013
   Modification:新建文件
"""

import os.path
import sys
import threading

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import mit
import tracelog
import err_code_mgr

import error_code
import db_sync_worker

from dba import base, db_cfg_info
from dba import oradb
from dba.base import DBConnectionPool, DBConnectionInfo
from dba.error import DBConnectError, DBQueryError

from db_sync_event_manager import DBSyncEventManager
from db_sync_util import DBSyncUtil

class DBSyncEventApp(bf.BasicApp):
    """
    Class: DBSyncApp
    Description: 数据库同步App类,负责数据库数据的同步
    Base: BasicApp
    Others:
        __db_sync_worker, 数据同步操作类
        __connection_pool, 数据库连接池
    """

    def __init__(self):
        """
        Method: __init__
        Description: 对象初始化函数
        Parameter: 无
        Return:
        Others:
        """
        bf.BasicApp.__init__(self, "DBSyncEventApp")
        self.__connection_pool = None

        self.__synchronized_mocs = {}

        # 将MOC表的数据插入到同步表中的SQL语句
        self.__moc_data_to_sync_tbl_sqls = [] #[(table_name, sql),....]

    def get_conn_pool(self):
        """
        Method: get_conn_pool
        Description: 获取DBConnetionPool实例
        Parameter: 无
        Return: __connection_pool
        Others:
        """

        return self.__connection_pool

    def get_synchronized_mocs(self):
        """
        Method: get_synchronized_mocs
        Description: 获取同步对象列表
        Parameter: 无
        Return: __synchronized_mocs
        Others:
        """

        return self.__synchronized_mocs

    def get_moc_data_to_sync_tbl_sqls(self):
        """
        Method: get_moc_data_to_sync_tbl_sqls
        Description: 
        Parameter: 无
        Return: 
        Others: 
        """

        return self.__moc_data_to_sync_tbl_sqls
        

    def __init_moc_data_to_sync_tbl_sqls(self):
        """
        Method: __init_moc_data_to_sync_tbl_sqls
        Description: 
        Parameter: 无
        Return: 
        Others: 
        """

        self.__moc_data_to_sync_tbl_sqls = []
        for moc in self.__synchronized_mocs.itervalues():
            
            fields = ["moid"]
            keys, nonkeys = moc.get_attr_names()
            fields += list(keys + nonkeys)
            fields += [attr.name for attr in moc.__COMPLEX_ATTR_DEF__]
            fields = ['"%s"' % f for f in fields]
            fields = ",".join(fields)
            
            table_name = "tbl_" + moc.get_moc_name()
                        
            sql = 'insert into user_sync.%s ("_SYNC_SOURCE", %s) select :1, %s from user_acp.%s' % (
                         table_name
                        , fields
                        , fields
                        , table_name)
                        
            self.__moc_data_to_sync_tbl_sqls.append((table_name, sql))

    def get_connection(self, name = None):
        """
        Method: get_connection_name
        Description: 得到数据库连接
        """
        if name is None:
            return self.__connection_pool.get_connection(db_cfg_info.ORACLE_DEFAULT_CON_NAME)
        else:
            return self.__connection_pool.get_connection(name)

    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: 父类实现方法，注册MOC对象
        Parameter: 无
        Return: 0，成功
                其他，失败
        Others:
        """
        tracelog.info('_ready_for_work started.')
        bf.BasicApp._ready_for_work(self)

        # 创建数据库连接
        self.__connection_pool = DBConnectionPool()
        conn_info = oradb.ConnectionInfo(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME))        
        self.__connection_pool.create_connection(db_cfg_info.ORACLE_DEFAULT_CON_NAME
                                            , conn_info
                                            , oradb.create_connection
                                            , 5)
        conn_info = oradb.ConnectionInfo(**db_cfg_info.get_configure(db_cfg_info.ORACLE_SYNC_CON_NAME))        
        self.__connection_pool.create_connection(db_cfg_info.ORACLE_SYNC_CON_NAME
                                            , conn_info
                                            , oradb.create_connection
                                            , 1)
        
                                            
        with self.get_connection(db_cfg_info.ORACLE_SYNC_CON_NAME) as db_conn:
            db_sync_event_manager = DBSyncEventManager(db_conn)
            db_sync_event_manager.create_schema()

        # 加载所有MOC对象
        curdir = os.path.join(self.get_app_top_path(), 'moc_def')
        DBSyncUtil.load_mocs(curdir, self.__synchronized_mocs)
        self.__init_moc_data_to_sync_tbl_sqls()
        
        # Register db sync worker
        self.register_worker(db_sync_worker.DBSyncWorker())
        tracelog.info('_ready_for_work ended.')
        
        return 0

if __name__=='__main__':
    DBSyncEventApp().run()
