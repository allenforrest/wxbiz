#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-25
Description: ������ʵ���˶�ʱ�˲����״̬��handler
Others:      
Key Class&Method List: 
             1. CheckProcessStatTimeHandler: ��ʱ�˲����״̬��handler
History: 
1. Date:
   Author:
   Modification:
"""

import bundleframework as bf
import tracelog

from process_stat_mgr import ProcessStatMgr


class CheckProcessStatTimeHandler(bf.TimeOutHandler):
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

        # ����5��֮�󣬿�ʼ������������
        # ����еĽ����Ѿ������У���ô�ͻ�ͨ������ֱ�Ӽ�⵽�ˣ�����Ҫ������
        self.__start_process_flag = 5 
        self.__notify_pids_flag = 0
        

    def time_out(self):

        ProcessStatMgr.check_process_stat()

        if self.__start_process_flag > 0:
            self.__start_process_flag -= 1
        else:        
            ProcessStatMgr.timer_process()
        
