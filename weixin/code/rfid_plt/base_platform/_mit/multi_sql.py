#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文中定义了用于多个不同数据库系统的SQL语句的包装类
Others:      
Key Class&Method List: 
             1. MultiSQL: 用于多个不同数据库系统的SQL语句的包装类
注: 

"""

# 存放多种数据库的SQL的容器
class MultiSQL:
    """
    Class: MultiSQL
    Description: 用于多个不同数据库系统的SQL语句的包装类
    Base: 
    Others: 
    """
    def __init__(self):
        """
        Method:  __init__  
        Description: 构造函数
        Parameter: 无
        Return:
        Others: 
        """
        self.__sqls = {}
        
        self.__default_sql = None

    def set_default_sql(self, sql):
        """
        Method: set_default_sql
        Description: 针对所有数据库系统设置默认的SQL
        Parameter: 
            sql: SQL语句
        Return:
        Others: 
        """
        self.__default_sql = sql
        
    def set_sqlite_sql(self, sql):
        """
        Method:    set_sqlite_sql
        Description: 设置用于sqlite的SQL
        Parameter: 
            sql: SQL语句
        Return: 
        Others: 
        """
        self.__sqls["sqlite"] = sql

    def set_oracle_sql(self, sql):
        """
        Method:    set_sqlite_sql
        Description: 设置用于oracle的SQL
        Parameter: 
            sql: SQL语句
        Return: 
        Others: 
        """
        # 注意, oracle中，需要将字段名使用双引号包起来
        self.__sqls["oracle"] = sql

    def get_sqlite_sql(self):
        """
        Method:    get_sqlite_sql
        Description: 获取用于sqlite的SQL
        Parameter: 无
        Return: 用于sqlite的SQL; 当不存在时，返回None
        Others: 
        """        
        return self.__sqls.get("sqlite")

    def get_oracle_sql(self):
        """
        Method: get_oracle_sql
        Description: 获取用于oracle的SQL
        Parameter: 无
        Return:用于oracle的SQL; 当不存在时，返回None
        Others: 
        """
        return self.__sqls.get("oracle")

    def get_sql(self, dbms_type, raise_err_when_not_found = True):
        """
        Method: get_sql
        Description: 根据数据库类型，获取SQL
        Parameter: 
            dbms_type: 数据库类型, 例如 sqlite oracle
            raise_err_when_not_found:当指定的SQL不存在时，是否抛出异常
        Return:SQL，当指定数据库类型的SQL不存在时，返回None或抛出异常
        Others: 
        """
        sql = self.__sqls.get(dbms_type, self.__default_sql)
        
        if raise_err_when_not_found is True and sql is None:
            raise Exception("SQL for %s has not been set!" % dbms_type)
                
        return sql
