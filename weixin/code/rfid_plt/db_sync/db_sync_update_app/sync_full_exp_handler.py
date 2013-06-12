#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ���ʵ���˶�ʱ�����Ҫȫͬ������Ԫ��handler�ͷ���ȫͬ����handler
Others:      
Key Class&Method List: 
             1. SyncFullCheckTimerHandler: ��ʱ�����Ҫȫͬ������Ԫ��handler
             2. StartSyncFullHandler: ����Ԫ����ȫͬ����handler
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
    Description: ��ʱ�����Ҫȫͬ������Ԫ��handler
    Base: bf.TimeOutHandler
    Others: 
    """

    def time_out(self):
        """
        Method: time_out
        Description: ��ʱ������
        Parameter: ��
        Return: ��
        Others:
        """

        # ��DB�ж�ȡȫͬ��������
        _mit = self.get_worker().get_mit()

        ne_stats = _mit.rdm_find("NEDbSyncState"
                        , need_sync_full = 1
                        , sync_state = db_sync_update_const.NE_STATE_NORMAL)

        for ne_stat in ne_stats:
            # ����ͬ��
            frame = bf.AppFrame()
            frame.set_cmd_code(cmd_code_def.CMD_START_EXP_FULL)
            frame.add_data(str(ne_stat.ne_id))
            self.get_worker().dispatch_frame_to_worker("SyncFullExpWorker", frame)
            
        


class StartSyncFullHandler(bf.CmdHandler):
    """
    Class: StartSyncFullHandler
    Description: ����Ԫ����ȫͬ����handler
    Base: bf.CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: ������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        ne_id = int(frame.get_data())
        self.ne_id = ne_id

        # ��ȡ�ڴ��е�״̬
        # ����Ѿ���ͬ���ˣ���ô�Ͳ�����᱾������
        ret = NEInfoMgr.change_ne_state_to_exp(ne_id, self.get_worker().get_mit())        
        if ret != 0:
            tracelog.error("can not start sync full task. ne_id: %d" % ne_id)
            return
        
        tracelog.info("start sync full, ne_id:%d" % ne_id)

        # �����������Ҫͬ����MOC����ô��ֱ���˳�
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

        
        # ��ȡNE��pid�����䷢��ͬ��
        self.__send_request_to_ne()
        

    def __prepare_file_dir(self):
        """
        Method: __prepare_file_dir
        Description: ׼���ļ�Ŀ¼����������Ԫ�ϴ������ļ�
        Parameter: ��
        Return: ������
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

        # ���Ŀ¼�����ڣ���ô����Ҫ����Ŀ¼
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
        Description: ���͵����������Ԫ
        Parameter: ��
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
        req.file_path = db_sync_update_const.NE_DB_DUMP_COMPRESSED_PATH % self.ne_id  # λ��data/ftpĿ¼��
        req.ftp_user = "ftp_user" # TODO
        req.ftp_pwd = "ftp_user" # TODO

       
        frame = bf.AppFrame()
        frame.set_cmd_code(cmd_code_def.CMD_SYNC_NE_EXP_FULL)
        frame.add_data(req.serialize())
        frame.set_receiver_pid(ne_pid)

        
        
        frame.set_next_pid(self.get_worker().get_pid("EAUGate"))

        mocs = self.get_worker().get_app().get_synchronized_mocs()
        timeout = len(mocs)*400 + 400
        self.wait_for_ack(frame, timeout) # ��ʱʱ�䣬��λ��




    def _on_round_over(self, round_id, r):
        """
        Method:    _on_round_over
        Description: ��Ӧround�������¼�
        Parameter: 
            round_id: round��id
            r: round����
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
            # ��������£�ֱ����Ϊͬ�����������Ҳ���������
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

        # ��NE��״̬�޸�Ϊ������
        ret = NEInfoMgr.change_ne_state_to_imp(self.ne_id
                                               , self.get_worker().get_mit())
        if ret != 0:
            tracelog.error("change_ne_state_to_imp failed. ne_id:%d" % self.ne_id)
        
        
        # ��ʼִ�е���
        frame = bf.AppFrame()
        frame.set_cmd_code(cmd_code_def.CMD_START_IMP_FULL)
        frame.add_data(str(self.ne_id))
        self.get_worker().dispatch_frame_to_worker("SyncFullImpWorker", frame)
        

    def __change_ne_state_when_exp_failed(self, need_retry):
        """
        Method: __change_ne_state_when_exp_failed
        Description: ����Ԫ����ʧ��ʱ���޸���Ԫ״̬
        Parameter: 
            need_retry: �Ƿ���Ҫ�´�ȫͬ��
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
        Description: ��Ӧround��ʱ�¼�
        Parameter: 
            round_id: round��id
            r: round����
        Return: 
        Others: 
        """
        tracelog.error("NE export data timeout. ne id:%d" % (self.ne_id))
        self.__change_ne_state_when_exp_failed(True)
        
