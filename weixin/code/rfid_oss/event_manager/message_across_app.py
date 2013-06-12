#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-13
Description: 
Others:      
Key Class&Method List: 
             1. EventFilter
             2. EventQueryRequest
             3. DisplayEvent
             4. EventQueryResponse
             5. EventExportRequest
             6. EventExportResponse
             7. ExportTaskRequest
             8. ExportTask
             9. ExportTaskResponse
             10. EventFilterListRequest
             11. EventFilterListResponse 
History: 
1. Date:2012-11-13
   Author:ACP2013
   Modification:新建文件
"""


import serializable_obj
import type_def
import basic_rep_to_web


class EventFilter(serializable_obj.JsonSerializableObj):    
    """
    Class: EventFilter
    Description: 事件过滤条件，其中的每个条件为 AND的关系，如果字符串类型为空，数值类型为0，表示该字段不进行过滤
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                      "event_id": type_def.TYPE_STRING
                    , "language": type_def.TYPE_STRING
                    , "level": type_def.TYPE_STRING                                          
                    , "start_time": type_def.TYPE_UINT32
                    , "end_time": type_def.TYPE_UINT32
                    , "device_type": type_def.TYPE_STRING
                    , "device_id": type_def.TYPE_STRING
                    , "object_type": type_def.TYPE_STRING
                    , "object_id": type_def.TYPE_STRING
                    }

class EventQueryRequest(serializable_obj.JsonSerializableObj):
    """
    Class: EventQueryRequest
    Description: EVENT_QUERY_REQUEST命令码对应的请求
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                      "user_session": type_def.TYPE_STRING
                    , "current_page": type_def.TYPE_UINT32 
                    , "num_per_page": type_def.TYPE_UINT32
                    , "event_filter": EventFilter
                    }    

class DisplayEvent(serializable_obj.JsonSerializableObj):    
    """
    Class: DisplayEvent
    Description: 返回给请求者的每条Event的信息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "event_sequence_no": type_def.TYPE_UINT32
                    , "event_id": type_def.TYPE_STRING
                    , "name": type_def.TYPE_STRING
                    , "level": type_def.TYPE_STRING
                    , "time": type_def.TYPE_STRING                    
                    , "device_type": type_def.TYPE_STRING
                    , "device_id": type_def.TYPE_STRING
                    , "object_type": type_def.TYPE_STRING
                    , "object_id": type_def.TYPE_STRING
                    , "description": type_def.TYPE_STRING
                    , "cause": type_def.TYPE_STRING
                    }
    
class EventQueryResponse(serializable_obj.JsonSerializableObj):
    """
    Class: EventQueryResponse
    Description: EVENT_QUERY_REQUEST命令码对应的响应
    Base: JsonSerializableObj
    Others: 
    """    

    __ATTR_DEF__ = {
                      "user_session": type_def.TYPE_STRING
                    , "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "count": type_def.TYPE_UINT32
                    , "event_query_result": [DisplayEvent]
                    }

class EventExportRequest(serializable_obj.JsonSerializableObj):
    """
    Class: EventExportRequest
    Description: EVENT_EXPORT_REQUEST 命令码对应的请求
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                      "user_session": type_def.TYPE_STRING                    
                    , "event_filter": EventFilter
                    }

class EventExportResponse(serializable_obj.JsonSerializableObj):
    """
    Class: EventExportResponse
    Description: EVENT_EXPORT_REQUEST 命令码对应的响应
    Base: 
    Others: 
    """
    

    __ATTR_DEF__ = {
                      "user_session": type_def.TYPE_STRING
                    , "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "task_no": type_def.TYPE_UINT32                    
                    }

class ExportTaskRequest(serializable_obj.JsonSerializableObj):
    """
    Class: ExportTaskRequest
    Description: EVENT_EXPORT_TASK_QUERY_REQUEST 命令码对应的请求
    Base: 
    Others: 
    """

    __ATTR_DEF__ = {
                      "user_session": type_def.TYPE_STRING                    
                    , "task_nos": [type_def.TYPE_UINT32]    
                    }

class ExportTask(serializable_obj.JsonSerializableObj):
    """
    Class: ExportTask
    Description: 查询得到的每条任务的信息
    Base: JsonSerializableObj
    Others: 
    1，    如果是已经没有task_no的文件，设置为0
    2，   status 有 running, finished, unknown 3种状态
    3, location返回绝对路径
    """

    __ATTR_DEF__ = {
                      "task_no": type_def.TYPE_UINT32                           
                    , "status": type_def.TYPE_STRING        
                    , "location": type_def.TYPE_STRING
                    }
    
class ExportTaskResponse(serializable_obj.JsonSerializableObj):
    """
    Class: EventQueryResponse
    Description: EVENT_EXPORT_TASK_QUERY_REQUEST 命令码对应的响应
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                      "user_session": type_def.TYPE_STRING
                    , "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "tasks": [ExportTask]                  
                    }

class EventFilterListRequest(serializable_obj.JsonSerializableObj):
    """
    Class: EventFilterListRequest
    Description: EVENT_FILTER_LIST_REQUEST 命令码对应的请求
    Base: JsonSerializableObj
    Others: 
    """   

    __ATTR_DEF__ = {
                      "user_session": type_def.TYPE_STRING
                    }

class EventFilterListResponse(serializable_obj.JsonSerializableObj):
    """
    Class: EventFilterListResponse
    Description: EVENT_FILTER_LIST_REQUEST 命令码对应的响应
    Base: JsonSerializableObj
    Others: 
    """    

    __ATTR_DEF__ = {
                      "user_session": type_def.TYPE_STRING
                    , "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "levels": [type_def.TYPE_STRING]                  
                    , "device_types": [type_def.TYPE_STRING]
                    , "object_types": [type_def.TYPE_STRING]
                    }

    
class EventImcQueryEauRequest(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: EventImcQueryEauRequest
    Description: EVENT_IMC_QUERY_EAU_REQUEST 命令码对应的请求
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                      "eau_ip": type_def.TYPE_STRING
                    , "current_page": type_def.TYPE_UINT32 
                    , "num_per_page": type_def.TYPE_UINT32
                    , "event_filter": EventFilter
                    }
     
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

class EventFromWebRequest(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: EventImcQueryEauRequest
    Description: EVENT_IMC_QUERY_EAU_REQUEST 命令码对应的请求
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                      "event_id": type_def.TYPE_STRING
                    , "event_flag": type_def.TYPE_STRING 
                    , "generate_time_inner": type_def.TYPE_UINT32
                    , "device_id": type_def.TYPE_STRING
                    , "object_id": type_def.TYPE_STRING
                    , "params": {}
                    }
     
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
            
if __name__=="__main__":
    buf = '{"num_per_page":10,"current_page":0,"user_session":"s2o7u08o7038shulji6fn0n9t2","event_filter":{"start_time":1354508006,"end_time":1355112806}}'
    try:
        req = EventQueryRequest.deserialize(buf)
    except Exception:
        print 'error'
        exit
    print 'success'
    print req.to_dict()            