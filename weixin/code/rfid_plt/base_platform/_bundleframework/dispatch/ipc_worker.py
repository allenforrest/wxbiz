#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-30
Description: 本文件中实现了ipc相关的worker
Others:      
Key Class&Method List: 
             1. IpcSendWorker: 发送消息的worker
             2. IpcRecvWorker: 接收消息的worker
History: 
1. Date:
   Author:
   Modification:
"""


import time
import threading
import random

import tracelog
import err_code_mgr

from _bundleframework.transport import eipc
from _bundleframework.dispatch.worker import Worker
from _bundleframework.protocol.appframe import AppFrame, ProcessStartNotify

from _bundleframework import local_const_def


EIPC_SEND_HWM  = 100000
EIPC_RECV_HWM  = 100000

################################################
# 使用EIPC的PUB-SUB模式，不使用PUSH-POLL模式
# PUSH-POLL模式下处理高水位时，存在问题
# 1）PUSH-PULL模式下，一旦到达了高水位，将会阻塞发送，且不会自动丢弃老的消息
#   （已经过时的消息积压，新的消息发送被阻塞）
# 2）如果设置了高水位，同时在send时，指定zmq.NOBLOCK，会出现：
#   到达高水位后，新的消息将被丢弃
#   如果当前进程达到了高水位，且对端一直没有启动，那么当前进程无法退出
#  （需要特殊处理才能OK，但是实际上如果程序异常的情况下，无法确保一定可能走到
#    特殊处理的代码）
################################################


DEBUG_LOG_IN_MSG = True
DEBUG_LOG_OUT_MSG = True

class IpcSendWorker(Worker):
    """
    Class: IpcSendWorker
    Description: 发送消息的worker
    Base: Worker
    Others: 
    """

    worker_name = "ipc_send_worker"

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
            __mutex: 锁
            __peer_sockets:所有与其他app发送消息的socket
        """

        Worker.__init__(self, IpcSendWorker.worker_name)

        self.__mutex = threading.RLock()
        
        self.__peer_sockets = {}  # pid: (endpoint, socket)
        self.__context    = eipc.Context.instance()



    def on_process_app_register(self, all_app_infos):
        """
        Method:    on_process_app_register
        Description: 响应register变更的消息
        Parameter: 
            all_app_infos: 系统内所有进程的app_info
        Return: 
        Others: 
        """

        try:
            with self.__mutex:
                tmp = self.__peer_sockets
                self.__peer_sockets = {}

                for app_info in all_app_infos:
                    old_endpoint, socket = tmp.pop(app_info.pid, ("", None))
                    if app_info.endpoint != old_endpoint:
                        if socket is not None:
                            socket.close()
                        socket = None

                    self.__peer_sockets[app_info.pid] = (app_info.endpoint, socket)

                # 关闭不再需要的socket
                for url, socket in tmp.itervalues():
                    if socket is not None:
                        socket.close()
        except:
            tracelog.exception("IpcSendWorker.on_process_app_register failed.")
            
            
    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker初始化工作
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        #for pid, endpoint in self.__peer_app_properties.items():
        #    socket = self.__context.socket(eipc.PUSH)
        #    socket.connect(endpoint)
        #    self.__peer_sockets[pid] = socket

        return 0

    def idle(self, total_ready_frames):
        """
        Method:    idle
        Description: 空闲处理函数
        Parameter: 
            total_ready_frames: 等待执行的命令的数目
        Return: 
        Others: 
        """

        frame, priority = self.pop_frame(0.8)
        if frame is not None:
            self.send_frame(frame)

    def send_frame(self, frame):
        """
        Method:    send_frame
        Description: 发送一条消息
        Parameter: 
            frame: 需要发送的消息
        Return: 
        Others: 
        """

        next_pid = frame.get_next_pid()
        
        if next_pid != local_const_def.INVALID_PID and next_pid != self.get_app().get_my_pid():
            pid = next_pid
        else:
            pid = frame.get_receiver_pid()

        #if DEBUG_LOG_OUT_MSG is True:
        #    tracelog.debug("Send:%s" % frame)

        try:
            with self.__mutex:
                tmp = self.__peer_sockets.get(pid)
                if tmp is None:
                    tracelog.error("IpcSendWorker.send_frame(): can not find pid(%d).%s" %(pid, frame))
                    return

                endpoint, socket = tmp
                
                # 按需创建socket
                if socket is None:
                    socket = self.__context.socket(eipc.PUB)
                    socket.setsockopt(eipc.HWM, EIPC_SEND_HWM)
                    try:
                        socket.connect(endpoint.replace("*", "127.0.0.1"))                        
                    except:
                        tracelog.exception("IpcSendWorker.send_frame(): endpoint=%s" % endpoint)
                        return
                        
                    self.__peer_sockets[pid] = (endpoint, socket)
                    
                try:
                    socket.send(frame.serialize_to_str())
                except:                
                    tracelog.exception("send frame to peer(%d) failed. %s" % (pid, frame))

        except:
            tracelog.exception("send_frame failed. peer is %d" %(pid))
            

