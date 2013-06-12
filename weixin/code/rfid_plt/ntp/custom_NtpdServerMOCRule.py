#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: ntpd服务器IP地址参数插入数据库时的规则检查
Others: 无
Key Class&Method List: 
             1. CustomNtpdSubnetMOC： ntpd服务器IP地址参数插入数据库时的规则检查
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:新建文件
"""

import mit
from NtpdServerMOC import NtpdServerMOCRule
import err_code_mgr

import ntpd_set

class CustomNtpdSubnetMOC(NtpdServerMOCRule):
    """
    Class: CustomNtpdSubnetMOC
    Description: ntpd服务器IP地址参数插入数据库时的规则检查
    Base: NtpdServerMOCRule
    Others: 无
    """

    def check_attr_value(self, new_instance):
        """
        Method: check_attr_value
        Description: ntpd服务器IP地址参数插入数据库时的规则检查
        Parameter: 
            new_instance: 插入数据库的新数据
        Return: 无
        Others: 无
        """

#        NtpdServerMOCRule.check_attr_value(self, new_instance)
        # 检查IP的合法性
        self.check(ntpd_set.ip_check(new_instance.serverip), err_code_mgr.ER_NTPD_IP_ERROR, name=new_instance.serverip)