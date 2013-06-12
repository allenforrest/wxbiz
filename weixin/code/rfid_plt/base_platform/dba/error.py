#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-22
Description: 数据库连接管理
Others:
Key Class&Method List:
    1. DBError: 数据库异常基类
    2. DBConnectError: 数据库连接异常
    3. DBQueryError: 数据库查询异常
History:
1. Date:
   Author:
   Modification:
"""

class DBError(Exception):
    """
    Class: DBError
    Description: DB基本异常
    Base: 
    Others: 
    """

    pass

class DBConnectError(DBError):
    """
    Class: DBConnectError
    Description: DB连接异常
    Base: DBError
    Others: 
    """

    pass

class DBQueryError(DBError):
    """
    Class: DBQueryError
    Description: DB查询异常
    Base: DBError
    Others: 
    """

    pass

