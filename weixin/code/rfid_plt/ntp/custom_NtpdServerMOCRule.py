#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: ntpd������IP��ַ�����������ݿ�ʱ�Ĺ�����
Others: ��
Key Class&Method List: 
             1. CustomNtpdSubnetMOC�� ntpd������IP��ַ�����������ݿ�ʱ�Ĺ�����
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:�½��ļ�
"""

import mit
from NtpdServerMOC import NtpdServerMOCRule
import err_code_mgr

import ntpd_set

class CustomNtpdSubnetMOC(NtpdServerMOCRule):
    """
    Class: CustomNtpdSubnetMOC
    Description: ntpd������IP��ַ�����������ݿ�ʱ�Ĺ�����
    Base: NtpdServerMOCRule
    Others: ��
    """

    def check_attr_value(self, new_instance):
        """
        Method: check_attr_value
        Description: ntpd������IP��ַ�����������ݿ�ʱ�Ĺ�����
        Parameter: 
            new_instance: �������ݿ��������
        Return: ��
        Others: ��
        """

#        NtpdServerMOCRule.check_attr_value(self, new_instance)
        # ���IP�ĺϷ���
        self.check(ntpd_set.ip_check(new_instance.serverip), err_code_mgr.ER_NTPD_IP_ERROR, name=new_instance.serverip)