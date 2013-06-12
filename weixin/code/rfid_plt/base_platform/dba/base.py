#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-22
Description: ���ݿ����ӹ���
Others:
Key Class&Method List:
    1. DBConnection: ���ݿ����ӵĻ���
    2. DBQuery: ���ݿ�����Ļ���
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
    Description: ���һ�����ݿ����ӵ���
    Base: 
    Others:
    """
    def __init__(self, conn_info, create_func, max_connections):
        """
        Method: __init__
        Description: �����캯��
        Parameter: 
            conn_info: ������Ϣ(�û��������)
            create_func: �������ݿ����ӵĻص�����
            max_connections: ���������
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
        Description: �ر���һ�����е�����
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
        Description: ���������������ʼ�����е�����
        Parameter: 
        Return:
        Others:
        """
        for i in xrange(self.max_connections):
            self.conns.append(self.create_func(self.conn_info))

    def get_connection(self):
        """
        Method: get_connection
        Description: �õ�һ�����õ�����
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
    Description: ���ݿ����ӳع���
    """

    def __init__(self):
        """
        Method: __init__
        Description: ���ӳس�ʼ��
        Parameters:
        """

        self._lock = threading.RLock()        
        self._conn_info = {}

    def get_connection_num(self, alias):
        """
        Method: get_connection_num
        Description: �õ�������
        """
        with self._lock:
            con_list = self._conn_info.get(alias)
            if con_list is None:
                return 0
                
            return len(con_list.conns)
        
    
    def create_connection(self, alias, conn_info, create_func, max_connections = 10):
        """
        Method: create_connection
        Description: ������������
        Parameters:
            alias: ���ӱ���
            conn_info: ������Ϣ
            max_connections: ���������
        """
        with self._lock:
            con_list = _DBConnectionList(conn_info, create_func, max_connections)
            #con_list.init()
            self._conn_info[alias] = con_list
        
   
    def release_connection(self, connection):
        """
        Method: release_connection
        Description: �ͷ����ݿ�����
        Parameters:
            1. conn_info ���ݿ�������Ϣ
            2. connection ��Ҫ�ͷŵ�����
        """
        with self._lock:
            for con_list in self._conn_info.itervalues():
                if connection in con_list.conns:
                    connection.used = False
                    break

    def get_connection(self, alias, transaction = True):
        """
        Method: get_connection
        Description: �õ�һ�����õ�����
        Parameters:
            alias: ���ӱ���
            transaction: �Ƿ�������,Ĭ����True
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
    Description: ���ݿ�������Ϣ
    """
    def __init__(self, *args, **kargs):
        """
        Method: __init__
        Description: ���ݿ�������Ϣ��ʼ��
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
    Description: ���ݿ����ӵĻ���
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
        Description: ���ݿ�������
        Parameters:
            1. conn_info: ���ݿ�������Ϣ
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
        Description: ���ݿ����ӽӿڣ������ฺ��ʵ��
        Parameters:
            1. conn_info: ���ݿ�������Ϣ
        """

        raise NotImplementedError('Class %s does not implement connect(self, user, password, sid, host, port, **kw)' % self.__class__)

    def get_active_query(self):
        """
        Method:    get_active_query
        Description: ��ȡһ����ѯ�ӿ�
        Parameter: ��
        Return: DBQuery��ʵ��
        Others:
        """

        query = self.get_query()
        self._query_list.append(query)
        return query

    def get_query(self):
        """
        Method:    get_query
        Description: ��ȡһ����ѯ�ӿ�
        Parameter: ��
        Return: DBQuery��ʵ��
        Others:
        """
        
        raise NotImplementedError('Class %s does not implement get_query(self)' % self.__class__)

    def __del__(self):
        """
        Method: __del__
        Description: ����ɾ��
        Parameter: ��
        Return: 
        Others: 
        """

        self.close()

    def is_closed(self):
        """
        Method:    close
        Description: ������ݿ����ӹر�
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
        Description: �ر����ݿ�����
        Return:
        Others:
        """

        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def begin(self, name):
        """
        Method:    begin
        Description: ��������
        Parameter:
            1. name: ���������
        Return:
        Others:
        """

        raise NotImplementedError('Class %s does not implement begin(self)' % self.__class__)

    def commit(self, name):
        """
        Method:    commit_trans
        Description: �ύ����
        Parameter:
            1. name: ���������
        Return:
        Others:
        """

        raise NotImplementedError('Class %s does not implement commit(self)' % self.__class__)


    def rollback(self, name):
        """
        Method:    rollback
        Description: �ع�����
        Parameter:
            1. name: ���������
        Return:
        Others:
        """

        raise NotImplementedError('Class %s does not implement rollback(self)' % self.__class__)

        
    def get_dbms_type(self):
        """
        Method:    get_dbms_type
        Description: ��ȡ���ݿ�ϵͳ������(oracle��sqlite��)
        Parameter: ��
        Return: ���ݿ�ϵͳ������
        Others:
        """

        return "unknown"


    def __enter__(self):
        """
        Method: __enter__
        Description: WITH���봦��
        Parameter:
        Return:
        Others: û�д���
        """
        if self.transaction is True:
            self.begin()
            
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Method: __exit__
        Description: WITH�˳�����
        Parameter:
        Return:
        Others: ��������״̬Ϊ����
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
    Description: ���ݿ�����ӿ�
    Base:
    Others:
    """

    def __init__(self, connection):
        """
        Method: __init__
        Description: ��ѯ��ĳ�ʼ��
        Parameter: 
            connection: ���ݿ�����
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
        Description: WITH���봦��
        Parameter:
        Return:
        Others: û�д���
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Method: __exit__
        Description: WITH�˳�����
        Parameter:
        Return:
        Others: �ر�Query��Cursor����
        """
        self.close()

    def __del__(self):
        """
        Method: __del__
        Description: ��������
        Parameter:
        Return:
        Others: �ر�Query��Cursor����
        """
        self.close()

    def select_cursor(self, sql, *args, **dw):
        """
        Method:    select
        Description: ִ��select��䣬���ز�ѯ���
        Parameter:
            sql: SQL���
            *args: ���ݸ����ݿ�ӿڵĲ���
            **dw: ���ݸ����ݿ�ӿڵĲ���
        Return: ��ѯ�α�
        Others:
        """

        raise NotImplementedError('Class %s does not implement select(self, sql, *args, **dw)' % self.__class__)

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

        raise NotImplementedError('Class %s does not implement select(self, sql, *args, **dw)' % self.__class__)

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

        raise NotImplementedError('Class %s does not implement execute(self, sql, *args, **dw)' % self.__class__)

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

        raise NotImplementedError('Class %s does not implement executemany(self, sql, seq_of_parameters)' % self.__class__)

    def executescript(self, sql_script):
        """
        Method:    executescript
        Description: ִ��һ��SQL�ű�
        Parameter:
            sql_script: һ��SQL�ű�
        Return:
        Others:
        """

        raise NotImplementedError('Class %s does not implement executescript(self, sql_script)' % self.__class__)

    def close(self):
        """
        Method:    close
        Description: �رյ�ǰ��ѯ
        Parameter:
        Return:
        Others:
        """

        raise NotImplementedError('Class %s does not implement close(self)' % self.__class__)

    def get_conn(self):
        return self._connection
        
