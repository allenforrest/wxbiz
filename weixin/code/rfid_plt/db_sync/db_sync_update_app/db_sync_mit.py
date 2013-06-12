#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��ж�������������ͬ�����ܵ�mit
Others:      
Key Class&Method List: 
             1. DBSyncMit: ��������ͬ�����ܵ�mit
History: 
1. Date:
   Author:
   Modification:
"""


import mit
import tracelog

from dba import db_cfg_info
from moc_db_sync import NEDbSyncState
import db_sync_update_const

class DBSyncMit(mit.Mit):
    """
    Class: DBSyncMit
    Description: ��������ͬ�����ܵ�mit
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

        
        self.regist_moc(NEDbSyncState.NEDbSyncState
                                , NEDbSyncState.NEDbSyncStateRule)

        self.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME)) 

        self.init_mit_lock()

    def get_NE_info(self, ne_id):
        """
        Method: get_NE_info
        Description: ȡ����Ԫ��Ϣ
        """
        data = self.rdm_find("NEDbSyncState", ne_id = ne_id)
        if len(data) > 0:
            return data[0]
        return None

    def update_NE_info(self, ne_info):
        """
        Method: update_NE_info
        Description:������Ԫ��Ϣ
        """
        return self.rdm_mod(ne_info)
        
    def refresh_NE_info(self, ne_id_pids):
        """
        Method: refresh_NE_info
        Description: ���¸�����Ԫ����Ϣ
        Parameter: 
            ne_id_pids: ��Ԫ��id��pid��Ϣ
        Return: �����룬���е���Ԫ��Ϣ
        Others: 
        """

        # ne_id_pids�Ľṹ: [[ne_id, pid]...]
        
        all_ne_infos =[] # [(ne_id,pid,state)...]

        with self.get_lock():
            # ��DB�ж�ȡ��ȫ������Ϣ
            ne_states_in_db = {}
            for item in self.rdm_find("NEDbSyncState"):
                ne_states_in_db[item.ne_id] = item

            mit_tran = mit.MitTran(self)
            with mit_tran:
            
                # ɾ��DB���ϵļ�¼
                ret = self.remove_all("NEDbSyncState")
                if ret.get_err_code() != 0:
                    tracelog.error("remove all NEDbSyncState failed. ret:%d, %s" % (
                          ret.get_err_code()
                        , ret.get_msg()))
                    mit_tran.rollback()
                    return ret.get_err_code(), all_ne_infos
                    
                # �����µļ�¼            
                for ne_id, pid in ne_id_pids:
                    old_rdm = ne_states_in_db.get(ne_id)
                    if old_rdm is None:
                        need_sync_full = 1
                        sync_state = db_sync_update_const.NE_STATE_NORMAL
                        sync_sn = 0
                    else:
                        need_sync_full = old_rdm.need_sync_full
                        sync_state = old_rdm.sync_state
                        sync_sn = old_rdm.sync_sn

                    all_ne_infos.append((ne_id, pid, sync_state))
                    
                    rdm = mit.RawDataMoi("NEDbSyncState"
                                        , ne_id = ne_id
                                        , need_sync_full = need_sync_full
                                        , sync_state = sync_state
                                        , sync_sn = sync_sn)
                    
                    ret = self.rdm_add(rdm)
                    if ret.get_err_code() != 0:
                        tracelog.error("add NEDbSyncState failed. ret:%d, %s" % (
                              ret.get_err_code()
                            , ret.get_msg()))
                        mit_tran.rollback()

                    
                        return ret.get_err_code(), all_ne_infos
            
        return 0, all_ne_infos



    def reset_NE_state(self):
        """
        Method: reset_NE_state
        Description: ������Ԫ��״̬
        Parameter: ��
        Return: ������
        Others: ��ȫͬ��δ�����ģ�������Ϊ��Ҫȫͬ�������ӿ��ڽ���������ʼ��ʱ����
        """

        # mit����ʱ������Щ֮ǰ״̬Ϊ��normal�ģ�����Ϊnormal��
        # �����Ƿ���Ҫͬ������Ϊ1
        multisql = mit.MultiSQL()
        multisql.set_oracle_sql(('update tbl_NEDbSyncState '
                                'set "need_sync_full"=1, "sync_state"=%d '
                                'where "sync_state"<>%d') % (
                                   db_sync_update_const.NE_STATE_NORMAL
                                 , db_sync_update_const.NE_STATE_NORMAL))
        multisql.set_sqlite_sql(('update tbl_NEDbSyncState '
                                'set [need_sync_full]=1, [sync_state]=%d '
                                'where [sync_state]<>%d') % (
                                   db_sync_update_const.NE_STATE_NORMAL
                                 , db_sync_update_const.NE_STATE_NORMAL))
                 
        ret = self.raw_exec_ex("NEDbSyncState", multisql)

        if ret.get_err_code() != 0:
            tracelog.error("update tbl_NEDbSyncState failed. %d, %s" % (
                            ret.get_err_code()
                          , ret.get_msg()))
            return ret.get_err_code() 

        return 0
        