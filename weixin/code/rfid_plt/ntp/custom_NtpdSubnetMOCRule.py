#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTPD�����β����������ݿ�ʱ�Ĺ�����
Others:  ��    
Key Class&Method List: 
             1. CustomNtpdSubnetMOC NTPD�����β����������ݿ�ʱ�Ĺ�����
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:�½��ļ�
"""

import mit
from NtpdSubnetMOC import NtpdSubnetMOCRule
import err_code_mgr

import ntpd_set

class CustomNtpdSubnetMOC(NtpdSubnetMOCRule):
    """
    Class: CustomNtpdSubnetMOC
    Description: NTPD�����β����������ݿ�ʱ�Ĺ�����
    Base: NtpdSubnetMOCRule
    Others: ��
    """

    def check_attr_value(self, new_instance):
        """
        Method: check_attr_value
        Description: NTPD�����β����������ݿ�ʱ�Ĺ�����
        Parameter: 
            new_instance: �������ݿ��������
        Return: ��
        Others: ��
        """

#        NtpdSubnetMOCRule.check_attr_value(self, new_instance)
        # ���IP����������ĺϷ���
        self.check(ntpd_set.ip_check(new_instance.subnetip), err_code_mgr.ER_NTPD_IP_ERROR, name=new_instance.subnetip)
        self.check(ntpd_set.mask_check(new_instance.mask), err_code_mgr.ER_NTPD_MASK_ERROR, name=new_instance.mask)