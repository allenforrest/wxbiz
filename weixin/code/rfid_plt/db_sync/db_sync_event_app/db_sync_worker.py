#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: 本文件中实现了发送数据变更通知的worker
Others:
Key Class&Method List:
    1. DBSyncWorker: 发送数据变更通知的worker
History:
1. Date:2013-03-23
   Author:ACP2013
   Modification:新建文件
"""


import bundleframework as bf
import tracelog
import err_code_mgr
import cmd_code_def

import db_sync_exp_handler
import db_sync_timer_handler

import db_sync_event_const



class DBSyncWorker(bf.CmdWorker):
    """
    Class: DBSyncWorker
    Description: DBSync操作worker
    Base: Worker
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
        bf.CmdWorker.__init__(self
            , name = "DBSyncWorker"
            , min_task_id = db_sync_event_const.DB_SYNC_WORKER_TASKID_MIN
            , max_task_id = db_sync_event_const.DB_SYNC_WORKER_TASKID_MAX)
            

    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: 注册handler,设置定时handler为1小时触发一次
        Parameter: 无
        Return: 0，成功
        Others:
        """
        tracelog.info('ready for db sync worker')

        handler = db_sync_timer_handler.DBSyncTimeoutHandler()
        period = 5 # 60*60
        handler.start_timer(period, False)
        self.register_time_out_handler(handler)

        self.register_handler(db_sync_exp_handler.DBSyncExportHandler()
                        , cmd_code_def.CMD_SYNC_NE_EXP_FULL)

        return 0


