#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ������ʵ���˰�IP�ͽ��IP�󶨵Ĺ���
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""

import subprocess
import utility

def _linux_bind_virtual_ip(vip, mask, NIC):
    """
    Function: _linux_bind_virtual_ip
    Description: linux�а�����ip
    Parameter: 
        vip: ����ip
        mask: ����
        NIC: ��������(����ӿڵ�����)
    Return: 
    Others: ������, ��׼���
    """

    p = subprocess.Popen(["ip", "addr", "add", "%s/%s"%(vip, mask), "dev", NIC]
                    , stdout=subprocess.PIPE
                    , stderr=subprocess.STDOUT
                    , close_fds = True)

    stdoutdata, stderrdata = p.communicate()
    return p.returncode, stdoutdata


def _linux_unbind_virtual_ip(vip, mask, NIC):
    """
    Function: _linux_unbind_virtual_ip
    Description: linux���������ip
    Parameter: 
        vip: ����ip
        mask: ����
        NIC: ��������
    Return: ������ͱ�׼���
    Others: 
    """

    p = subprocess.Popen(["ip", "addr", "del", "%s/%s"%(vip, mask), "dev", NIC]
                    , stdout=subprocess.PIPE
                    , stderr=subprocess.STDOUT
                    , close_fds = True)

    stdoutdata, stderrdata = p.communicate()
    return p.returncode, stdoutdata
    
    
def _win_bind_virtual_ip(vip, mask, NIC):
    """
    Function: _win_bind_virtual_ip
    Description: 
    Parameter: 
        vip: ����ip
        mask: ����
        NIC: ��������
    Return: 
    Others: �ݲ�֧��
    """

    #raise Exception("No implementation")
    return 0, ""


def _win_unbind_virtual_ip(vip, mask, NIC):
    """
    Function: _win_unbind_virtual_ip
    Description: 
    Parameter: 
        vip: ����ip
        mask: ����
        NIC: ��������
    Return: 
    Others: �ݲ�֧��
    """

    #raise Exception("No implementation")
    return 0, ""

    
if utility.is_windows():
    bind_virtual_ip = _win_bind_virtual_ip
    unbind_virtual_ip = _win_unbind_virtual_ip
else:
    bind_virtual_ip = _linux_bind_virtual_ip
    unbind_virtual_ip = _linux_unbind_virtual_ip


