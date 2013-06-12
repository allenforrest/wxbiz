#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-22
Description: Sqlite���ݿ����
Others:
Key Class&Method List:
    1. SqliteConnection: Sqlite���ݿ�����
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
    Description: ���ݿ����Ӵ����ص�����
    """
    return Connection(conn_info)

class ConnectionInfo(DBConnectionInfo):
    """
    Class: ConnectionInfo
    Description: sqlite ���ݿ�������Ϣ
    """
    def __init__(self, *args, **kargs):
        """
        Method: __init__
        Description: ���ݿ�������Ϣ��ʼ��
        """
        info = {
                'db_file': ':memory:'
                }
            
        info.update(kargs)         
        
        DBConnectionInfo.__init__(self, *args, **info)



class Connection(DBConnection):
    """
    Class: Connection
    Description: Sqlite���ݿ�����
    Base: DBConnection
    Others:
    """

    def connect(self, conn_info):
        """
        Method: connect
        Description: ���ݿ����ӽӿڣ������ฺ��ʵ��
        Parameters:
            1. conn_info: ���ݿ�������Ϣ
        """
        self._connection = sqlite3.connect(conn_info.info["db_file"]
                                    , isolation_level=None
                                    , check_same_thread = False)
                                    
        self._connection.text_factory = str
        

    def get_query(self):
        """
        Method:    get_query
        Description: ��ȡһ����ѯ�ӿ�
        Parameter: ��
        Return: DBQuery��ʵ��
        Others:
        """

        return Query(self)

    def begin(self, name = ROOT_TRANS):
        """
        Method:    begin
        Description: ��������
        Parameter:
            1. name: ���������
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
        Description: �ύ����
        Parameter:
            1. name: ���������
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
        Description: �ع�����
        Parameter:
            1. name: ���������
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
        Description: ��ȡ���ݿ�ϵͳ������(oracle��sqlite��)
        Parameter: ��
        Return: ���ݿ�ϵͳ������
        Others:
        """

        return "sqlite"

    
    
class Query(DBQuery):
    """
    Class: Query
    Description: ���ݿ������
    Base: DBQuery
    Others:
    """

    def __init__(self, connection):
        """
        Method: __init__
        Description: Query���ʼ��
        Parameter: 
            connection: ���ݿ�����
        Return: 
        Others: 
        """
        self._cursor = None
        
        DBQuery.__init__(self, connection)
       
        self._cursor = self._connection._connection.cursor()
        
    def select(self, sql, *args, **dw):
        """
        Method:    select
        Description: ִ��select��䣬���ز�ѯ���
        Parameter:
            sql: SQL���
            *args: ���ݸ����ݿ�ӿڵĲ���
            **dw: ���ݸ����ݿ�ӿڵĲ���
        Return: ��ѯ���
        Others:
        """

        self._cursor.execute(sql, *args, **dw)        
        rst = self._cursor.fetchall()
        return rst

    def execute(self, sql, *args, **dw):
        """
        Method:    execute
        Description: ִ���޸����SQL���
        Parameter:
            sql: SQL���
            *args: ���ݸ����ݿ�ӿڵĲ���
            **dw: ���ݸ����ݿ�ӿڵĲ���
        Return:
        Others:
        """

        self._cursor.execute(sql, *args, **dw)

    def executemany(self, sql, seq_of_parameters):
        """
        Method:    executemany
        Description: ����ִ��SQL
        Parameter:
            sql: SQL���
            seq_of_parameters: ��SQL������׵�����
        Return:
        Others:
        """

        self._cursor.executemany(sql, seq_of_parameters)

    def executescript(self, sql_script):
        """
        Method:    executescript
        Description: ִ��һ��SQL�ű�
        Parameter:
            sql_script: һ��SQL�ű�
        Return:
        Others:
        """

        self._cursor.executescript(sql_script)

    def close(self):
        """
        Method:    close
        Description: �رյ�ǰ��ѯ
        Parameter:
        Return:
        Others:
        """

        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

