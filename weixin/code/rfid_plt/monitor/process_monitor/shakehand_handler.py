#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-08
Description: ������ʵ���˴����������������Ϣ��handler
Others:      
Key Class&Method List: 
             1. ShakehandHandler: �����������������Ϣ��handler
History: 
1. Date:
   Author:
   Modification:
"""

import bundleframework as bf
import tracelog

from process_stat_mgr import ProcessStatMgr

class ShakehandHandler(bf.CmdHandler):
    """
    Class: ShakehandHandler
    Description: �����������������Ϣ��handler
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: ����������Ϣ
        Parameter: 
            frame: ������Ϣ
        Return: 
        Others: 
        """

        process_name = frame.get_data(0)
        statflag = frame.get_data(1)

        if statflag != bf.BasicApp.SHAKEHAND_STOPPING:

            ack_datas = ProcessStatMgr.get_shakehand_ack(process_name)
            self.get_worker().send_ack(frame, ack_datas)
        
        ProcessStatMgr.on_process_shakehand(frame.get_sender_pid(), process_name, statflag)

        
