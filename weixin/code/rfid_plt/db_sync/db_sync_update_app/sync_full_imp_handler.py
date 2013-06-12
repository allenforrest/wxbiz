#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ���ʵ���˽���Ԫ���ݵ��뵽���ݿ��handler

Others:      
Key Class&Method List: 
             1. ....
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
import mit
from dba import db_cfg_info

from ne_info_mgr import NEInfoMgr
import db_sync_update_const
import db_sync_common_const
import call_oracle_cmd


class SyncFullImpHandler(bf.CmdHandler):
    """
    Class: SyncFullImpHandler
    Description: ����Ԫ���ݵ��뵽���ݿ��handler
    Base: 
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
        
        tracelog.info("begin import NE(%d) data." % ne_id)
        
        ret = self.__decompress_data_file()
        if ret != 0:
            tracelog.error("decompress data file failed. NE id:%d" % self.ne_id)
            self.__change_ne_state_when_imp_failed()
            return
        tracelog.info("decompress data file ok. NE id:%d" % self.ne_id)

        ret = self.__delete_old_ne_data_in_db()
        if ret != 0:
            tracelog.error("delete old NE data in DB failed. NE id:%d" % self.ne_id)
            self.__change_ne_state_when_imp_failed()
            return
        tracelog.info("delete old NE data in DB ok. NE id:%d" % self.ne_id)

        ret = self.__call_oracle_imp()
        if ret != 0:
            tracelog.error("import NE data to DB failed. NE id:%d" % self.ne_id)
            self.__change_ne_state_when_imp_failed()
            return
        
        self.__change_ne_state_when_imp_ok()
        
        tracelog.info("import NE data ok. NE id:%d" % ne_id)
        
    def __change_ne_state_when_imp_failed(self):
        """
        Method: __change_ne_state_when_imp_failed
        Description: ��������Ԫ����ʧ�ܵ�ʱ���޸���Ԫ��״̬
        Parameter: ��
        Return: 
        Others: 
        """

           
        ret = NEInfoMgr.change_ne_state_to_normal(self.ne_id
                                            , self.get_worker().get_mit()
                                            , True)  

        if ret != 0:
            tracelog.error("__change_ne_state_when_imp_failed failed."
                            "ne_id:%d" % self.ne_id)


    def __change_ne_state_when_imp_ok(self):
        """
        Method: __change_ne_state_when_imp_ok
        Description: ��������Ԫ�����ݳɹ�ʱ�޸���Ԫ��״̬
        Parameter: ��
        Return: 
        Others: 
        """

        ret = NEInfoMgr.change_ne_state_to_normal(self.ne_id
                                            , self.get_worker().get_mit()
                                            , False)  

        if ret != 0:
            tracelog.error("__change_ne_state_when_imp_failed failed."
                            "ne_id:%d" % self.ne_id)


    def __decompress_data_file(self):
        """
        Method: __decompress_data_file
        Description: ����Ԫ�������ļ���ѹ��
        Parameter: ��
        Return: ������
        Others: 
        """

        zfile_path = os.path.join(self.get_worker().get_app().get_app_top_path()
                                , "data/ftp"
                                , db_sync_update_const.NE_DB_DUMP_COMPRESSED_PATH % self.ne_id
                                )
        # �ж��ļ��Ƿ����
        if not os.path.exists(zfile_path):
            tracelog.error("DB sync file of NE not exists! NE id:%d" %self.ne_id)
            return

        # ɾ���Ѿ����ڵ����ļ�
        dmp_file_path = os.path.join(self.get_worker().get_app().get_app_top_path()
                                , db_sync_common_const.DB_SYNC_DIR
                                )
        try:
            if os.path.exists(dmp_file_path):
                pass #os.remove(dmp_file_path)
        except:
            pass
            
        try:
            with zipfile.ZipFile(zfile_path, 'r', zipfile.ZIP_DEFLATED) as zfile:
                zfile.extract(db_sync_common_const.DB_SYNC_FILE_NAME, dmp_file_path)
        except:
            tracelog.exception("decompress file %s failed." % zfile_path)
            return -1
            
        return 0

    def __delete_old_ne_data_in_db(self):
        """
        Method: __delete_old_ne_data_in_db
        Description: ɾ����Ԫ�ϵ�����
        Parameter: ��
        Return: ������
        Others: 
        """

        # ɾ�����ݿ�����Ԫ��������
        try:
            con_pool = self.get_worker().get_app().get_conn_pool()
            with con_pool.get_connection(db_cfg_info.ORACLE_SYNC_CON_NAME) as db_con:                
                with db_con.get_query() as db_query:
                    mocs = self.get_worker().get_app().get_synchronized_mocs()
                    for moc in mocs.itervalues():
                        sql = 'delete from tbl_%s where "_SYNC_SOURCE"=:1' % moc.get_moc_name()
                        db_query.execute(sql, (self.ne_id,))

                
        except:
            tracelog.exception("delete old NE data in DB failed.")
            return -1
            
        return 0
    def __call_oracle_imp(self):
        """
        Method: __call_oracle_imp
        Description: ����oracle��impdp����
        Parameter: ��
        Return: ������
        Others: 
        """


        mocs = self.get_worker().get_app().get_synchronized_mocs()
        tables = ["tbl_"+moc.get_moc_name() for moc in mocs.itervalues()]
        timeout = len(tables)*300 + 300 # ��
              
        db_file_dir = os.path.join(self.get_worker().get_app().get_app_top_path()
                                , db_sync_common_const.DB_SYNC_DIR
                                )
                                
        ret = call_oracle_cmd.call_impdp(tables
                                            , db_file_dir
                                            , timeout)
        if ret != 0:
            tracelog.error("call_impdp failed. ret:%d" % ret)
            return -1
        
        return 0
    
