#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-24
Description: 本文件中实现了处理RPC请求的handler
Others:      
Key Class&Method List: 
             1. RpcHandler: 处理RPC请求的handler
History: 
1. Date:
   Author:
   Modification:
"""



import tracelog
import err_code_mgr

from _bundleframework.cmdhandler.cmd_handler import CmdHandler



class RpcHandler(CmdHandler):
    """
    Class: RpcHandler
    Description: 处理RPC请求的handler
    Base: CmdHandler
    Others: 
    """


    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
            __rpc_context:RPC调用上下文
        """

        CmdHandler.__init__(self)
        
        self.__rpc_context = None
        
    def handle_cmd_context(self, rpc_context):
        """
        Method:    handle_cmd_context
        Description: 处理一次RPC请求
        Parameter: 
            rpc_context: RPC调用上下文
        Return: 
        Others: 
        """

        self.__rpc_context = rpc_context 

        # 将rpc_context中的命令发送出去，并且开始等待应答
        self.wait_for_ack(rpc_context.get_req_frame(), rpc_context.get_timeout())

        
    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 
        Parameter: 
            frame: 
        Return: 
        Others: 此处不需要处理任何事情
        """

        pass


    def _on_all_rounds_over(self, rounds):
        """
        Method:    _on_all_rounds_over
        Description: 收到RPC应答后的处理
        Parameter: 
            rounds: 
        Return: 
        Others: 
        """

        self.__rpc_context.set_ack_frames(rounds.values()[0].get_response_frames())
        self.over(0)


    def _on_over(self, result):
        """
        Method:    _on_over
        Description: RPC调用结束后的处理
        Parameter: 
            result: 
        Return: 
        Others: 有两种情况下，RPC调用会结束: 收到了应答或则超时
        """

        #if resutl != 0:
        #    self.__rpc_context.set_timeout_flag()

        self.__rpc_context.signal_event()

