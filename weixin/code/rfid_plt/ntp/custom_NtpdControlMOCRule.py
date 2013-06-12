#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTP开关参数插入数据库时的规则
Others: 无
Key Class&Method List: 
             1. CustomNtpdContolMOC： NTP开关参数插入数据库时的规则
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:新建文件
"""

import mit
from NtpdControlMOC import NtpdControlMOCRule
import err_code_mgr

import ntpd_set

class CustomNtpdContolMOC(NtpdControlMOCRule):
    """
    Class: CustomNtpdContolMOC
    Description: NTP开关参数插入数据库时的规则
    Base: NtpdControlMOCRule
    Others: 无
    """

    def check_attr_value(self, new_instance):
        """
        Method: check_attr_value
        Description: NTP开关参数插入数据库时的规则
        Parameter: 
            new_instance: 插入数据库的新数据
        Return: 无
        Others: 无
        """

#        NtpdNtpdControlMOCRule.check_attr_value(self, new_instance)
        # 检查控制开关参数是否正确
        self.check(ntpd_set.control_check(new_instance.openserver,new_instance.stratum), err_code_mgr.ER_NTPD_CONTROL_ERROR,
                                            open_param = new_instance.openserver, stratum_param = new_instance.stratum)