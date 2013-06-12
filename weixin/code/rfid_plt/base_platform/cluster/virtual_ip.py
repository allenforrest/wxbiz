#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文中实现了绑定IP和解除IP绑定的功能
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
    Description: linux中绑定虚拟ip
    Parameter: 
        vip: 虚拟ip
        mask: 掩码
        NIC: 网卡名称(网络接口的名称)
    Return: 
    Others: 错误码, 标准输出
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
    Description: linux解除绑定虚拟ip
    Parameter: 
        vip: 虚拟ip
        mask: 掩码
        NIC: 网卡名称
    Return: 错误码和标准输出
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
        vip: 虚拟ip
        mask: 掩码
        NIC: 网卡名称
    Return: 
    Others: 暂不支持
    """

    #raise Exception("No implementation")
    return 0, ""


def _win_unbind_virtual_ip(vip, mask, NIC):
    """
    Function: _win_unbind_virtual_ip
    Description: 
    Parameter: 
        vip: 虚拟ip
        mask: 掩码
        NIC: 网卡名称
    Return: 
    Others: 暂不支持
    """

    #raise Exception("No implementation")
    return 0, ""

    
if utility.is_windows():
    bind_virtual_ip = _win_bind_virtual_ip
    unbind_virtual_ip = _win_unbind_virtual_ip
else:
    bind_virtual_ip = _linux_bind_virtual_ip
    unbind_virtual_ip = _linux_unbind_virtual_ip


