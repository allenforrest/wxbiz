#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: 提供FTP用户密码修改,提供FTP用户列表返回
Others: 无
Key Class&Method List: 
             1. FtpServerChangePasswordHandler :handler类,提供FTP用户密码修改
             2. FtpServerGetUserHandler :handler类,提供FTP用户列表返回
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:新建文件
"""


import bundleframework as bf
import tracelog
import err_code_mgr
from hashlib import md5

import ftp_server_params

class FtpServerChangePasswordHandler(bf.CmdHandler):
    """
    Class: FtpServerChangePasswordHandler
    Description: 提供FTP用户密码修改
    Base: CmdHandler
    Others: 无
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 提供FTP用户密码修改
        Parameter: 
            frame: 收到的处理消息
            data区1个参数:
            msg: FtpChangePassword对象 
        Return: 无
        Others: 无
        """

        try:
            msg = ftp_server_params.FtpChangePassword().deserialize(frame.get_data())
        except:
            result = ftp_server_params.GetFtpServerHandlerResult()
            result.return_code = err_code_mgr.ER_FTPSERVER_INVALID_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_FTPSERVER_INVALID_DESERIALIZE_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return

        rdms = self.get_worker().get_app().get_mit_manager().rdm_find("FtpServerUserMOC",username=msg.username)
        if len(rdms)==0:
            result = ftp_server_params.GetFtpServerHandlerResult()
            result.return_code = err_code_mgr.ER_FTPSERVER_USER_NOT_EXISTS_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_FTPSERVER_USER_NOT_EXISTS_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return

        rdms[0].password = md5(msg.newpassword).hexdigest()
        ret = self.get_worker().get_app().get_mit_manager().rdm_mod(rdms[0])
        if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
            result = ftp_server_params.GetFtpServerHandlerResult()
            result.return_code = err_code_mgr.ER_FTPSERVER_DB_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_FTPSERVER_DB_ERROR)
            self.get_worker().send_ack(frame, (result.serialize(), ))
            return 
        
        self.get_worker().get_app().get_ftp_server_manage().get_authorizer().change_password(msg.username
                                                                                             ,msg.newpassword)
        
        result = ftp_server_params.GetFtpServerHandlerResult()
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        self.get_worker().send_ack(frame, (result.serialize(), ))
        
class FtpServerGetUserHandler(bf.CmdHandler):
    """
    Class: FtpServerGetUserHandler
    Description: 提供FTP用户列表返回
    Base: CmdHandler
    Others: 无
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 提供FTP用户列表返回
        Parameter: 
            frame:无 
        Return: 无
        Others: 无
        """

        
        records =  self.get_worker().get_app().get_mit_manager().lookup_attrs("FtpServerUserMOC"
                                                                              ,['username','password','homedir','perm'])
        results = ftp_server_params.GetFtpUserListResult()
        results.init_all_attr()
        results.FtpUsers = []
        
        for record in records:
            ftp_user = ftp_server_params.FtpUser()
            ftp_user.init_all_attr()
            ftp_user.username = record[0]
            ftp_user.homedir = record[2]
            ftp_user.perm = record[3]
            results.FtpUsers.append(ftp_user)
        
        results.return_code = err_code_mgr.ER_SUCCESS
        results.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        self.get_worker().send_ack(frame, (results.serialize(), ))
        
        