#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: maintain_app �� maintain_log_worker �Ĳ��������б�
Others:��
Key Class&Method List: 
             1. PackageLog�� ��־���������������ֹʱ��
             2. PackageLogHandlerResult�� ��־�������
             3. PackageLogExportTask�� ��������������
             4. PackageLogExportTaskResponse�� ���صĴ�������������Ĳ����б�
             5. PackageLogExportTaskRequest�������ѯ���������������б�
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:�½��ļ�
"""

import serializable_obj
import type_def
import basic_rep_to_web
    
class PackageLog(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PackageLog
    Description: ��־���������������ֹʱ��
    Base: JsonSerializableObj
    Others: ��
    """

    __ATTR_DEF__ = {
                      "start_time": type_def.TYPE_UINT32
                    , "end_time": type_def.TYPE_UINT32
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

class PackageLogHandlerResult(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PackageLogHandlerResult
    Description: ��־�������
    Base: JsonSerializableObj
    Others: ��
    """

    __ATTR_DEF__ = {
                      "task_no": type_def.TYPE_UINT32 
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    
class PackageLogExportTask(serializable_obj.JsonSerializableObj):
    """
    Class: PackageLogExportTask
    Description: ��������������
    Base: JsonSerializableObj
    Others: ��
    """

    __ATTR_DEF__ = {
                      "task_no": type_def.TYPE_UINT32                           
                    , "status": type_def.TYPE_STRING        
                    , "location": type_def.TYPE_STRING
                    }
    
class PackageLogExportTaskResponse(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PackageLogExportTaskResponse
    Description: ���صĴ�������������Ĳ����б�
    Base: BasicRepToWeb
    Others: ��
    """

    __ATTR_DEF__ = {                      
                    "tasks": [PackageLogExportTask]                  
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    
class PackageLogExportTaskRequest(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PackageLogExportTaskRequest
    Description: �����ѯ���������������б�
    Base: BasicReqFromWeb
    Others: ��
    """

    __ATTR_DEF__ = {               
                      "task_nos": [type_def.TYPE_UINT32]    
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)