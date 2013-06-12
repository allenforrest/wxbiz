#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTPD_APP�Ĳ��������б�
Others:      
Key Class&Method List: 
             1. NtpdControl�� NTPD���ؿ��Ʋ���
             2. NtpdSubnet�� NTPD�����β���
             3. NtpdServer�� NTPD������IP����
             4. GetNtpdHandlerResult�� NTPD_APP������Handler���������ز���
             5. GetNtpdSubnetListResult�� NTPD�����β����б�
             6. GetNtpdServerListResult: NTPD������IP�����б�
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:�½��ļ�
"""


import serializable_obj
import type_def
    
class NtpdControl(serializable_obj.JsonSerializableObj):
    """
    Class: NtpdControl
    Description: NTPD���ؿ��Ʋ���
    Base: JsonSerializableObj
    Others: ��
    """

    __ATTR_DEF__ = {
                      "openserver": type_def.TYPE_STRING
                    , "stratum": type_def.TYPE_UINT32
                    }
        
class NtpdSubnet(serializable_obj.JsonSerializableObj):
    """
    Class: NtpdSubnet
    Description: NTPD�����β���
    Base: JsonSerializableObj
    Others: ��
    """

    __ATTR_DEF__ = {
                      "subnetip": type_def.TYPE_STRING
                    , "mask": type_def.TYPE_STRING
                    }   
    
class NtpdServer(serializable_obj.JsonSerializableObj):
    """
    Class: NtpdServer
    Description: NTPD������IP����
    Base: JsonSerializableObj
    Others: ��
    """

    __ATTR_DEF__ = {
                      "serverip": type_def.TYPE_STRING
                    }
    
class GetNtpdHandlerResult(serializable_obj.JsonSerializableObj):
    """
    Class: GetNtpdHandlerResult
    Description: NTPD_APP������Handler���������ز���
    Base: JsonSerializableObj
    Others: ��
    """

    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    }

class GetNtpdSubnetListResult(serializable_obj.JsonSerializableObj):
    """
    Class: GetNtpdSubnetListResult
    Description: NTPD�����β����б�
    Base: JsonSerializableObj
    Others: ��
    """

    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "ntpdsubnets": [NtpdSubnet]
                    }   
    
class GetNtpdServerListResult(serializable_obj.JsonSerializableObj):
    """
    Class: GetNtpdServerListResult
    Description:  NTPD������IP�����б�
    Base: JsonSerializableObj
    Others: ��
    """

    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "ntpdservers": [NtpdServer]
                    }
    