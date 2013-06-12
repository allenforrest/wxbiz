#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-14
Description: 本文中实现了监控进程状态的worker
Others:      
Key Class&Method List: 
             1. ProcessMonitorWorker: 监控进程状态的worker
History: 
1. Date:
   Author:
   Modification:
"""
import os.path

import bundleframework as bf
import tracelog
from install_info import InstallInfo

from process_stat_mgr import ProcessStatMgr

from shakehand_handler import ShakehandHandler
from check_process_stat_time_handler import CheckProcessStatTimeHandler
from restart_acp_system_handler import RestartACPSystemHandler
from send_running_pid_time_handler import SendRunningPidTimeHandler

import plt_cmd_code_def

class ProcessMonitorWorker(bf.CmdWorker):
    """
    Class: ProcessMonitorWorker
    Description: 监控进程状态的worker
    Base: CmdWorker
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
        """

        bf.CmdWorker.__init__(self
                            , name = "ProcessMonitorWorker"
                            , min_task_id=1
                            , max_task_id=2000)

        # 从配置文件中读取的信息
        self._install_info = None
        
    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker初始化工作
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        ret = self.__load_app_info()
        if ret != 0:
            return ret
        
        handler = CheckProcessStatTimeHandler()
        handler.start_timer(1, False)
        self.register_time_out_handler(handler)

        handler = SendRunningPidTimeHandler()
        handler.start_timer(5, False)
        self.register_time_out_handler(handler)

        self.register_handler(ShakehandHandler(), bf.CMD_SHAKEHAND_WITH_MONITOR)
        self.register_handler(RestartACPSystemHandler(), plt_cmd_code_def.CMD_RESTART_ACP_SYSTEM)
        
        return 0

    def __load_install_info(self):
        """
        Method:    _load_install_info
        Description: 加载软件安装等相关的信息
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        

        self._install_info = InstallInfo()
        install_path = self.get_app().get_app_top_path()
        ret = self._install_info.load(os.path.join(install_path, "configure/install_info.xml"))
              
        return ret


    def __load_app_info(self):
        # 初始化进程的启动信息
        ret = self.__load_install_info()        
        if ret != 0:
            tracelog.error("_load_install_info() failed.")
            return ret 
        
        all_app_info = self._install_info.get_app_info()        
        for app in all_app_info:
            if app.get_service_name() == self.get_app().get_service_name():
                continue

            # 根据配置文件中的相对位置，获取绝对位置
            program_path = os.path.join(self.get_app().get_app_top_path()
                                        , app.get_program_path())
            
            for i in xrange(app.get_instance_num()):
                ProcessStatMgr.add_process('%s_%s'%(app.get_service_name(), i)
                                        , i
                                        , app.is_auto_run_on_master()
                                        , app.is_auto_run_on_slave()
                                        , app.is_exclude()
                                        , program_path)
        return 0
        
        
