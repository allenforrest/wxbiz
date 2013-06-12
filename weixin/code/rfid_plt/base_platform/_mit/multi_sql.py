#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: �����ж��������ڶ����ͬ���ݿ�ϵͳ��SQL���İ�װ��
Others:      
Key Class&Method List: 
             1. MultiSQL: ���ڶ����ͬ���ݿ�ϵͳ��SQL���İ�װ��
ע: 

"""

# ��Ŷ������ݿ��SQL������
class MultiSQL:
    """
    Class: MultiSQL
    Description: ���ڶ����ͬ���ݿ�ϵͳ��SQL���İ�װ��
    Base: 
    Others: 
    """
    def __init__(self):
        """
        Method:  __init__  
        Description: ���캯��
        Parameter: ��
        Return:
        Others: 
        """
        self.__sqls = {}
        
        self.__default_sql = None

    def set_default_sql(self, sql):
        """
        Method: set_default_sql
        Description: ����������ݿ�ϵͳ����Ĭ�ϵ�SQL
        Parameter: 
            sql: SQL���
        Return:
        Others: 
        """
        self.__default_sql = sql
        
    def set_sqlite_sql(self, sql):
        """
        Method:    set_sqlite_sql
        Description: ��������sqlite��SQL
        Parameter: 
            sql: SQL���
        Return: 
        Others: 
        """
        self.__sqls["sqlite"] = sql

    def set_oracle_sql(self, sql):
        """
        Method:    set_sqlite_sql
        Description: ��������oracle��SQL
        Parameter: 
            sql: SQL���
        Return: 
        Others: 
        """
        # ע��, oracle�У���Ҫ���ֶ���ʹ��˫���Ű�����
        self.__sqls["oracle"] = sql

    def get_sqlite_sql(self):
        """
        Method:    get_sqlite_sql
        Description: ��ȡ����sqlite��SQL
        Parameter: ��
        Return: ����sqlite��SQL; ��������ʱ������None
        Others: 
        """        
        return self.__sqls.get("sqlite")

    def get_oracle_sql(self):
        """
        Method: get_oracle_sql
        Description: ��ȡ����oracle��SQL
        Parameter: ��
        Return:����oracle��SQL; ��������ʱ������None
        Others: 
        """
        return self.__sqls.get("oracle")

    def get_sql(self, dbms_type, raise_err_when_not_found = True):
        """
        Method: get_sql
        Description: �������ݿ����ͣ���ȡSQL
        Parameter: 
            dbms_type: ���ݿ�����, ���� sqlite oracle
            raise_err_when_not_found:��ָ����SQL������ʱ���Ƿ��׳��쳣
        Return:SQL����ָ�����ݿ����͵�SQL������ʱ������None���׳��쳣
        Others: 
        """
        sql = self.__sqls.get(dbms_type, self.__default_sql)
        
        if raise_err_when_not_found is True and sql is None:
            raise Exception("SQL for %s has not been set!" % dbms_type)
                
        return sql
