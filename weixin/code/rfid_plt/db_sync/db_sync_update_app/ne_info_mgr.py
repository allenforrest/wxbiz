#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中实现了存放网元信息的类
Others:      
Key Class&Method List: 
             1. NEInfo: 存放网元信息的类
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
    Description: 网元信息的类
    Base: 
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

        #self.ip = ""
        self.id = 0
        self.pid = 0
        self.state = NE_STATE_NORMAL

    def is_state_normal(self):
        """
        Method: is_state_normal
        Description: 判断当前网元的数据同步状态是否是normal状态
        Parameter: 无
        Return: 
        Others: 
        """

        return self.state == NE_STATE_NORMAL

class NEInfoMgr:
    """
    Class: NEInfoMgr
    Description: 网元信息管理类
    Base: 
    Others: 
    """

    # pid到网元信息的map
    __ne_pid_to_ne = {}   

    # id到网元信息的map
    __ne_id_to_ne = {}    

    __lock = threading.Lock()
    
    @classmethod
    def refresh(cls, ne_id_pids):
        """
        Method: refresh
        Description: 更新网元信息
        Parameter: 
            ne_id_pids: 网元的id和pid信息
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
        Description: 根据网元的pid获取其id
        Parameter: 
            pid: 用于进程间通信的pid(名字服务分配的)
        Return: 网元的id。如果网元不存在，返回None
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
        Description: 根据网元的id获取pid
        Parameter: 
            ne_id: 网元的id
        Return: 网元的pid。如果网元不存在，返回None
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
        Description: 根据pid获取网元的数据同步状态
        Parameter: 
            pid: 网元的pid
        Return: 网元的状态，如果网元不存在，返回None
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
        Description: 判断网元的同步状态是否是normal状态
        Parameter: 
            ne_id: 网元的id
        Return: 网元的同步状态是否是normal状态
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
        Description: 将网元的数据同步状态设置为正在导出中
        Parameter: 
            ne_id: 网元的id
            mit_obj: mit对象
        Return: 错误码
        Others: 
        """

        # 只有当状态为正常时，才可以转为导出状态
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
                    
            # 更改DB中的状态
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
        Description: 将网元的数据同步状态设置为正在导入状态
        Parameter: 
            ne_id: 网元的id
            mit_obj: mit对象
        Return: 
        Others: 
        """

        # 只有当状态为导出状态时，才可以转为导入状态
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
                    
            # 更改DB中的状态
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
        Description: 将网元的数据同步状态设置为normal状态
        Parameter: 
            ne_id: 网元的id
            mit_obj: mit对象
            need_sync_full: 是否需要全同步, True or False
        Return: 
        Others: 
        """

        # 如果need_sync_full不为None，那么就会更改DB中的need_sync_full字段
        
        with cls.__lock:
            ne_info = cls.__ne_id_to_ne.get(ne_id)
            if ne_info is None:    
                tracelog.error("NE not found by ne_id(%d)" % ne_id)
                return -1
                                
            # 更改DB中的状态
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
        Description: 将网元是否需要全同步的标记
        Parameter: 
            ne_id: 网元的id
            mit_obj: mit对象
            need_sync_full: 是否需要全同步, True or False
        Return: 错误码
        Others: 
        """
        
        with cls.__lock:
            ne_info = cls.__ne_id_to_ne.get(ne_id)
            if ne_info is None:    
                tracelog.error("NE not found by ne_id(%d)" % ne_id)
                return -1
                                
            # 更改DB中的状态
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
