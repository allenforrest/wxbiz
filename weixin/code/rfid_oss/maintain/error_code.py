#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: maintain_app错误码定义
Others:无 
Key Class&Method List: 无
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:新建文件
"""


import err_code_mgr

MAINTAIN_LOG_ERROR_BASE = 0x02005000

maintainlog_error_defs = {  
                     "ER_MAINTAINLOG_INVALID_DESERIALIZE_ERROR" : (MAINTAIN_LOG_ERROR_BASE + 1
                                            , "(%(cmd)s)得到非法的反序列化字符串"
                                            ,"%(cmd)s : invalid string to deserialize")
                   , "ER_MAINTAINGLOG_MAX_EXPORT_TASK_LIMIT" : (MAINTAIN_LOG_ERROR_BASE + 2
                                            , "日志打包任务数已经到达最大值"
                                            ,"The maximum number of package log tasks have arrived")     
             }

err_code_mgr.regist_errors(maintainlog_error_defs)