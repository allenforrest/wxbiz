#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-02
Description:�ṩ����ע�ᣬע������ѯ�Ͷ��������� 
Others:      
Key Class&Method List: 
             1. RegisterHandler
             2. UnRegisterHandler
             3. QueryHandler
             4. ClearOfflineAppTimeoutHandler
             5. NameManageWorker
History: 
1. Date:2012-11-02
   Author:ACP2013
   Modification:�½��ļ�
"""

import time
import os.path
import threading

import bundleframework as bf
import tracelog
import err_code_mgr
import pycallacp
from . import name_msg_def
import monitor_cmd_code

from name import name_mit_manager

class RegisterHandler(bf.CmdHandler):
    """
    Class: RegisterHandler
    Description: ���ַ���ע��ӿڣ���Ҫ�ṩ������ģ��ע��Զ�endpointʹ��
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ע����������������name_mit_manager����Ӧ�������д���Ȼ����±��ػ��棬�ٹ㲥������APP��
        Parameter: 
            frame: ע������������ΪAppRegisterRequest
        Return: 
        Others: 
        """

        buf = frame.get_data()
        result = bf.AppRegisterResponse()
        result.init_all_attr()
        app = self.get_worker().get_app()
        try:
            reg_req = bf.AppRegisterRequest.deserialize(buf)            
        except Exception:            
            result.return_code = err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
                                                            , cmd='RegisterApp'
                                                            , param_name='AppRegisterRequest')            
            app.send_ack(frame, (result.serialize(), ))
            return
        
        result = self.get_worker().register_app(reg_req)       
        
        app.send_ack(frame, result.serialize())            
        return

class UnRegisterHandler(bf.CmdHandler):
    """
    Class: UnRegisterHandler
    Description: ���ַ���ע���ӿڣ��ṩ������APPע�����Լ�����ģ��ע���Զ�endpointʹ��
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ע����������������name_mit_manager����Ӧ�������д���Ȼ����±��ػ��棬�ٹ㲥������APP��
        Parameter: 
            frame: ע��������Ϣ��������ΪAppUnRegisterRequest
        Return: 
        Others: 
        """

        buf = frame.get_data()
        result = bf.AppUnRegisterResponse()
        result.init_all_attr()
        app = self.get_worker().get_app()
        try:
            un_reg_req = bf.AppUnRegisterRequest.deserialize(buf)
            tracelog.info("unregist name service:%r" % un_reg_req)
        except Exception:            
            result.return_code = err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
                                                            , cmd='UnRegisterApp'
                                                            , param_name='AppUnRegisterRequest')            
            app.send_ack(frame, result.serialize())
            tracelog.error('%s\n%s'%(result.description, buf))
            return
            
        result = self.get_worker().unregister_app(un_reg_req)        

        if un_reg_req.need_reponse is True:
            app.send_ack(frame, result.serialize())
        
        return

class QueryHandler(bf.CmdHandler):
    """
    Class: QueryHandler
    Description: ���ַ����ѯ�ӿڣ����ڲ�ѯע����Ϣ
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ���ַ����ѯ������������name_mit_manager����Ӧ�������д������ظ�������
        Parameter: 
            frame: ���ַ����ѯ������Ϣ��������Ϊ AppQueryRequest
        Return: 
        Others: 
        """

        buf = frame.get_data()
        result = bf.AppQueryResponse()
        result.init_all_attr()
        app = self.get_worker().get_app()
        try:
            req = bf.AppQueryRequest.deserialize(buf)            
        except Exception:            
            result.return_code = err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
                                                            , cmd='QueryApp'
                                                            , param_name='AppQueryRequest')            
            app.send_ack(frame, result.serialize())
            return        
        result = self.get_worker().query_registered_app(req)
        app.send_ack(frame, result.serialize())
        return
        
class ClearOfflineAppTimeoutHandler(bf.TimeOutHandler):
    """
    Class: ClearOfflineAppTimeoutHandler
    Description: ��ʱ��������ע����Ϣ
    Base: TimeOutHandler
    Others: 
    """

    def time_out(self):
        """
        Method: time_out
        Description: ��ʱ���������������ע����Ϣ
        Parameter: ��
        Return: 
        Others: 
        """
        worker = self.get_worker().clear_offline_app()




class NotifyRunningPidsHandler(bf.CmdHandler):
    def handle_cmd(self, frame):

        try:
            req = name_msg_def.NotifyRunningPidsMsg.deserialize(frame.get_data())
        except:
            tracelog.exception("NotifyRunningPidsMsg deserialize failed")
            return

        monitor_pid = frame.get_sender_pid()
        running_pids = req.running_pids
        self.get_worker().on_notify_running_pids(monitor_pid, running_pids)
                
        
class NameEventHandler(pycallacp.AcpEventHandler):
    def __init__(self, name_server):
        pycallacp.AcpEventHandler.__init__(self)
        
        self.__name_server = name_server

        
    # ��Ӧ�¼�: �յ���Ϣ
    def on_msg_received(self, url_or_srv_name, msg):
        #print "on_msg_received:", msg.get_cmd_code(), url_or_srv_name, msg.get_data(), msg.get_msg_id()

        cmd_code = msg.get_cmd_code()
        
        if cmd_code == bf.CMD_QUERY_CLUSTER_MASTER_IP:            
            rep = bf.QueryClusterMasterIpResponse()
            rep.ip = self.__name_server.get_cluster_master_ip()
        elif cmd_code == bf.REGISTER_NAME_COMMAND:
            try:
                req = bf.AppRegisterRequest.deserialize(msg.get_data())
            except:
                tracelog.exception("AppRegisterRequest deserialize failed.")
                return

            rep = self.__name_server.register_app(req)

            if rep.return_code == 0:
                tracelog.info("app regist name service: %r, pid:%r" % (req, rep.app_info.pid))
            else:
                tracelog.error("app regist name service failed: %r" % req)

        ack_msg = pycallacp.AcpMessage(pycallacp.CMD_ACK_MSG, rep.serialize())
        ack_msg.set_msg_id(msg.get_msg_id())
        self._callacp_inst.send(url_or_srv_name, ack_msg)

  
class NameManageWorker(bf.CmdWorker):    
    """
    Class: NameManageWorker
    Description: 
    Base: 
    Others: 
        __timeout����ʱ���ʱ��
    """

    def __init__(self):
        """
        Method: __init__
        Description: ��ʼ������
        Parameter: ��
        Return: 
        Others: 
        """

        bf.CmdWorker.__init__(self, name = "NameManageWorker"
                            , min_task_id = 2001
                            , max_task_id = 4000)
        
        


        self.__name_mit_manager = None    
        self.__name_callacp_server = None

        self.__cluster_master_ip = ""

        # ��ǰ���ַ����Ƿ���master��
        self.__is_master = False

        self.__clear_offline_app_handler = None

        self.__mit_mutex = threading.RLock()
        
    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: ע��Handler������
        Parameter: ��
        Return: 
            0,�ɹ�
            ��0�����ɹ�
        Others: 
        """        
        
        
        self.register_handler(RegisterHandler(), bf.REGISTER_NAME_COMMAND )
        self.register_handler(UnRegisterHandler(), bf.UNREGISTER_NAME_COMMAND)
        self.register_handler(QueryHandler(), bf.QUERY_APP_COMMAND)
        self.register_handler(NotifyRunningPidsHandler(), monitor_cmd_code.CMD_NOTIFI_RUNNING_PIDS)
         
        
        handler = ClearOfflineAppTimeoutHandler()
        

        # ���ﲻ������ʱ������set_cluster_role������
        if self.__is_master:
            period = 30 * 60
            handler.start_timer(period, False)
        
        self.register_time_out_handler(handler)
        self.__clear_offline_app_handler = handler
        
        return 0


    def init_mit_and_name_srv(self):
        db_file = os.path.join(self.get_app().get_app_top_path()
                                , "data"
                                , "sqlite"
                                , "nameservice.db")
        self.__name_mit_manager = name_mit_manager.NameMitManager(db_file)

        self.__name_callacp_server = pycallacp.CallAcpServer()
        self.__name_callacp_server.set_event_handler(NameEventHandler(self))

        ip = self.get_app().get_my_name_ip()
        ret = self.__name_callacp_server.bind(ip, bf.NAME_SERVER_PORT)
        if ret != 0:
            tracelog.error("name service bind on (%s, %d) failed. ret:%d" % (ip, bf.NAME_SERVER_PORT, ret))
            
        return ret

    def set_cluster_role(self, is_master):
        self.__is_master = is_master

        if self.__clear_offline_app_handler is not None:
            if is_master:
                period = 30 * 60
                self.__clear_offline_app_handler.start_timer(period, False)
            else:
                self.__clear_offline_app_handler.stop_timer()

        # ���������Ϣ����ֹ��������Ϊmaster�󣬲����˹�ʱ����Ϣ
        # ע: master ip�����仯�������ڵ������ע�����ַ���
        if is_master is False and self.__name_mit_manager is not None:
            self.__name_mit_manager.clear_all_name()

        
    def set_cluster_master_ip(self, ip):
        self.__cluster_master_ip = ip
    
    def get_cluster_master_ip(self):
        return self.__cluster_master_ip
    
        
    def close_mit_and_name_srv(self):
        if self.__name_callacp_server is not None:
            self.__name_callacp_server.clear()

        if self.__name_mit_manager is not None:
            self.__name_mit_manager.close()
            self.__name_mit_manager = None
            
    def unregister_app(self, req):
        """
        Method: unregister_app
        Description: �ṩ��mit��ע��������Ϣ�ĺ���
        Parameter: 
            req: ע����������
        Return: ע�����ֵķ�����Ϣ
        Others: 
        """

        with self.__mit_mutex:
            # ֻ��master�ſ��Խ�������ע��
            if not self.__is_master:
                result = bf.AppUnRegisterResponse()
                result.init_all_attr()
                result.return_code = err_code_mgr.ER_NAME_SERVER_IS_NOT_MASTER
                result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NAME_SERVER_IS_NOT_MASTER
                                                                        , ip=self.__cluster_master_ip)    
                return result
                
            result = self.__name_mit_manager.unregister_app(req)
            if result.return_code==0:      
                self.broadcast_reg_names()    

            return result
        
    def register_app(self, req):
        """
        Method: register_app
        Description: �ṩע�����ֵ�mit�ĺ���������Ѿ����ִ��ھɵ�ע����Ϣ������ע����Ϣ�����������µ�ע����Ϣ
        Parameter: 
            req: ע��������Ϣ
        Return: ע������Ϣ
        Others: 
        """

        with self.__mit_mutex:
            # ֻ��master�ſ��Խ�������ע��
            if not self.__is_master:
                result = bf.AppUnRegisterResponse()
                result.init_all_attr()
                result.return_code = err_code_mgr.ER_NAME_SERVER_IS_NOT_MASTER
                result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_NAME_SERVER_IS_NOT_MASTER
                                                                        , ip=self.__cluster_master_ip)    
                return result
                
            result =  self.__name_mit_manager.register_app(req)

            if result.return_code==0:
                self.broadcast_reg_names() 
                
            return result
        
    def broadcast_reg_names(self):
        query_result = self.query_all_registered_app()
        
        #�ȸ��±��ػ���
        self.get_app().on_process_app_register(query_result.app_infos)            
        self.get_app().broadcast_reg_names(query_result.app_infos)

    def query_all_registered_app(self):
        return self.__name_mit_manager.query_all_registered_app()

        
    def query_registered_app(self, req):
        """
        Method: query_registered_app
        Description: ��mit�в�ѯ������Ϣ
        Parameter: 
            req: ���ֲ�ѯ����
        Return: ���ֲ�ѯ����ķ�����Ϣ
        Others: 
        """
        with self.__mit_mutex:
            return self.__name_mit_manager.query_registered_app(req)


    def clear_offline_app(self):
        with self.__mit_mutex:
            return self.__name_mit_manager.clear_offline_app()

    def on_notify_running_pids(self, monitor_pid, running_pids):
        with self.__mit_mutex:
            unregist_someone = self.__name_mit_manager.on_notify_running_pids(monitor_pid, running_pids)
            if unregist_someone:
                self.broadcast_reg_names()
            
    def exit_work(self):
        """
        Method:    exit_work
        Description: worker�˳�ǰ�Ĵ�����
        Parameter: ��
        Return: 
        Others: 
        """
        bf.CmdWorker.exit_work(self)
        
        self.close_mit_and_name_srv()

        
        
        