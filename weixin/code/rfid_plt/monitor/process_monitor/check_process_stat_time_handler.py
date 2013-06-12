#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-25
Description: 本文中实现了定时核查进程状态的handler
Others:      
Key Class&Method List: 
             1. CheckProcessStatTimeHandler: 定时核查进程状态的handler
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
    Description: 定时核查进程状态的handler
    Base: TimeOutHandler
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
        """

        bf.TimeOutHandler.__init__(self)

        # 经过5秒之后，开始启动其他进程
        # 如果有的进程已经在运行，那么就会通过握手直接检测到了，不需要再启动
        self.__start_process_flag = 5 
        self.__notify_pids_flag = 0
        

    def time_out(self):

        ProcessStatMgr.check_process_stat()

        if self.__start_process_flag > 0:
            self.__start_process_flag -= 1
        else:        
            ProcessStatMgr.timer_process()
        
