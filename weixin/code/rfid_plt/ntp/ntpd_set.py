#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: ntp_appʹ�õ��ĳ��ú�����װ
Others:��
Key Class&Method List: 
             1. ip_check: ���IP��ַ�Ƿ�Ϸ�
             2. mask_check�� ������������Ƿ�Ϸ�
             3. control_check�� ���NTPD���ز����Ƿ���Ϲ���
             4. ntpd_write����ϵͳntp�����ļ�����IO��д����������ntp����
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:�½��ļ�
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
    Description: ���IP��ַ�Ƿ�Ϸ�
    Parameter: 
        ipaddress: Ҫ����IP��ַ
    Return: True��IP��ַ�Ϸ�
            False��IP��ַ�Ƿ�
    Others: ��
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
    Description: ������������Ƿ�Ϸ�
    Parameter: 
        mask: Ҫ������������
    Return: True����������Ϸ�
            False�� ��������Ƿ�
    Others: ��
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
    Description: ���NTPD���ز����Ƿ���Ϲ���
    Parameter: 
        openserver: Ҫ���Ŀ��ز���
        stratum: Ҫ����NTPD�������
    Return: True�����ز������Ϲ���
            False�� ���ز��������Ϲ���
    Others: �رշ���ʱ������������
    """

    if openserver not in ("on", "off"):
        return False
    if  openserver=="on" and stratum <1 or stratum >15:
        return False
    return True

def ntpd_write(mit_manager):
    """
    Function: ntpd_write
    Description: ��ϵͳntp�����ļ�����IO��д����������ntp����
    Parameter: 
        mit_manager: ��worker��ע���mit
    Return: errcode: �������Ĵ�����
            errdescription�� ���������ڴ�����Ϣ������
    Others: ��
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
