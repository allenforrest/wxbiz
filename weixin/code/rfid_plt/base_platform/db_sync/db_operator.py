#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: 数据库定义
Others:      
Key Class&Method List: 
    1. ....
History: 
1. Date:2013-03-23
   Author:ACP2013
   Modification:新建文件
"""

import type_def

class DBOperator:
    """
    Class: DBOperator
    Description: 数据库表结构操作类
    Others:
    """

    @classmethod
    def check_table_exists(self, db_query, table_name):
        """
        Method: check_table_exists
        Description: 检查表是否存在
        Parameter:
            db_query: DB查询对象
            table_name: 表名 
        Return:
            存在返回true,否则返回false
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
        Description: 得到字段的定义字符串
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