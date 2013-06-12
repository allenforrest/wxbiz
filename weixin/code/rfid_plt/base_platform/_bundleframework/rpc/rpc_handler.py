#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-24
Description: ���ļ���ʵ���˴���RPC�����handler
Others:      
Key Class&Method List: 
             1. RpcHandler: ����RPC�����handler
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
    Description: ����RPC�����handler
    Base: CmdHandler
    Others: 
    """


    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
            __rpc_context:RPC����������
        """

        CmdHandler.__init__(self)
        
        self.__rpc_context = None
        
    def handle_cmd_context(self, rpc_context):
        """
        Method:    handle_cmd_context
        Description: ����һ��RPC����
        Parameter: 
            rpc_context: RPC����������
        Return: 
        Others: 
        """

        self.__rpc_context = rpc_context 

        # ��rpc_context�е�����ͳ�ȥ�����ҿ�ʼ�ȴ�Ӧ��
        self.wait_for_ack(rpc_context.get_req_frame(), rpc_context.get_timeout())

        
    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 
        Parameter: 
            frame: 
        Return: 
        Others: �˴�����Ҫ�����κ�����
        """

        pass


    def _on_all_rounds_over(self, rounds):
        """
        Method:    _on_all_rounds_over
        Description: �յ�RPCӦ���Ĵ���
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
        Description: RPC���ý�����Ĵ���
        Parameter: 
            result: 
        Return: 
        Others: ����������£�RPC���û����: �յ���Ӧ�����ʱ
        """

        #if resutl != 0:
        #    self.__rpc_context.set_timeout_flag()

        self.__rpc_context.signal_event()

