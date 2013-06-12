#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-06
Description: ���ļ���ʵ���˴���RPC�����worker
Others:      
Key Class&Method List: 
             1. RpcWorker: ����RPC�����worker
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
    Description: ����RPC�����worker
    Base: CmdWorker
    Others: 
    """

    worker_name = "rpc_worker"
    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
        """

        CmdWorker.__init__(self, RpcWorker.worker_name, min_task_id = 0xFFFF0000, max_task_id = 0xFFFFFFF0)

        # ���ڷ���RPC��������һ���̣߳���������Ҫ����
        self._lock = threading.RLock()
        #self._rpc_contexts = collections.deque()
        

    def process_rpc_context(self, rpc_context):
        """
        Method:    process_rpc_context
        Description: ����RPC����
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
    Description: RPC�����������
    Base: 
    Others: 
    """


    def __init__(self, appframe, timeout):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            appframe: ������Ϣ
            timeout: ��ʱʱ��(��)
        Return: 
        Others: 
            __req_frame: ������Ϣ
            __timeout: ��ʱʱ��
            __event: �ź��������ڵȴ��Է���Ӧ��
            __ack_frames: Ӧ����Ϣ�б�
        """

        self.__req_frame = appframe
        self.__timeout = timeout
        self.__event = None
        self.__ack_frames = []
        #self.__is_timeout = False
    
    
    def init_event(self):
        """
        Method:    init_event
        Description: ��ʼ���ź���
        Parameter: ��
        Return: 
        Others: 
        """

        self.destory_event()
        self.__event = threading.Event()
        self.__event.clear()

    def wait_event(self):
        """
        Method:    wait_event
        Description: �ȴ��ź���
        Parameter: ��
        Return: 
        Others: 
        """

        
        self.__event.wait()
        self.destory_event()

    def signal_event(self):
        """
        Method:    signal_event
        Description: �����ź���Ϊ����
        Parameter: ��
        Return: 
        Others: 
        """

        if self.__event is not None:
            self.__event.set()

        
    def destory_event(self):
        """
        Method:    destory_event
        Description: �����ź���
        Parameter: ��
        Return: 
        Others: 
        """

        if self.__event is not None:
            del self.__event
            self.__event = None            

    def get_req_frame(self):
        """
        Method:    get_req_frame
        Description: ��ȡ������Ϣ
        Parameter: ��
        Return: 
        Others: 
        """

        return self.__req_frame

    def get_timeout(self):
        """
        Method:    get_timeout
        Description: ��ȡ��ʱʱ��
        Parameter: ��
        Return: 
        Others: 
        """

        return self.__timeout
    
    def set_ack_frames(self, frames):
        """
        Method:    set_ack_frames
        Description: ����Ӧ����Ϣ
        Parameter: 
            frames: Ӧ����Ϣ�б�
        Return: 
        Others: 
        """

        self.__ack_frames = frames[:]

    def get_ack_frames(self):
        """
        Method:    get_ack_frames
        Description: ��ȡӦ����Ϣ
        Parameter: ��
        Return: Ӧ����Ϣ�б�
        Others: 
        """

        return self.__ack_frames


    def get_ack_frame(self):
        """
        Method:    get_ack_frame
        Description: ��ȡ��һ��Ӧ����Ϣ
        Parameter: ��
        Return: 
            None:û���յ�Ӧ����Ϣ
            ��None:��һ��Ӧ����Ϣ
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
    Description: ��ȡ����RPC��worker
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
    Description: ����RPC��ʽ����ִ��
    Parameter: 
        appframe: ������Ϣ
        timeout: ��ʱʱ��
    Return: Ӧ����Ϣ
    Others: 
    """

    """
    ����һ��RPC����
    appframe - ������Ϣ�������˶Զ�ִ��������Ҫ����Ϣ
    timeout - ��ʱʱ��(��)

    ����ֵ: Ӧ����Ϣ�б�. ����б�Ϊ�գ����ʾû���յ�Ӧ��(��ʱ��)
    """

    if timeout > MAX_RPC_TIMEOUT:
        timeout = MAX_RPC_TIMEOUT
    
    rpc_context = RpcContext(appframe, timeout)
    
    get_rpc_worker().process_rpc_context(rpc_context)


    return rpc_context.get_ack_frames()
    
    