class IpcRecvWorker(Worker):
    """
    Class: IpcRecvWorker
    Description: 接收消息的worker
    Base: 
    Others: 
    """

    worker_name = "ipc_recv_worker"

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            endpoint: 本app绑定的endpoint，其他app通过连接到该endpoint后方可发送消息过来
        Return: 
            __endpoint: 本app绑定的endpoint
            __socket: 处于监听状态的socket
            __context:eipc的Context对象
            __poll: eipc的Poller对象
        Others: 
        """

        Worker.__init__(self, IpcRecvWorker.worker_name)
        self.__endpoint = ""
        self.__socket     = None
        self.__context    = eipc.Context.instance()
        self.__poll = eipc.Poller()
        
    def get_endpoint(self):
        """
        Method: get_endpoint
        Description: 获取endpoint
        Parameter: 无
        Return:endpoint
        Others: 
        """
        return self.__endpoint


    def __close_socket(self):
        """
        Method: __close_socket
        Description: 关闭socket
        Parameter: 无
        Return:
        Others: 
        """
        if self.__socket is not None:
            try:
                self.__socket.close()
            except:
                pass

            self.__socket = None
            
    
    def bind_on_avalible_endpoint(self, ip, min_port, max_port): 
        """
        Method: bind_on_avalible_endpoint
        Description: 在给定的区间里，绑定在可用的端口上
        Parameter: 
            ip: 需要绑定的IP
            min_port: 起始端口号
            max_port: 结束端口号
            
        Return:错误码
        Others: 
        """
        if min_port == max_port:
            # 固定在指定的端口
            try_times = 1
        else:
            #最多尝试100次
            try_times = 100
            
        ret = -1
        endpoint = ""
        
        random.seed("%s %s" %(id(self), time.time()))
        
        
        for i in xrange(try_times):
            self.__close_socket()
            eipc_sock= self.__context.socket(eipc.PULL)
            eipc_sock.setsockopt(eipc.HWM, EIPC_RECV_HWM)

            if min_port == max_port:
                port = min_port
            else:
                port = random.randrange(min_port, max_port + 1)
            
            try:
                endpoint = 'tcp://%s:%d'%(ip, port) 
                eipc_sock.bind(endpoint)
                ret = 0
            except socket.error, e:
                continue

            self.__endpoint = endpoint
            self.__socket = eipc_sock
            break
        return ret
    

    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker初始化函数
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        try:
            if self.__socket is None:
                tracelog.error("IpcRecvWorker socket is not initialized")
                return -1
                
            self.__poll.register(self.__socket, eipc.POLLIN)
            
        except:
            tracelog.exception("IpcRecvWorker.ready_for_work() failed. endpoint:%s" % self.__endpoint)
            return -1
        return 0

    def idle(self, total_ready_frames): 
        """
        Method:    idle
        Description: 空闲处理函数
        Parameter: 
            total_ready_frames: 等待执行的命令的数目
        Return: 
        Others:  
        """

        socks = dict(self.__poll.poll(1000))

        if socks.get(self.__socket) != eipc.POLLIN:
            return

        try:
            msg = self.__socket.recv()
        except:
            tracelog.exception("receive data failed.")
            return
            
        oneFrame = AppFrame.serialize_from_str(msg)

        if oneFrame is None:
            return

        #if DEBUG_LOG_IN_MSG is True:
        #    tracelog.debug("Recv:%s" % oneFrame)
            
        self.get_app().dispatch_frame_to_duty_worker(oneFrame)
        
        
