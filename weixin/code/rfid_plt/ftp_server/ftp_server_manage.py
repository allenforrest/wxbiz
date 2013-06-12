#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: FTP服务管理
Others:无
Key Class&Method List: 
             1. FtpServerManage: FTP服务管理,初始化FtpServerTimerThread
             2. DummyMD5Authorizer: 重载pyftpdlib中Authorizer类
             3. EventFTPHandler: 重载pyftpdlib中FTPHandler
             4. EventTLSFTPHandler: 重载pyftpdlib中TLSFTPHandler
             5. FtpServerTimerThread: FTP服务线程
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:新建文件
"""


import os
import threading
from hashlib import md5

import bundleframework as bf
import tracelog
import err_code_mgr

import ftpserver
import ftps_handlers

class FtpServerManage():
    """
    Class: FtpServerManage
    Description: FTP服务管理,初始化FtpServerTimerThread
    Base: 无
    Others: 无
    """

    def __init__(self,app):
        """
        Method: __init__
        Description: 初始化
        Parameter: 
            app: ftp_server_app对象
        Return: 无
        Others: 1. ftp_server_set 设置ftpServer参数
        """

        self.__app = app
        self.__ftpserver = ftpserver
        self.__ftphandler =None
        self.__ftp_server_thread = FtpServerTimerThread()
        self.__ftpserver.log = self.standard_logger
        self.__ftpserver.logline = self.line_logger
        self.__ftpserver.logerror = self.err_logger
        
    def ftp_server_set(self):
        """
        Method: ftp_server_set
        Description: 设置ftp参数
        Parameter: 无
        Return: errcode: 设置FTP服务是否成功代码
        Others: 无
        """

        errcode = err_code_mgr.ER_SUCCESS
        
        #读取DB判断是否需要FTPS
        rdm = self.__app.get_mit_manager().rdm_lookup("FtpServerFTPSMOC")
        if rdm is None:
            errcode = err_code_mgr.ER_FTPSERVER_SET_WRONG
            tracelog.error('FTPS Set not exists')
            return errcode
        if rdm.tls_control_required ==1 or rdm.tls_data_required ==1:
            EventTLSFTPHandler.ftp_server_app = self.__app
            self.__ftphandler = EventTLSFTPHandler
            self.__ftphandler.certfile = os.path.join(self.__app.get_app_top_path(),rdm.certfile)
            self.__ftphandler.keyfile = os.path.join(self.__app.get_app_top_path(),rdm.keyfile)
            self.__ftphandler.tls_control_required = True
            self.__ftphandler.tls_data_required = True
        else:
            EventFTPHandler.ftp_server_app = self.__app
            self.__ftphandler = EventFTPHandler

        #添加用户
        self.__ftphandler.authorizer = DummyMD5Authorizer()
        records = self.__app.get_mit_manager().rdm_find("FtpServerUserMOC")
        if len(records)>0:
            try:
                for record in records:
                    print record.username, record.password, record.homedir 
                    home = os.path.join(self.__app.get_app_top_path(),record.homedir )
                    self.__ftphandler.authorizer.add_user(record.username 
                                                          , record.password, home, record.perm)
            except Exception, err:
                errcode = err_code_mgr.ER_FTPSERVER_SET_WRONG
                tracelog.exception('Can not add user: %s'%  err)
                return errcode
        else:
            errcode = err_code_mgr.ER_FTPSERVER_SET_WRONG
            tracelog.error('ftp user not exists')
            return errcode  
        
        #设置控制链路
        rdm = self.__app.get_mit_manager().rdm_lookup("FtpServerCtrlLinkMOC")
        if rdm is None:
            errcode = err_code_mgr.ER_FTPSERVER_SET_WRONG
            tracelog.error('ftp ControlConnection Set not exists')
            return errcode
        self.__ftphandler.timeout = rdm.timeout
        self.__ftphandler.banner = rdm.banner
        self.__ftphandler.max_login_attempts = rdm.max_login_attempts
        if rdm.permit_foreign_addresses==0:
            self.__ftphandler.permit_foreign_addresses = False
        else:
            self.__ftphandler.permit_foreign_addresses = True
        if rdm.permit_privileged_ports==0:
            self.__ftphandler.permit_privileged_ports = False
        else:
            self.__ftphandler.permit_privileged_ports = True
        self.__ftphandler.passive_ports = range(rdm.passive_ports_min, rdm.passive_ports_max)
        if rdm.use_gmt_times==0:
            self.__ftphandler.use_gmt_times = False
        else:
            self.__ftphandler.use_gmt_times = True
        if rdm.tcp_no_delay==0:
            self.__ftphandler.tcp_no_delay = False
        else:
            self.__ftphandler.tcp_no_delay = True
        if rdm.use_sendfile==0:
            self.__ftphandler.use_sendfile = False
        else:
            self.__ftphandler.use_sendfile = True
        
        #设置数据链路    
        rdm = self.__app.get_mit_manager().rdm_lookup("FtpServerDataLinkMOC") 
        if rdm is None:
            errcode = err_code_mgr.ER_FTPSERVER_SET_WRONG
            tracelog.error('ftp DataConnection Set not exists')
            return errcode
        self.__ftpserver.DTPHandler.timeout = rdm.timeout
        self.__ftpserver.DTPHandler.ac_in_buffer_size = rdm.ac_in_buffer_size
        self.__ftpserver.DTPHandler.ac_out_buffer_size = rdm.ac_out_buffer_size
        self.__ftpserver.DTPHandler.read_limit = rdm.read_limit
        self.__ftpserver.DTPHandler.write_limit = rdm.write_limit
        
        #设置服务器
        rdm = self.__app.get_mit_manager().rdm_lookup("FtpServerAcceptorMOC")
        if rdm is None:
            errcode = err_code_mgr.ER_FTPSERVER_SET_WRONG
            tracelog.error('ftp Serveracceptor set not exists')
            return errcode
        self.__ftpserver.max_cons = rdm.max_cons
        self.__ftpserver.max_cons_per_ip = rdm.max_cons_per_ip
    
        #设置MasqueradeAddress
        records = self.__app.get_mit_manager().rdm_find("FtpServerMasqueradeAddr")
        if len(records)>0:
            for record in records:
                self.__ftphandler.masquerade_address_map[record.private_ip] = record.public_ip
                
        #获取监听地址以及控制链路端口
        rdm = self.__app.get_mit_manager().rdm_lookup("FtpServerPortMOC")
        if rdm is None:
            errcode = err_code_mgr.ER_FTPSERVER_SET_WRONG
            tracelog.error('ftp con port set not exists')
            return errcode
        ftp_port = rdm.ftp_port
        ip_listen = rdm.ip_listen
        
        try:
            self.__ftpserver.FTPServer((ip_listen, ftp_port), self.__ftphandler)
            self.__ftp_server_thread.set_ftp_server(self.__ftpserver)
        except Exception, err:
            errcode = err_code_mgr.ER_FTPSERVER_SET_WRONG
            tracelog.exception('Fail to Set Ftp Server and error is %s' % err)
            return errcode
        
        return errcode
        
    def get_ftpthread(self):
        """
        Method: get_ftpthread
        Description: 获取ftp服务线程
        Parameter: 无
        Return: self.__ftp_server_thread
        Others: 无
        """

        return self.__ftp_server_thread
    
    def get_authorizer(self):
        """
        Method: get_authorizer
        Description: 获取ftp用户信息
        Parameter: 无
        Return: self.__ftphandler.authorizer
        Others: 无
        """

        return self.__ftphandler.authorizer
    
    def standard_logger(self,msg):
        """
        Method: standard_logger
        Description: 重载基础日志方法
        Parameter: 
            msg: ftp服务基础信息
        Return: 无
        Others: 无
        """

        tracelog.info(msg)

    def line_logger(self,msg):
        """
        Method: line_logger
        Description: 重载ftp服务命令通道日志记录方法
        Parameter: 
            msg: ftp服务命令通道信息
        Return: 无
        Others: 无
        """

        tracelog.info(msg)
        
    def err_logger(self,msg):
        """
        Method: err_logger
        Description: 重载ftp服务错误日志记录方法
        Parameter: 
            msg: ftp服务错误信息
        Return: 无
        Others: 无
        """

        tracelog.error(msg)
               
class DummyMD5Authorizer(ftpserver.DummyAuthorizer):
    """
    Class: DummyMD5Authorizer
    Description: 重载ftpserver中DummyAuthorizer类
    Base: DummyAuthorizer
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

        self.user_table = {}
        ftpserver.DummyAuthorizer.__init__(self)
        self.__lock = threading.Lock()
    
    def validate_authentication(self, username, password):
        """
        Method: validate_authentication
        Description: 验证用户是否合法
        Parameter: 
            username: 用户名
            password: 密码
        Return: 布尔值，代表是否验证成功
        Others: 无
        """

        with self.__lock:
            if not self.has_user(username):
                return False
            hash = md5(password).hexdigest()
            return self.user_table[username]['pwd'] == hash
    
    def change_password(self,username,newpassword):
        """
        Method: change_password
        Description: 修改ftp用户密码
        Parameter: 
            username: 用户名
            newpassword: 新密码
        Return: 无
        Others: 无
        """

        with self.__lock:
            self.user_table[username]['pwd'] = md5(newpassword).hexdigest()
            
