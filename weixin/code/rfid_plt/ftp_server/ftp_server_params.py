#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-01-08
Description: ftp_server_app�Ĳ�������
Others: �� 
Key Class&Method List: 
             1. FtpChangePassword: �޸��������
             2. GetFtpServerHandlerResult: ftp_server_app������Handler���������ز���
             3. FtpUser: �û�����
             4. GetFtpUserListResult: �û��б����
History: 
1. Date:2012-01-08
   Author:ACP2013
   Modification:�½��ļ�
"""


import serializable_obj
import type_def
    
class FtpChangePassword(serializable_obj.JsonSerializableObj):
    """
    Class: FtpChangePassword
    Description: �޸��������
    Base: JsonSerializableObj
    Others: ��
    """


    __ATTR_DEF__ = {
                      "username": type_def.TYPE_STRING
                    , "newpassword": type_def.TYPE_STRING
                    }
    
class GetFtpServerHandlerResult(serializable_obj.JsonSerializableObj):
    """
    Class: GetFtpServerHandlerResult
    Description: ftp_server_app������Handler���������ز���
    Base: JsonSerializableObj
    Others: ��
    """


    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    }
    
class FtpUser(serializable_obj.JsonSerializableObj):
    """
    Class: FtpUser
    Description: �û�����
    Base: JsonSerializableObj
    Others: ��
    """


    __ATTR_DEF__ = {
                      "username": type_def.TYPE_STRING
                    , "homedir": type_def.TYPE_STRING
                    , "perm": type_def.TYPE_STRING
                    }

class GetFtpUserListResult(serializable_obj.JsonSerializableObj):
    """
    Class: GetFtpUserListResult
    Description: �û��б����
    Base: JsonSerializableObj
    Others: ��
    """


    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "FtpUsers": [FtpUser]
                    }