#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTP���ز����������ݿ�ʱ�Ĺ���
Others: ��
Key Class&Method List: 
             1. CustomNtpdContolMOC�� NTP���ز����������ݿ�ʱ�Ĺ���
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:�½��ļ�
"""

import mit
from NtpdControlMOC import NtpdControlMOCRule
import err_code_mgr

import ntpd_set

class CustomNtpdContolMOC(NtpdControlMOCRule):
    """
    Class: CustomNtpdContolMOC
    Description: NTP���ز����������ݿ�ʱ�Ĺ���
    Base: NtpdControlMOCRule
    Others: ��
    """

    def check_attr_value(self, new_instance):
        """
        Method: check_attr_value
        Description: NTP���ز����������ݿ�ʱ�Ĺ���
        Parameter: 
            new_instance: �������ݿ��������
        Return: ��
        Others: ��
        """

#        NtpdNtpdControlMOCRule.check_attr_value(self, new_instance)
        # �����ƿ��ز����Ƿ���ȷ
        self.check(ntpd_set.control_check(new_instance.openserver,new_instance.stratum), err_code_mgr.ER_NTPD_CONTROL_ERROR,
                                            open_param = new_instance.openserver, stratum_param = new_instance.stratum)