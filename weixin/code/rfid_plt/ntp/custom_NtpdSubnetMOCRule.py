#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTPD子网段参数插入数据库时的规则检查
Others:  无    
Key Class&Method List: 
             1. CustomNtpdSubnetMOC NTPD子网段参数插入数据库时的规则检查
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:新建文件
"""

import mit
from NtpdSubnetMOC import NtpdSubnetMOCRule
import err_code_mgr

import ntpd_set

class CustomNtpdSubnetMOC(NtpdSubnetMOCRule):
    """
    Class: CustomNtpdSubnetMOC
    Description: NTPD子网段参数插入数据库时的规则检查
    Base: NtpdSubnetMOCRule
    Others: 无
    """

    def check_attr_value(self, new_instance):
        """
        Method: check_attr_value
        Description: NTPD子网段参数插入数据库时的规则检查
        Parameter: 
            new_instance: 插入数据库的新数据
        Return: 无
        Others: 无
        """

#        NtpdSubnetMOCRule.check_attr_value(self, new_instance)
        # 检查IP与子网掩码的合法性
        self.check(ntpd_set.ip_check(new_instance.subnetip), err_code_mgr.ER_NTPD_IP_ERROR, name=new_instance.subnetip)
        self.check(ntpd_set.mask_check(new_instance.mask), err_code_mgr.ER_NTPD_MASK_ERROR, name=new_instance.mask)