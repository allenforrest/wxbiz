#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTPD NTP服务配置的worker，该worker负责配置NTPD服务设置，打开关闭NTP服务，获取NTPD服务设置的信息，并且启动时还原NTPD服务设置
Others: 无   
Key Class&Method List: 
             1. NtpdWorker：worker类，负责handler的注册，并且还原NTPD服务设置
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:新建文件
"""

    
import bundleframework as bf
import tracelog
import err_code_mgr
import mit
from dba import db_cfg_info

import error_code
import command_code
import ntpd_params
import NtpdSubnetMOC
import NtpdServerMOC
import NtpdControlMOC
import custom_NtpdSubnetMOCRule
import custom_NtpdServerMOCRule
import custom_NtpdControlMOCRule
import ntpd_handler
import ntpd_set

class NtpdWorker(bf.CmdWorker):
    """
    Class: NtpdWorker
    Description: NTPD NTP服务配置的worker，该worker负责配置NTPD服务设置，打开关闭NTP服务，获取NTPD服务设置的信息，并且启动时还原NTPD服务设置
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

        bf.CmdWorker.__init__(self, name = "NtpdWorker", min_task_id=1, max_task_id=20000)
        self._mit_manager = mit.Mit()
        
    def ready_for_work(self): 
        """
        Method: ready_for_work
        Description: 注册该worker关联的handler，注册该worker关联的mit，并且还原NTPD服务设置
        Parameter: 无
        Return: isrestore，是否成功还原NTPD服务的错误码
        Others: 无
        """
        
        self.register_mit_for_work()
        self.register_handler_for_work()
        isrestore = NtpdWorker.restore_ntp_data(self)
        return isrestore
    
    def register_mit_for_work(self):
        """
        Method: register_mit_for_work
        Description: 注册该worker关联的mit
        Parameter: 无
        Return: 无
        Others: 无
        """

        self._mit_manager.init_mit_lock()
        self._mit_manager.regist_moc(NtpdSubnetMOC.NtpdSubnetMOC, custom_NtpdSubnetMOCRule.CustomNtpdSubnetMOC)
        self._mit_manager.regist_moc(NtpdServerMOC.NtpdServerMOC, custom_NtpdServerMOCRule.CustomNtpdSubnetMOC)
        self._mit_manager.regist_moc(NtpdControlMOC.NtpdControlMOC, custom_NtpdControlMOCRule.CustomNtpdContolMOC)
        self._mit_manager.regist_complex_attr_type(ntpd_params.NtpdServer)
        self._mit_manager.regist_complex_attr_type(ntpd_params.NtpdSubnet) 
        self._mit_manager.open_sqlite("./ntpd.db") 
        #self._mit_manager.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME)) 
        
    def register_handler_for_work(self):
        """
        Method: register_handler_for_work
        Description: 注册该worker关联的handler
        Parameter: 无
        Return: 无
        Others: 无
        """

        self.register_handler(ntpd_handler.AddSubnetHandler(), command_code.NTPD_ADD_SUBNET_COMMAND)
        self.register_handler(ntpd_handler.AddServerHandler(), command_code.NTPD_ADD_SERVER_COMMAND)
        self.register_handler(ntpd_handler.GetServerHandler(), command_code.NTPD_GET_SERVER_COMMAND)
        self.register_handler(ntpd_handler.GetSubnetHandler(), command_code.NTPD_GET_SUBNET_COMMAND)
        self.register_handler(ntpd_handler.DelServerHandler(), command_code.NTPD_DEL_SERVER_COMMAND)
        self.register_handler(ntpd_handler.DelSubnetHandler(), command_code.NTPD_DEL_SUBNET_COMMAND)
        self.register_handler(ntpd_handler.NtpdServerControlHandler(), command_code.NTPD_CONTROL_COMMAND)
    
    def get_mit_manager(self):
        """
        Method: get_mit_manager
        Description: 获取worker注册过的mit
        Parameter: 无
        Return: _mit_manager，注册过的mit
        Others: 无
        """

        return self._mit_manager
    
    def send_ack(self, frame, datas):
        """
        Method: send_ack
        Description: 向发出请求的进程发送处理结果的错误码
        Parameter: 
            frame: 收到的要处理的消息
            datas: 发送处理结果的消息
        Return: 无
        Others: 无
        """

        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(frame)        
        for data in datas:
            frame_ack.add_data(data)
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)
        
    def restore_ntp_data(self):    
        """
        Method: restore_ntp_data
        Description: 还原NTPD服务数据
        Parameter: 无
        Return: return_code，还原NTPD服务数据处理结果的错误码
        Others: 无
        """

        return_code, description = ntpd_set.ntpd_write(self._mit_manager) 
        return return_code
