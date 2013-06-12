#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-01-08
Description: FTP�������
Others:��
Key Class&Method List: 
             1. FtpServerManage: FTP�������,��ʼ��FtpServerTimerThread
             2. DummyMD5Authorizer: ����pyftpdlib��Authorizer��
             3. EventFTPHandler: ����pyftpdlib��FTPHandler
             4. EventTLSFTPHandler: ����pyftpdlib��TLSFTPHandler
             5. FtpServerTimerThread: FTP�����߳�
History: 
1. Date:2013-01-08
   Author:ACP2013
   Modification:�½��ļ�
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
    Description: FTP�������,��ʼ��FtpServerTimerThread
    Base: ��
    Others: ��
    """

    def __init__(self,app):
        """
        Method: __init__
        Description: ��ʼ��
        Parameter: 
            app: ftp_server_app����
        Return: ��
        Others: 1. ftp_server_set ����ftpServer����
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
        Description: ����ftp����
        Parameter: ��
        Return: errcode: ����FTP�����Ƿ�ɹ�����
        Others: ��
        """

        errcode = err_code_mgr.ER_SUCCESS
        
        #��ȡDB�ж��Ƿ���ҪFTPS
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

        #����û�
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
        
        #���ÿ�����·
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
        
        #����������·    
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
        
        #���÷�����
        rdm = self.__app.get_mit_manager().rdm_lookup("FtpServerAcceptorMOC")
        if rdm is None:
            errcode = err_code_mgr.ER_FTPSERVER_SET_WRONG
            tracelog.error('ftp Serveracceptor set not exists')
            return errcode
        self.__ftpserver.max_cons = rdm.max_cons
        self.__ftpserver.max_cons_per_ip = rdm.max_cons_per_ip
    
        #����MasqueradeAddress
        records = self.__app.get_mit_manager().rdm_find("FtpServerMasqueradeAddr")
        if len(records)>0:
            for record in records:
                self.__ftphandler.masquerade_address_map[record.private_ip] = record.public_ip
                
        #��ȡ������ַ�Լ�������·�˿�
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
        Description: ��ȡftp�����߳�
        Parameter: ��
        Return: self.__ftp_server_thread
        Others: ��
        """

        return self.__ftp_server_thread
    
    def get_authorizer(self):
        """
        Method: get_authorizer
        Description: ��ȡftp�û���Ϣ
        Parameter: ��
        Return: self.__ftphandler.authorizer
        Others: ��
        """

        return self.__ftphandler.authorizer
    
    def standard_logger(self,msg):
        """
        Method: standard_logger
        Description: ���ػ�����־����
        Parameter: 
            msg: ftp���������Ϣ
        Return: ��
        Others: ��
        """

        tracelog.info(msg)

    def line_logger(self,msg):
        """
        Method: line_logger
        Description: ����ftp��������ͨ����־��¼����
        Parameter: 
            msg: ftp��������ͨ����Ϣ
        Return: ��
        Others: ��
        """

        tracelog.info(msg)
        
    def err_logger(self,msg):
        """
        Method: err_logger
        Description: ����ftp���������־��¼����
        Parameter: 
            msg: ftp���������Ϣ
        Return: ��
        Others: ��
        """

        tracelog.error(msg)
               
