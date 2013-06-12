#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: DbSyncUpdate APP，负责处理数据库的同步
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

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import mit
import tracelog
import err_code_mgr

class DBSyncUpdateManager():
    """
    Class: DBSyncUpdateManager
    Description: 更新数据管理类,负责接收同步消息，将数据更新到数据库
    Base: BasicApp
    Others:
        _db，db访问对象
    """

    def __init__(self, db):
        """
        Method: __init__
        Description: 对象初始化函数
        Parameter:
            db: db访问对象
        Return:
        Others:
        """
        self._db = db

    def insert():
        """
        Method: insert
        Description: 追加MOC对象到数据库
        Parameters: 无
        Others: 无
        """
        #TODO:
        if self._db is None:
            raise ValueError('no db connection object')
        self._db.add(self._moc)

    def mod():
        """
        Method: mod
        Description: 更新MOC对象
        Parameters: 无
        Others: 无
        """
        #TODO:
        if self._db is None:
            raise ValueError('no db connection object')
        self._db.mod(self._moc)

    def remove():
        """
        Method: remove
        Description: 删除MOC对象
        Parameters: 无
        Others: 无
        """
        #TODO:
        if self._db is None:
            raise ValueError('no db connection object')
        self._db.remove(self._moc.get_moid())
