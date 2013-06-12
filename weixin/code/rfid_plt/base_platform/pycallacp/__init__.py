#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中定义了python中使用的pycallacp时，处理网络事件的handler
Others:      
Key Class&Method List: 
             1. AcpEventHandler: python中使用的pycallacp时，处理网络事件的handler
History: 
1. Date:
   Author:
   Modification:
"""

from _pycallacp import *

class AcpEventHandler:
    """
    Class: AcpEventHandler
    Description: python中使用的pycallacp时，处理网络事件的handler
    Base: 无
    Others: 子类需要重新相关的接口
    """
    def __init__(self):
        self._callacp_inst = None
        
    # 设置pycallacp.CallAcpClient或pycallacp.CallAcpServer实例
    # 该方法是在pycallacp.CallAcpClient.set_event_handler（或CallAcpServer.set_event_handler）自动调用的
    # 不需要使用者手工调用
    def set_callacp_inst(self, callacp_inst):
        self._callacp_inst = callacp_inst
        
    # 响应事件: 连接到服务端失败
    def on_connect_failed(self, url_or_srv_name):
        pass

    # 响应事件: 连接到服务端OK
    def on_connect_ok(self, url_or_srv_name):
        pass

    # 响应事件: 连接断开
    def on_disconnect(self, url_or_srv_name):
        pass

    # 响应事件: 收到消息
    def on_msg_received(self, url_or_srv_name, msg):
        pass
    
    # 响应事件：接受了客户端
    def on_accept_client(self, url):
        pass