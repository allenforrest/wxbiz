#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: ���ݿⶨ��
Others:      
Key Class&Method List: 
    1. ....
History: 
1. Date:2013-03-23
   Author:ACP2013
   Modification:�½��ļ�
"""

import type_def

class DBOperator:
    """
    Class: DBOperator
    Description: ���ݿ��ṹ������
    Others:
    """

    @classmethod
    def check_table_exists(self, db_query, table_name):
        """
        Method: check_table_exists
        Description: �����Ƿ����
        Parameter:
            db_query: DB��ѯ����
            table_name: ���� 
        Return:
            ���ڷ���true,���򷵻�false
        Others: 
        """
        sql = "select table_name from user_tables where table_name='%s'" % table_name.upper();
        records = db_query.select(sql)
        if len(records) == 0:
            return False
        return True;

    @classmethod
    def get_field_def(self, attr):
        """
        Method: get_field_def
        Description: �õ��ֶεĶ����ַ���
        Parameter:
        Return: 
        Others: 
        """
        field = attr.name
        if (attr.attr_type == type_def.TYPE_UINT32 or attr.attr_type == type_def.TYPE_INT32):
            field = '"%s" NUMBER(10, 0)' % (field)
        elif (attr.attr_type == type_def.TYPE_STRING and attr.max_len >= 65535):
            field = '"%s" CLOB NULL' % (field)
        elif (attr.attr_type == type_def.TYPE_BINARY):
            field = '"%s" CLOB NULL' % (field)
        elif attr.max_len == 0:
            field = '"%s" VARCHAR2(%d) NULL' % (field, 255)
        else:
            field = '"%s" VARCHAR2(%d) NULL' % (field, attr.max_len)
        return field