#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中实现了负责与网元全同步导出的worker
Others:      
Key Class&Method List: 
             1. SyncFullExpWorker: 负责与网元全同步导出的worker
History: 
1. Date:
   Author:
   Modification:
"""


import bundleframework as bf
import tracelog
import err_code_mgr
import cmd_code_def


import sync_full_exp_handler
import worker_taskid_define


class SyncFullExpWorker(bf.CmdWorker):
    """
    Class: SyncFullExpWorker
    Description: 负责与网元全同步导出的worker
    Base: bf.CmdWorker
    Others: 
    """


    def __init__(self):
        """
        Method: __init__
        Description: 对象初始化函数
        Parameter: 无
        Return:
        Others:
        """

        bf.CmdWorker.__init__(self, name = "SyncFullExpWorker"
                              ,min_task_id = worker_taskid_define.DB_SYNC_FULL_EXP_WORKER_MIN_TASK_ID
                              ,max_task_id = worker_taskid_define.DB_SYNC_FULL_EXP_WORKER_MAX_TASK_ID)
        

    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker初始化函数
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        handler = sync_full_exp_handler.SyncFullCheckTimerHandler()
        handler.start_timer(3, False)
        self.register_time_out_handler(handler)

        handler = sync_full_exp_handler.StartSyncFullHandler()
        self.register_handler(handler, cmd_code_def.CMD_START_EXP_FULL)
        
        
        
        return 0

    def get_mit(self):
        """
        Method: get_mit
        Description: 获取mit对象
        Parameter: 无
        Return: 
        Others: 
        """

        return self.get_app().get_mit_manager()
        