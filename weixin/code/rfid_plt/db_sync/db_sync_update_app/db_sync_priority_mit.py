#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��ж�������������ͬ�����ȼ����ܵ�mit
Others:      
Key Class&Method List: 
             1. DBSyncPriorityMit: ��������ͬ�����ȼ����ܵ�mit
History: 
1. Date:
   Author:
   Modification:
"""

import mit
import debug
import tracelog

from dba import db_cfg_info
from moc_db_sync import OraSyncPriority

class DBSyncPriorityMit(mit.Mit):
    """
    Class: DBSyncPriorityMit
    Description: ��������ͬ�����ȼ����ܵ�mit
    Base: mit.Mit
    Others: 
    """


    def __init__(self):
        """
        Method: __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
        """

        mit.Mit.__init__(self)

        self.regist_moc(OraSyncPriority.OraSyncPriority, OraSyncPriority.OraSyncPriorityRule)

        self.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_SYNC_CON_NAME)) 

        self.init_mit_lock()

    def get_priority_info(self, ne_id, priority):
        """
        Method: get_priority_info
        Description: �������ȼ�ȡ��ͬ����¼
        Paramters:
            ne_id: ��ԪID
            priority: ���ȼ�
        Return:
            ����ͬ����¼������Ҳ�������None
        """
        data = self.rdm_find('OraSyncPriority', ne_id = ne_id, priority = priority)
        if (len(data) > 0):
            return data[0]
        return None

    def get_event_id(self, ne_id, priority):
        """
        Method: get_sn
        Description: �������ȼ�ȡͬ��ID
        Paramters:
            ne_id: ��ԪID
            priority: ���ȼ�
        Return:
            ��������ͬ��ID������Ҳ�������-1
        """
        info = self.get_priority_info(ne_id, priority)
        if info is None:
            return -1
        return info.event_id

    def update_event_id(self, ne_id, priority, event_id):
        """
        Method: update_event_id
        Description: ����ͬ��ID
        Paramters:
            ne_id: ��ԪID
            priority: ���ȼ�
            sn: ͬ��IDֵ
        Return:
        """
        info = self.get_priority_info(ne_id, priority)
        if info is None:
            info = OraSyncPriority.OraSyncPriority()
            info.ne_id = ne_id
            info.priority = priority
            info.event_id = event_id
            self.rdm_add(info)
        elif info.event_id != event_id:
            info.event_id = event_id
            self.rdm_mod(info)
        debug.info('ne_id:%d priority:%d event_id:%d' % (ne_id, priority, event_id))
    