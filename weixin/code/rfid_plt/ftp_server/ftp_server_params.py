#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-01-08
Description: ftp_server_app的参数对象
Others: 无 
Key Class&Method List: 
             1. FtpChangePassword: 修改密码参数
             2. GetFtpServerHandlerResult: ftp_server_app中所有Handler处理结果返回参数
             3. FtpUser: 用户参数
             4. GetFtpUserListResult: 用户列表参数
History: 
1. Date:2012-01-08
   Author:ACP2013
   Modification:新建文件
"""


import serializable_obj
import type_def
    
class FtpChangePassword(serializable_obj.JsonSerializableObj):
    """
    Class: FtpChangePassword
    Description: 修改密码参数
    Base: JsonSerializableObj
    Others: 无
    """


    __ATTR_DEF__ = {
                      "username": type_def.TYPE_STRING
                    , "newpassword": type_def.TYPE_STRING
                    }
    
class GetFtpServerHandlerResult(serializable_obj.JsonSerializableObj):
    """
    Class: GetFtpServerHandlerResult
    Description: ftp_server_app中所有Handler处理结果返回参数
    Base: JsonSerializableObj
    Others: 无
    """


    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    }
    
class FtpUser(serializable_obj.JsonSerializableObj):
    """
    Class: FtpUser
    Description: 用户参数
    Base: JsonSerializableObj
    Others: 无
    """


    __ATTR_DEF__ = {
                      "username": type_def.TYPE_STRING
                    , "homedir": type_def.TYPE_STRING
                    , "perm": type_def.TYPE_STRING
                    }

class GetFtpUserListResult(serializable_obj.JsonSerializableObj):
    """
    Class: GetFtpUserListResult
    Description: 用户列表参数
    Base: JsonSerializableObj
    Others: 无
    """


    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "FtpUsers": [FtpUser]
                    }