#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTPD NTP�������õ�worker����worker��������NTPD�������ã��򿪹ر�NTP���񣬻�ȡNTPD�������õ���Ϣ����������ʱ��ԭNTPD��������
Others: ��   
Key Class&Method List: 
             1. NtpdWorker��worker�࣬����handler��ע�ᣬ���һ�ԭNTPD��������
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:�½��ļ�
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
    Description: NTPD NTP�������õ�worker����worker��������NTPD�������ã��򿪹ر�NTP���񣬻�ȡNTPD�������õ���Ϣ����������ʱ��ԭNTPD��������
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

        bf.CmdWorker.__init__(self, name = "NtpdWorker", min_task_id=1, max_task_id=20000)
        self._mit_manager = mit.Mit()
        
    def ready_for_work(self): 
        """
        Method: ready_for_work
        Description: ע���worker������handler��ע���worker������mit�����һ�ԭNTPD��������
        Parameter: ��
        Return: isrestore���Ƿ�ɹ���ԭNTPD����Ĵ�����
        Others: ��
        """
        
        self.register_mit_for_work()
        self.register_handler_for_work()
        isrestore = NtpdWorker.restore_ntp_data(self)
        return isrestore
    
    def register_mit_for_work(self):
        """
        Method: register_mit_for_work
        Description: ע���worker������mit
        Parameter: ��
        Return: ��
        Others: ��
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
        Description: ע���worker������handler
        Parameter: ��
        Return: ��
        Others: ��
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
        Description: ��ȡworkerע�����mit
        Parameter: ��
        Return: _mit_manager��ע�����mit
        Others: ��
        """

        return self._mit_manager
    
    def send_ack(self, frame, datas):
        """
        Method: send_ack
        Description: �򷢳�����Ľ��̷��ʹ������Ĵ�����
        Parameter: 
            frame: �յ���Ҫ�������Ϣ
            datas: ���ʹ���������Ϣ
        Return: ��
        Others: ��
        """

        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(frame)        
        for data in datas:
            frame_ack.add_data(data)
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)
        
    def restore_ntp_data(self):    
        """
        Method: restore_ntp_data
        Description: ��ԭNTPD��������
        Parameter: ��
        Return: return_code����ԭNTPD�������ݴ������Ĵ�����
        Others: ��
        """

        return_code, description = ntpd_set.ntpd_write(self._mit_manager) 
        return return_code
