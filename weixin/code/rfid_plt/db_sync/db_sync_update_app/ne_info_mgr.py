#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ���ʵ���˴����Ԫ��Ϣ����
Others:      
Key Class&Method List: 
             1. NEInfo: �����Ԫ��Ϣ����
History: 
1. Date:
   Author:
   Modification:
"""

import threading

import tracelog
import bundleframework as bf
import mit


from db_sync_update_const import (NE_STATE_NORMAL
                            , NE_STATE_FULL_SYNC_IMP
                            , NE_STATE_FULL_SYNC_EXP)


class NEInfo:
    """
    Class: NEInfo
    Description: ��Ԫ��Ϣ����
    Base: 
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

        #self.ip = ""
        self.id = 0
        self.pid = 0
        self.state = NE_STATE_NORMAL

    def is_state_normal(self):
        """
        Method: is_state_normal
        Description: �жϵ�ǰ��Ԫ������ͬ��״̬�Ƿ���normal״̬
        Parameter: ��
        Return: 
        Others: 
        """

        return self.state == NE_STATE_NORMAL

class NEInfoMgr:
    """
    Class: NEInfoMgr
    Description: ��Ԫ��Ϣ������
    Base: 
    Others: 
    """

    # pid����Ԫ��Ϣ��map
    __ne_pid_to_ne = {}   

    # id����Ԫ��Ϣ��map
    __ne_id_to_ne = {}    

    __lock = threading.Lock()
    
    @classmethod
    def refresh(cls, ne_id_pids):
        """
        Method: refresh
        Description: ������Ԫ��Ϣ
        Parameter: 
            ne_id_pids: ��Ԫ��id��pid��Ϣ
        Return: 
        Others: 
        """

        #print "=== NEInfoMgr.refresh"
        with cls.__lock:
            cls.__ne_pid_to_ne.clear()
            cls.__ne_id_to_ne.clear()

            for ne_id, pid, state in ne_id_pids:
                item = NEInfo()
                item.id = ne_id
                item.pid = pid
                item.state = state
                cls.__ne_pid_to_ne[pid] = item
                cls.__ne_id_to_ne[ne_id] = item

                #print "=== refresh:", ne_id, pid, state
                



        
    @classmethod
    def get_ne_id_by_pid(cls, pid):
        """
        Method: get_ne_id_by_pid
        Description: ������Ԫ��pid��ȡ��id
        Parameter: 
            pid: ���ڽ��̼�ͨ�ŵ�pid(���ַ�������)
        Return: ��Ԫ��id�������Ԫ�����ڣ�����None
        Others: 
        """

        with cls.__lock:
            ne_info = cls.__ne_pid_to_ne.get(pid)
            if ne_info is not None:
                return ne_info.id
            
        return None

    @classmethod
    def get_ne_pid_by_id(cls, ne_id):
        """
        Method: get_ne_pid_by_id
        Description: ������Ԫ��id��ȡpid
        Parameter: 
            ne_id: ��Ԫ��id
        Return: ��Ԫ��pid�������Ԫ�����ڣ�����None
        Others: 
        """

        with cls.__lock:
            ne_info = cls.__ne_id_to_ne.get(ne_id)
            if ne_info is not None:
                return ne_info.pid
            
        return None
        
    @classmethod
    def get_ne_state_by_pid(cls, pid):
        """
        Method: get_ne_state_by_pid
        Description: ����pid��ȡ��Ԫ������ͬ��״̬
        Parameter: 
            pid: ��Ԫ��pid
        Return: ��Ԫ��״̬�������Ԫ�����ڣ�����None
        Others: 
        """

        with cls.__lock:
            ne_info = cls.__ne_pid_to_ne.get(pid)
            if ne_info is not None:
                return ne_info.state
        
        return None

    @classmethod
    def is_ne_state_normal(cls, ne_id):
        """
        Method: is_ne_state_normal
        Description: �ж���Ԫ��ͬ��״̬�Ƿ���normal״̬
        Parameter: 
            ne_id: ��Ԫ��id
        Return: ��Ԫ��ͬ��״̬�Ƿ���normal״̬
        Others: 
        """

        with cls.__lock:
            ne_info = cls.__ne_id_to_ne.get(ne_id)
            if ne_info is not None:
                return ne_info.state == NE_STATE_NORMAL
        
        return False


    @classmethod
    def change_ne_state_to_exp(cls, ne_id, mit_obj):
        """
        Method: change_ne_state_to_exp
        Description: ����Ԫ������ͬ��״̬����Ϊ���ڵ�����
        Parameter: 
            ne_id: ��Ԫ��id
            mit_obj: mit����
        Return: ������
        Others: 
        """

        # ֻ�е�״̬Ϊ����ʱ���ſ���תΪ����״̬
        with cls.__lock:
            ne_info = cls.__ne_id_to_ne.get(ne_id)
            if ne_info is None:    
                tracelog.error("NE not found by ne_id(%d)" % ne_id)
                return -1
            else:
                if ne_info.state != NE_STATE_NORMAL:
                    tracelog.error("can not change NE state(%d) to EXP, ne_id(%d)" % (
                                ne_info.state, ne_id))
                    return -1
                    
            # ����DB�е�״̬
            if mit_obj is not None:
                rdm = mit.RawDataMoi("NEDbSyncState"
                                        , ne_id = ne_id
                                        , sync_state = NE_STATE_FULL_SYNC_EXP)

                ret = mit_obj.rdm_mod(rdm)
                if ret.get_err_code() != 0:
                    tracelog.error("modify NE state to DB failed. ret:%d, %s" % (
                                ret.get_err_code()
                               , ret.get_msg()))
                    return ret.get_err_code()

                        
            ne_info.state = NE_STATE_FULL_SYNC_EXP

        return 0




    @classmethod
    def change_ne_state_to_imp(cls, ne_id, mit_obj):
        """
        Method: change_ne_state_to_imp
        Description: ����Ԫ������ͬ��״̬����Ϊ���ڵ���״̬
        Parameter: 
            ne_id: ��Ԫ��id
            mit_obj: mit����
        Return: 
        Others: 
        """

        # ֻ�е�״̬Ϊ����״̬ʱ���ſ���תΪ����״̬
        with cls.__lock:
            ne_info = cls.__ne_id_to_ne.get(ne_id)
            if ne_info is None:    
                tracelog.error("NE not found by ne_id(%d)" % ne_id)
                return -1
            else:
                if ne_info.state != NE_STATE_FULL_SYNC_EXP:
                    tracelog.error("can not change NE state(%d) to IMP, ne_id(%d)" % (
                                ne_info.state, ne_id))
                    return -1
                    
            # ����DB�е�״̬
            if mit_obj is not None:
                rdm = mit.RawDataMoi("NEDbSyncState"
                                        , ne_id = ne_id
                                        , sync_state = NE_STATE_FULL_SYNC_IMP)

                ret = mit_obj.rdm_mod(rdm)
                if ret.get_err_code() != 0:
                    tracelog.error("modify NE state to DB failed. ret:%d, %s" % (
                                ret.get_err_code()
                               , ret.get_msg()))
                    return ret.get_err_code()

                        
            ne_info.state = NE_STATE_FULL_SYNC_IMP

        return 0

    @classmethod
    def change_ne_state_to_normal(cls, ne_id, mit_obj, need_sync_full):
        """
        Method: change_ne_state_to_normal
        Description: ����Ԫ������ͬ��״̬����Ϊnormal״̬
        Parameter: 
            ne_id: ��Ԫ��id
            mit_obj: mit����
            need_sync_full: �Ƿ���Ҫȫͬ��, True or False
        Return: 
        Others: 
        """

        # ���need_sync_full��ΪNone����ô�ͻ����DB�е�need_sync_full�ֶ�
        
        with cls.__lock:
            ne_info = cls.__ne_id_to_ne.get(ne_id)
            if ne_info is None:    
                tracelog.error("NE not found by ne_id(%d)" % ne_id)
                return -1
                                
            # ����DB�е�״̬
            if mit_obj is not None:
                rdm = mit.RawDataMoi("NEDbSyncState"
                                        , ne_id = ne_id
                                        , sync_state = NE_STATE_NORMAL)

                if need_sync_full is True:
                    rdm.need_sync_full = 1
                elif need_sync_full is False:
                    rdm.need_sync_full = 0

                ret = mit_obj.rdm_mod(rdm)
                if ret.get_err_code() != 0:
                    tracelog.error("modify NE state to DB failed. ret:%d, %s" % (
                                 ret.get_err_code()
                               , ret.get_msg()))
                    return ret.get_err_code()

                        
            ne_info.state = NE_STATE_NORMAL

        return 0

    @classmethod
    def set_ne_need_sync_full(cls, ne_id, mit_obj, need_sync_full):
        """
        Method: set_ne_need_sync_full
        Description: ����Ԫ�Ƿ���Ҫȫͬ���ı��
        Parameter: 
            ne_id: ��Ԫ��id
            mit_obj: mit����
            need_sync_full: �Ƿ���Ҫȫͬ��, True or False
        Return: ������
        Others: 
        """
        
        with cls.__lock:
            ne_info = cls.__ne_id_to_ne.get(ne_id)
            if ne_info is None:    
                tracelog.error("NE not found by ne_id(%d)" % ne_id)
                return -1
                                
            # ����DB�е�״̬
            if mit_obj is not None:
                rdm = mit.RawDataMoi("NEDbSyncState"
                                        , ne_id = ne_id)

                if need_sync_full is True:
                    rdm.need_sync_full = 1
                elif need_sync_full is False:
                    rdm.need_sync_full = 0
                else:
                    raise Exception("need_sync_full invalid value:%r" % need_sync_full)

                ret = mit_obj.rdm_mod(rdm)
                if ret.get_err_code() != 0:
                    tracelog.error("modify NE state to DB failed. ret:%d, %s" % (
                                 ret.get_err_code()
                               , ret.get_msg()))
                    return ret.get_err_code()


        return 0
