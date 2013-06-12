#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��ж�����python��ʹ�õ�pycallacpʱ�����������¼���handler
Others:      
Key Class&Method List: 
             1. AcpEventHandler: python��ʹ�õ�pycallacpʱ�����������¼���handler
History: 
1. Date:
   Author:
   Modification:
"""

from _pycallacp import *

class AcpEventHandler:
    """
    Class: AcpEventHandler
    Description: python��ʹ�õ�pycallacpʱ�����������¼���handler
    Base: ��
    Others: ������Ҫ������صĽӿ�
    """
    def __init__(self):
        self._callacp_inst = None
        
    # ����pycallacp.CallAcpClient��pycallacp.CallAcpServerʵ��
    # �÷�������pycallacp.CallAcpClient.set_event_handler����CallAcpServer.set_event_handler���Զ����õ�
    # ����Ҫʹ�����ֹ�����
    def set_callacp_inst(self, callacp_inst):
        self._callacp_inst = callacp_inst
        
    # ��Ӧ�¼�: ���ӵ������ʧ��
    def on_connect_failed(self, url_or_srv_name):
        pass

    # ��Ӧ�¼�: ���ӵ������OK
    def on_connect_ok(self, url_or_srv_name):
        pass

    # ��Ӧ�¼�: ���ӶϿ�
    def on_disconnect(self, url_or_srv_name):
        pass

    # ��Ӧ�¼�: �յ���Ϣ
    def on_msg_received(self, url_or_srv_name, msg):
        pass
    
    # ��Ӧ�¼��������˿ͻ���
    def on_accept_client(self, url):
        pass