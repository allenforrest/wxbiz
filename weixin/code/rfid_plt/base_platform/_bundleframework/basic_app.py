#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-07
Description: app基类，提供了相关的app运行的机制
Others:      
Key Class&Method List: 
             1. BasicApp: app基类，提供了相关的app运行的机制
             
History: 
1. Date:
   Author:
   Modification:
"""


from __future__ import with_statement

import struct
from threading import Event
from threading import RLock

import time, os, sys, copy
import os.path
import random
import socket

import getopt

import tracelog
import err_code_mgr
import pycallacp
import device_cfg_info
import language_cfg

from _bundleframework.dispatch.work_thread import WorkThread
from _bundleframework.dispatch.work_thread import CommunicationThread
from _bundleframework.dispatch.work_thread import WatchedThread

from _bundleframework.protocol.appframe import AppFrame

from _bundleframework.dispatch.ipc_worker      import IpcSendWorker
from _bundleframework.dispatch.ipc_worker      import IpcRecvWorker

from _bundleframework.rpc import rpc_worker
from _bundleframework import local_cmd_code


from _bundleframework.common_cmd.common_cmd_worker import CommonCmdWorker

from _bundleframework.name import msg_def as name_msg_def

from _bundleframework import local_const_def

import utility


class SimpleCallAcpSrv(pycallacp.CallAcpServer, pycallacp.AcpEventHandler):
    """
    Class: SimpleCallAcpSrv
    Description: 简单的callacp服务端
    Base: pycallacp.CallAcpServer, pycallacp.AcpEventHandler
    Others: 
    """
    def __init__(self, app, port, ssl_option = None):
        """
        Method: __init__
        Description: 构造函数
        Parameter: 
            app: BasicApp子类的对象 
            port:监听的端口
            ssl_option:SSL选项
            
        Return:
        Others: 
        """

        pycallacp.CallAcpServer.__init__(self)
        pycallacp.AcpEventHandler.__init__(self)

        self.set_event_handler(self)
        
        self._app = app
        self._port = port
        self._ssl_option = ssl_option

        if ssl_option is not None:
            assert("cert_file" in ssl_option)
            assert("proto_version" in ssl_option)

        self._struct = struct.Struct("Q")

    def start_listen(self):
        """
        Method: start_listen
        Description: 开始监听
        Parameter: 无
        Return:错误码
        Others: 
        """

        if self._ssl_option is None:
            ret = self.bind("", self._port)
        else:
            ret = self.bind_with_ssl(""
                                , self._port
                                , self._ssl_option.get("key_file", "")
                                , self._ssl_option["cert_file"]
                                , self._ssl_option["proto_version"])

        if ret == 0:
            tracelog.info("SimpleCallAcpSrv start listen on port %d, ssl_option:%s"%(
                            self._port
                            , self._ssl_option))
        else:
            tracelog.error("SimpleCallAcpSrv listen on port %d failed, ssl_option:%s"%(
                            self._port
                            , self._ssl_option))

        return ret
        
    def on_accept_client(self, url):
        """
        Method: on_accept_client
        Description: 接受到客户端连接的处理接口
        Parameter: 
            url: 客户端的url
        Return:错误码，0表示成功
        Others: 当返回值非0时，将断开该客户端的连接
        """

        tracelog.info("SimpleCallAcpSrv.on_client_accept: %s " % url)
        
        return 0

    def on_disconnect(self, url_or_srv_name):
        """
        Method: on_disconnect
        Description: 当客户端连接断开时的处理接口
        Parameter:
            url_or_srv_name: 客户端的url
        Return:
        Others: 
        """

        tracelog.info("SimpleCallAcpSrv.on_client_close: %s " % url_or_srv_name)
        

    def on_msg_received(self, url_or_srv_name, msg):
        """
        Method: on_msg_received
        Description: 当收到消息时的处理接口
        Parameter:
            url_or_srv_name: 客户端的url
            msg: 消息
        Return:
        Others: 
        """
        
        frame = self._msg_to_frame(url_or_srv_name, msg)

        if frame is not None:
            self._app.dispatch_frame_to_duty_worker(frame)

    
    def send_appframe(self, appframe):
        """
        Method: send_appframe
        Description: 发送AppFrame
        Parameter: 
            appframe: AppFrame
        Return:
        Others: 
        """

        url, msg = self._frame_to_msg(appframe)
        if msg is not None:
            self.send(url, msg)


    def _msg_to_frame(self, url_or_srv_name, msg):
        """
        Method: _msg_to_frame
        Description: 将AcpMessage装换为AppFrame
        Parameter: 
            url_or_srv_name: 消息发送者的url
            msg: AcpMessage消息
            
        Return:AppFrame
        Others: 
        """

        # CallAcpMsg转换为AppFrame
        frame = AppFrame()
        frame.set_cmd_code(msg.get_cmd_code())
        frame.set_sender_pid(local_const_def.CALLACPSRV_PID)
             
        custom_bytes = self._struct.pack(msg.get_msg_id()) + url_or_srv_name
        frame.set_custom_bytes(custom_bytes)
        frame.add_data(msg.get_data())
        
        return frame
        
        
    def _frame_to_msg(self, frame):
        """
        Method: _frame_to_msg
        Description: 将frame装换为AcpMessage消息
        Parameter: 
            frame: AppFrame
        Return: 待接受消息端的url和AcpMessage消息
        Others: 
        """

        # AppFrame转换为CallAcpMsg
        try:
            msg_id = self._struct.unpack_from(frame.get_custom_bytes())[0]
        except:
            tracelog.exception("SimpleCallAcpSrv._frame_to_msg() failed. "
                                "frame.get_custom_bytes():%s" % (
                                    repr(frame.get_custom_bytes())))
            return None, None

        url = frame.get_custom_bytes()[self._struct.size:]
        if len(url) == 0:
            tracelog.error("SimpleCallAcpSrv._frame_to_msg() failed. "
                            "url is null")
            return None, None
            
        msg = pycallacp.AcpMessage(frame.get_cmd_code(), frame.get_data())
        msg.set_msg_id(msg_id)
                
        return url, msg



class AppPids:

    def __init__(self):
        self.__all_name_pids = [] # [(instance_name, pid).]
        self.__local_service2pid = {} # service_name: [pid] 只包含本机的
        self.__master_service2pid = {} # service_name: [pid] 只包含master系统的
        self.__name2pids = {}  # service_name: [pid] 包含所有的
        
        self.__endpoint2pid = {} # {url: pid}
        self.__pid2appinfo = {} # {pid: AppInfo}

    def on_process_app_register(self, my_system_ip, all_app_infos):
        """
        Method:    on_process_app_register
        Description: 处理app register的消息
        Parameter: 
            all_app_infos: 系统内所有进程的all_app_infos
        Return: 
        Others: 
        """        
        self.__all_name_pids = [(app_info.instance_name, app_info.pid
                                 , app_info.endpoint_protocol, app_info.system_ip) for app_info in all_app_infos]
        
        self.__name2pids.clear()
        self.__local_service2pid.clear()
        self.__master_service2pid.clear()
        self.__endpoint2pid.clear()
        self.__pid2appinfo.clear()
        
        
        
        for app_info in all_app_infos:          
            self.__name2pids.setdefault(app_info.service_name, []).append(app_info.pid)
            
            if my_system_ip == app_info.system_ip:
                self.__local_service2pid.setdefault(app_info.service_name, []).append(app_info.pid)
                
            if app_info.node_type == 'MASTER':
                self.__master_service2pid.setdefault(app_info.service_name, []).append(app_info.pid)

            self.__endpoint2pid[app_info.endpoint] = app_info.pid
            self.__pid2appinfo[app_info.pid] = app_info
            

    def get_all_name_pids(self):
        """
        Method: get_all_name_pids
        Description: 获取全部的pid
        Parameter: 无
        Return:全部的pid信息
        Others: 
        """

        return self.__all_name_pids
        
    def get_pid(self, service_name, strategy=local_const_def.FIRSTLOCAL_PID):
        """
        Method:    get_pid
        Description: 根据选择策略获取指定service_name的进程的pid
        Parameter: 
            service_name: 服务名
        Return: 
            -1: 指定的进程不存在
            其他: 进程的pid
        Others: 
                        选择策略有多种：
        FIRSTLOCAL_PID，优选本机的进程，本机的进程不存在，则随机选择其他系统的进程
        ONLYLOCAL_PID,只选择本机的进程，本机的进程不存在，返回查找不到的信息
        RANDOM_PID,随机选择
        MASTER_PID,选择EAU或者IMC MASTER上的进程
        """

        
        if strategy == local_const_def.FIRSTLOCAL_PID:
            pid = self.__get_pid_firstlocal(service_name)
        elif strategy == local_const_def.ONLYLOCAL_PID:
            pid = self.__get_pid_onlylocal(service_name) 
        elif strategy == local_const_def.RANDOM_PID:
            pid = self.__get_pid_random(service_name)
        elif strategy == local_const_def.MASTER_PID:
            pid = self.__get_pid_master(service_name)
        else:
            pid = local_const_def.INVALID_PID
            
        return pid
    
    def __get_pid_firstlocal(self, service_name):
        """
        Method:    __get_pid_firstlocal
        Description: 根据本机优先来选择pid
        Parameter: 无
        Return: 
        Others: 
        """
        
        local_pids = self.__local_service2pid.get(service_name, None)
        if local_pids is not None:
            local_pids_len = len(local_pids)
            if local_pids_len == 1:
                return local_pids[0]
            elif local_pids_len > 1:
                return random.choice(local_pids)
            
       
        service_pids = self.__name2pids.get(service_name, None)
        if service_pids is not None and len(service_pids) > 0:
            if len(service_pids) > 1:
                return random.choice(service_pids)
            else:
                return service_pids[0]
                        
        return local_const_def.INVALID_PID

    def __get_pid_onlylocal(self, service_name):
        """
        Method:    __get_pid_onlylocal
        Description: 根据只选本机来选择pid
        Parameter: 无
        Return: 
        Others: 
        """

        local_pids = self.__local_service2pid.get(service_name, None)
        if local_pids is not None:
            local_pids_len = len(local_pids)
            if local_pids_len == 1:
                return local_pids[0]
            elif local_pids_len > 1:
                return random.choice(local_pids)
                
        return local_const_def.INVALID_PID
    
    def __get_pid_random(self, service_name):
        """
        Method:    __get_pid_random
        Description: 根据随机来选择pid
        Parameter: 无
        Return: 
        Others: 
        """
        service_pids = self.__name2pids.get(service_name, None)
        if service_pids is not None and len(service_pids) > 0:
            if len(service_pids) > 1:
                return random.choice(service_pids)
            else:
                return service_pids[0]
                        
        return local_const_def.INVALID_PID

    def __get_pid_master(self, service_name):
        """
        Method:    __get_pid_master
        Description: 根据只选master来选择pid
        Parameter: 无
        Return: 
        Others: 
        """
        pid = local_const_def.INVALID_PID
        master_pids = self.__master_service2pid.get(service_name, None)
        if master_pids is not None and len(master_pids) > 0:
            pid = random.choice(master_pids)
            
        return pid        
    
    def get_pids(self, service_name):
        """
        Method:    get_pids
        Description: 获取指定service_name的所有进程的pid
        Parameter: 
            service_name: 服务名
        Return: pid列表
        Others:                  
        """
        
        return self.__name2pids.get(service_name, [])
               


    
    def get_pid_by_endpiont(self, endpiont):
        """
        Method:    get_pid_by_endpiont
        Description: 根据指定的endpoint获取pid
        Parameter: 
            endpiont: endpoint
        Return: pid
        Others:                  
        """
            
        return self.__endpoint2pid.get(endpiont, local_const_def.INVALID_PID )


    def get_endpoint_by_pid(self, pid):
        """
        Method:    get_endpoint_by_pid
        Description: 根据指定的pid获取endpoint
        Parameter: 
            pid: pid
        Return: 如果存在执行的pid，那么返回endpoint字符串，否则返回None
        Others:                  
        """
            
        appinfo = self.__pid2appinfo.get(pid)
        
        if appinfo is not None:
            return appinfo.endpoint

        return None
    

class BasicApp(object):
    """
    Class: BasicApp
    Description: app基类，提供了相关的app运行的机制
    Base: object
    Others: 
    """


    SHAKEHAND_INITIALIZING = "INITIALIZING"
    SHAKEHAND_RUNNING = "RUNNING"
    SHAKEHAND_STOPPING = "STOPPING"
    
    SHAKEHANDACK_OK = "OK"
    SHAKEHANDACK_STOP = "stop"
    
    
    def __init__(self, service_name):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            service_name: 服务名称
        Return: 
        Others: 
        """
        #self._instance_id = self.prase_opt()
        self._instance_id = 0
        self._instance_name = "%s_%d"%(service_name, self._instance_id)
       
        self._service_name = service_name

        
                
        self._pid = local_const_def.INVALID_PID
        self._endpoint = ""
        
        #使用该对象必须进行加锁
        self.__app_pid = AppPids()
        
        self.__mutex = RLock()
        
        # 所有需要监控状态的线程
        self.__watched_threads = [] 

        # 所有需要处理业务的线程(通过register_worker注册的线程)
        self.__my_threads = [] 

        self.__ipc_send_work = None
        self.__dispatch_work = None

        self.__stop_event = Event()
        self.__stop_abruptly_time_out = -1
        self.__stopping = False        

        # 与monitor握手失败的计数器
        self.__shakehandl_failed_count = 0


        # callacp服务端
        self.__callacp_srv = None
        
        # 名字服务的服务端ip
        self._name_master_ip = ""
        
        # 注册名字服务时，客户端自己使用的ip
        self._my_name_ip = ""

        # 从device.xml中加载的设备信息
        self._device_info = None
        

    def get_name(self):
        """
        Method:    get_name
        Description: 获取当前app的名称
        Parameter: 无
        Return: 当前app的名称
        Others: 
        """

        return self._instance_name
    
    def get_service_name(self):
        """
        Method:    get_service_name
        Description: 获取当前app的service_name
        Parameter: 无
        Return: 当前app的service_name
        Others: 
        """

        return self._service_name

    def get_my_pid(self):
        """
        Method:    get_my_pid
        Description: 获取当前app的pid
        Parameter: 无
        Return: 当前app的pid
        Others: 
        """

        return self._pid

    def get_endpoint(self):
        """
        Method:    get_endpoint
        Description: 获取当前app与其他进程通信使用的endpoint
        Parameter: 
        Return: 当前app与其他进程通信使用的endpoint
        Others: 
        """

        
        return self._endpoint
        
    def on_process_app_register(self, all_app_infos):
        """
        Method:    on_process_app_register
        Description: 处理app register的消息
        Parameter: 
            all_app_infos: 系统内所有进程的all_app_infos
        Return: 
        Others: 
        """        
        if self.__ipc_send_work is not None:
            self.__ipc_send_work.on_process_app_register(all_app_infos)

        with self.__mutex:
            self.__app_pid.on_process_app_register(self.get_my_name_ip(), all_app_infos)
            
            
    def _open_log(self):
        """
        Method:    _open_log
        Description: 打开日志文件
        Parameter: 无
        Return: 
        Others: 
        """

        install_path = self.get_app_top_path()
        
        log_file = os.path.join(install_path
                            , "log"
                            , self._instance_name + ".log")
                            
        try:            
            tracelog.open(self._instance_name, log_file)
        except:
            print "open log file failed. log_file =", log_file

        

    def _close_log(self):
        """
        Method:    _close_log
        Description: 关闭日志文件
        Parameter: 无
        Return: 
        Others: 
        """

        tracelog.close()

    def get_name_master_ip(self):
        """
        Method: get_name_master_ip
        Description: 获取名字服务master的ip
        Parameter: 无
        Return:名字服务master的ip
        Others: 
        """

        return self._name_master_ip


    def __query_name_master_ip(self, callacp):
        """
        Method: __query_name_master_ip
        Description: 向monitor查询名字服务的ip
        Parameter: 无
        Return: 错误码和名字服务的ip
        Others: 
        """

        # 获取名字服务端的ip
        req_msg = pycallacp.AcpMessage(local_cmd_code.CMD_QUERY_CLUSTER_MASTER_IP, "")        
        local_name_serivce_url = "tcp://%s:%d" % (self._my_name_ip, local_const_def.NAME_SERVER_PORT)

        name_master_ip = ""
        
        # 重试次数
        retry_times = 15
        for i in xrange(retry_times):
            ret, rep_msg = callacp.call(local_name_serivce_url, req_msg, 3)            
            if ret != 0:
                continue

            try:
                rep_data = name_msg_def.QueryClusterMasterIpResponse.deserialize(rep_msg.get_data())
            except:
                tracelog.exception("QueryClusterMasterIpResponse deserialize failed.")
                return -1, ""
                
            name_master_ip = rep_data.ip
            if name_master_ip == "":
                # 此时master还没有产生，等待几秒后重试
                if i +1 < retry_times:
                    time.sleep(2)
                continue

            break


        if ret != 0:
            tracelog.error("query name master ip from local name service failed, the monitor maybe not running."
                            " url:%s, ret:%d" % (local_name_serivce_url, ret)
                            )
            return ret, ""

        if name_master_ip == "":
            tracelog.error("the name master ip returned by local name service is null.")
            return -1, ""
        
        return 0, name_master_ip
        

    def regist_name_service(self):
        """
        Method:    regist_name_service
        Description: 向名字服务中心注册服务
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
            注册后得到的通信地址， 例如"tcp://127.0.0.1:10000"            
        """
        tracelog.info("regist_name_service, service name:%s " % (self._service_name))

        callacp = pycallacp.CallAcpClient()

        if self._name_master_ip == "":
            # 获取名字服务端的ip
            ret, self._name_master_ip = self.__query_name_master_ip(callacp)

            if ret !=0 :
                return ret
            
            tracelog.info("the name master is %s" % self._name_master_ip)
        

        # 向名字服务发送注册请求
        req_data = name_msg_def.AppRegisterRequest()
        req_data.init_all_attr()
        req_data.service_name = self._service_name
        req_data.instance_id = self._instance_id 
        req_data.system_ip = self._my_name_ip
        req_data.node_type = "MASTER" if self.is_cluster_master() else "SLAVE"
        req_data.endpoint = self._endpoint
        req_data.endpoint_protocol = local_const_def.EIPC_PROTOCOL
        req_data.need_return_all_app_info = True
        
        req_msg = pycallacp.AcpMessage(local_cmd_code.REGISTER_NAME_COMMAND
                                        , req_data.serialize())

        master_name_serivce_url = "tcp://%s:%d" % (self._name_master_ip, local_const_def.NAME_SERVER_PORT)
        
        # 重试3次
        for i in xrange(3):
            ret, rep_msg = callacp.call(master_name_serivce_url, req_msg, 3)
            if ret == 0:
                break
                
        if ret != 0:
            tracelog.error("regist name service failed. name master ip is %s, "
                            "ret:%d" % (self._name_master_ip, ret))
            return ret
        
        # 更新名字信息      
        try:
            rep_data = name_msg_def.AppRegisterResponse.deserialize(rep_msg.get_data())
        except:
            tracelog.exception("AppRegisterResponse deserialize failed.")
            return -1

        if rep_data.return_code==0:
            self._pid = rep_data.app_info.pid
            self.on_process_app_register(rep_data.all_app_infos)
            tracelog.info("my pid is :%d" % self._pid)

        else:
            tracelog.error("regist name service failed. name master ip is %s, "
                            "ret:%d, %s" % (self._name_master_ip
                                            , rep_data.return_code
                                            , rep_data.description))

        callacp.clear()
        return rep_data.return_code

    def unregist_name_service(self):
        """
        Method:    unregist_name_service
        Description: 向名字服务中心注销服务
        Parameter: 无
        Return: 
        Others: 
        """
        if self._pid == local_const_def.INVALID_PID:
            return
            
        #按pid注销        
        frame = AppFrame()
        frame.set_cmd_code(local_cmd_code.UNREGISTER_NAME_COMMAND)

        #向MASTER的Monitor注册
        frame.set_receiver_pid(self.get_pid("Monitor", local_const_def.MASTER_PID))
        
        req = name_msg_def.AppUnRegisterRequest()
        req.init_all_attr()
        req.pid = self._pid        
        req.need_reponse = False
        frame.add_data(req.serialize())
        
        #不用关心结果
        rpc_worker.rpc_request(frame, 2)        

    def get_app_top_path(self):
        """
        Method:    get_app_top_path
        Description: 获取整个软件目录的顶层目录
        Parameter: 无
        Return: 整个软件目录的顶层目录
        Others: 
        """

        # 根据相对代码文件的相对位置，推算出软件所在的根目录
        # 在软件发布时，最好直接将路径固定(linux: /APC    windows: e:/APC)
        p = os.path.dirname(__file__)
        p = os.path.join(p, "../../../")
        p = os.path.abspath(p)
        return p
        
    



    def stop(self, minisecond = 60):
        """
        Method:    stop
        Description: 停止app
        Parameter: 
            minisecond: 等待线程退出的超时时间(秒)
        Return: 
        Others: 
        """

        with self.__mutex:
            if self.__stop_abruptly_time_out == -1:
                self.__stop_abruptly_time_out = minisecond
                self.__stop_event.set()

    def _is_need_shake_with_monitor(self):
        """
        Method:    _is_need_shake_with_monitor
        Description: 判断是否需要与monitor握手
        Parameter: 无
        Return: 是否需要与monitor握手
        Others: 
            如果不需要与monitor握手，则重载本函数
        """

        return True
    
    def _shakehand_with_monitor(self, statflag):
        """
        Method:    _shakehand_with_monitor
        Description: 与monitor握手一次
        Parameter: 
            statflag: 握手消息中带的状态
        Return: 
            -1: 握手失败
            0: monitor返回握手应答，应答中带有stop消息
            1: 握手成功
        Others: 
        """


        if not self._is_need_shake_with_monitor():
            return 1
        
        frame = AppFrame()
        frame.set_cmd_code(local_cmd_code.CMD_SHAKEHAND_WITH_MONITOR)
        #和本机Monitor握手
        frame.set_receiver_pid(self.get_pid("Monitor", local_const_def.ONLYLOCAL_PID))        
        frame.add_data(self._instance_name)
        frame.add_data(statflag)
        ack_frames = rpc_worker.rpc_request(frame, 2)

        if len(ack_frames) == 0:
            self.__shakehandl_failed_count += 1
            
            if self.__shakehandl_failed_count >= 3:
                tracelog.error("shake hand with monitor failed.")
                self.stop()                
            return -1

        self.__shakehandl_failed_count = 0
        ack_frame = ack_frames[0]
        rst = ack_frame.get_data(0)
        
        if rst == BasicApp.SHAKEHANDACK_STOP:
            tracelog.info("receive stop event from monitor.")
            self.stop()
            return 0

        return 1


    def notify_monitor_stop_event(self):
        """
        Method:    notify_monitor_stop_event
        Description: 通知monitor当前进程将要停止了
        Parameter: 无
        Return: 
        Others: 
        """

        if not self._is_need_shake_with_monitor():
            return

        if self.__ipc_send_work is None:
            return 
            
        try:
            frame = AppFrame()
            frame.set_cmd_code(local_cmd_code.CMD_SHAKEHAND_WITH_MONITOR)
            frame.add_data(self._instance_name)
            frame.add_data(BasicApp.SHAKEHAND_STOPPING)    
            frame.set_receiver_pid(self.get_pid("Monitor", local_const_def.ONLYLOCAL_PID))  
            self.dispatch_frame_to_process_by_pid(frame.get_receiver_pid(), frame)
        except:
            tracelog.exception("notify_monitor_stop_event failed.")
            
    def run(self):
        """
        Method:    run
        Description: app运行的接口函数
        Parameter: 无
        Return: 
        Others: 
        """

        try:
            self.__stop_event.clear()
            
            if self._initialize() != 0:
                raise Exception("app _initialize failed!")

            if self._create_base_worker_and_threads() != 0:
                raise Exception("_create_base_worker_and_threads failed!")

            # 启动时，自动与monitor握手
            while 1:
                if self._shakehand_with_monitor(BasicApp.SHAKEHAND_INITIALIZING) == 1:
                    break
                    
                if self.__stop_event.isSet():
                    raise Exception("shake hand with monitor failed while starting.")
                    
            
            if self._ready_for_work() != 0:
                raise Exception("_ready_for_work failed!")

            tracelog.info("process %s starts successfully." % (self._instance_name))

            self.__stop_event.clear()
            while True:
                self.__stop_event.wait(1)
                if self.__stop_event.isSet():
                    break

                self.__monitor_all_threads()
                self._shakehand_with_monitor(BasicApp.SHAKEHAND_RUNNING)
                
        except:            
            tracelog.exception("process run failed.")            
            
        finally:
            tracelog.info("process %s is stopping......" % (self._instance_name))
            
            self._pre_exit()
            self.__stop_all_threads()
            self._exit_work()
            
            self.notify_monitor_stop_event()
            tracelog.info("process %s exits successfully." % (self._instance_name))
            
            return 0

    def __monitor_all_threads(self):
        """
        Method:    __monitor_all_threads
        Description: 监控所有的线程
        Parameter: 无
        Return: 
        Others: 
        """

        with self.__mutex:
            for thrd in self.__watched_threads:
                if thrd.overflow_max_busy_ticks():
                    thrd.over()

                if thrd.is_over():
                    self.stop()  # 如果有线程意外停止了，那么就退出进程
                    return

    def __stop_all_threads(self):
        """
        Method:    __stop_all_threads
        Description: 停止所有的线程
        Parameter: 无
        Return: 
        Others: 
        """

        with self.__mutex:
            self.__stopping = True

            for wt in self.__watched_threads:
                wt.stop()

        WatchedThread.sleep(0.1)

        elapsed_seconds = time.time()
        while True:
            with self.__mutex:
                for wt in self.__watched_threads:
                    if wt.is_over():
                        self.__watched_threads.remove(wt)
                        break # 防止for循环异常

                if len(self.__watched_threads) == 0:
                    return

            if time.time() - elapsed_seconds > self.__stop_abruptly_time_out:
                return

            WatchedThread.sleep(0.1)
    
    def register_worker(self, wrkr, wrk_thrd = None, start_thread = True):
        """
        Method:    register_worker
        Description: 注册worker
        Parameter: 
            wrkr: worker实例
            wrk_thrd: worker依附的线程，如果wrk_thrd为None，那么就会自动创建一个新的线程
            start_thread: 是否立即启动线程
        Return: 
            0: 成功
            非0: 失败
        Others: 
            多个worker可以共用一个线程，此时需要注意，最后一次调用register_worker
            时，才设置start_thread为True。否则会导致除了第一个worker之外，其他worker
            没有执行ready_for_work
            
        """

        if wrkr == None:
            return -1

        with self.__mutex:
            for wt in self.__my_threads:
                if wrkr in wt.get_workers():
                    return -1

            wrkr.set_app(self)

            if wrk_thrd is None:
                wrk_thrd = WorkThread()

            wrk_thrd.append_worker(wrkr)

            if wrk_thrd not in self.__my_threads:
                self.__my_threads.append(wrk_thrd) 

            if start_thread is True:
                self.register_watched_thread(wrk_thrd)

            return 0


    def unregister_worker(self, wrkr, unreg_thread):
        """
        Method:    unregister_worker
        Description: 注销worker
        Parameter: 
            wrkr: worker实例
            unreg_thread: 当线程没有其他worker的时候, 是否同时注销线程
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        if wrkr == None:
            return -1

        with self.__mutex:
            wrk_thrd = None
            for wt in self.__my_threads:
                if wrkr in wt.get_workers():
                    wrk_thrd = wt
                    break

            if wrk_thrd is None:
                return -1

            wrk_thrd.remove_worker(wrkr)

            # 当线程中没有其他worker的时候，注销线程
            if len(wt.get_workers()) == 0 and unreg_thread:
                self.unregister_watched_thread(wrk_thrd)
                
            return 0

   
    def register_watched_thread(self, wtch_thrd):
        """
        Method:    register_watched_thread
        Description: 注册线程
        Parameter: 
            wtch_thrd: 线程
        Return: 
        Others: 
        """

        if wtch_thrd is None:
            return -1

        with self.__mutex:
            for wt in self.__watched_threads:
                if wt is wtch_thrd:
                    return

            self.__watched_threads.append(wtch_thrd)
            wtch_thrd.start_me()

    def unregister_watched_thread(self, wtch_thrd):
        """
        Method:    unregister_watched_thread
        Description: 
        Parameter: 
            wtch_thrd: 
        Return: 
            0: 成功
            非0: 失败
        Others: 通过本接口注册的线程，是随着进程的生命周期而存在的
        """

        if wtch_thrd == None:
            return -1

        with self.__mutex:
            wtch_thrd.stop()

            if self.__watched_threads.index(wtch_thrd) >= 0:
                self.__watched_threads.remove(wtch_thrd)

            # 尽量等待线程退出
            # 否则从任务管理中仍然可以看到线程存在
            wtch_thrd.join(10)
        return 0

    def get_watched_threads(self):
        """
        Method:    get_watched_threads
        Description: 获取所有被监控的线程
        Parameter: 无
        Return: 线程列表
        Others: 
        """
        return self.__watched_threads
        
    def _create_base_worker_and_threads(self):
        """
        Method:    _create_base_worker_and_threads
        Description: 创建app中基本的worker和线程
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败        
        Others: 
        """
        # 接收消息的worker
        irw = IpcRecvWorker()
        irw.set_app(self)        
        min_port, max_port = self._get_name_port_range()
        ret = irw.bind_on_avalible_endpoint(self.get_my_name_ip(), min_port, max_port)
        if ret != 0:
            tracelog.error("bind on avalible endpoint failed.")
            return ret

        self._endpoint = irw.get_endpoint()
        assert(len(self._endpoint) > 0)

        tracelog.info("my endpoint is %s" % self._endpoint)
        self.register_watched_thread(CommunicationThread(irw))
        
        # 发送消息的worker
        isw = IpcSendWorker()
        isw.set_app(self)       
        ret = isw.ready_for_work()
        if ret != 0:
            return ret
        
        self.__ipc_send_work = isw
        
        # rpc的worker
        wth = WorkThread()
        rworker = rpc_worker.get_rpc_worker()
        self.register_worker(rworker, wth, False)

        # 处理app公共命令的worker
        cworker = CommonCmdWorker()
        self.register_worker(cworker, wth, True)
        
        
        # 注册名字服务,必须在__ipc_send_work实例化以后，否则__ipc_send_work的__peer_sockets不会被更新
        ret = self.regist_name_service()
        if ret != 0:
            return ret

        # 启动callacp服务端
        self.__callacp_srv = self.get_callacp_srv()
        if self.__callacp_srv is not None:
            ret = self.__callacp_srv.start_listen()
            if ret != 0:
                tracelog.error("start callacp server failed.")

        return ret
    
    def _query_from_nameservice(self):
        """
        Method:    _query_from_nameservice
        Description: 从名字服务查询所有注册信息
        Parameter: 无
        Return: 
        Others: 
        """
        frame = AppFrame()
        frame.set_cmd_code(local_cmd_code.QUERY_APP_COMMAND)
        frame.set_receiver_pid(self.get_pid("Monitor", local_const_def.MASTER_PID))
        
        req = name_msg_def.AppQueryRequest()
        req.init_all_attr()        
        frame.add_data(req.serialize())
        
        ack_frames = rpc_worker.rpc_request(frame, 10)
        all_app_infos = []
        if len(ack_frames)==0:            
            return all_app_infos
        
        #这里不需要捕获异常
        rep = name_msg_def.AppQueryResponse.deserialize(ack_frames[0].get_data())
        if rep.return_code==0:
            all_app_infos = rep.app_infos

        return all_app_infos

    def _pre_exit(self):
        """
        Method:    _pre_exit
        Description: app退出时，线程停止前的处理接口
        Parameter: 无
        Return: 
        Others: 
        """
        # 注销名字服务，需要在worker注销前进行
        self.unregist_name_service()
        

    def _exit_work(self):
        """
        Method:    _exit_work
        Description: 所有的工作线程停止后的调用接口，进程退出前的善后工作
        Parameter: 无
        Return: 
        Others: 
        """

                    
        self._close_log()

    def _init_name_service_ip(self):
        """        
        如果当前启用了cluster，那么：
        	名字服务监听在内网ip上
            注册名字服务时，ip也使用master的ip
            
        如果当前没有启用cluster，那么：
            名字服务监听在127.0.0.1的端口上
            注册名字服务时，ip也使用127.0.0.1            
        """
        if self._device_info.is_cluster_enable():
            self._my_name_ip = self._device_info.get_device_internal_ip()
            self._name_master_ip = ""
        else:
            self._my_name_ip = "127.0.0.1"
            self._name_master_ip = "127.0.0.1"

        return 0

        
    def _initialize(self):
        """
        Method:    _initialize
        Description: app初始化接口
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败   
        Others: 
        """
        #获取命令行参数,必须放在最前面
        ret = self.prase_opt()
        if ret!=0:
            return ret
        
        self._open_log()

        # 初始化语种
        lang_cfg_file = os.path.join(self.get_app_top_path(), "configure/language.xml")        
        ret = language_cfg.load_from_cfg_file(lang_cfg_file)
        if ret != 0:
            tracelog.error("load language configuration failed.")
            return ret

        tracelog.info("process start: " + self._instance_name)
        tracelog.info("python version is %s" % sys.version)
        tracelog.info("language is %s" % language_cfg.get_language())

        device_info_file = os.path.join(self.get_app_top_path(), "configure", "device.xml")
        self._device_info = device_cfg_info.DeviceCfgInfo()
        ret = self._device_info.load(device_info_file)
        if ret != 0:
            return ret
     
        ret = self._init_name_service_ip()
        if ret != 0:
            return ret
            
        return 0


    def _ready_for_work(self):
        """
        Method:    _ready_for_work
        Description: app开始正式工作前的初始化接口
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败   
        Others: 
        """

        return 0

    def get_pid(self, service_name, strategy=local_const_def.FIRSTLOCAL_PID):
        """
        Method:    get_pid
        Description: 根据选择策略获取指定service_name的进程的pid
        Parameter: 
            service_name: 服务名
        Return: 
            -1: 指定的进程不存在
            其他: 进程的pid
        Others: 
                        选择策略有多种：
        FIRSTLOCAL_PID，优选本机的进程，本机的进程不存在，则随机选择其他系统的进程
        ONLYLOCAL_PID,只选择本机的进程，本机的进程不存在，返回查找不到的信息
        RANDOM_PID,随机选择
        MASTER_PID,选择EAU或者IMC MASTER上的进程
        """
        with self.__mutex:
            pid = self.__app_pid.get_pid(service_name, strategy)
            if pid==0:
                #tracelog.info('get pid failed. service_name: %s all_name_pids: %s'%(
                #                service_name
                #                , self.__app_pid.get_all_name_pids()
                #                ))
                tracelog.info('get pid failed. service_name: %s'%(service_name))
        return pid
    

    def get_pids(self, service_name):
        """
        Method:    get_pids
        Description: 获取指定service_name的所有进程的pid
        Parameter: 
            service_name: 服务名
        Return: pid列表
        Others:                  
        """
        with self.__mutex:
            pids = self.__app_pid.get_pids(service_name)
        return pids
                

    def get_pid_by_endpiont(self, endpiont):
        """
        Method:    get_pid_by_endpiont
        Description: 根据指定的endpoint获取pid
        Parameter: 
            endpiont: endpoint
        Return: pid
        Others:                  
        """
        
        with self.__mutex:
            pid = self.__app_pid.get_pid_by_endpiont(endpiont)
            
        return pid


    def get_endpoint_by_pid(self, pid):
        """
        Method:    get_endpoint_by_pid
        Description: 根据指定的pid获取endpoint
        Parameter: 
            pid: pid
        Return: 如果存在执行的pid，那么返回endpoint字符串，否则返回None
        Others:                  
        """
        
        with self.__mutex:
            endpoint = self.__app_pid.get_endpoint_by_pid(pid)
            
        return endpoint

            
    def get_callacp_srv(self):
        """
        返回callacp的服务实例
        如果需要部署callcap服务端，那么就重载本函数，返回一个CallAcpSrv(或派生类)
        的对象实例
        """
        return None
    

    def __dispatch_frame_to_callacp(self, frame):
        """
        Method:    __dispatch_frame_to_callacp
        Description:发送消息到callacp的客户端
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        
        if self.__callacp_srv is None:
            return 
        
        self.__callacp_srv.send_appframe(frame)

    def send_ack(self, frame, datas):
        """
        Method:    send_ack
        Description:发送应答消息
        Parameter: 
            frame: AppFrame实例，对应的请求消息
            datas: 应答消息体，字符串或二进制数据，可以是一个字符串或二进制数据的列表
        Return: 
        Others: 
        """
        
        frame_ack = AppFrame()
        frame_ack.prepare_for_ack(frame)
        if isinstance(datas, list) or isinstance(datas, tuple):
            for data in datas:
                frame_ack.add_data(data)
        else:
            frame_ack.add_data(datas)
            
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack) 
        
        
    def dispatch_frame_to_process_by_pid(self, pid, frame):
        """
        Method:    dispatch_frame_to_process_by_pid
        Description: 
        Parameter: 发送appframe到指定的进程
            pid: 指定进程的pid
            frame: AppFrame
        Return: 
        Others: 
        """

        
        if frame.get_sender_pid() == local_const_def.INVALID_PID:
            frame.set_sender_pid(self._pid)
        
        frame.set_receiver_pid(pid)
        if pid == self._pid:
            self.dispatch_frame_to_duty_worker(frame)
        elif pid == local_const_def.CALLACPSRV_PID:
            self.__dispatch_frame_to_callacp(frame)
        else:
            self.__ipc_send_work.send_frame(frame)


    def dispatch_frame_to_process(self, process_name, frame):
        """
        Method:    dispatch_frame_to_process
        Description: 发送appframe到指定的进程
        Parameter: 
            process_name: 指定进程的名字
            frame: AppFrame
        Return: 
        Others: 
        """

        pid = self.get_pid(process_name)
        self.dispatch_frame_to_process_by_pid(pid, frame)

    def dispatch_frame_to_worker(self, worker_name, frame):
        """
        Method:    dispatch_frame_to_worker
        Description: 发送appframe到指定的worker
        Parameter: 
            worker_name: worker的名字
            frame: AppFrame
        Return: 
        Others: 
        """

        threads = []
        with self.__mutex:
            for thrd in self.__my_threads:
                if (thrd.get_worker(worker_name) is not None):
                    threads.append(thrd)
        
        self.__dispatch_frame(threads, frame)
        
    def dispatch_frame_to_all_workers(self, frame):
        """
        Method:    dispatch_frame_to_all_workers
        Description: 发送appframe到所有的worker
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """

        
        with self.__mutex:
            threads = self.__my_threads[:]
            
        self.__dispatch_frame(threads, frame)

    def dispatch_frame_to_duty_worker(self, frame, multi_worker=False):
        """
        Method:    dispatch_frame_to_duty_worker
        Description: 将appframe发送到需要处理该消息的worker
        Parameter: 
            frame: AppFrame
            multi_worker: frame是否会被多个worker处理
        Return: 
        Others: 
        """

        threads = []
        
        with self.__mutex:
            for thread in self.__my_threads:
                for worker in  thread.get_workers():
                    if worker.is_my_duty(frame):
                        threads.append(thread)
                                                
                        if multi_worker is False:
                            break
                else:
                    continue

                break
    
        if len(threads) > 0:
            self.__dispatch_frame(threads, frame)
        else:
            tracelog.error("dispatch frame to duty worker failed.%s" % str(frame))
                                    

    def dispatch_frame_to_any_other_processes(self, frame):
        """
        Method:    dispatch_frame_to_any_other_processes
        Description: 发送appframe到其他所有的app
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """

        with self.__mutex:
            for instance_name, pid, endpoint_procotol, system_ip in self.__app_pid.get_all_name_pids():            
                if (endpoint_procotol!=local_const_def.EIPC_PROTOCOL
                     or (instance_name == self._instance_name and system_ip==self._my_name_ip)):
                    continue
                    
                self.dispatch_frame_to_process_by_pid(pid, frame.clone())

    def __dispatch_frame_to_thread(self, thrd, frame):
        """
        Method:    __dispatch_frame_to_thread
        Description: 发送appframe到指定的线程
        Parameter: 
            thrd: 线程对象
            frame: AppFrame
        Return: 
        Others: 
        """

        if frame and thrd and not self.__stopping:
            thrd.push_frame(frame)

    def __dispatch_frame(self, threads, frame):
        """
        Method:    __dispatch_frame
        Description: 发送appframe到若干个线程
        Parameter: 
            threads: 线程列表
            frame: AppFrame
        Return: 
        Others: 
        """

        if frame is None or self.__stopping:
            return

        if frame.get_sender_pid() == local_const_def.INVALID_PID:
            frame.set_sender_pid(self._pid)
            
        if len(threads) == 1:
            threads[0].push_frame(frame)
            return

        for thrd in threads:
            if thrd is not None and len(thrd.get_workers()) > 0:
                thrd.push_frame(frame.clone())

    def get_my_name_ip(self):
        """
        Method: get_my_name_ip
        Description: 获取自己用于注册名字服务的ip
        Parameter: 无
        Return:自己的名字信息的ip
        Others: 
        """

        # 获取自己的名字服务ip
        return self._my_name_ip

        
    def is_cluster_master(self):
        """
        Method: is_cluster_master
        Description: 判断当前是否是集群的master节点
        Parameter: 无
        Return:当前是否是集群的master节点
        Others: 
        """

        # 返回当前系统是否是cluster中的master
        return self._my_name_ip == self.get_name_master_ip()
    
    
    def get_device_id(self):
        """
        Method: get_device_id
        Description: 获取设备的id
        Parameter: 无
        Return:设备的id
        Others: 
        """

        return self._device_info.get_device_id()

    def get_device_cfg_info(self):
        """
        Method: get_device_cfg_info
        Description: 获取设备的配置信息
        Parameter: 无
        Return:设备的配置信息
        Others: 
        """

        return self._device_info

    def _get_name_port_range(self):
        """
        Method: _get_name_port_range
        Description: 获取用于注册名字服务的端口的范围
        Parameter: 无
        Return:用于注册名字服务的端口的范围
        Others: 
        """

        # 普通的app，可以使用的端口号范围是[6100,6999]
        # 需要固定端口的进程，会重载该接口
        return 6100, 6999
    

    def prase_opt(self):
        """
        Function: prase_opt
        Description: 解析命令行参数
        Parameter: 
        Return: 
        Others: 
        """
        
    
        try:
            opts, args = getopt.getopt(sys.argv[1:], '',  
                      [ 'id=' ] 
                      ) 
        except Exception, e:
            tracelog.error(str(e))
            return 1
            
        for option, value in opts:
            if  option == "--id": 
                if value.isdigit():
                    self._instance_id = int(value)
                    self._instance_name = "%s_%d"%(self._service_name, self._instance_id)
                
        return 0
        

