#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ���ʵ���˸�������Ԫ���ݵ�worker
Others:      
Key Class&Method List: 
             1. SyncFullImpWorker: ��������Ԫ���ݵ�worker
History: 
1. Date:
   Author:
   Modification:
"""


import bundleframework as bf
import tracelog
import err_code_mgr
import cmd_code_def


import worker_taskid_define
import sync_full_imp_handler

class SyncFullImpWorker(bf.CmdWorker):
    """
    Class: SyncFullImpWorker
    Description: ��������Ԫ���ݵ�worker
    Base: bf.CmdWorker
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

        bf.CmdWorker.__init__(self, name = "SyncFullImpWorker"
                              ,min_task_id = worker_taskid_define.DB_SYNC_FULL_IMP_WORKER_MIN_TASK_ID
                              ,max_task_id = worker_taskid_define.DB_SYNC_FULL_IMP_WORKER_MAX_TASK_ID)
        

    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker��ʼ������
        Parameter: ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
        Others: 
        """


        handler = sync_full_imp_handler.SyncFullImpHandler()
        self.register_handler(handler, cmd_code_def.CMD_START_IMP_FULL)
        
        
        
        return 0

    def get_mit(self):
        """
        Method: get_mit
        Description: ��ȡmit����
        Parameter: ��
        Return: mit����
        Others: 
        """

        return self.get_app().get_mit_manager()
        