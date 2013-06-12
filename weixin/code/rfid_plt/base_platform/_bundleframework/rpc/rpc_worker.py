#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-06
Description: 本文件中实现了处理RPC请求的worker
Others:      
Key Class&Method List: 
             1. RpcWorker: 处理RPC请求的worker
History: 
1. Date:
   Author:
   Modification:
"""


import threading
import collections

import tracelog
import err_code_mgr

from _bundleframework.protocol.appframe import AppFrame
from _bundleframework.cmdhandler.cmd_worker import CmdWorker
from _bundleframework.rpc.rpc_handler import RpcHandler
from _bundleframework.dispatch.work_thread import WorkThread
from _bundleframework import local_cmd_code

class RpcWorker(CmdWorker):
    """
    Class: RpcWorker
    Description: 处理RPC请求的worker
    Base: CmdWorker
    Others: 
    """

    worker_name = "rpc_worker"
    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
        """

        CmdWorker.__init__(self, RpcWorker.worker_name, min_task_id = 0xFFFF0000, max_task_id = 0xFFFFFFF0)

        # 由于发起RPC请求在另一个线程，所以在需要加锁
        self._lock = threading.RLock()
        #self._rpc_contexts = collections.deque()
        

    def process_rpc_context(self, rpc_context):
        """
        Method:    process_rpc_context
        Description: 处理RPC请求
        Parameter: 
            rpc_context: 
        Return: 
        Others: 
        """

        #self._rpc_contexts.append(rpc_context)

        if self.get_app() is None:
            raise Exception("RpcWorker is not registed in app.")

        rpc_context.init_event()
        handler = RpcHandler()
        handler.set_worker(self)
        
        with self._lock:
            handler.handle_cmd_context(rpc_context)

        rpc_context.wait_event()
        rpc_context.destory_event()

        
class RpcContext:
    """
    Class: RpcContext
    Description: RPC请求的上下文
    Base: 
    Others: 
    """


    def __init__(self, appframe, timeout):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            appframe: 请求消息
            timeout: 超时时间(秒)
        Return: 
        Others: 
            __req_frame: 请求消息
            __timeout: 超时时间
            __event: 信号量，用于等待对方的应答
            __ack_frames: 应答消息列表
        """

        self.__req_frame = appframe
        self.__timeout = timeout
        self.__event = None
        self.__ack_frames = []
        #self.__is_timeout = False
    
    
    def init_event(self):
        """
        Method:    init_event
        Description: 初始化信号量
        Parameter: 无
        Return: 
        Others: 
        """

        self.destory_event()
        self.__event = threading.Event()
        self.__event.clear()

    def wait_event(self):
        """
        Method:    wait_event
        Description: 等待信号量
        Parameter: 无
        Return: 
        Others: 
        """

        
        self.__event.wait()
        self.destory_event()

    def signal_event(self):
        """
        Method:    signal_event
        Description: 设置信号量为可用
        Parameter: 无
        Return: 
        Others: 
        """

        if self.__event is not None:
            self.__event.set()

        
    def destory_event(self):
        """
        Method:    destory_event
        Description: 销毁信号量
        Parameter: 无
        Return: 
        Others: 
        """

        if self.__event is not None:
            del self.__event
            self.__event = None            

    def get_req_frame(self):
        """
        Method:    get_req_frame
        Description: 获取请求消息
        Parameter: 无
        Return: 
        Others: 
        """

        return self.__req_frame

    def get_timeout(self):
        """
        Method:    get_timeout
        Description: 获取超时时间
        Parameter: 无
        Return: 
        Others: 
        """

        return self.__timeout
    
    def set_ack_frames(self, frames):
        """
        Method:    set_ack_frames
        Description: 设置应答消息
        Parameter: 
            frames: 应答消息列表
        Return: 
        Others: 
        """

        self.__ack_frames = frames[:]

    def get_ack_frames(self):
        """
        Method:    get_ack_frames
        Description: 获取应答消息
        Parameter: 无
        Return: 应答消息列表
        Others: 
        """

        return self.__ack_frames


    def get_ack_frame(self):
        """
        Method:    get_ack_frame
        Description: 获取第一个应答消息
        Parameter: 无
        Return: 
            None:没有收到应答消息
            非None:第一个应答消息
        Others: 
        """

        if len(self.__ack_frames) > 0:
            return self.__ack_frames[0]
            
        return None

    #def set_timeout_flag(self):
    #    self.__is_timeout = True
        
    #def is_timeout(self):
    #    return self.__is_timeout
           

g_rpc_worker = None
MAX_RPC_TIMEOUT = 60*60*12

def get_rpc_worker():
    """
    Function: get_rpc_worker
    Description: 获取处理RPC的worker
    Parameter: 
    Return: 
    Others: 
    """

    global g_rpc_worker
    
    if g_rpc_worker is None:
        g_rpc_worker = RpcWorker()
        
    return g_rpc_worker    



def rpc_request(appframe, timeout):
    """
    Function: rpc_request
    Description: 进行RPC方式命令执行
    Parameter: 
        appframe: 请求消息
        timeout: 超时时间
    Return: 应答消息
    Others: 
    """

    """
    进行一次RPC调用
    appframe - 请求消息，包含了对端执行命令需要的信息
    timeout - 超时时间(秒)

    返回值: 应答消息列表. 如果列表为空，则表示没有收到应答(超时了)
    """

    if timeout > MAX_RPC_TIMEOUT:
        timeout = MAX_RPC_TIMEOUT
    
    rpc_context = RpcContext(appframe, timeout)
    
    get_rpc_worker().process_rpc_context(rpc_context)


    return rpc_context.get_ack_frames()
    
    
