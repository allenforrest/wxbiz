#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: DbSyncUpdate APP�����������ݿ��ͬ��
Others:
Key Class&Method List:
    1. DBSyncApp
History:
1. Date:2013-03-23
   Author:ACP2013
   Modification:�½��ļ�
"""

import os
import sys
import importlib

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import mit
import tracelog
import err_code_mgr

import error_code

from dba import base, db_cfg_info
from dba import oradb
from dba.base import DBConnectionPool, DBConnectionInfo
from dba.error import DBConnectError, DBQueryError
from db_sync_data_manager import DBSyncDataManager

import db_sync_update_worker
import sync_full_exp_worker
import sync_full_imp_worker

from db_sync_util import DBSyncUtil

#from moc_db_sync import NEDbSyncState
from moc_db_sync import OraSyncPriority
import db_sync_mit
import db_sync_priority_mit
import cmd_code_def
import db_sync_base
import ne_info_mgr

class DBSyncUpdateApp(bf.BasicApp):
    """
    Class: DBSyncUpdateApp
    Description: �������ݿ�ͬ��App��,���������ݿ�����ͬ����Ϣ
    Base: BasicApp
    Others:
    """
    

    def __init__(self):
        """
        Method: __init__
        Description: �����ʼ������
        Parameter: ��
        Return:
        Others:
            __mit_manager��mit������
            _db_sync_update_worker, ͬ������������
        """
        bf.BasicApp.__init__(self, "DBSyncUpdateApp")
        self.__mit_manager = None
        self.__priority_mit_manager = None
        self.__connection_pool = None

        self.__synchronized_mocs = {}
        self.__sync_sns = {}

    def get_sync_sn(self, ne_id, priority):
        """
        Method: get_sync_sn
        Description: ��ȡ���һ��ִ�е�scn
        Parameter: 
            ne_id: ��ԪID
            priority: ���ȼ�
        Return: 
        Others: 
        """
        key = '%s_%d' % (ne_id, priority)
        if key not in self.__sync_sns:
            return -1
        return self.__sync_sns[key]

    def set_sync_sn(self, ne_id, priority, sync_sn):
        """
        Method: set_sync_sn
        Description: �������һ��ִ�е�ͬ��ID
        Parameter: 
            ne_id: ��ԪID
            priority: ���ȼ�
            sync_sn: ���һ��ͬ��ID
        Return: 
        Others: 
        """
        key = '%s_%d' % (ne_id, priority)
        if key in self.__sync_sns.keys():
            if self.__sync_sns[key] != sync_sn:
                self.__priority_mit_manager.update_event_id(ne_id, priority, sync_sn)
                self.__sync_sns[key] = sync_sn
        else:
            self.__sync_sns[key] = sync_sn

    def get_conn_pool(self):
        """
        Method: get_conn_pool
        Description: ��ȡDBConnetionPoolʵ��
        Parameter: ��
        Return: __connection_pool
        Others:
        """

        return self.__connection_pool

    def get_data_manager(self):
        """
        Method: get_data_manager
        Description: ��ȡDBSyncDataManagerʵ��
        Parameter: ��
        Return: __data_manager
        Others:
        """

        return self.__data_manager
      
    def get_mit_manager(self):
        """
        Method: get_mit_manager
        Description: ��ȡmit_manager����ʵ��
        Parameter: ��
        Return: __mit_manager
        Others:
        """

        return self.__mit_manager

    def get_connection_name(self):
        """
        Method: get_connection_name
        Description: �õ����ݿ����ӵı���
        """
        return db_cfg_info.ORACLE_SYNC_CON_NAME

    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: ����ʵ�ַ�����ע��MOC����
        Parameter: ��
        Return: 0���ɹ�
                ������ʧ��
        Others:
        """
        bf.BasicApp._ready_for_work(self)

        self.__mit_manager = db_sync_mit.DBSyncMit()
        ret = self.__mit_manager.reset_NE_state()
        if ret != 0:
            return ret

        # Register MOC objects to be synchonized
        curdir = os.path.join(self.get_app_top_path(), 'moc_def', 'moc_for_sync')
        DBSyncUtil.load_mocs(curdir, self.__synchronized_mocs)

        conn_info = oradb.ConnectionInfo(**db_cfg_info.get_configure(db_cfg_info.ORACLE_SYNC_CON_NAME))
        self.__connection_pool = DBConnectionPool()
        self.__connection_pool.create_connection(self.get_connection_name()
                                , conn_info
                                , oradb.create_connection
                                , 10)

        self.__data_manager = DBSyncDataManager(self)
        self.__data_manager.create_schemas(self.__synchronized_mocs.values())

        # ��ʼ��ͬ�����ȼ�����
        moc_priority = OraSyncPriority.OraSyncPriority()
        self.__data_manager.create_schemas([moc_priority], False);

        self.__priority_mit_manager = db_sync_priority_mit.DBSyncPriorityMit()
        rows = self.__priority_mit_manager.rdm_find(moc_priority.get_moc_name())
        tracelog.info('priority records: %d' % len(rows))
        for row in rows:
            tracelog.info('ne_id: %d, priority: %d, event_id: %d' % (row.ne_id, row.priority, row.event_id))
            self.set_sync_sn(row.ne_id, row.priority, row.event_id)

        # ��ʼ����Ԫ��Ϣ
        ret = self.__init_NE_info()
        if ret != 0:
            tracelog.info("initialize NE information failed.")
            return ret
       
        # Register db sync update worker
        work_thread = bf.WorkThread()
        self.register_worker(db_sync_update_worker.DBSyncUpdateWorker(), work_thread, False)
        self.register_worker(sync_full_exp_worker.SyncFullExpWorker(), work_thread, True)
        
        self.register_worker(sync_full_imp_worker.SyncFullImpWorker())
        
        return 0

    def get_moc(self, moc_name):
        """
        Method: load_moc
        Description: ����MOC����
        Parameter:
            moc_name: MOC������
        return: MOC����ʵ��
        Others: �Ҳ����ĳ��Ϸ���None
        """
        return self.__synchronized_mocs.get(moc_name)

    def get_synchronized_mocs(self):
        """
        Method: load_moc
        Description: ����MOC����
        Parameter:
            moc_name: MOC������
        return: MOC����ʵ��
        Others: �Ҳ����ĳ��Ϸ���None
        """
        return self.__synchronized_mocs


    def __init_NE_info(self):
        """
        Method: __init_NE_info
        Description: ��ʼ�����е���Ԫ��Ϣ
        Parameter: ��
        Return: 
        Others: 
        """

        # ��IMCDeviceMgr��ѯEAU ID��PID
        frame = bf.AppFrame()
        frame.set_cmd_code(cmd_code_def.CMD_QUERY_NE_ID_PID)
        frame.set_receiver_pid(self.get_pid("IMCDeviceMgr"))
        reponses = bf.rpc_request(frame, 5)
        if len(reponses) == 0:
            tracelog.error("query NE information from IMCDeviceMgr timeout.")
            return -1

        ret = self.on_NE_cfg_change(reponses[0])
        
        return ret

    def on_NE_cfg_change(self, frame):
        """
        Method: on_NE_cfg_change
        Description: ����Ԫ��Ϣ�����仯��Ĵ���ӿ�
        Parameter: 
            frame: AppFrameʵ��
        Return: 
        Others: 
        """

        ne_id_pids = db_sync_base.NEIDAndPidNotification.deserialize(frame.get_data())

        ret_code, ne_infos = self.__mit_manager.refresh_NE_info(ne_id_pids.ne_id_pids)
        if ret_code != 0:
            tracelog.error("NEInfoMgr.initialize failed. ret:%d" % ret)
            return ret

        ne_info_mgr.NEInfoMgr.refresh(ne_infos)
        return 0


if __name__=='__main__':
    DBSyncUpdateApp().run()
    
