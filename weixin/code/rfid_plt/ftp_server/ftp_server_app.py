#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: FTP Server ��APP�����ṩFTP�����ṩFTP�û������޸ģ��ṩFTP�û��б���
Others: �� 
Key Class&Method List: 
             1. FtpServerApp: APP�࣬����worker��ע��,mit��ע��
                ,ftp_manager�ĳ�ʼ��,event_sender�ĳ�ʼ��
                ,watched_thread��ע��
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:�½��ļ�
"""


if __name__ == "__main__":
    import import_paths
    
import bundleframework as bf
import tracelog
import err_code_mgr
import copy

import event_sender

import ftp_mit
import ftp_server_worker
import ftp_server_manage
import FtpServerUserMOC
import FtpServerAcceptorMOC
import FtpServerCtrlLinkMOC
import FtpServerDataLinkMOC
import FtpServerFTPSMOC
import FtpServerMasqueradeAddr
import FtpServerPortMOC

class FtpServerApp(bf.BasicApp):  
    """
    Class: FtpServerApp
    Description: �ṩFTP�����ṩFTP�û������޸ģ��ṩFTP�û��б���
    Base: BasicApp
    Others: ��
    """

    def __init__(self):
        """
        Method: __init__
        Description: ��ʼ��
        Parameter: ��
        Return: ��
        Others: 
            1. self.__mit_manager  ftp_mitʵ����
            2. self.__mit_manager  ftp�������ģ��ʵ����
            3. self.__ftp_thread  ftp�߳�ʵ����
        """

        bf.BasicApp.__init__(self, "FtpServerApp")
        self.__mit_manager = ftp_mit.FtpServerMit()
        self.__ftp_server_manage = None
        self.__ftp_thread = None
    
    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: �ṩFTP�����ṩFTP�û������޸ģ��ṩFTP�û��б���
        Parameter: ��
        Return: return_code:FTP�����Ƿ�ɹ����еķ�����
        Others: ��
        """

        bf.BasicApp._ready_for_work(self)  
        worker = ftp_server_worker.FtpServerWorker()        
        self.register_worker(worker) 
        
        event_sender.set_local_app(self)
        
        self.__ftp_server_manage = ftp_server_manage.FtpServerManage(self)
        return_code = self.__ftp_server_manage.ftp_server_set()
        if return_code!=0:
            return return_code
        self.__ftp_thread = self.__ftp_server_manage.get_ftpthread()
        self.__ftp_thread.set_app(self)
        self.register_watched_thread(self.__ftp_thread)    
        return 0
            
    def get_mit_manager(self):
        """
        Method: get_mit_manager
        Description: ��ȡmit_manager
        Parameter: ��
        Return: ��
        Others: self.__mit_manager
        """

        return self.__mit_manager
    
    def get_ftp_server_manage(self):
        """
        Method: get_ftp_server_manage
        Description: ��ȡftp_server_manage
        Parameter: ��
        Return: self.__ftp_server_manage
        Others: ��
        """

        return self.__ftp_server_manage
    
    def get_event_sender(self):
        """
        Method: get_event_sender
        Description: ��ȡevent_sender
        Parameter: ��
        Return: self.__event_sender
        Others: ��
        """

        return event_sender
        
FtpServerApp().run()