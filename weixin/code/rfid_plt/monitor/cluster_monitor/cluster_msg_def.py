#coding=gbk

import serializable_obj
import type_def

class ClusterNodeInfo(serializable_obj.JsonSerializableObj):
    
    __ATTR_DEF__ = {
                  "ip"          : type_def.TYPE_STRIP_STRING
                , "is_online"   : type_def.TYPE_INT32        #  0: ����  1:����
                , "role"        : type_def.TYPE_INT32        #  0: δ֪  1:master  2:slave
                }
    
class QueryClusterNodeResponse(serializable_obj.JsonSerializableObj):


    __ATTR_DEF__ = { "node_list": [ClusterNodeInfo] }
    


class RmvClusterNodeRequest(serializable_obj.JsonSerializableObj):

    __ATTR_DEF__ = {
                  "ip"              : type_def.TYPE_STRIP_STRING
                }

class RmvClusterNodeResponse(serializable_obj.JsonSerializableObj):

    __ATTR_DEF__ = {
                    "return_code": type_def.TYPE_UINT32
                   ,"description": type_def.TYPE_STRING
                }
    
