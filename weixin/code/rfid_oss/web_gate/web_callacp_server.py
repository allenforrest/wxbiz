#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 
Others:      
Key Class&Method List: 
             1. �����ж�������web֮�佻����callacp�ķ����
History: 
1. Date:
   Author:
   Modification:
"""

import bundleframework as bf
import pycallacp

import tracelog

import cmd_dispatch_map

WEB_GATE_SERVER_PORT = 7005

class WebCallAcpServer(bf.SimpleCallAcpSrv):
    """
    Class: WebCallAcpServer
    Description: web֮�佻����callacp�ķ����
    Base: SimpleCallAcpSrv
    Others: 
    """

    def __init__(self, app):
        """
        Method: __init__
        Description: ���캯��
        Parameter: 
            app: ����app����
        Return: 
        Others: 
        """

        bf.SimpleCallAcpSrv.__init__(self, app, WEB_GATE_SERVER_PORT)

        
    def on_msg_received(self, url_or_srv_name, msg):
        """
        Method: on_msg_received
        Description: ���յ���Ϣʱ�Ĵ���ӿ�
        Parameter:
            url_or_srv_name: �ͻ��˵�url
            msg: ��Ϣ
        Return:
        Others: 
        """
        cmd_code = msg.get_cmd_code()
        service_name, strategy = cmd_dispatch_map.get_duty_service(cmd_code)
        if service_name is None:
            tracelog.error("discard message(%d)" % cmd_code)
            return
        
        frame = self._msg_to_frame(url_or_srv_name, msg)

        # SimpleCallAcpSrv�н�sender_pid����Ϊ��CALLACPSRV_PID
        # ������Ҫ��������
        frame.set_sender_pid(self._app.get_my_pid())
        
        if frame is None:
            tracelog.error("_msg_to_frame failed, discard message(%d)" % cmd_code)
            return
            
        self._app.dispatch_frame_to_process_by_pid(self._app.get_pid(service_name, strategy)
                                                , frame)
        
        