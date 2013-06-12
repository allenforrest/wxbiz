#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-22
Description: event manager命令码定义文件
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:2012-11-22
   Author:ACP2013
   Modification:新建文件
"""


#OSS 命令码
OSS_BASE = 0x02000000

#一个APP分配0x1000个命令码
EVENT_REPORT_BASE = 0x0






########################################################################
#EVENT MANAGER COMMAND CODE
########################################################################
"""
EVENT_REPORT_COMMAND
data区有1个参数
event_data:上报event数据,pickle编码
没有返回信息
"""
EVENT_REPORT_COMMAND = OSS_BASE + EVENT_REPORT_BASE + 0


"""
EVENT_QUERY_REQUEST
data区有1个参数
query_req:EventQueryRequest 的JSON编码
返回 EventQueryResponse 的JSON编码
"""
EVENT_QUERY_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 1

"""
EVENT_EXPORT_REQUEST
data区有1个参数
query_req:EventQueryRequest 的JSON编码
返回 EventQueryResponse 的JSON编码
"""
EVENT_EXPORT_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 2

"""
EVENT_EXPORT_TASK_QUERY_REQUEST
data区有1个参数
query_req:EventQueryRequest 的JSON编码
返回 EventQueryResponse 的JSON编码
"""
EVENT_EXPORT_TASK_QUERY_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 3

"""
EVENT_FILTER_LIST_REQUEST
data区没有参数
返回 EventFilterListResponse 的JSON编码
"""
EVENT_FILTER_LIST_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 4

"""
EVENT_IMC_QUERY_EAU_REQUEST
data区有1个参数
query_req:EventImcQueryEauRequest 的JSON编码
返回 EventQueryResponse 的JSON编码
"""
EVENT_IMC_QUERY_EAU_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 5

"""
EVENT_QUERY_TO_IMC_REQUEST,消息格式同 EVENT_QUERY_REQUEST，用于IMC向EAU查询
"""
EVENT_QUERY_TO_IMC_REQUEST = OSS_BASE + EVENT_REPORT_BASE + 6

"""
WEB_EVENT_REPORT_COMMAND，用于WEB相关模块向event manager发送事件

"""
WEB_EVENT_REPORT_COMMAND = OSS_BASE + EVENT_REPORT_BASE + 7

if __name__=='__main__':
    print EVENT_QUERY_REQUEST, EVENT_EXPORT_REQUEST, EVENT_EXPORT_TASK_QUERY_REQUEST, EVENT_IMC_QUERY_EAU_REQUEST, WEB_EVENT_REPORT_COMMAND

