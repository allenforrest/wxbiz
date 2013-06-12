#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中定义了DBSyncUpdateApp的常量
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


NE_STATE_NORMAL = 0  
NE_STATE_FULL_SYNC_EXP = 1  # 正在全同步导出数据
NE_STATE_FULL_SYNC_IMP = 2  # 正在全同步导入数据


FTP_SERVER_PORT = 7421

NE_DB_DUMP_DIR = "NE/%d/db_sync"
NE_DB_DUMP_COMPRESSED_PATH = "NE/%d/db_sync/ne_mocs.dmp.zip"
NE_DB_DUMP_PATH = "NE/%d/db_sync/ne_mocs.dmp"