#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: log�Ķ�ʱά����log�����ڴ����log������������ѯ
Others:      
Key Class&Method List: 
             1. MaintainLogWorker�� worker�࣬����handler��ע��
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:�½��ļ�
"""

import os

import bundleframework as bf
import tracelog
import err_code_mgr
import command_code
from dba import db_cfg_info

import maintain_log_handler
import maintain_log_manager
import error_code

import mit
import MtnLogMgrParamMoc
import copy

class MaintainLogWorker(bf.CmdWorker):    
    """
    Class: MaintainLogWorker
    Description: log�Ķ�ʱά����log�����ڴ����log������������ѯ
    Base: CmdWorker
    Others: ��
    """

    def __init__(self):
        """
        Method: __init__
        Description: ��ʼ��
        Parameter: ��
        Return: ��
        Others: ��
        """
        
        bf.CmdWorker.__init__(self, name = "MaintainPackageLogWorker", min_task_id = 1 , max_task_id = 20000)       
    	self.__mit_manager = mit.Mit()
        self.__global_param = None  

    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: ע���worker������handler��ע���worker������mit������ȫ�ֱ�������ʼ��MaintainLogManager
        Parameter: ��
        Return: 0
        Others: ��
        """
        ret = self.register_mit()
        if ret != 0:
            tracelog.error("initialize mit failed.")
            return ret
        
        self.register_handler(maintain_log_handler.PackageLogHandler(), command_code.MAINTAIN_PACKAGE_LOG_COMMAND)
        self.register_handler(maintain_log_handler.PackageLogExportTaskQueryHandler(), command_code.MAINTAIN_PACKAGELOG_TASK_QUERY)
        param = self.get_global_param()
        self.__maintain_log_manager = maintain_log_manager.MaintainLogManager(self.get_log_path()
                                                                              ,self.get_export_log_path()
                                                                              ,param.max_running_export_task
                                                                              )
        handler = maintain_log_handler.ZipLogFileTimeoutHandler()
        period = 10*60
        handler.start_timer(period, False)

        self.register_time_out_handler(handler)
        
        return 0

    def register_mit(self):
        """
        Method: register_mit
        Description: ע��MtnLogMgrParamMoc�����Ҽ���ȫ�ֱ���
        Parameter: ��
        Return: ��
        Others: ��
        """

        self.__mit_manager.init_mit_lock()
        self.__mit_manager.regist_moc(MtnLogMgrParamMoc.MtnLogMgrParamMoc, 
                                      MtnLogMgrParamMoc.MtnLogMgrParamMocRule)
                                      
                                      
        self.__mit_manager.open_sqlite("./maintainlog_manager.db")
        #self.__mit_manager.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME)) 
        
        #����ȫ�ֲ���
        rdms = self.__mit_manager.rdm_find("MtnLogMgrParamMoc")
        if len(rdms)!=1:
            tracelog.error("can't load the default global parameter(MtnLogMgrParamMoc)")
            return 1
        else:
            self.__global_param = copy.copy(rdms[0])

        return 0

    def get_global_param(self):
        """
        Method: get_global_param
        Description: ��ȡȫ�ֱ���
        Parameter: ��
        Return: MtnLogMgrParamMoc�е�ȫ�ֱ���
        Others: ��
        """

        return self.__global_param        

    def get_maintain_log_manager(self):
        """
        Method: get_maintain_log_manager
        Description: ��ȡMaintainLogManager
        Parameter: ��
        Return: MaintainLogManager
        Others: ��
        """

        return self.__maintain_log_manager
    
    def get_log_path(self):
        """
        Method: get_log_path
        Description: ��ȡ��־�ļ�·��
        Parameter: ��
        Return: ��־�ļ�·��
        Others: ��
        """

        export_path = os.path.join(self.get_app().get_app_top_path(), 'log')        
        return export_path
    
    def get_export_log_path(self):
        """
        Method: get_export_log_path
        Description: ��ȡ�������־�ļ���·��
        Parameter: ��
        Return: �������־�ļ���·��
        Others: ��
        """

        export_path = os.path.join(self.get_app().get_app_top_path(), 'data', 'http', 'export_data', 'log')        
        return export_path
