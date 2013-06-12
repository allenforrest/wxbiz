#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-20
Description: ���ļ���ʵ����mit�����ݿ�������
Others:      
Key Class&Method List: 
             1. MitDbMgr: mit�����ݿ�������
History: 
1. Date:
   Author:
   Modification:
"""


from dba import sqlitedb
try:
    from dba import oradb
except:
    # oracle�����ݿⲻ����
    oradb = None
    
class MitDbMgr:
    """
    Class: MitDbMgr
    Description: mit�����ݿ�������
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
            _active_db: ��ǰ�����������
            _db_con_map: ���е����ݿ�����(����:���ݿ�����)
        """

        self._active_db = None
        self._db_con_map = {}

    def get_db_con(self, name): 
        """
        Method:    get_db_con
        Description: �������ƻ�ȡ���ݿ�����
        Parameter: 
            name: ���ݿ����ӵ�����
        Return: 
            None: ָ�������ݿ����Ӳ�����
            ��None: ���ݿ�����
        Others: 
        """

        return self._db_con_map.get(name)
        
    def open_sqlite(self, name, db_file):
        """
        Method:    open_sqlite
        Description: ��һ��sqlite���ݿ�
        Parameter: 
            name: ���ݿ����ӵ�����
            db_file: ���ݿ��ļ�·��(������ :memory:)
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
        Description: ��Oracle���ݿ�����
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
        Description: �ر����ݿ�����
        Parameter: 
            name: ���رյ����ݿ����ӵ�����
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
        Description: �ر����е����ݿ�����
        Parameter: ��
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
        Description: ��ָ�������ݿ���������Ϊ������ݿ�����
        Parameter: 
            name: ���ݿ����ӵ�����
        Return: 
        Others: 
        """

        
        con = self._db_con_map.get(name)

        # ���conΪNone����self._active_dbҲ������ΪNone
        self._active_db = con
        
    def get_active_db(self):
        """
        Method:    get_active_db
        Description: ��ȡ��ǰ������ݿ�����
        Parameter: ��
        Return: ��ǰ������ݿ�����
        Others: 
        """

        return self._active_db
        
        