#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ��Ⱥ�ڵ�֮��������Ϣ
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


import serializable_obj
import type_def

class ClusterStateMsg(serializable_obj.BsonSerializableObj):
    """
    Class: ClusterStateMsg
    Description: ��Ⱥ�ڵ�֮��������Ϣ
    Base: serializable_obj.BsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                      "ip" : type_def.TYPE_STRING
                    , "role": type_def.TYPE_INT32
                    , "start_time": type_def.TYPE_STRING
                    }                     




