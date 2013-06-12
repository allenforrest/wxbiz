#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: log的定时维护，log按日期打包，log打包任务情况查询
Others:      
Key Class&Method List: 
             1. MaintainLogWorker： worker类，负责handler的注册
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:新建文件
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
    Description: log的定时维护，log按日期打包，log打包任务情况查询
    Base: CmdWorker
    Others: 无
    """

    def __init__(self):
        """
        Method: __init__
        Description: 初始化
        Parameter: 无
        Return: 无
        Others: 无
        """
        
        bf.CmdWorker.__init__(self, name = "MaintainPackageLogWorker", min_task_id = 1 , max_task_id = 20000)       
    	self.__mit_manager = mit.Mit()
        self.__global_param = None  

    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: 注册该worker关联的handler，注册该worker关联的mit，加载全局变量，初始化MaintainLogManager
        Parameter: 无
        Return: 0
        Others: 无
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
        Description: 注册MtnLogMgrParamMoc，并且加载全局变量
        Parameter: 无
        Return: 无
        Others: 无
        """

        self.__mit_manager.init_mit_lock()
        self.__mit_manager.regist_moc(MtnLogMgrParamMoc.MtnLogMgrParamMoc, 
                                      MtnLogMgrParamMoc.MtnLogMgrParamMocRule)
                                      
                                      
        self.__mit_manager.open_sqlite("./maintainlog_manager.db")
        #self.__mit_manager.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME)) 
        
        #加载全局参数
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
        Description: 获取全局变量
        Parameter: 无
        Return: MtnLogMgrParamMoc中的全局变量
        Others: 无
        """

        return self.__global_param        

    def get_maintain_log_manager(self):
        """
        Method: get_maintain_log_manager
        Description: 获取MaintainLogManager
        Parameter: 无
        Return: MaintainLogManager
        Others: 无
        """

        return self.__maintain_log_manager
    
    def get_log_path(self):
        """
        Method: get_log_path
        Description: 获取日志文件路径
        Parameter: 无
        Return: 日志文件路径
        Others: 无
        """

        export_path = os.path.join(self.get_app().get_app_top_path(), 'log')        
        return export_path
    
    def get_export_log_path(self):
        """
        Method: get_export_log_path
        Description: 获取打包后日志文件的路径
        Parameter: 无
        Return: 打包后日志文件的路径
        Others: 无
        """

        export_path = os.path.join(self.get_app().get_app_top_path(), 'data', 'http', 'export_data', 'log')        
        return export_path
