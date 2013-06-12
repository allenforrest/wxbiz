#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: Ŀ¼directory�Ķ�ʱά����Ŀ¼directory�����趨��С�������޸�ʱ��˳��ɾ�����ĵ�
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

import maintain_directory_handler
import maintain_directory_manager
import error_code

import mit
import MtnDirMonitorParamMOC


class MaintainDirectoryWorker(bf.Worker):    
    """
    Class: MaintainLogWorker
    Description: Ŀ¼�ļ��Ķ�ʱ��أ���������涨��С���ϱ� 
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

        bf.Worker.__init__(self, name = "MaintainDirectoryMonitorWorker")       
        
        self.__global_param = None
        
    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: ע�����worker������MonitorFileSizeTimeouthandler���������ݿ��������ʼ��MaintainDirectoryManager
        Parameter: ��
        Return: 0mit
        Others: ��
        """
        # ��ȡ���ݿ��е�������Ϣ
        self.get_directory_param()

        param = self.get_global_param()

        # �õ����Ŀ¼·��
        self.__maintain_directory_manager =  maintain_directory_manager.MaintainDirectoryManager(self, param, self.get_app().get_app_top_path())

        #���ü��Ŀ¼��С��handler
        handler = maintain_directory_handler.MonitorFileSizeTimeoutHandler()

        period = 300
        handler.start_timer(period, False)
        self.register_time_out_handler(handler)
        
        return 0

    def get_directory_param(self):
        """
        Method: get_param
        Description: ע��MtnDirMonitorParamMOC�������ݿ��ж�ȡ�趨����
        Parameter: ��
        Return: ��
        Others: ��
        """

        # ͨ��mit�õ����ݿ��������Ϣ
        mit_manager = mit.Mit()
        mit_manager.init_mit_lock()
        mit_manager.regist_moc(MtnDirMonitorParamMOC.MtnDirMonitorParamMOC, 
                                      MtnDirMonitorParamMOC.MtnDirMonitorParamMOCRule)
                                      
        mit_manager.open_sqlite("./maintaindirectory_manager.db")
        #mit_manager.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME)) 
        
        # �������ݿ��в���
        self.__global_param = mit_manager.rdm_find("MtnDirMonitorParamMOC")

        mit_manager.close()


    def get_global_param(self):
        """
        Method: get_global_param
        Description: ��ȡȫ�ֱ���
        Parameter: ��
        Return: MtnDirMonitorParamMOC�е�ȫ�ֱ���
        Others: ��
        """

        return self.__global_param
        
    def get_maintain_directory_manager(self):
        """
        Method: get_maintain_directory_manager
        Description: ��ȡMaintainDirectoryManager
        Parameter: ��
        Return: MaintainDirectoryManager
        Others: ��
        """

        return self.__maintain_directory_manager