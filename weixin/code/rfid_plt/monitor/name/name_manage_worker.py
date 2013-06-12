#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-02
Description:提供名字注册，注销，查询和定期清理功能 
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
   Modification:新建文件
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
    Description: 名字服务注册接口，主要提供给配置模块注册对端endpoint使用
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 注册请求处理函数，调用name_mit_manager的相应函数进行处理，然后更新本地缓存，再广播到其他APP。
        Parameter: 
            frame: 注册请求，数据区为AppRegisterRequest
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
    Description: 名字服务注销接口，提供给各个APP注销，以及配置模块注销对端endpoint使用
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 注销请求处理函数，调用name_mit_manager的相应函数进行处理，然后更新本地缓存，再广播到其他APP。
        Parameter: 
            frame: 注销请求消息，数据区为AppUnRegisterRequest
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
    Description: 名字服务查询接口，用于查询注册信息
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 名字服务查询处理函数，调用name_mit_manager的相应函数进行处理，返回给发送者
        Parameter: 
            frame: 名字服务查询请求消息，数据区为 AppQueryRequest
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
    Description: 定时清理离线注册信息
    Base: TimeOutHandler
    Others: 
    """

    def time_out(self):
        """
        Method: time_out
        Description: 定时处理函数，清除离线注册信息
        Parameter: 无
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

        
    # 响应事件: 收到消息
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
        __timeout，超时清除时间
    """

    def __init__(self):
        """
        Method: __init__
        Description: 初始化函数
        Parameter: 无
        Return: 
        Others: 
        """

        bf.CmdWorker.__init__(self, name = "NameManageWorker"
                            , min_task_id = 2001
                            , max_task_id = 4000)
        
        


        self.__name_mit_manager = None    
        self.__name_callacp_server = None

        self.__cluster_master_ip = ""

        # 当前名字服务是否在master上
        self.__is_master = False

        self.__clear_offline_app_handler = None

        self.__mit_mutex = threading.RLock()
        
    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: 注册Handler处理函数
        Parameter: 无
        Return: 
            0,成功
            非0，不成功
        Others: 
        """        
        
        
        self.register_handler(RegisterHandler(), bf.REGISTER_NAME_COMMAND )
        self.register_handler(UnRegisterHandler(), bf.UNREGISTER_NAME_COMMAND)
        self.register_handler(QueryHandler(), bf.QUERY_APP_COMMAND)
        self.register_handler(NotifyRunningPidsHandler(), monitor_cmd_code.CMD_NOTIFI_RUNNING_PIDS)
         
        
        handler = ClearOfflineAppTimeoutHandler()
        

        # 这里不启动定时器，在set_cluster_role中启动
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

        # 清空名字信息，防止后面升级为master后，残留了过时的信息
        # 注: master ip发生变化后，其他节点会重新注册名字服务
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
        Description: 提供从mit中注销名字信息的函数
        Parameter: 
            req: 注销名字请求
        Return: 注销名字的返回信息
        Others: 
        """

        with self.__mit_mutex:
            # 只有master才可以进行名字注销
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
        Description: 提供注册名字到mit的函数，如果已经发现存在旧的注册信息，更新注册信息；否则，生成新的注册信息
        Parameter: 
            req: 注册请求消息
        Return: 注册结果信息
        Others: 
        """

        with self.__mit_mutex:
            # 只有master才可以进行名字注册
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
        
        #先更新本地缓存
        self.get_app().on_process_app_register(query_result.app_infos)            
        self.get_app().broadcast_reg_names(query_result.app_infos)

    def query_all_registered_app(self):
        return self.__name_mit_manager.query_all_registered_app()

        
    def query_registered_app(self, req):
        """
        Method: query_registered_app
        Description: 从mit中查询名字信息
        Parameter: 
            req: 名字查询请求
        Return: 名字查询请求的返回信息
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
        Description: worker退出前的处理函数
        Parameter: 无
        Return: 
        Others: 
        """
        bf.CmdWorker.exit_work(self)
        
        self.close_mit_and_name_srv()

        
        
        