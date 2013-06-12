#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: DbSyncUpdate APP�����������ݿ��ͬ��
Others:
Key Class&Method List:
    1. DBSyncApp
History:
1. Date:2013-03-23
   Author:ACP2013
   Modification:�½��ļ�
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
    Description: �������ݹ�����,�������ͬ����Ϣ�������ݸ��µ����ݿ�
    Base: BasicApp
    Others:
        _db��db���ʶ���
    """

    def __init__(self, db):
        """
        Method: __init__
        Description: �����ʼ������
        Parameter:
            db: db���ʶ���
        Return:
        Others:
        """
        self._db = db

    def insert():
        """
        Method: insert
        Description: ׷��MOC�������ݿ�
        Parameters: ��
        Others: ��
        """
        #TODO:
        if self._db is None:
            raise ValueError('no db connection object')
        self._db.add(self._moc)

    def mod():
        """
        Method: mod
        Description: ����MOC����
        Parameters: ��
        Others: ��
        """
        #TODO:
        if self._db is None:
            raise ValueError('no db connection object')
        self._db.mod(self._moc)

    def remove():
        """
        Method: remove
        Description: ɾ��MOC����
        Parameters: ��
        Others: ��
        """
        #TODO:
        if self._db is None:
            raise ValueError('no db connection object')
        self._db.remove(self._moc.get_moid())