class EventFTPHandler(ftpserver.FTPHandler):
    """
    Class: EventFTPHandler
    Description: 重载ftpserver中FTPHandler类
    Base: FTPHandler
    Others: 无
    """

    ftp_server_app = None
    def on_login(self, username):
        """
        Method: on_login
        Description: 用户登录成功进行eventmanage上报
        Parameter: 
            username: 登入用户名
        Return: 无
        Others: 无
        """

        event_data = EventFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.0')        
        event_data.set_object_id(username)
        event_data.set_device_id(EventFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'user_name':username}
        event_data.set_params(params)
        EventFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)
        
    def on_login_failed(self,username, password):
        """
        Method: on_login_failed
        Description: 用户登录失败进行eventmanage上报
        Parameter: 
            username: 输入的用户名
            password: 输入的密码
        Return: 无
        Others: 无
        """

        event_data = EventFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.1')        
        event_data.set_object_id(username)
        event_data.set_device_id(EventFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'user_name':username}
        event_data.set_params(params)
        EventFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)

    def on_logout(self, username):
        """
        Method: on_logout
        Description: 用户退出FTP服务进行eventmanage上报
        Parameter: 
            username: 退出的用户的用户名
        Return: 无
        Others: 无
        """

        event_data = EventFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.2')        
        event_data.set_object_id(username)
        event_data.set_device_id(EventFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'user_name':username}
        event_data.set_params(params)
        EventFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)
        
    def on_file_sent(self, file):
        """
        Method: on_file_sent
        Description: 文件传输成功进行eventmanage上报
        Parameter: 
            file: 传输成功的文件名
        Return: 无
        Others: 无
        """

        event_data = EventFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.3')        
        event_data.set_object_id(file)
        event_data.set_device_id(EventFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'file_name':file}
        event_data.set_params(params)
        EventFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)

    def on_file_received(self, file):
        """
        Method: on_file_received
        Description: 文件接受成功进行eventmanage上报
        Parameter: 
            file: 传输成功的文件名
        Return: 无
        Others: 无
        """

        event_data = EventFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.4')        
        event_data.set_object_id(file)
        event_data.set_device_id(EventFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'file_name':file}
        event_data.set_params(params)
        EventFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)
            
    def on_incomplete_file_sent(self, file):
        """
        Method: on_incomplete_file_sent
        Description: 文件传输未完成进行eventmanage上报
        Parameter: 
            file: 传输未完成的文件名
        Return: 无
        Others: 无
        """

        event_data = EventFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.5')        
        event_data.set_object_id(file)
        event_data.set_device_id(EventFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'file_name':file}
        event_data.set_params(params)
        EventFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)

    def on_incomplete_file_received(self, file):
        """
        Method: on_incomplete_file_received
        Description: 文件接受未完成进行eventmanage上报
        Parameter: 
            file: 接受未完成的文件名
        Return: 无
        Others: 无
        """

        event_data = EventFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.6')        
        event_data.set_object_id(file)
        event_data.set_device_id(EventFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'file_name':file}
        event_data.set_params(params)
        EventFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)

