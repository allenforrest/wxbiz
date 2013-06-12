#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: ntp_app命令码定义
Others: 无
Key Class&Method List: 无
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:新建文件
"""


NTPD_MANAGER_BASE = 3101
########################################################################
#NTPD REPORT COMMANDE CODE
########################################################################
NTPD_ADD_SUBNET_COMMAND = NTPD_MANAGER_BASE + 0
NTPD_ADD_SERVER_COMMAND = NTPD_MANAGER_BASE + 1
NTPD_GET_SERVER_COMMAND = NTPD_MANAGER_BASE + 2
NTPD_GET_SUBNET_COMMAND = NTPD_MANAGER_BASE + 3
NTPD_DEL_SERVER_COMMAND = NTPD_MANAGER_BASE + 4
NTPD_DEL_SUBNET_COMMAND = NTPD_MANAGER_BASE + 5
NTPD_CONTROL_COMMAND = NTPD_MANAGER_BASE + 6