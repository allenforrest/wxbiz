#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: DbSync APP，负责数据库同步的测试数据的生成
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
import math

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import mit
import tracelog
import err_code_mgr

import db_sync_worker

from dba import base, db_cfg_info
from dba import oradb
from dba.base import DBConnectionPool, DBConnectionInfo
from dba.error import DBConnectError, DBQueryError

from db_sync_event_manager import DBSyncEventManager

EVENTS_NUM = 100
if sys.argv[1] is not None:
    EVENTS_NUM = int(sys.argv[1])

class DBSyncEventTestDataApp(bf.BasicApp):
    """
    Class: DBSyncApp
    Description: 数据库同步App类,负责数据库数据的同步
    Base: BasicApp
    Others:
        __mit_manager，mit管理器
        _db_sync_worker, 数据同步操作类
    """

    def __init__(self):
        """
        Method: __init__
        Description: 对象初始化函数
        Parameter: 无
        Return:
        Others:
        """
        bf.BasicApp.__init__(self, "DBSyncEventTestDataApp")
        self.__connection_pool = None

    def get_conn_pool(self):
        """
        Method: get_conn_pool
        Description: 获取DBConnetionPool实例
        Parameter: 无
        Return: __connection_pool
        Others:
        """

        return self.__connection_pool

    def get_connection(self, name = None):
        """
        Method: get_connection_name
        Description: 得到数据库连接
        """
        if name is None:
            return self.__connection_pool.get_connection(db_cfg_info.ORACLE_SYNC_CON_NAME)
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
        bf.BasicApp._ready_for_work(self)

        # Reister MOC object
        conn_info = oradb.ConnectionInfo(**db_cfg_info.get_configure(db_cfg_info.ORACLE_SYNC_CON_NAME))
        self.__connection_pool = DBConnectionPool()
        self.__connection_pool.create_connection(db_cfg_info.ORACLE_SYNC_CON_NAME
                                            , conn_info
                                            , oradb.create_connection
                                            , 10)

        mit_manager = mit.Mit()
        mit_manager.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME))
        with self.get_connection(db_cfg_info.ORACLE_SYNC_CON_NAME) as db_conn:
            db_sync_event_manager = DBSyncEventManager(db_conn)
            db_sync_event_manager.remove_schema()
            db_sync_event_manager.create_schema()

            testdir = os.path.join(self.get_app_top_path(), 'moc_def', 'moc_test')
            sys.path.append(testdir)
            import TestAntenna
            import TestPhysicalReader
            mit_manager.regist_moc(TestAntenna.TestAntenna, TestAntenna.TestAntennaRule)
            mit_manager.regist_moc(TestPhysicalReader.TestPhysicalReader, TestPhysicalReader.TestPhysicalReaderRule)
            for i in xrange(1, int(math.ceil(float(EVENTS_NUM)/5)) + 1):
                ta = TestAntenna.TestAntenna()
                ta.readerId = 'readerId-%d' % i
                mit_manager.rdm_add(ta)
                ta.ChannelIndex = 99
                mit_manager.rdm_mod(ta)
                mit_manager.rdm_remove(ta)

                reader = TestPhysicalReader.TestPhysicalReader()
                reader.readerId = 'readerId-%d' % i
                mit_manager.rdm_add(reader)
                mit_manager.rdm_remove(reader)
            #db_sync_event_manager.add_full_event()
            
        return 1

if __name__=='__main__':
    DBSyncEventTestDataApp().run()
