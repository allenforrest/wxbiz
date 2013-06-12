#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-30
Description: ���ļ���ʵ����ipc��ص�worker
Others:      
Key Class&Method List: 
             1. IpcSendWorker: ������Ϣ��worker
             2. IpcRecvWorker: ������Ϣ��worker
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
# ʹ��EIPC��PUB-SUBģʽ����ʹ��PUSH-POLLģʽ
# PUSH-POLLģʽ�´����ˮλʱ����������
# 1��PUSH-PULLģʽ�£�һ�������˸�ˮλ�������������ͣ��Ҳ����Զ������ϵ���Ϣ
#   ���Ѿ���ʱ����Ϣ��ѹ���µ���Ϣ���ͱ�������
# 2����������˸�ˮλ��ͬʱ��sendʱ��ָ��zmq.NOBLOCK������֣�
#   �����ˮλ���µ���Ϣ��������
#   �����ǰ���̴ﵽ�˸�ˮλ���ҶԶ�һֱû����������ô��ǰ�����޷��˳�
#  ����Ҫ���⴦�����OK������ʵ������������쳣������£��޷�ȷ��һ�������ߵ�
#    ���⴦��Ĵ��룩
################################################


DEBUG_LOG_IN_MSG = True
DEBUG_LOG_OUT_MSG = True

class IpcSendWorker(Worker):
    """
    Class: IpcSendWorker
    Description: ������Ϣ��worker
    Base: Worker
    Others: 
    """

    worker_name = "ipc_send_worker"

    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
            __mutex: ��
            __peer_sockets:����������app������Ϣ��socket
        """

        Worker.__init__(self, IpcSendWorker.worker_name)

        self.__mutex = threading.RLock()
        
        self.__peer_sockets = {}  # pid: (endpoint, socket)
        self.__context    = eipc.Context.instance()



    def on_process_app_register(self, all_app_infos):
        """
        Method:    on_process_app_register
        Description: ��Ӧregister�������Ϣ
        Parameter: 
            all_app_infos: ϵͳ�����н��̵�app_info
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

                # �رղ�����Ҫ��socket
                for url, socket in tmp.itervalues():
                    if socket is not None:
                        socket.close()
        except:
            tracelog.exception("IpcSendWorker.on_process_app_register failed.")
            
            
    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker��ʼ������
        Parameter: ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
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
        Description: ���д�����
        Parameter: 
            total_ready_frames: �ȴ�ִ�е��������Ŀ
        Return: 
        Others: 
        """

        frame, priority = self.pop_frame(0.8)
        if frame is not None:
            self.send_frame(frame)

    def send_frame(self, frame):
        """
        Method:    send_frame
        Description: ����һ����Ϣ
        Parameter: 
            frame: ��Ҫ���͵���Ϣ
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
                
                # ���贴��socket
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
    Description: ������Ϣ��worker
    Base: 
    Others: 
    """

    worker_name = "ipc_recv_worker"

    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            endpoint: ��app�󶨵�endpoint������appͨ�����ӵ���endpoint�󷽿ɷ�����Ϣ����
        Return: 
            __endpoint: ��app�󶨵�endpoint
            __socket: ���ڼ���״̬��socket
            __context:eipc��Context����
            __poll: eipc��Poller����
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
        Description: ��ȡendpoint
        Parameter: ��
        Return:endpoint
        Others: 
        """
        return self.__endpoint


    def __close_socket(self):
        """
        Method: __close_socket
        Description: �ر�socket
        Parameter: ��
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
        Description: �ڸ�������������ڿ��õĶ˿���
        Parameter: 
            ip: ��Ҫ�󶨵�IP
            min_port: ��ʼ�˿ں�
            max_port: �����˿ں�
            
        Return:������
        Others: 
        """
        if min_port == max_port:
            # �̶���ָ���Ķ˿�
            try_times = 1
        else:
            #��ೢ��100��
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
        Description: worker��ʼ������
        Parameter: ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
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
        Description: ���д�����
        Parameter: 
            total_ready_frames: �ȴ�ִ�е��������Ŀ
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
        
        
