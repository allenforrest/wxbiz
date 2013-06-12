#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: ftp_server_app的错误码
Others: 无
Key Class&Method List: 无
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:新建文件
"""


import err_code_mgr

FTPSERVER_ERROR_BASE = 3101

ftp_server_error_defs = {"ER_FTPSERVER_SET_WRONG" : (FTPSERVER_ERROR_BASE + 1
                                             , "设置ftp服务发生错误 ： %(errinfo)s"
                                             , "Fail to set ftp server: %(errinfo)s" )  
                         ,"ER_FTPSERVER_INVALID_DESERIALIZE_ERROR" : (FTPSERVER_ERROR_BASE + 2
                                             , "ftp_server得到非法的反序列化字符串"
                                             , "invalid string to deserialize" )
                         ,"ER_FTPSERVER_USER_NOT_EXISTS_ERROR" : (FTPSERVER_ERROR_BASE + 3
                                             , "不存在该FTP用户"
                                             , "Ftp User not exists" )  
                         ,"ER_FTPSERVER_DB_ERROR" : (FTPSERVER_ERROR_BASE + 4
                                             , "修改密码失败"
                                             , "Fail to change ftp password" ) 
             }

err_code_mgr.regist_errors(ftp_server_error_defs)