#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��ж�������Ӧ��Ԫ�ڵ�����handler
Others:      
Key Class&Method List: 
             1. NotifyNEIdPidHandler: ��Ӧ��Ԫ�ڵ�����handler
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
    Description: ��Ӧ��Ԫ�ڵ�����handler
    Base: bf.CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: ������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """

        self.get_worker().get_app().on_NE_cfg_change(frame)


