#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中定义了用于数据同步优先级功能的mit
Others:      
Key Class&Method List: 
             1. DBSyncPriorityMit: 用于数据同步优先级功能的mit
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
    Description: 用于数据同步优先级功能的mit
    Base: mit.Mit
    Others: 
    """


    def __init__(self):
        """
        Method: __init__
        Description: 构造函数
        Parameter: 无
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
        Description: 根据优先级取得同步记录
        Paramters:
            ne_id: 网元ID
            priority: 优先级
        Return:
            返回同步记录，如果找不到返回None
        """
        data = self.rdm_find('OraSyncPriority', ne_id = ne_id, priority = priority)
        if (len(data) > 0):
            return data[0]
        return None

    def get_event_id(self, ne_id, priority):
        """
        Method: get_sn
        Description: 根据优先级取同步ID
        Paramters:
            ne_id: 网元ID
            priority: 优先级
        Return:
            返回最大的同步ID，如果找不到返回-1
        """
        info = self.get_priority_info(ne_id, priority)
        if info is None:
            return -1
        return info.event_id

    def update_event_id(self, ne_id, priority, event_id):
        """
        Method: update_event_id
        Description: 更新同步ID
        Paramters:
            ne_id: 网元ID
            priority: 优先级
            sn: 同步ID值
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
    