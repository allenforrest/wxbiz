#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: FTP Server 该APP负责提供FTP服务，提供FTP用户密码修改，提供FTP用户列表返回
Others: 无 
Key Class&Method List: 
             1. FtpServerApp: APP类，负责worker的注册,mit的注册
                ,ftp_manager的初始化,event_sender的初始化
                ,watched_thread的注册
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:新建文件
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
    Description: 提供FTP服务，提供FTP用户密码修改，提供FTP用户列表返回
    Base: BasicApp
    Others: 无
    """

    def __init__(self):
        """
        Method: __init__
        Description: 初始化
        Parameter: 无
        Return: 无
        Others: 
            1. self.__mit_manager  ftp_mit实例化
            2. self.__mit_manager  ftp服务管理模块实例化
            3. self.__ftp_thread  ftp线程实例化
        """

        bf.BasicApp.__init__(self, "FtpServerApp")
        self.__mit_manager = ftp_mit.FtpServerMit()
        self.__ftp_server_manage = None
        self.__ftp_thread = None
    
    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: 提供FTP服务，提供FTP用户密码修改，提供FTP用户列表返回
        Parameter: 无
        Return: return_code:FTP服务是否成功运行的返回码
        Others: 无
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
        Description: 获取mit_manager
        Parameter: 无
        Return: 无
        Others: self.__mit_manager
        """

        return self.__mit_manager
    
    def get_ftp_server_manage(self):
        """
        Method: get_ftp_server_manage
        Description: 获取ftp_server_manage
        Parameter: 无
        Return: self.__ftp_server_manage
        Others: 无
        """

        return self.__ftp_server_manage
    
    def get_event_sender(self):
        """
        Method: get_event_sender
        Description: 获取event_sender
        Parameter: 无
        Return: self.__event_sender
        Others: 无
        """

        return event_sender
        
FtpServerApp().run()