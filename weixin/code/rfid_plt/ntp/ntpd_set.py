#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: ntp_app使用到的常用函数封装
Others:无
Key Class&Method List: 
             1. ip_check: 检查IP地址是否合法
             2. mask_check： 检查子网掩码是否合法
             3. control_check： 检查NTPD开关参数是否符合规则
             4. ntpd_write：对系统ntp配置文件进行IO重写，并且重启ntp服务
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:新建文件
"""

import re
import os
import socket
import struct
import time

import tracelog
import err_code_mgr

filepath = os.path.join("/etc/","ntp.conf")
#filepath = os.path.join("D:/","ntp.conf")

def ip_check(ipaddress):
    """
    Function: ip_check
    Description: 检查IP地址是否合法
    Parameter: 
        ipaddress: 要检查的IP地址
    Return: True：IP地址合法
            False：IP地址非法
    Others: 无
    """

    ipv4Pattern = r"\b([1-9]\d{0,2}|0)\.([1-9]\d{0,2}|0)\.([1-9]\d{0,2}|0)\.([1-9]\d{0,2}|0)\b"
    ipv4=re.match(ipv4Pattern,ipaddress)
    if ipv4 is not None:
        for i in xrange(1,5):
            if int(ipv4.group(i))>254:
                return False
        return True
    else:
        return False
        
def mask_check(mask):
    """
    Function: mask_check
    Description: 检查子网掩码是否合法
    Parameter: 
        mask: 要检查的子网掩码
    Return: True：子网掩码合法
            False： 子网掩码非法
    Others: 无
    """

    if mask == '0.0.0.0':
        return False
    try:
        maskint = struct.unpack("!I", socket.inet_aton(mask))[0]
        maskbinary  = format(maskint,'032b')
    except socket.error,e:
        return False
    if '01' in maskbinary:
        return False
    else:
        return True 
    
def control_check(openserver,stratum):
    """
    Function: control_check
    Description: 检查NTPD开关参数是否符合规则
    Parameter: 
        openserver: 要检查的开关参数
        stratum: 要检查的NTPD服务阶数
    Return: True：开关参数符合规则
            False： 开关参数不符合规则
    Others: 关闭服务时不检查阶数参数
    """

    if openserver not in ("on", "off"):
        return False
    if  openserver=="on" and stratum <1 or stratum >15:
        return False
    return True

def ntpd_write(mit_manager):
    """
    Function: ntpd_write
    Description: 对系统ntp配置文件进行IO重写，并且重启ntp服务
    Parameter: 
        mit_manager: 在worker中注册的mit
    Return: errcode: 处理结果的错误码
            errdescription： 处理结果关于错误信息的描述
    Others: 无
    """

    openfile = None
    errcode = err_code_mgr.ER_SUCCESS
    errdescription = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
    try:
        openfile = open(filepath,'w+')
        openfile.write("driftfile /var/lib/ntp/drift\n")   
        openfile.write("includefile /etc/ntp/crypto/pw\n")
        openfile.write("keys /etc/ntp/keys\n")
        
        records = mit_manager.lookup_attrs("NtpdControlMOC", ['openserver' ,'stratum'])
        for record in records:
            if record[0] == "on":
                openfile.write("fudge 127.127.1.0 stratum %d\n" %(record[1]))
                openfile.write("restrict default\n")
                openfile.write("restrict 127.0.0.1\n")
                openfile.write("server 127.127.1.0\n")
            
        records = mit_manager.lookup_attrs("NtpdSubnetMOC", ['subnetip' ,'mask'])
        for record in records:
            openfile.write("restrict %s mask %s nomodify\n" % (record[0],record[1]))
        
        records = mit_manager.lookup_attrs("NtpdServerMOC", ['serverip'])
        for record in records:
            openfile.write("server %s minpoll 4 maxpoll 5\n" %  (record[0]))
    except IOError:
        errcode = err_code_mgr.ER_NTPD_IO_WRONG
        errdescription = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_IO_WRONG)
    finally:
        if openfile is not None:
            openfile.close()
            
    if errcode == err_code_mgr.ER_NTPD_IO_WRONG:
        return errcode,errdescription
    
    for i in xrange(3):
        if os.system("service ntpd restart") == 0:
            return errcode,errdescription
        time.sleep(1)    
    
    tracelog.error('Can Not ReStart NTPD Service')
    errcode = err_code_mgr.ER_NTPD_SERVICE_OPEN_ERROR
    errdescription = err_code_mgr.get_error_msg(err_code_mgr.ER_NTPD_SERVICE_OPEN_ERROR)
    return errcode,errdescription
