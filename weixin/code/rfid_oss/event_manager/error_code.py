#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-30
Description: event manager错误码定义文件
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:2012-11-30
   Author:ACP2013
   Modification:新建文件
"""

import err_code_mgr

#OSS 命令码
OSS_BASE = 0x02000000
EVENT_MANAGER_ERROR_BASE = OSS_BASE + 0X0


event_manager_error_defs = {"ER_RAW_SELECT_EXCEPTION" : (EVENT_MANAGER_ERROR_BASE + 1
                                             , "执行 raw select 异常。 异常信息 : %(err)s"
                                             , "execute raw select exception. Exception information: %(err)s")
                            , "ER_MAX_EXPORT_TASK_LIMIT" : (EVENT_MANAGER_ERROR_BASE + 2
                                            , "超出当前运行的导出日志任务限制"
                                            , "current running export event tasks reach to the max amount")
                            ,"ER_INVALID_DESERIALIZE_STRING_ERROR": (EVENT_MANAGER_ERROR_BASE+3
                                            ,"从命令   %(cmd)s 的参数  %(param_name)s 为非法的反序列化字符串"
                                            ,"invalid string to deserialize from command %(cmd)s parameter  %(param_name)s")
                            , "ER_NO_CURRENT_PAGE_PARAMETER" : (EVENT_MANAGER_ERROR_BASE + 4
                                            , "没有current_page参数"
                                            , "current_page parameter does not exist")
                            , "ER_NO_NUM_PER_PAGE_PARAMETER" : (EVENT_MANAGER_ERROR_BASE + 5
                                            , "没有 num_per_page 参数"
                                            , "num_per_page parameter does not exist")      
                            , "ER_NUM_PER_PAGE_OUT_OF_SCOPE" : (EVENT_MANAGER_ERROR_BASE + 6
                                            , "num_per_page %(value)s 超出范围"
                                            , "num_per_page %(value)s out of scope")
                            , "ER_NO_EVENT_FILTER_PARAMETER" : (EVENT_MANAGER_ERROR_BASE + 7
                                            , "没有 event_filter 参数"
                                            , "event_filter parameter does not exist")           
                            , "ER_NEGATIVE_START_TIME" : (EVENT_MANAGER_ERROR_BASE + 8
                                            , "start_time %(start_time)s 是负数"
                                            , "start_time %(start_time)s is negative")
                            , "ER_NEGATIVE_END_TIME" : (EVENT_MANAGER_ERROR_BASE + 9
                                            , "end_time %(end_time)s 是负数"
                                            , "end_time %(end_time)s is negative")
                            , "ER_END_LESS_START" : (EVENT_MANAGER_ERROR_BASE + 10
                                            , "end_time %(end_time)s 小于  start_time %(start_time)s"
                                            , "end_time %(end_time)s is less than start_time %(start_time)s")
                            , "ER_EAU_NOT_REGISTER" : (EVENT_MANAGER_ERROR_BASE + 11
                                            , "EAU %(eau_ip)s 的pid不存在"
                                            , "the pid of EAU %(eau_ip)s does not exist")
                            , "ER_EAU_GATE_NOT_ACTIVE" : (EVENT_MANAGER_ERROR_BASE + 12
                                            , "EAUGate 没有运行"
                                            , "EAUGate is not active")
                            , "ER_QUERY_FROM_EAU_TIMEOUT" : (EVENT_MANAGER_ERROR_BASE + 13
                                            , "从 EAU %(eau_ip)s 获取事件超时"
                                            , "query event timeout from EAU %(eau_ip)s")
                
             }
err_code_mgr.regist_errors(event_manager_error_defs)