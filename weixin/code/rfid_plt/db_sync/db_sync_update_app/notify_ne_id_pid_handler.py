#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中定义了响应网元节点变更的handler
Others:      
Key Class&Method List: 
             1. NotifyNEIdPidHandler: 响应网元节点变更的handler
History: 
1. Date:
   Author:
   Modification:
"""

import bundleframework as bf
import tracelog
import err_code_mgr
import mit


class NotifyNEIdPidHandler(bf.CmdHandler):
    """
    Class: NotifyNEIdPidHandler
    Description: 响应网元节点变更的handler
    Base: bf.CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """

        self.get_worker().get_app().on_NE_cfg_change(frame)


