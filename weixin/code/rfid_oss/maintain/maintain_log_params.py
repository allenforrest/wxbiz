#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: maintain_app 中 maintain_log_worker 的参数对象列表
Others:无
Key Class&Method List: 
             1. PackageLog： 日志打包参数，包含起止时间
             2. PackageLogHandlerResult： 日志处理情况
             3. PackageLogExportTask： 打包任务情况参数
             4. PackageLogExportTaskResponse： 返回的打包任务情况结果的参数列表
             5. PackageLogExportTaskRequest：请求查询打包任务情况参数列表
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:新建文件
"""

import serializable_obj
import type_def
import basic_rep_to_web
    
class PackageLog(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PackageLog
    Description: 日志打包参数，包含起止时间
    Base: JsonSerializableObj
    Others: 无
    """

    __ATTR_DEF__ = {
                      "start_time": type_def.TYPE_UINT32
                    , "end_time": type_def.TYPE_UINT32
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

class PackageLogHandlerResult(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PackageLogHandlerResult
    Description: 日志处理情况
    Base: JsonSerializableObj
    Others: 无
    """

    __ATTR_DEF__ = {
                      "task_no": type_def.TYPE_UINT32 
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    
class PackageLogExportTask(serializable_obj.JsonSerializableObj):
    """
    Class: PackageLogExportTask
    Description: 打包任务情况参数
    Base: JsonSerializableObj
    Others: 无
    """

    __ATTR_DEF__ = {
                      "task_no": type_def.TYPE_UINT32                           
                    , "status": type_def.TYPE_STRING        
                    , "location": type_def.TYPE_STRING
                    }
    
class PackageLogExportTaskResponse(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PackageLogExportTaskResponse
    Description: 返回的打包任务情况结果的参数列表
    Base: BasicRepToWeb
    Others: 无
    """

    __ATTR_DEF__ = {                      
                    "tasks": [PackageLogExportTask]                  
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    
class PackageLogExportTaskRequest(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PackageLogExportTaskRequest
    Description: 请求查询打包任务情况参数列表
    Base: BasicReqFromWeb
    Others: 无
    """

    __ATTR_DEF__ = {               
                      "task_nos": [type_def.TYPE_UINT32]    
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)