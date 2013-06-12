#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中实现了定时检查需要全同步的网元的handler和发起全同步的handler
Others:      
Key Class&Method List: 
             1. SyncFullCheckTimerHandler: 定时检查需要全同步的网元的handler
             2. StartSyncFullHandler: 向网元发起全同步的handler
History: 
1. Date:
   Author:
   Modification:
"""

import os.path, os

import bundleframework as bf
import tracelog
import err_code_mgr
import mit


from ne_info_mgr import NEInfoMgr
import db_sync_update_const
import cmd_code_def
import db_sync_base


class SyncFullCheckTimerHandler(bf.TimeOutHandler):
    """
    Class: SyncFullCheckTimerHandler
    Description: 定时检查需要全同步的网元的handler
    Base: bf.TimeOutHandler
    Others: 
    """

    def time_out(self):
        """
        Method: time_out
        Description: 定时处理函数
        Parameter: 无
        Return: 无
        Others:
        """

        # 从DB中读取全同步的请求
        _mit = self.get_worker().get_mit()

        ne_stats = _mit.rdm_find("NEDbSyncState"
                        , need_sync_full = 1
                        , sync_state = db_sync_update_const.NE_STATE_NORMAL)

        for ne_stat in ne_stats:
            # 启动同步
            frame = bf.AppFrame()
            frame.set_cmd_code(cmd_code_def.CMD_START_EXP_FULL)
            frame.add_data(str(ne_stat.ne_id))
            self.get_worker().dispatch_frame_to_worker("SyncFullExpWorker", frame)
            
        


class StartSyncFullHandler(bf.CmdHandler):
    """
    Class: StartSyncFullHandler
    Description: 向网元发起全同步的handler
    Base: bf.CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        ne_id = int(frame.get_data())
        self.ne_id = ne_id

        # 获取内存中的状态
        # 如果已经在同步了，那么就不用理会本次请求
        ret = NEInfoMgr.change_ne_state_to_exp(ne_id, self.get_worker().get_mit())        
        if ret != 0:
            tracelog.error("can not start sync full task. ne_id: %d" % ne_id)
            return
        
        tracelog.info("start sync full, ne_id:%d" % ne_id)

        # 如果不存在需要同步的MOC，那么就直接退出
        mocs = self.get_worker().get_app().get_synchronized_mocs()
        if len(mocs) == 0:
            tracelog.info("NE has no MOC to sync, ne_id:%d" % ne_id)
            NEInfoMgr.change_ne_state_to_normal(self.ne_id
                                                , self.get_worker().get_mit()
                                                , False)
            return
            
        if self.__prepare_file_dir() != 0:
            tracelog.error("can not start sync full task. ne_id: %d" % ne_id)
            self.__change_ne_state_when_exp_failed(True)
            return

        
        # 获取NE的pid，向其发起同步
        self.__send_request_to_ne()
        

    def __prepare_file_dir(self):
        """
        Method: __prepare_file_dir
        Description: 准备文件目录，用于让网元上传数据文件
        Parameter: 无
        Return: 错误码
        Others: 
        """

        file_path = os.path.join(self.get_worker().get_app().get_app_top_path()
                                , "data/ftp"
                                , db_sync_update_const.NE_DB_DUMP_COMPRESSED_PATH % self.ne_id
                                )

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            tracelog.exception("remove old file %s failed." % file_path)
            return -1

        # 如果目录不存在，那么就需要建立目录
        file_dir =  os.path.join(self.get_worker().get_app().get_app_top_path()
                                , "data/ftp/NE/%d/db_sync" % self.ne_id)
        try:
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
        except:
            tracelog.exception("make dir %s failed." % file_dir)
            return -1
            
        
        return 0
            
    def __send_request_to_ne(self):
        """
        Method: __send_request_to_ne
        Description: 发送导出命令给网元
        Parameter: 无
        Return: 
        Others: 
        """

        ne_pid = NEInfoMgr.get_ne_pid_by_id(self.ne_id)
        if ne_pid is None:
            tracelog.error("get_ne_pid_by_id(%d) failed." % self.ne_id)
            return 

        req = db_sync_base.SyncFullRequest()
        req.ne_id = self.ne_id
        req.ftp_ip = self.get_worker().get_app().get_device_cfg_info().get_device_external_ip()
        req.ftp_port = db_sync_update_const.FTP_SERVER_PORT
        req.file_path = db_sync_update_const.NE_DB_DUMP_COMPRESSED_PATH % self.ne_id  # 位于data/ftp目录中
        req.ftp_user = "ftp_user" # TODO
        req.ftp_pwd = "ftp_user" # TODO

       
        frame = bf.AppFrame()
        frame.set_cmd_code(cmd_code_def.CMD_SYNC_NE_EXP_FULL)
        frame.add_data(req.serialize())
        frame.set_receiver_pid(ne_pid)

        
        
        frame.set_next_pid(self.get_worker().get_pid("EAUGate"))

        mocs = self.get_worker().get_app().get_synchronized_mocs()
        timeout = len(mocs)*400 + 400
        self.wait_for_ack(frame, timeout) # 超时时间，单位秒




    def _on_round_over(self, round_id, r):
        """
        Method:    _on_round_over
        Description: 响应round结束的事件
        Parameter: 
            round_id: round的id
            r: round对象
        Return: 
        Others: 
        """
        try:
            frame = r.get_response_frame()            
            rep = db_sync_base.SyncFullResponse.deserialize(frame.get_data())                           
        except:        
            tracelog.exception("_on_round_over error, NE id:%d" % self.ne_id)
            self.__change_ne_state_when_exp_failed(True)
            return

        if rep.return_code == err_code_mgr.ER_SYNC_NO_TABLE_NEED_SYNC:
            tracelog.info("the NE has no table to sync.")
            # 这种情况下，直接认为同步结束，并且不用再重试
            self.__change_ne_state_when_exp_failed(False)
            return
            
        
        if rep.return_code != 0:
            tracelog.error("NE export data failed. ne id:%d, error:%d,%s" % (
                              self.ne_id
                            , rep.return_code
                            , rep.description))
                            
            self.__change_ne_state_when_exp_failed(True)
            return
        
        tracelog.info("NE export data ok. ne id:%d" % (self.ne_id))

        # 将NE的状态修改为导入中
        ret = NEInfoMgr.change_ne_state_to_imp(self.ne_id
                                               , self.get_worker().get_mit())
        if ret != 0:
            tracelog.error("change_ne_state_to_imp failed. ne_id:%d" % self.ne_id)
        
        
        # 开始执行导入
        frame = bf.AppFrame()
        frame.set_cmd_code(cmd_code_def.CMD_START_IMP_FULL)
        frame.add_data(str(self.ne_id))
        self.get_worker().dispatch_frame_to_worker("SyncFullImpWorker", frame)
        

    def __change_ne_state_when_exp_failed(self, need_retry):
        """
        Method: __change_ne_state_when_exp_failed
        Description: 当网元导出失败时，修改网元状态
        Parameter: 
            need_retry: 是否需要下次全同步
        Return: 
        Others: 
        """

        ret = NEInfoMgr.change_ne_state_to_normal(self.ne_id
                                                , self.get_worker().get_mit()
                                                , need_retry)
        if ret != 0:
            tracelog.error("__change_ne_state_when_exp_failed failed."
                            "ne_id:%d" % self.ne_id)

    def _on_round_timeout(self, round_id, r):
        """
        Method:    _on_round_timeout
        Description: 响应round超时事件
        Parameter: 
            round_id: round的id
            r: round对象
        Return: 
        Others: 
        """
        tracelog.error("NE export data timeout. ne id:%d" % (self.ne_id))
        self.__change_ne_state_when_exp_failed(True)
        
