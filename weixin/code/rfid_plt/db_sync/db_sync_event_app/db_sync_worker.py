#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: ���ļ���ʵ���˷������ݱ��֪ͨ��worker
Others:
Key Class&Method List:
    1. DBSyncWorker: �������ݱ��֪ͨ��worker
History:
1. Date:2013-03-23
   Author:ACP2013
   Modification:�½��ļ�
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
    Description: DBSync����worker
    Base: Worker
    Others:
    """

    def __init__(self):
        """
        Method: __init__
        Description: �����ʼ������
        Parameter: ��
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
        Description: ע��handler,���ö�ʱhandlerΪ1Сʱ����һ��
        Parameter: ��
        Return: 0���ɹ�
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


