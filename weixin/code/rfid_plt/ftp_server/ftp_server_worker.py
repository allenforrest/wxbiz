#coding=gbk    
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: �ṩFTP�û������޸ģ��ṩFTP�û��б���
Others:��
Key Class&Method List: 
             1. FtpServerWorker:�ṩFTP�û������޸ģ��ṩFTP�û��б���
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:�½��ļ�
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
    Description: �ṩFTP�û������޸ģ��ṩFTP�û��б���
    Base: CmdWorker
    Others: ��
    """

    def __init__(self):
        """
        Method: __init__
        Description: ��ʼ��
        Parameter: ��
        Return: ��
        Others: ��
        """

        bf.CmdWorker.__init__(self, name = "FtpServerWorker", min_task_id=1, max_task_id=20000)
        
    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: ע���worker������handler
        Parameter: ��
        Return: 0
        Others: ��
        """

        self.register_handler(ftp_server_handler.FtpServerChangePasswordHandler(), command_code.FTP_SERVER_CHANGE_PASSWORD)
        self.register_handler(ftp_server_handler.FtpServerGetUserHandler(), command_code.FTP_SERVER_GET_USER)
        return 0
    
    def send_ack(self, frame, datas):
        """
        Method: send_ack
        Description: �򷢳�����Ľ��̷��ʹ������Ĵ�����
        Parameter: 
            frame: �յ���Ҫ�������Ϣ
            datas: ���ʹ���������Ϣ
        Return: ��
        Others: ��
        """

        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(frame)        
        for data in datas:
            frame_ack.add_data(data)
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)