class DummyMD5Authorizer(ftpserver.DummyAuthorizer):
    """
    Class: DummyMD5Authorizer
    Description: ����ftpserver��DummyAuthorizer��
    Base: DummyAuthorizer
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

        self.user_table = {}
        ftpserver.DummyAuthorizer.__init__(self)
        self.__lock = threading.Lock()
    
    def validate_authentication(self, username, password):
        """
        Method: validate_authentication
        Description: ��֤�û��Ƿ�Ϸ�
        Parameter: 
            username: �û���
            password: ����
        Return: ����ֵ�������Ƿ���֤�ɹ�
        Others: ��
        """

        with self.__lock:
            if not self.has_user(username):
                return False
            hash = md5(password).hexdigest()
            return self.user_table[username]['pwd'] == hash
    
    def change_password(self,username,newpassword):
        """
        Method: change_password
        Description: �޸�ftp�û�����
        Parameter: 
            username: �û���
            newpassword: ������
        Return: ��
        Others: ��
        """

        with self.__lock:
            self.user_table[username]['pwd'] = md5(newpassword).hexdigest()
            
class EventFTPHandler(ftpserver.FTPHandler):
    """
    Class: EventFTPHandler
    Description: ����ftpserver��FTPHandler��
    Base: FTPHandler
    Others: ��
    """

    ftp_server_app = None
    def on_login(self, username):
        """
        Method: on_login
        Description: �û���¼�ɹ�����eventmanage�ϱ�
        Parameter: 
            username: �����û���
        Return: ��
        Others: ��
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
        Description: �û���¼ʧ�ܽ���eventmanage�ϱ�
        Parameter: 
            username: ������û���
            password: ���������
        Return: ��
        Others: ��
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
        Description: �û��˳�FTP�������eventmanage�ϱ�
        Parameter: 
            username: �˳����û����û���
        Return: ��
        Others: ��
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
        Description: �ļ�����ɹ�����eventmanage�ϱ�
        Parameter: 
            file: ����ɹ����ļ���
        Return: ��
        Others: ��
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
        Description: �ļ����ܳɹ�����eventmanage�ϱ�
        Parameter: 
            file: ����ɹ����ļ���
        Return: ��
        Others: ��
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
        Description: �ļ�����δ��ɽ���eventmanage�ϱ�
        Parameter: 
            file: ����δ��ɵ��ļ���
        Return: ��
        Others: ��
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
        Description: �ļ�����δ��ɽ���eventmanage�ϱ�
        Parameter: 
            file: ����δ��ɵ��ļ���
        Return: ��
        Others: ��
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
    Description: ����ftps_handlers��TLS_FTPHandler��
    Base: TLS_FTPHandler
    Others: ��
    """

    ftp_server_app = None
    def on_login(self, username):
        """
        Method: on_login
        Description: �û���¼�ɹ�����eventmanage�ϱ�
        Parameter: 
            username: �����û���
        Return: ��
        Others: ��
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
        Description: �û���¼ʧ�ܽ���eventmanage�ϱ�
        Parameter: 
            username: ������û���
            password: ���������
        Return: ��
        Others: ��
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
        Description: �û��˳�FTP�������eventmanage�ϱ�
        Parameter: 
            username: �˳����û���
        Return: ��
        Others: ��
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
        Description: �ļ����ͳɹ�����eventmanage�ϱ�
        Parameter: 
            file: ���ͳɹ����ļ���
        Return: ��
        Others: ��
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
        Description: �ļ����ճɹ�����eventmanage�ϱ�
        Parameter: 
            file: ���ճɹ����ļ���
        Return: ��
        Others: ��
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
        Description: �ļ�����δ��ɽ���eventmanage�ϱ�
        Parameter: 
            file: ����δ��ɵ��ļ���
        Return: ��
        Others: ��
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
        Description: �ļ�����δ��ɽ���eventmanage�ϱ�
        Parameter: 
            file: ����δ��ɵ��ļ���
        Return: ��
        Others: ��
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
    Description: FTP�����߳�
    Base: WatchedThread
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

        bf.WatchedThread.__init__(self)
        self.__app = None
        self.__ftpserver = None
        
    def set_ftp_server(self,ftp_server):
        """
        Method: set_ftp_server
        Description: ����ftp_server
        Parameter: 
            ftp_server: ftp_manager�����úõ�ftp_server
        Return: ��
        Others: ��
        """

        self.__ftpserver = ftp_server
        
    def set_app(self, app):
        """
        Method: set_app
        Description: ����app
        Parameter: 
            app: �߳�������app
        Return: ��
        Others: ��
        """

        self.__app = app
        
    def run(self):
        """
        Method: run
        Description: ftp�߳�����
        Parameter: ��
        Return: ��
        Others: ��
        """

        while True:
            self.__ftpserver.FTPServer.serve_forever(count=1)
            
            if self.feed_dog():
                    break
                
        self.over()
