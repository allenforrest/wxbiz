#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description:maintain_app命令码定义
Others:无
Key Class&Method List: 无
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:新建文件
"""

MAINTAIN_LOG_MANAGER_BASE = 0x02005000
########################################################################
#MAINTAIN LOG REPORT COMMANDE CODE
########################################################################
MAINTAIN_PACKAGE_LOG_COMMAND = MAINTAIN_LOG_MANAGER_BASE + 0
MAINTAIN_PACKAGELOG_TASK_QUERY = MAINTAIN_LOG_MANAGER_BASE + 1
MAINTAIN_DIRECTORY_MONITOR_COMMAND =  MAINTAIN_LOG_MANAGER_BASE + 2