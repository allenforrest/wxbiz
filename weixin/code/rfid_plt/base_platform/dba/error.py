#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-22
Description: ���ݿ����ӹ���
Others:
Key Class&Method List:
    1. DBError: ���ݿ��쳣����
    2. DBConnectError: ���ݿ������쳣
    3. DBQueryError: ���ݿ��ѯ�쳣
History:
1. Date:
   Author:
   Modification:
"""

class DBError(Exception):
    """
    Class: DBError
    Description: DB�����쳣
    Base: 
    Others: 
    """

    pass

class DBConnectError(DBError):
    """
    Class: DBConnectError
    Description: DB�����쳣
    Base: DBError
    Others: 
    """

    pass

class DBQueryError(DBError):
    """
    Class: DBQueryError
    Description: DB��ѯ�쳣
    Base: DBError
    Others: 
    """

    pass

