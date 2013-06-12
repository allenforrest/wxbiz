#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTPD_APP的参数对象列表
Others:      
Key Class&Method List: 
             1. NtpdControl： NTPD开关控制参数
             2. NtpdSubnet： NTPD子网段参数
             3. NtpdServer： NTPD服务器IP参数
             4. GetNtpdHandlerResult： NTPD_APP中所有Handler处理结果返回参数
             5. GetNtpdSubnetListResult： NTPD子网段参数列表
             6. GetNtpdServerListResult: NTPD服务器IP参数列表
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:新建文件
"""


import serializable_obj
import type_def
    
class NtpdControl(serializable_obj.JsonSerializableObj):
    """
    Class: NtpdControl
    Description: NTPD开关控制参数
    Base: JsonSerializableObj
    Others: 无
    """

    __ATTR_DEF__ = {
                      "openserver": type_def.TYPE_STRING
                    , "stratum": type_def.TYPE_UINT32
                    }
        
class NtpdSubnet(serializable_obj.JsonSerializableObj):
    """
    Class: NtpdSubnet
    Description: NTPD子网段参数
    Base: JsonSerializableObj
    Others: 无
    """

    __ATTR_DEF__ = {
                      "subnetip": type_def.TYPE_STRING
                    , "mask": type_def.TYPE_STRING
                    }   
    
class NtpdServer(serializable_obj.JsonSerializableObj):
    """
    Class: NtpdServer
    Description: NTPD服务器IP参数
    Base: JsonSerializableObj
    Others: 无
    """

    __ATTR_DEF__ = {
                      "serverip": type_def.TYPE_STRING
                    }
    
class GetNtpdHandlerResult(serializable_obj.JsonSerializableObj):
    """
    Class: GetNtpdHandlerResult
    Description: NTPD_APP中所有Handler处理结果返回参数
    Base: JsonSerializableObj
    Others: 无
    """

    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    }

class GetNtpdSubnetListResult(serializable_obj.JsonSerializableObj):
    """
    Class: GetNtpdSubnetListResult
    Description: NTPD子网段参数列表
    Base: JsonSerializableObj
    Others: 无
    """

    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "ntpdsubnets": [NtpdSubnet]
                    }   
    
class GetNtpdServerListResult(serializable_obj.JsonSerializableObj):
    """
    Class: GetNtpdServerListResult
    Description:  NTPD服务器IP参数列表
    Base: JsonSerializableObj
    Others: 无
    """

    __ATTR_DEF__ = {
                      "return_code": type_def.TYPE_UINT32
                    , "description": type_def.TYPE_STRING
                    , "ntpdservers": [NtpdServer]
                    }
    