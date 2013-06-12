#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��ж�����web���̨app֮��ͨ�ŵĻ�������Ϣ�ṹ
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

# ���͵�web�Ļ�����Ӧ����Ϣ���



class BasicReqFromWeb(serializable_obj.JsonSerializableObj):
    """
    Class: BasicReqFromWeb
    Description: Web���͸���̨app������Ϣ�Ļ����ṹ
    Base: JsonSerializableObj
    Others: 
    """
    
    __ATTR_DEF__ = {
                   "user_session": type_def.TYPE_STRING
                    }


class BasicRepToWeb(serializable_obj.JsonSerializableObj):
    """
    Class: BasicRepToWeb
    Description: ��̨app���͸�WebӦ����Ϣ�Ļ����ṹ
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
      