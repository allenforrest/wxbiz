#coding=gbk

import serializable_obj
import type_def


class QueryClusterMasterIpResponse(serializable_obj.BsonSerializableObj): 
    __ATTR_DEF__ = {
                      "ip": type_def.TYPE_STRING
                    }     

        
class AppRegisterRequest(serializable_obj.BsonSerializableObj): 
    __ATTR_DEF__ = {
                      "service_name": type_def.TYPE_STRING
                    , "instance_id": type_def.TYPE_UINT32
                    , "system_ip": type_def.TYPE_STRING
                    , "node_type": type_def.TYPE_STRING
                    , "endpoint": type_def.TYPE_STRING
                    , "endpoint_protocol": type_def.TYPE_STRING
                    , "need_return_all_app_info": type_def.TYPE_BOOL
                    }     
        
class AppInfo(serializable_obj.BsonSerializableObj):
    __ATTR_DEF__ = {
                      "pid": type_def.TYPE_UINT32
                    , "instance_name": type_def.TYPE_STRING
                    , "service_name": type_def.TYPE_STRING
                    , "instance_id": type_def.TYPE_UINT32
                    , "system_ip": type_def.TYPE_STRING
                    , "node_type": type_def.TYPE_STRING
                    , "endpoint": type_def.TYPE_STRING
                    , "endpoint_protocol": type_def.TYPE_STRING
                    } 
    
class AppRegisterResponse(serializable_obj.BsonSerializableObj): 
    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "app_info": AppInfo
                    , "all_app_infos": [AppInfo]                   
                    }

class AppUnRegisterRequest(serializable_obj.BsonSerializableObj): 
    __ATTR_DEF__ = {
                      "pid": type_def.TYPE_UINT32
                    , "service_name": type_def.TYPE_STRING
                    , "system_ip": type_def.TYPE_STRING
                    , "endpoint": type_def.TYPE_STRING
                    , "need_reponse":type_def.TYPE_BOOL # 是否需要返回应答
                    }    
        
class AppUnRegisterResponse(serializable_obj.BsonSerializableObj):
    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    }     

class AllAppInfo(serializable_obj.BsonSerializableObj):
    __ATTR_DEF__ = {
                      "app_infos": [AppInfo]                    
                    }

#查询条件为单选
class AppQueryRequest(serializable_obj.BsonSerializableObj): 
    __ATTR_DEF__ = {
                      "pid": type_def.TYPE_UINT32
                    , "instance_name": type_def.TYPE_STRING
                    , "service_name": type_def.TYPE_STRING
                    , "system_ip": type_def.TYPE_STRING
                    , "endpoint": type_def.TYPE_STRING
                    }
            
class AppQueryResponse(serializable_obj.BsonSerializableObj): 
    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "app_infos": [AppInfo]
                    }

class NameBroadCastMessage(serializable_obj.BsonSerializableObj): 
    __ATTR_DEF__ = {
                      "name_app_info": AppInfo
                    , "all_app_infos": [AppInfo]                   
                    }

    