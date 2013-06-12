#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: ntp_app错误码定义
Others: 无
Key Class&Method List: 无
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:新建文件
"""

import err_code_mgr

NTPD_ERROR_BASE = 3101

ntpd_error_defs = {"ER_NTPD_IO_WRONG" : (NTPD_ERROR_BASE + 1
                                             , "写入NTPD配置文件发生错误"
                                             , "Write NTPD configuration files wrong" )  
                   , "ER_NTPD_INVALID_DESERIALIZE_ERROR" : (NTPD_ERROR_BASE + 2
                                            , "得到非法的反序列化字符串"
                                            ,"invalid string to deserialize")
                   , "ER_NTPD_IP_ERROR" : (NTPD_ERROR_BASE + 3
                                            , "输入的IP %(name)s地址非法"
                                            ,"IP (%(name)s) address is invalid") 
                   , "ER_NTPD_MASK_ERROR" : (NTPD_ERROR_BASE + 4
                                            , "输入的子网掩码  %(name)s 非法"
                                            ,"Mask( %(name)s) is invalid")   
                   , "ER_NTPD_SERVER_NOT_EXIST" : (NTPD_ERROR_BASE + 5
                                            , "没有找到NTPD上层服务"
                                            ,"Can not find NTPD Server Set")  
                   , "ER_NTPD_SUBNET_NOT_EXIST" : (NTPD_ERROR_BASE + 6
                                            , "没有找到NTPD可服务的子网段设置"
                                            ,"Can not find NTPD Subnetwork Set")  
                    , "ER_DUPLICATE_NTPD_SERVER_ERROR" : (NTPD_ERROR_BASE + 7
                                            , "NTPD的上层服务设置重复"
                                            ,"NTPD Server Set DUPLICATE Exception") 
                    , "ER_DUPLICATE_NTPD_SUBNET_ERROR" : (NTPD_ERROR_BASE + 8
                                            , "NTPD可服务的子网段设置重复"
                                            ,"NTPD Subnetwork Set DUPLICATE Exception")
                    , "ER_NTPD_RESTORE_ERROR" : (NTPD_ERROR_BASE + 9
                                            , "NTPDAPP启动时复原配置失败"
                                            ,"NTPD APP Restore fail")   
                   , "ER_NTPD_CHANGE_ERROR" : (NTPD_ERROR_BASE + 10
                                            , "修改NTPD工作状态失败"
                                            ,"Close or Open NTPD Server fail") 
                   , "ER_NTPD_SERVICE_OPEN_ERROR" : (NTPD_ERROR_BASE + 11
                                            , "NTPD进程启动失败"
                                            ,"SYSREM ERROR:Can Not Srart NTPD Service") 
                   , "ER_NTPD_CONTROL_ERROR" : (NTPD_ERROR_BASE + 12
                                            , "NTPD阶数或者开关设置错误"
                                            ,"ntpd openserver (%(open_param)s) or stratum (%(stratum_param)d) is invalid")  
                   , "ER_NTPD_DB_ERROR" : (NTPD_ERROR_BASE + 13
                                            , "数据库中没有关于NTPD开启关闭的数据"
                                            ,"Can not find data in DateBase") 
                   , "ER_NTPD_HAS_OP_ERROR" : (NTPD_ERROR_BASE + 14
                                            , "已经打开或者关闭NTPD服务"
                                            ,"Has Opened or Closed NTPD Service")  
             }

err_code_mgr.regist_errors(ntpd_error_defs)