#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: ftp_server_app�Ĵ�����
Others: ��
Key Class&Method List: ��
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:�½��ļ�
"""


import err_code_mgr

FTPSERVER_ERROR_BASE = 3101

ftp_server_error_defs = {"ER_FTPSERVER_SET_WRONG" : (FTPSERVER_ERROR_BASE + 1
                                             , "����ftp���������� �� %(errinfo)s"
                                             , "Fail to set ftp server: %(errinfo)s" )  
                         ,"ER_FTPSERVER_INVALID_DESERIALIZE_ERROR" : (FTPSERVER_ERROR_BASE + 2
                                             , "ftp_server�õ��Ƿ��ķ����л��ַ���"
                                             , "invalid string to deserialize" )
                         ,"ER_FTPSERVER_USER_NOT_EXISTS_ERROR" : (FTPSERVER_ERROR_BASE + 3
                                             , "�����ڸ�FTP�û�"
                                             , "Ftp User not exists" )  
                         ,"ER_FTPSERVER_DB_ERROR" : (FTPSERVER_ERROR_BASE + 4
                                             , "�޸�����ʧ��"
                                             , "Fail to change ftp password" ) 
             }

err_code_mgr.regist_errors(ftp_server_error_defs)