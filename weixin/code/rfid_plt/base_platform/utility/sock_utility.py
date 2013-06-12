#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-19
Description: socket相关的实用接口
Others:      
Key Class&Method List: 

History: 
1. Date:
   Author:
   Modification:
"""

import re
import socket
import struct


def recv_bytes(sock, byte_num):
    """
    Function: recv_bytes
    Description: 持续接收消息，直到达到指定的字节数
    Parameter: 
        sock: socket
        byte_num: 希望接收的字节数
    Return: 
    Others: 发送全部字节，直接使用socket.sendall
    """

    if byte_num <= 0:
        return ''
    
    wholedata = []
    while byte_num > 0:
        data = sock.recv(byte_num)
        datalen = len(data)
        if datalen == 0:
            return '' # lose connection
                           
        byte_num -= datalen
        
        if byte_num <= 0 and len(wholedata) == 0:
            return data
       
        wholedata.append(data)
   
    return "".join(wholedata)


from .is_windows import is_windows


def get_ip_by_NIC(nic):
    """
    Function: get_ip_by_NIC
    Description: 获取网卡的IP(如果网卡上有多个ip，那么也只返回1个)
    Parameter:
        nic: 网卡名称
    Return: IPv4地址        
    Others: 
        linux上，nic为eth0, eth1等等
        windows上，nic为网络连接中看到的网卡名称，例如'本地连接', '无线网络连接'
    """
    
    if is_windows():
    
        #from wmi import wmi
        import wmi
        ws = wmi.WMI()

        # 中文windows默认是GBK编码
        nic = nic.decode("utf-8").encode("gbk")

        # 先从Win32_NetworkAdapter中根据NetConnectionID获取
        net_adapters = ws.query("select * from Win32_NetworkAdapter where NetConnectionID='%s'" % nic.replace("'", "''"))
        if len(net_adapters) == 0:
            raise Exception("the specified network adapter (%s) dose not exist" % nic)

        index = net_adapters[0].Index
        
        # 根据index查找Win32_NetworkAdapterConfiguration        
        net_adapter_cfgs = ws.Win32_NetworkAdapterConfiguration(Index = index)
        if len(net_adapter_cfgs) == 0:
            raise Exception("the specified network adapter (%s) is not found "
                            "in Win32_NetworkAdapterConfiguration, index:%d" % (nic, index))

        ips = net_adapter_cfgs[0].IPAddress

        # ips中有可能同时存在ipv4和ipv6，通过过滤的方式获取到ipv4
        rep = re.compile("\d+\.\d+\.\d+\.\d+")
        for ip in ips:
            ip = str(ip)
            if rep.match(ip) is not None:
                return ip

        raise Exception("IPv4 not found on '%s'" % nic)
        
        
    else:
        import fcntl
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,  # SIOCGIFADDR, Linux下为0x8915， freebsd为3223349537
                    struct.pack('256s', nic[:15])
                )[20:24])

        return ip


def get_hw_address(ifname): 
    import fcntl
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))  # SIOCGIFHWADDR 
   
    return ':'.join(['%02X' % ord(char) for char in info[18:24]])

