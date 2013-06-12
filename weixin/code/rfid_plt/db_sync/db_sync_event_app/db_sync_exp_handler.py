#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ���ʵ���˴������ݵ��������handler
Others:      
Key Class&Method List: 
             1. DBSyncExportHandler: �������ݵ��������handler
History: 
1. Date:
   Author:
   Modification:
"""

import os.path
import zipfile 


import bundleframework as bf
import tracelog
import err_code_mgr
from utility import ftp_action
import plt_const_def
from dba import db_cfg_info

from db_sync_event_manager import DBSyncEventManager


import cmd_code_def
import db_sync_base

import call_oracle_cmd
import db_sync_common_const


class DBSyncExportHandler(bf.CmdHandler):
    """
    Class: DBSyncExportHandler
    Description: �������ݵ��������handler
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
        req = db_sync_base.SyncFullRequest.deserialize(frame.get_data())
        self.req = req
        self.db_file_dir = os.path.join(self.get_worker().get_app().get_app_top_path()
                            ,  db_sync_common_const.DB_SYNC_DIR)

        self.db_file_path = os.path.join(self.db_file_dir
                            , db_sync_common_const.DB_SYNC_FILE_NAME)
        
        tmp_pwd = req.ftp_pwd
        req.ftp_pwd = "******"
        tracelog.info("start to export data for sync full. %r" % req)
        req.ftp_pwd = tmp_pwd
        
        # ɾ��ͬ������ȫ����¼������ȫͬ��֪ͨ��
        ret = self.__delete_all_sync_events()
        if ret != 0:
            self.__send_ack(frame, ret)
            return        
        
        ret = self.__init_sync_table_data()
        if ret != 0:
            self.__send_ack(frame, ret)
            return
        tracelog.info("init sync table data ok.")
        
        # ��������
        ret = self.__export_data()
        if ret != 0:
            self.__send_ack(frame, ret)
            return
        tracelog.info("export data ok.")
        
        ret = self.__compress_data()
        if ret != 0:
            self.__send_ack(frame, ret)
            return
        tracelog.info("compress data ok.")
        
        ret = self.__upload_data()
        if ret != 0:
            self.__send_ack(frame, ret)
            return
        tracelog.info("upload data ok.")
        
        self.__send_ack(frame, 0)

    def __send_ack(self, req_frame, ret, msg=None):
        """
        Method: __send_ack
        Description: ����Ӧ����Ϣ
        Parameter: 
            req_frame: ������Ϣ
            ret: ������
            msg: ������Ϣ
        Return: 
        Others: 
        """

        if msg is None:
            msg = err_code_mgr.get_error_msg(ret)
            
        rep = db_sync_base.SyncFullResponse()
        rep.ne_id = self.req.ne_id
        rep.return_code = ret        
        rep.description = msg

        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(req_frame)
        frame_ack.add_data(rep.serialize())
        frame_ack.set_receiver_pid(plt_const_def.IMC_PID)        
        frame_ack.set_next_pid(self.get_worker().get_pid("IMCGate"))
        self.get_worker().dispatch_frame_to_process_by_pid(plt_const_def.IMC_PID, frame_ack)
        
        #self.get_worker().send_ack(req_frame, )

    def __delete_all_sync_events(self):
        """
        Method: __delete_all_sync_events
        Description: ɾ�����ݿ���ȫ�����������֪ͨ
        Parameter: ��
        Return: ������
        Others: 
        """    
        try:
            con_pool = self.get_worker().get_app().get_conn_pool()
            with con_pool.get_connection(db_cfg_info.ORACLE_SYNC_CON_NAME) as con:
                DBSyncEventManager(con).remove_all_events()
        except:
            tracelog.exception("delete all sync events failed.")
            return err_code_mgr.ER_SYNC_EXPORT_DATA_FAILED

        return 0
        
    def __delete_old_sync_table_data(self):
        """
        Method: __delete_old_sync_table_data
        Description: ɾ��ͬ�����е�������
        Parameter: ��
        Return: ������
        Others: 
        """
        
        try:
            con_pool = self.get_worker().get_app().get_conn_pool()
            with con_pool.get_connection(db_cfg_info.ORACLE_SYNC_CON_NAME) as con:
                with con.get_query() as db_query:
                    sqls = self.get_worker().get_app().get_moc_data_to_sync_tbl_sqls()
                    for table_name, sql in sqls:
                        db_query.execute("truncate table user_sync.%s" % table_name)
        except:
            tracelog.exception("__delete_old_sync_table_data failed.")
            return -1
            
        return 0

        
    def __lock_table(self, db_con):
        """
        Method: __lock_table
        Description: �������ݱ�tbl_OraSyncEvent
        Parameter: 
            db_con: oracle���ݿ�����
        Return: ������
        Others: tbl_OraSyncEvent�������������Ӳ����޸ĸñ���
        """

        # ��֪ͨ����ס����������������д
        # ���������޸�MOCʱ����д֪ͨ��
        # ��������������Ҳͬ�������޸���Щ��Ҫͬ����MOC����
        try:
            with db_con.get_query() as db_query:
                db_query.execute("LOCK TABLE tbl_OraSyncEvent IN SHARE MODE")
                
                # ���֪ͨ��, ȫͬ���󣬲���Ҫ����֮ǰ������֪ͨ��
                db_query.execute("DELETE FROM tbl_OraSyncEvent")
                    
        except:
            tracelog.exception("lock table tbl_OraSyncEvent failed.")
            return -1
                   
        
        return 0

    def __commit_tran(self, db_con):
        """
        Method: __commit_tran
        Description: �ύ����
        Parameter: 
            db_con: ���ݿ�����
        Return: ������
        Others: 
        """

        try:
            db_con.commit()
        except:
            tracelog.exception("commit transaction failed.")
            return -1
            
        return 0

    def __update_sync_table(self):
        """
        Method: __update_sync_table
        Description: ��������ͬ����
        Parameter: 
            db_con: ���ݿ�����
        Return: ������
        Others: 
        """


        try:
            sqls = self.get_worker().get_app().get_moc_data_to_sync_tbl_sqls()
            #tables = ["tbl_"+moc.get_moc_name() for moc in mocs.itervalues()]

            # ����ʹ����һ�����ݿ����ӣ�
            # Ϊ�˷�ֹinsert���������������ÿ�ű�������ύ����
            con_pool = self.get_worker().get_app().get_conn_pool()
            with con_pool.get_connection(db_cfg_info.ORACLE_DEFAULT_CON_NAME, False) as db_con:                 
                          
                for table_name, sql in sqls:
                    #print "===", sql   
                    db_con.begin()
                    try:
                        with db_con.get_query() as db_query:  
                            db_query.execute(sql, (self.req.ne_id, ))  
                            db_con.commit()
                    except:
                        db_con.rollback()
                
        except:
            tracelog.exception("update sync table failed.")
            return -1
        return 0
        
        
    def __init_sync_table_data(self):
        """
        Method: __init_sync_table_data
        Description: ��ʼ������ͬ������MOC���ݣ���user_acp�û�
                     ͬ����user_sync�û��ı���
        Parameter: ��
        Return: ������
        Others: 
        """

        ret = self.__delete_old_sync_table_data()
        if ret != 0:            
            return err_code_mgr.ER_SYNC_EXPORT_DATA_FAILED

        con_pool = self.get_worker().get_app().get_conn_pool()
        with con_pool.get_connection(db_cfg_info.ORACLE_DEFAULT_CON_NAME, False) as db_con:   
            db_con.begin()
            ret = self.__lock_table(db_con)
            if ret != 0:
                db_con.rollback()
                return err_code_mgr.ER_SYNC_EXPORT_DATA_FAILED
                
            tracelog.info("lock table ok.")
                         
            ret = self.__update_sync_table()
            if ret != 0:
                db_con.rollback()
                return err_code_mgr.ER_SYNC_EXPORT_DATA_FAILED

            db_con.commit()
            
        return ret
        
    def __export_data(self):
        """
        Method: __export_data
        Description: ��������
        Parameter: ��
        Return: ������
        Others: 
        """


        mocs = self.get_worker().get_app().get_synchronized_mocs()
        tables = ["tbl_"+moc.get_moc_name() for moc in mocs.itervalues()]
        if len(tables) == 0:
            tracelog.error("No table need to sync.")
            return err_code_mgr.ER_SYNC_NO_TABLE_NEED_SYNC
            
        timeout = len(tables)*300 + 300 # ��
        

        ret = call_oracle_cmd.call_expdp(tables, self.db_file_dir, timeout)
        if ret != 0:
            tracelog.error("call_expdp failed. ret:%d" % ret)
            return err_code_mgr.ER_SYNC_EXPORT_DATA_FAILED
        
        return 0

    def __compress_data(self):
        """
        Method: __compress_data
        Description: ѹ�������ļ�
        Parameter: ��
        Return: ������
        Others: 
        """

        try:
            zfile_path = os.path.join(self.db_file_dir
                                , db_sync_common_const.DB_SYNC_COMPRESSED_FILE_NAME)

            # ��ɾ�����ܴ��ڵ����ļ�
            if os.path.exists(zfile_path):
                os.remove(zfile_path)
    
            with zipfile.ZipFile(zfile_path, 'w', zipfile.ZIP_DEFLATED) as zfile:
                zfile.write(self.db_file_path, db_sync_common_const.DB_SYNC_FILE_NAME)

            self.db_file_path = zfile_path
        except:
            tracelog.exception("compress data failed.")
            return err_code_mgr.ER_SYNC_EXPORT_DATA_FAILED

        return 0

    def __upload_data(self):
        """
        Method: __upload_data
        Description: ���������ļ�
        Parameter: ��
        Return: ������
        Others: 
        """


        # ����3��
        for i in xrange(3):
            ret, msg = ftp_action.upload_file(self.req.ftp_ip
                            , self.req.ftp_port
                            , self.req.ftp_user
                            , self.req.ftp_pwd
                            , self.db_file_path
                            , self.req.file_path)
            if ret == 0:
                break
                            
        if ret != 0:
            tracelog.error("upload file %s to (%s, %d) failed. %s" % (
                              self.db_file_path
                            , self.req.ftp_ip
                            , self.req.ftp_port
                            , msg))
        return ret
        
        
