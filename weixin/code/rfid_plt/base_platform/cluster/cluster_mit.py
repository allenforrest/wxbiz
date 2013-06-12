#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��ж�����clusterʹ�õ�mit
Others:      
Key Class&Method List: 
             1. 
History: 
1. Date:
   Author:
   Modification:
"""


import mit
from moc_cluster import MocClusterNode
import tracelog
from dba import db_cfg_info


class ClusterMit(mit.Mit):
    """
    Class: ClusterMit
    Description: clusterʹ�õ�mit
    Base: mit.Mit
    Others: 
    """

    def __init__(self, db_file=None):
        """
        Method: __init__
        Description: ���캯��
        Parameter: 
            db_file: ���ݿ��ļ�·��(��ʹ��sqlite��������)
        Return: 
        Others: 
        """

        mit.Mit.__init__(self)
        
        self.regist_moc(MocClusterNode.MocClusterNode, MocClusterNode.MocClusterNodeRule)        
        self.open_sqlite(db_file)
        #self.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME)) 

    def get_all_nodes(self):
        """
        Method: get_all_nodes
        Description: ��ȡ���еĽڵ�
        Parameter: ��
        Return: ���еĽڵ�
        Others: 
        """

        return self.rdm_find("MocClusterNode")

    def save_node(self, ip, is_enable):
        """
        Method: save_node
        Description: ����ڵ�
        Parameter: 
            ip: �ڵ��ip
            is_enable: �ڵ��Ƿ������õ�
        Return: ������
        Others: 
        """

        rdm = mit.RawDataMoi("MocClusterNode", ip = ip, is_enable = is_enable)
        ret = self.rdm_add(rdm)
        
        if ret.get_err_code() != 0:
            tracelog.error("save node to mit faield. ret:%d, %s" % (
                      ret.get_err_code()
                    , ret.get_msg()))
                    
        return ret.get_err_code()

    
    def rmv_node(self, ip):
        """
        Method: rmv_node
        Description: ɾ���ڵ�
        Parameter: 
            ip: �ڵ��ip
        Return: ������
        Others: 
        """

        rdm = mit.RawDataMoi("MocClusterNode", ip = ip)
        ret = self.rdm_remove(rdm)
        
        if ret.get_err_code() != 0:
            tracelog.error("remove node in mit faield. ret:%d, %s" % (
                      ret.get_err_code()
                    , ret.get_msg()))
                    
        return ret.get_err_code(), ret.get_msg()
