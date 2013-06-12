#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: 目录directory的定时维护：目录directory超过设定大小，按照修改时间顺序删除旧文档
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

import maintain_directory_handler
import maintain_directory_manager
import error_code

import mit
import MtnDirMonitorParamMOC


class MaintainDirectoryWorker(bf.Worker):    
    """
    Class: MaintainLogWorker
    Description: 目录文件的定时监控，如果超过规定大小，上报 
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

        bf.Worker.__init__(self, name = "MaintainDirectoryMonitorWorker")       
        
        self.__global_param = None
        
    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: 注册与该worker关联的MonitorFileSizeTimeouthandler，加载数据库参数，初始化MaintainDirectoryManager
        Parameter: 无
        Return: 0mit
        Others: 无
        """
        # 获取数据库中的配置信息
        self.get_directory_param()

        param = self.get_global_param()

        # 得到监控目录路径
        self.__maintain_directory_manager =  maintain_directory_manager.MaintainDirectoryManager(self, param, self.get_app().get_app_top_path())

        #设置监控目录大小的handler
        handler = maintain_directory_handler.MonitorFileSizeTimeoutHandler()

        period = 300
        handler.start_timer(period, False)
        self.register_time_out_handler(handler)
        
        return 0

    def get_directory_param(self):
        """
        Method: get_param
        Description: 注册MtnDirMonitorParamMOC，从数据库中读取设定参数
        Parameter: 无
        Return: 无
        Others: 无
        """

        # 通过mit得到数据库的配置信息
        mit_manager = mit.Mit()
        mit_manager.init_mit_lock()
        mit_manager.regist_moc(MtnDirMonitorParamMOC.MtnDirMonitorParamMOC, 
                                      MtnDirMonitorParamMOC.MtnDirMonitorParamMOCRule)
                                      
        mit_manager.open_sqlite("./maintaindirectory_manager.db")
        #mit_manager.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME)) 
        
        # 加载数据库中参数
        self.__global_param = mit_manager.rdm_find("MtnDirMonitorParamMOC")

        mit_manager.close()


    def get_global_param(self):
        """
        Method: get_global_param
        Description: 获取全局变量
        Parameter: 无
        Return: MtnDirMonitorParamMOC中的全局变量
        Others: 无
        """

        return self.__global_param
        
    def get_maintain_directory_manager(self):
        """
        Method: get_maintain_directory_manager
        Description: 获取MaintainDirectoryManager
        Parameter: 无
        Return: MaintainDirectoryManager
        Others: 无
        """

        return self.__maintain_directory_manager