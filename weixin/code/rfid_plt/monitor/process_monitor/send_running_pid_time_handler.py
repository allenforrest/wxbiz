#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ������ʵ���˶�ʱ֪ͨmaster��ǰ�ڵ����������е�app��pid
Others:      
Key Class&Method List: 
             
History: 
1. Date:
   Author:
   Modification:
"""

import bundleframework as bf
import tracelog

from process_stat_mgr import ProcessStatMgr
from name import name_msg_def
import monitor_cmd_code

class SendRunningPidTimeHandler(bf.TimeOutHandler):
    """
    Class: CheckProcessStatTimeHandler
    Description: ��ʱ�˲����״̬��handler
    Base: TimeOutHandler
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
        """

        bf.TimeOutHandler.__init__(self)

    def time_out(self):
        master_monitor_pid = self.get_worker().get_pid("Monitor", bf.MASTER_PID)
        if master_monitor_pid == bf.INVALID_PID:
            # ��ʱmaster���ܻ�û���о�����
            return
            
        # ֪ͨ���ַ��������Ϣ
        msg = name_msg_def.NotifyRunningPidsMsg()
        msg.running_pids = ProcessStatMgr.get_running_process_pids()

        frame = bf.AppFrame()
        frame.set_cmd_code(monitor_cmd_code.CMD_NOTIFI_RUNNING_PIDS)
        frame.set_receiver_pid(master_monitor_pid)
        frame.add_data(msg.serialize())
        self.get_worker().dispatch_frame_to_process_by_pid(frame.get_receiver_pid(), frame)
        
            
            
            
        

