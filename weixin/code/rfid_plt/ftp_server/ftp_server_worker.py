#coding=gbk    
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: 提供FTP用户密码修改，提供FTP用户列表返回
Others:无
Key Class&Method List: 
             1. FtpServerWorker:提供FTP用户密码修改，提供FTP用户列表返回
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:新建文件
"""

import bundleframework as bf
import tracelog
import err_code_mgr
import error_code

import command_code
import ftp_server_handler

class FtpServerWorker(bf.CmdWorker):
    """
    Class: FtpServerWorker
    Description: 提供FTP用户密码修改，提供FTP用户列表返回
    Base: CmdWorker
    Others: 无
    """

    def __init__(self):
        """
        Method: __init__
        Description: 初始化
        Parameter: 无
        Return: 无
        Others: 无
        """

        bf.CmdWorker.__init__(self, name = "FtpServerWorker", min_task_id=1, max_task_id=20000)
        
    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: 注册该worker关联的handler
        Parameter: 无
        Return: 0
        Others: 无
        """

        self.register_handler(ftp_server_handler.FtpServerChangePasswordHandler(), command_code.FTP_SERVER_CHANGE_PASSWORD)
        self.register_handler(ftp_server_handler.FtpServerGetUserHandler(), command_code.FTP_SERVER_GET_USER)
        return 0
    
    def send_ack(self, frame, datas):
        """
        Method: send_ack
        Description: 向发出请求的进程发送处理结果的错误码
        Parameter: 
            frame: 收到的要处理的消息
            datas: 发送处理结果的消息
        Return: 无
        Others: 无
        """

        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(frame)        
        for data in datas:
            frame_ack.add_data(data)
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)