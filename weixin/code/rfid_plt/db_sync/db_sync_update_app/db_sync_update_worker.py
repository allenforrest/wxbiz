#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: 本文件中实现了响应网元数据变更通知的类
Others:
Key Class&Method List:
    1. DBSyncWorker
History:
1. Date:2013-03-23
   Author:ACP2013
   Modification:新建文件
"""

import os.path
import datetime

import bundleframework as bf
import debug
import tracelog
import err_code_mgr
import cmd_code_def
import worker_taskid_define
import db_sync_mit
import mit

from ne_info_mgr import NEInfoMgr
from db_sync_base import DBSyncStatus
from db_sync_base import DBSyncResult
from db_sync_base import DBSyncObject, DBSyncEvent
from db_sync_base import DBSyncType, DBSyncOperationType
from db_sync_util import DBSyncUtil

from notify_ne_id_pid_handler import NotifyNEIdPidHandler

class DBSyncUpdateHandler(bf.CmdHandler):
    """
    Class: DBSyncUpdateHandler
    Description: 数据同步接收处理类
    Base: CmdHandler
    Others:
    """
    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 同步消息处理函数
        Parameter:
            frame: 请求消息
        Return: 无
        Others:
        """
        buf = frame.get_data()
        tracelog.info('received data from client at %s' % datetime.datetime.now().isoformat())
        ne_id = NEInfoMgr.get_ne_id_by_pid(frame.get_sender_pid())

        if ne_id is None:
            tracelog.error("received unknow data sync notification from NE, "
                            "pid:%d" % frame.get_sender_pid())
            return

        debug.info('ne id: %d' % (ne_id))

        # 如果网元正处于全同步中，那么直接忽视本次事件通知
        if not NEInfoMgr.is_ne_state_normal(ne_id):
            tracelog.info('database is full-synchonizing')
            return

        sync_object = DBSyncObject.deserialize(buf)
        result = DBSyncResult()
        result.id = sync_object.id
        debug.info('sync object id: %d' % sync_object.id)
       
        for event in sync_object.sync_events:
            if event.type == DBSyncType.FULL:
                self.__handle_full_sync_ntf(frame, ne_id, sync_object, event)
                self.get_worker().get_app().set_sync_sn(ne_id, event.priority, event.id)
                return

        events = []
        for event in sync_object.sync_events:
            sync_sn = self.get_worker().get_app().get_sync_sn(ne_id, event.priority)
            debug.info('ne_id: %d, priority: %d, event_id: %d sync_sn: %d' % (ne_id, event.priority, event.id, sync_sn))
            if event.id <= sync_sn:
                #该Event已经同步成功，重复提交将被忽略
                tracelog.info('event#%d was already synchonized.current sn: %d' % (event.id, sync_sn))
                result.event_ids.append(event.id)
            else:
                events.append(event)

        manager = self.get_worker().get_app().get_data_manager()
        debug.info('incremental sync starts')
        ret_code = manager.sync_data(events, ne_id)
        if ret_code != DBSyncStatus.ERROR_SUCCESS:
            tracelog.info('sync data failed. exit code: %d' % ret_code)
            if ret_code == DBSyncStatus.ERROR_CONFLICT:
                # 将EAU的状态设置为需要全同步
                NEInfoMgr.set_ne_need_sync_full(ne_id
                       , self.get_worker().get_app().get_mit_manager()
                       , True)
            # 不给EAU回应答；EAU收到收不到应答超时后，下次重试
            return

        for event in events:
            self.get_worker().get_app().set_sync_sn(ne_id, event.priority, event.id)
            debug.info('  event#%04d: return %d' % (event.id, ret_code))
            result.event_ids.append(event.id)

        self.__send_ack(frame, result.serialize())
        tracelog.info(result.event_ids)
        tracelog.info('sync processing completed.')

    def __handle_full_sync_ntf(self, frame, ne_id, sync_object, event):
        """
        Method: __handle_full_sync_ntf
        Description: 处理全同步事件通知
        Parameter:
            frame: 数据帧
            ne_id: 网元的ID
            sync_object: 同步传输对象
            event: 事件通知
        Return: 
        Others: 
        """
        
        tracelog.info('receive full sync notification from NE(%d)' % ne_id)
        
        error_code = NEInfoMgr.set_ne_need_sync_full(ne_id
                    , self.get_worker().get_app().get_mit_manager()
                    , True)
                    
        if error_code != 0:
            tracelog.error("set_ne_need_sync_full() failed: %d" % error_code)
            # 不给EAU回应答；EAU收到收不到应答后，下次重试
            return
            
        result = DBSyncResult()
        result.id = sync_object.id
        result.return_code = error_code
        result.error_message = ''
        result.event_ids = []
        self.__send_ack(frame, result.serialize())
    
    def __send_ack(self, req_frame, data):
        """
        Method: __send_ack
        Description: 发送应答消息给网元
        Parameter: 
            req_frame: 请求消息
            data: 应答消息的数据
        Return: 
        Others: 
        """

        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(req_frame)
        frame_ack.add_data(data)
        
        frame_ack.set_next_pid(self.get_worker().get_pid("EAUGate"))
        self.get_worker().dispatch_frame_to_process_by_pid(frame_ack.get_receiver_pid(), frame_ack)
        


class DBSyncUpdateWorker(bf.CmdWorker):
    """
    Class: DBSyncWorker
    Description: DBSync操作worker
    Base: CmdWorker
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

        bf.CmdWorker.__init__(self, name = "DBSyncUpdateWorker"
                              ,min_task_id = worker_taskid_define.DB_SYNC_WORKER_MIN_TASK_ID
                              ,max_task_id = worker_taskid_define.DB_SYNC_WORKER_MAX_TASK_ID)

    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: 注册同步消息处理handler
        Parameter: 无
        Return: 0，成功
        Others:
        """
        tracelog.info('ready for db sync update worker')

        handler = DBSyncUpdateHandler()
        self.register_handler(handler, cmd_code_def.CMD_SYNC_DATA)

        handler = NotifyNEIdPidHandler()
        self.register_handler(handler, cmd_code_def.CMD_NTF_NE_ID_PID)
        return 0

        


