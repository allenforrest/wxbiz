#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中定义了数据同步功能使用到的命令码
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


#3701~3800 数据同步使用

DB_SYNC_BASE = 3700

########################################################################
#DB SYNC COMMAND CODE
########################################################################
"""
CMD_SYNC_DATA
发送数据同步通知消息
"""
CMD_SYNC_DATA = DB_SYNC_BASE + 1

# 全同步通知
CMD_NOTIFY_SYNC_FULL = DB_SYNC_BASE + 2


# 网管发给网元，导出并上传全部数据
CMD_SYNC_NE_EXP_FULL = DB_SYNC_BASE + 3

CMD_START_EXP_FULL = DB_SYNC_BASE + 4
CMD_START_IMP_FULL = DB_SYNC_BASE + 5

# imc_device_mgr发过来的EAU变更后的信息
CMD_NTF_NE_ID_PID = DB_SYNC_BASE + 6

# 向imc_device_mgr发送查询命令
CMD_QUERY_NE_ID_PID = 0x02001009


