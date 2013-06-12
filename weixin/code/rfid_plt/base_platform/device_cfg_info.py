#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中实现了读取设备配置信息的功能
Others:      
Key Class&Method List: 
             1. DeviceCfgInfo: 保存了设配的配置信息
History: 
1. Date:
   Author:
   Modification:
"""

import xml.etree.ElementTree as ET   
import tracelog

import utility

        
        
class DeviceCfgInfo:
    """
    Class: DeviceCfgInfo
    Description: 保存了设配的配置信息
    Base: 
    Others: 
    """


    def __init__(self):
        """
        Method: __init__
        Description: 构造 函数
        Parameter: 无
        Return: 
        Others: 
        """

        self.__cluster_info = None

        # 设备的ip等信息
        self.__device_id = "unknow"
        self.__device_external_NIC = ""
        self.__device_external_ip = ""
        self.__device_internal_NIC = ""
        self.__device_internal_ip = ""

        # 集群的选项
        self.__cluster_enable = 0
        self.__cluster_virtual_ip = ""
        self.__cluster_virtual_mask = ""
        self.__cluster_max_nodes_num = 0

    def log_device_info(self):
        """
        Method: log_device_info
        Description: 将设备信息记录到日志
        Parameter: 无
        Return: 
        Others: 
        """

        tracelog.info("device_id: %s" % self.__device_id)
        tracelog.info("device_external_NIC: %s" % self.__device_external_NIC)
        tracelog.info("device_external_ip: %s" % self.__device_external_ip)
        tracelog.info("device_internal_NIC: %s" % self.__device_internal_NIC)
        tracelog.info("device_internal_ip: %s" % self.__device_internal_ip)
        tracelog.info("cluster_enable: %s" % self.__cluster_enable)
        tracelog.info("cluster_virtual_ip: %s" % self.__cluster_virtual_ip)
        tracelog.info("cluster_virtual_mask: %s" % self.__cluster_virtual_mask)
        tracelog.info("cluster_max_nodes_num: %s" % self.__cluster_max_nodes_num)
        
    def get_device_id(self):
        """
        Method: get_device_id
        Description: 获取设备的id
        Parameter: 无
        Return: 设备的ip
        Others: 
        """

        return self.__device_id

    def get_device_external_NIC(self):
        """
        Method: get_device_external_NIC
        Description: 获取设备外网网卡的名称
        Parameter: 无
        Return: 设备外网网卡的名称
        Others: 
        """

        return self.__device_external_NIC

    def get_device_external_ip(self):
        """
        Method: get_device_external_ip
        Description: 获取设备外网网卡的ip
        Parameter: 无
        Return: 设备外网网卡的ip
        Others: 
        """

        return self.__device_external_ip

    def get_device_internal_NIC(self):
        """
        Method: get_device_internal_NIC
        Description: 获取设备内外网卡名称
        Parameter: 无
        Return: 设备内外网卡名称
        Others: 
        """

        return self.__device_internal_NIC

    def get_device_internal_ip(self):
        """
        Method: get_device_internal_ip
        Description: 获取设备内网网卡的ip
        Parameter: 无
        Return: 设备内网网卡的ip
        Others: 
        """

        return self.__device_internal_ip

 
    def is_cluster_enable(self):
        """
        Method: is_cluster_enable
        Description: 判断是否启用了集群
        Parameter: 无
        Return: 
        Others: 
        """

        return self.__cluster_enable != 0

    def get_cluster_virtual_ip(self):
        """
        Method: get_cluster_virtual_ip
        Description: 获取集群的虚拟ip
        Parameter: 无
        Return: 集群的虚拟ip
        Others: 
        """

        return self.__cluster_virtual_ip
        
    def get_cluster_virtual_mask(self):
        """
        Method: get_cluster_virtual_mask
        Description: 获取集群虚拟ip的掩码
        Parameter: 无
        Return: 集群虚拟ip的掩码
        Others: 
        """

        return self.__cluster_virtual_mask

    def get_cluster_max_nodes_num(self):
        """
        Method: get_cluster_max_nodes_num
        Description: 获取集群支持的最大节点数目
        Parameter: 无
        Return: 集群支持的最大节点数目
        Others: 
        """

        return self.__cluster_max_nodes_num
    
    def init_ip_from_os(self):
        """
        Method: init_ip_from_os
        Description: 从操作系统中获取到内网、外网的ip
        Parameter: 无
        Return: 错误码
        Others: 
        """

        
        self.__device_external_ip = ""
        self.__device_internal_ip = ""
        
        # 从OS中读取网卡对应的ip
        if self.__device_external_NIC != "":
            try:
                self.__device_external_ip = utility.get_ip_by_NIC(self.__device_external_NIC)
            except:
                tracelog.exception("get external ip failed. NIC:%s" % self.__device_external_NIC)
                return -1

        if self.__device_internal_NIC != "":
            try:
                self.__device_internal_ip = utility.get_ip_by_NIC(self.__device_internal_NIC)
            except:
                tracelog.exception("get internal ip failed. NIC:%s" % self.__device_internal_NIC)
                return -1
                
        return 0
        
    def __load_device_info(self, xmlroot):
        """
        Method: __load_device_info
        Description: 从配置文件中加载设备信息
        Parameter: 
            xmlroot: xml解析后的ET结构
        Return: 错误码
        Others: 
        """

        
        dev_ele = xmlroot.find("device")
        if dev_ele is None:
            tracelog.error("'device' element not found!")
            return -1

        dev_id = dev_ele.get("id", "").strip().encode("utf-8")
        if dev_id == "":
            tracelog.error("'device.id' is not configured!")
            return -1
            
        self.__device_id = dev_id
        
        nic = dev_ele.get("external_NIC", "").strip()
        self.__device_external_NIC = nic.encode("utf-8")

        nic= dev_ele.get("internal_NIC", "").strip()
        #if nic == "":
        #    tracelog.error("'device.internal_NIC' is not configured!")
        #    return -1

        self.__device_internal_NIC = nic.encode("utf-8")

        return  self.init_ip_from_os()
        
        

    def __load_cluster_info(self, xmlroot):
        """
        Method: __load_cluster_info
        Description: 从XML结构中，解析得到设备的信息
        Parameter: 
            xmlroot: ET结构，xml的根节点
        Return: 
        Others: 
        """

        cluster_ele = xmlroot.find("cluster")
        if cluster_ele is None:
            tracelog.error("'cluster' element not found!")
            return -1
        
        enable = cluster_ele.get("enable", "").strip()
        if enable == "":
            tracelog.error("'cluster.enable' is not configured!")
            return -1
        
        self.__cluster_enable = int(enable)
        
        self.__cluster_virtual_ip = cluster_ele.get("virtual_ip", "").strip()
        self.__cluster_virtual_mask = cluster_ele.get("virtual_mask", "").strip()
        self.__cluster_max_nodes_num = int(cluster_ele.get("max_nodes_num", "0").strip())
        

        return 0
        
    def load(self, cfg_file_path):
        """
        Method: load
        Description: 从指定的配置文件中加载设备配置信息
        Parameter: 
            cfg_file_path: 配置文件的路径
        Return: 错误码
        Others: 
        """

        ret = 0
        
        try:
            xmldoc = ET.parse(cfg_file_path)
            xmlroot = xmldoc.getroot()
            
            ret = self.__load_device_info(xmlroot)

            if ret == 0:
                ret = self.__load_cluster_info(xmlroot)

            if ret != 0:
                tracelog.error("load device configuration failed. cfg_file_path:%s" % cfg_file_path)
                
        except:
            tracelog.exception("load device configuration failed. cfg_file_path:%s" % cfg_file_path)
            return -1

        return ret


if __name__ == "__main__":
    import sys
    sys.path.append("../../share_libs")
    dev_info = DeviceCfgInfo()
    ret = dev_info.load(r"e:\view_local\code_platform\code_imc\configure\device.xml")
    assert(ret == 0 )

    print dev_info.get_device_id()
    print dev_info.get_device_external_NIC()
    print dev_info.get_device_internal_NIC()
    print dev_info.get_device_external_ip()
    print dev_info.get_device_internal_ip()
    print dev_info.is_cluster_enable()
    print dev_info.get_cluster_virtual_ip()
    print dev_info.get_cluster_virtual_mask()
    print dev_info.get_cluster_max_nodes_num()
    