class EventTLSFTPHandler(ftps_handlers.TLS_FTPHandler):
    """
    Class: EventTLSFTPHandler
    Description: 重载ftps_handlers中TLS_FTPHandler类
    Base: TLS_FTPHandler
    Others: 无
    """

    ftp_server_app = None
    def on_login(self, username):
        """
        Method: on_login
        Description: 用户登录成功进行eventmanage上报
        Parameter: 
            username: 登入用户名
        Return: 无
        Others: 无
        """

        event_data = EventTLSFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.0')        
        event_data.set_object_id(username)
        event_data.set_device_id(EventTLSFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'user_name':username}
        event_data.set_params(params)
        EventTLSFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)
        
    def on_login_failed(self,username, password):
        """
        Method: on_login_failed
        Description: 用户登录失败进行eventmanage上报
        Parameter: 
            username: 输入的用户名
            password: 输入的密码
        Return: 无
        Others: 无
        """

        event_data = EventTLSFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.1')        
        event_data.set_object_id(username)
        event_data.set_device_id(EventTLSFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'user_name':username}
        event_data.set_params(params)
        EventTLSFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)

    def on_logout(self, username):
        """
        Method: on_logout
        Description: 用户退出FTP服务进行eventmanage上报
        Parameter: 
            username: 退出的用户名
        Return: 无
        Others: 无
        """

        event_data = EventTLSFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.2')        
        event_data.set_object_id(username)
        event_data.set_device_id(EventTLSFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'user_name':username}
        event_data.set_params(params)
        EventTLSFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)
        
    def on_file_sent(self, file):
        """
        Method: on_file_sent
        Description: 文件发送成功进行eventmanage上报
        Parameter: 
            file: 发送成功的文件名
        Return: 无
        Others: 无
        """

        event_data = EventTLSFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.3')        
        event_data.set_object_id(file)
        event_data.set_device_id(EventTLSFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'file_name':file}
        event_data.set_params(params)
        EventTLSFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)

    def on_file_received(self, file):
        """
        Method: on_file_received
        Description: 文件接收成功进行eventmanage上报
        Parameter: 
            file: 接收成功的文件名
        Return: 无
        Others: 无
        """

        event_data = EventTLSFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.4')        
        event_data.set_object_id(file)
        event_data.set_device_id(EventTLSFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'file_name':file}
        event_data.set_params(params)
        EventTLSFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)
            
    def on_incomplete_file_sent(self, file):
        """
        Method: on_incomplete_file_sent
        Description: 文件发送未完成进行eventmanage上报
        Parameter: 
            file: 发送未完成的文件名
        Return: 无
        Others: 无
        """

        event_data = EventTLSFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.5')        
        event_data.set_object_id(file)
        event_data.set_device_id(EventTLSFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'file_name':file}
        event_data.set_params(params)
        EventTLSFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)

    def on_incomplete_file_received(self, file):
        """
        Method: on_incomplete_file_received
        Description: 文件接受未完成进行eventmanage上报
        Parameter: 
            file: 接受未完成的文件名
        Return: 无
        Others: 无
        """

        event_data = EventTLSFTPHandler.ftp_server_app.get_event_sender().EventData()
        event_data.set_event_id('event.FtpServerApp.6')        
        event_data.set_object_id(file)
        event_data.set_device_id(EventTLSFTPHandler.ftp_server_app.get_device_id())
        event_data.set_event_flag('event')
        params = {'file_name':file}
        event_data.set_params(params)
        EventTLSFTPHandler.ftp_server_app.get_event_sender().send_event(event_data)

class FtpServerTimerThread(bf.WatchedThread):
    """
    Class: FtpServerTimerThread
    Description: FTP服务线程
    Base: WatchedThread
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

        bf.WatchedThread.__init__(self)
        self.__app = None
        self.__ftpserver = None
        
    def set_ftp_server(self,ftp_server):
        """
        Method: set_ftp_server
        Description: 设置ftp_server
        Parameter: 
            ftp_server: ftp_manager中设置好的ftp_server
        Return: 无
        Others: 无
        """

        self.__ftpserver = ftp_server
        
    def set_app(self, app):
        """
        Method: set_app
        Description: 设置app
        Parameter: 
            app: 线程所属的app
        Return: 无
        Others: 无
        """

        self.__app = app
        
    def run(self):
        """
        Method: run
        Description: ftp线程运行
        Parameter: 无
        Return: 无
        Others: 无
        """

        while True:
            self.__ftpserver.FTPServer.serve_forever(count=1)
            
            if self.feed_dog():
                    break
                
        self.over()
