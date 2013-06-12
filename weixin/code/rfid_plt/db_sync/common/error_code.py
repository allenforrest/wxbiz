#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: db sync错误码定义文件
Others:      
Key Class&Method List: 
    1. ....
History: 
1. Date:2013-03-23
   Author:ACP2013
   Modification:新建文件
"""

import err_code_mgr

#OSS 命令码
DB_SYNC_ERROR_BASE = 3700

db_sync_error_defs = {"ER_SYNC_FAILED" : (DB_SYNC_ERROR_BASE + 1
                                        , "执行数据同步异常。 异常信息 : %(err)s"
                                        , "execute db sync exception. Exception information: %(err)s")
                    , "ER_SYNC_HOST_NOT_FOUND" : (DB_SYNC_ERROR_BASE + 2
                                        , "同步服务器找不到"
                                        , "sync host was not found.")
                    , "ER_SYNC_TABLE_NOT_FOUND" : (DB_SYNC_ERROR_BASE + 3
                                        , "同步数据表不到"
                                        , "sync table was not found.")

                    , "ER_SYNC_NO_TABLE_NEED_SYNC" : (DB_SYNC_ERROR_BASE + 4
                                        , "不存在需要同步的数据表"
                                        , "There is no table need to sync")     
                                        
                    , "ER_SYNC_EXPORT_DATA_FAILED" : (DB_SYNC_ERROR_BASE + 5
                                        , "导出数据失败"
                                        , "Export data failed")   
                                        
                    , "ER_SYNC_UPLOAD_DATA_FAILED" : (DB_SYNC_ERROR_BASE + 6
                                        , "上载数据失败"
                                        , "Upload data failed")  
                    }
err_code_mgr.regist_errors(db_sync_error_defs)
