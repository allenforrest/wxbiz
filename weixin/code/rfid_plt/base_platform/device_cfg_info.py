#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ���ʵ���˶�ȡ�豸������Ϣ�Ĺ���
Others:      
Key Class&Method List: 
             1. DeviceCfgInfo: �����������������Ϣ
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
    Description: �����������������Ϣ
    Base: 
    Others: 
    """


    def __init__(self):
        """
        Method: __init__
        Description: ���� ����
        Parameter: ��
        Return: 
        Others: 
        """

        self.__cluster_info = None

        # �豸��ip����Ϣ
        self.__device_id = "unknow"
        self.__device_external_NIC = ""
        self.__device_external_ip = ""
        self.__device_internal_NIC = ""
        self.__device_internal_ip = ""

        # ��Ⱥ��ѡ��
        self.__cluster_enable = 0
        self.__cluster_virtual_ip = ""
        self.__cluster_virtual_mask = ""
        self.__cluster_max_nodes_num = 0

    def log_device_info(self):
        """
        Method: log_device_info
        Description: ���豸��Ϣ��¼����־
        Parameter: ��
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
        Description: ��ȡ�豸��id
        Parameter: ��
        Return: �豸��ip
        Others: 
        """

        return self.__device_id

    def get_device_external_NIC(self):
        """
        Method: get_device_external_NIC
        Description: ��ȡ�豸��������������
        Parameter: ��
        Return: �豸��������������
        Others: 
        """

        return self.__device_external_NIC

    def get_device_external_ip(self):
        """
        Method: get_device_external_ip
        Description: ��ȡ�豸����������ip
        Parameter: ��
        Return: �豸����������ip
        Others: 
        """

        return self.__device_external_ip

    def get_device_internal_NIC(self):
        """
        Method: get_device_internal_NIC
        Description: ��ȡ�豸������������
        Parameter: ��
        Return: �豸������������
        Others: 
        """

        return self.__device_internal_NIC

    def get_device_internal_ip(self):
        """
        Method: get_device_internal_ip
        Description: ��ȡ�豸����������ip
        Parameter: ��
        Return: �豸����������ip
        Others: 
        """

        return self.__device_internal_ip

 
    def is_cluster_enable(self):
        """
        Method: is_cluster_enable
        Description: �ж��Ƿ������˼�Ⱥ
        Parameter: ��
        Return: 
        Others: 
        """

        return self.__cluster_enable != 0

    def get_cluster_virtual_ip(self):
        """
        Method: get_cluster_virtual_ip
        Description: ��ȡ��Ⱥ������ip
        Parameter: ��
        Return: ��Ⱥ������ip
        Others: 
        """

        return self.__cluster_virtual_ip
        
    def get_cluster_virtual_mask(self):
        """
        Method: get_cluster_virtual_mask
        Description: ��ȡ��Ⱥ����ip������
        Parameter: ��
        Return: ��Ⱥ����ip������
        Others: 
        """

        return self.__cluster_virtual_mask

    def get_cluster_max_nodes_num(self):
        """
        Method: get_cluster_max_nodes_num
        Description: ��ȡ��Ⱥ֧�ֵ����ڵ���Ŀ
        Parameter: ��
        Return: ��Ⱥ֧�ֵ����ڵ���Ŀ
        Others: 
        """

        return self.__cluster_max_nodes_num
    
    def init_ip_from_os(self):
        """
        Method: init_ip_from_os
        Description: �Ӳ���ϵͳ�л�ȡ��������������ip
        Parameter: ��
        Return: ������
        Others: 
        """

        
        self.__device_external_ip = ""
        self.__device_internal_ip = ""
        
        # ��OS�ж�ȡ������Ӧ��ip
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
        Description: �������ļ��м����豸��Ϣ
        Parameter: 
            xmlroot: xml�������ET�ṹ
        Return: ������
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
        Description: ��XML�ṹ�У������õ��豸����Ϣ
        Parameter: 
            xmlroot: ET�ṹ��xml�ĸ��ڵ�
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
        Description: ��ָ���������ļ��м����豸������Ϣ
        Parameter: 
            cfg_file_path: �����ļ���·��
        Return: ������
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
    