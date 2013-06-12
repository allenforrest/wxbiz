#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中定义了cluster使用的mit
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
    Description: cluster使用的mit
    Base: mit.Mit
    Others: 
    """

    def __init__(self, db_file=None):
        """
        Method: __init__
        Description: 构造函数
        Parameter: 
            db_file: 数据库文件路径(当使用sqlite是有意义)
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
        Description: 获取所有的节点
        Parameter: 无
        Return: 所有的节点
        Others: 
        """

        return self.rdm_find("MocClusterNode")

    def save_node(self, ip, is_enable):
        """
        Method: save_node
        Description: 保存节点
        Parameter: 
            ip: 节点的ip
            is_enable: 节点是否是启用的
        Return: 错误码
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
        Description: 删除节点
        Parameter: 
            ip: 节点的ip
        Return: 错误码
        Others: 
        """

        rdm = mit.RawDataMoi("MocClusterNode", ip = ip)
        ret = self.rdm_remove(rdm)
        
        if ret.get_err_code() != 0:
            tracelog.error("remove node in mit faield. ret:%d, %s" % (
                      ret.get_err_code()
                    , ret.get_msg()))
                    
        return ret.get_err_code(), ret.get_msg()
