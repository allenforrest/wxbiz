#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中实现了定时发送变更通知的handler
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""

import threading
import datetime
import time

import bundleframework as bf
import debug
import tracelog
import err_code_mgr
import mit
import plt_const_def

import cmd_code_def

from dba import db_cfg_info

from db_sync_util import DBSyncUtil
from db_sync_base import DBSyncStatus
from db_sync_base import DBSyncResult
from db_sync_base import DBSyncObject, DBSyncEvent
from db_sync_base import DBSyncType, DBSyncOperationType
from db_sync_event_manager import DBSyncEventManager

class DBSyncTimeoutHandler(bf.TimeOutHandler):
    """
    Class: DBSyncTimeoutHandler
    Description: 数据同步定期处理类
    Base: TimeOutHandler
    Others:
    """

    def __init__(self):

        """
        Method: __init__
        Description: 初始化函数
        Parameter: 无
        Return: 无
        Others:
            _polling_count: 调用次数
            _sending_scn: 发送次数
        """
        bf.TimeOutHandler.__init__(self)
        self._polling_count = 1
        self._sending_scn = 0
        self.MAX_EVENT_NUMS = 100000

    def time_out(self):
        """
        Method: time_out
        Description: 定时处理函数
        Parameter: 无
        Return: 无
        Others:
        """
        tracelog.info('db synchonization started.[%d]' % self._polling_count)
        try:
            # Get data from database
            self._polling_count = self._polling_count + 1
            debug.info('get sync data from database')
            db_conn = self.get_worker().get_app().get_connection(db_cfg_info.ORACLE_SYNC_CON_NAME)
            with db_conn:
                manager = DBSyncEventManager(db_conn)
                if manager.get_total_num() >= self.MAX_EVENT_NUMS:
                    tracelog.info('event number exceeds to %d, so full-sync will start' % self.MAX_EVENT_NUMS)
                    manager.remove_all_events()
                    manager.add_full_event()
                    return;

                while True:
                    events = manager.get_events()
                    if len(events) == 0:
                        tracelog.info('no db synchonization data')
                        return
                    debug.info('sync event count: %d' % len(events))
                    full_event = None
                    incremental_events = []
                    for event in events:
                        if (event.type == DBSyncType.FULL):
                            full_event = event
                        else:
                            incremental_events.append(event)
                    if (full_event is None):
                        tracelog.info('incremental synchronization starts')
                        ret_code = self._handle_incremental_sync(incremental_events)
                        if ret_code != DBSyncStatus.ERROR_SUCCESS:
                            tracelog.info('db synchonization failed. exit code: %d' % ret_code)
                            return
                    else:
                        tracelog.info('full synchronization starts')
                        ret_code = self._handle_full_sync(full_event)
                        if (ret_code == DBSyncStatus.ERROR_SUCCESS):
                            manager.remove_all_events()
                        else:
                            tracelog.info('db synchonization failed. exit code: %d' % ret_code)
                        return
                    
        except:
            tracelog.exception('db synchonization failed')
        tracelog.info('db synchonization ended.')

    def _handle_full_sync(self, event):
        """
        Method: _handle_incremental_sync
        Description: 全同步
        Parameters:
            event: 全同步消息
        Return:
            0 成功
            非0 失败
        """
        #sync_mocs = self.get_worker().get_app().get_synchronized_mocs()
        data = self._generate_data([event])
        result = self._send_command(data)
        return result.return_code

    def _handle_incremental_sync(self, events):
        """
        Method: _handle_incremental_sync
        Description: 增量同步
        Return:
            0 成功
            非0 失败
        """
        data = self._generate_data(events)
        result = self._send_command(data)
        debug.info('  received response at %s' %  datetime.datetime.now().isoformat())
        debug.info('  sync object id: %d' % result.id)
        debug.info('  event_ids: %d' % len(result.event_ids))

        db_conn = self.get_worker().get_app().get_connection()
        with db_conn:
            manager = DBSyncEventManager(db_conn)
            if (result.return_code == DBSyncStatus.ERROR_SUCCESS):
                #同步成功的场合，删除该Event通知
                debug.info('event ids: %s' % str(result.event_ids))
                manager.remove_events(result.event_ids)
                tracelog.info('incremental sync completed.')
            else:
                debug.info('return code: %d, error message: %s, event ids: %s' % (result.return_code
                                                                                  ,result.error_message
                                                                                  ,result.event_ids))
                tracelog.error('incremental sync failed')
        return result.return_code

    def _generate_data(self, events):
        """
        Method: _generate_data
        Description: 生成同步对象数据
        Parameters:
            event: 数据库同步事件
        Return:
            同步对象数据
        Others:
        """
        self._sending_scn = self._sending_scn + 1
        data = DBSyncObject()
        data.sync_events = []
        data.id = self._sending_scn
        debug.info('sync object id: %d' % data.id)
        for event in events:
            e = DBSyncEvent()
            e.id = event.id
            e.type = event.type
            e.priority = event.priority
            e.target = event.target
            e.operation = event.operation
            e.data = event.data
            e.condition = event.condition
            data.sync_events.append(e)
            debug.info('  event#%04d: target=%s operation=%d priority=%d'% (event.id, e.target, e.operation, e.priority))
        return data

    def _send_command(self, data):
        """
        Method: _send_command
        Description: 发送命令到同步服务器
        Parameters:
            data: DBSyncObject对象
        Return:
            0 成功
            非0 失败
        Others:
        """
        # Send to target host for sync
        new_frame = bf.AppFrame()
        debug.info('cmd: CMD_SYNC_DATA(%d) ' % cmd_code_def.CMD_SYNC_DATA)
        new_frame.set_cmd_code(cmd_code_def.CMD_SYNC_DATA)
        new_frame.add_data(data.serialize())
        # 经过IMCGate转发
        new_frame.set_receiver_pid(plt_const_def.IMC_PID)
        new_frame.set_next_pid(self.get_worker().get_pid("IMCGate"))
        #new_frame.set_receiver_pid(self.get_worker().get_app().get_pid("DBSyncUpdateApp"))
        
        result = bf.rpc_request(new_frame, 10)
        if len(result) <= 0:
            tracelog.info("connection to server '%s' timeouted." % plt_const_def.IMC_PID)
            result = DBSyncResult()
            result.return_code = DBSyncStatus.ERROR_NETWORK
            return result
        frame = result[0]
        buf = frame.get_data()
        result = DBSyncResult.deserialize(buf)
        tracelog.info('received response from server: #%d' % result.id)
        return result
