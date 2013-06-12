#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中定义了web与后台app之间通信的基本的消息结构
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

# 发送到web的基本的应答消息结果



class BasicReqFromWeb(serializable_obj.JsonSerializableObj):
    """
    Class: BasicReqFromWeb
    Description: Web发送给后台app请求消息的基本结构
    Base: JsonSerializableObj
    Others: 
    """
    
    __ATTR_DEF__ = {
                   "user_session": type_def.TYPE_STRING
                    }


class BasicRepToWeb(serializable_obj.JsonSerializableObj):
    """
    Class: BasicRepToWeb
    Description: 后台app发送给Web应答消息的基本结构
    Base: JsonSerializableObj
    Others: 
    """
    
    __ATTR_DEF__ = {
                   "user_session": type_def.TYPE_STRING
                 , "return_code": type_def.TYPE_UINT32
                 , "description": type_def.TYPE_STRING
                    }
    
    def prepare_for_ack(self, req_msg, return_code, description):
        self.user_session =  req_msg.user_session
        self.return_code = return_code
        self.description = description
      