#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 集群配置信息
Others:      
Key Class&Method List: 
             1. ClusterCfgInfo: 集群的配置信息
             2. ClusterNode:集群的节点
History: 
1. Date:
   Author:
   Modification:
"""

import os
import os.path
import xml.etree.ElementTree as ET   


import tracelog
import err_code_mgr


from cluster.cluster_thread import ClusterThread


# 集群配置文件中的信息
class ClusterCfgInfo:
    """
    Class: ClusterCfgInfo
    Description: 集群的配置信息
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method: __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
        """


        # 虚拟集群ip
        self.virtual_cluster_ip = ""

        # 虚拟集群ip掩码
        self.virtual_cluster_mask = ""

        # 虚拟ip所在的网卡名称
        self.external_NIC = ""

        # 内部ip
        self.my_inner_ip = ""

        self.max_nodes_num = 0


#def load_cur_cluster_node_info(app_top_path):
#    # 从配置文件中加载当前节点的配置信息
#    cluster_info_xml = os.path.join(app_top_path, "configure", "cluster_info.xml")
#    ret = err_code_mgr.ER_CLUSTER_LOAD_CFG_FAILED, None
#    
#    try:
#        xmldoc = ET.parse(cluster_info_xml)
#        xmlroot = xmldoc.getroot()
#
#        info_ele = xmlroot.find("info")
#        if info_ele is None:
#            tracelog.error("load cluster information from %s failed. "
#                            "content is invalid" % cluster_info_xml)
#            return ret
#
#        cluster_cfg_info = ClusterCfgInfo()
#        cluster_cfg_info.enable_cluster      = int(info_ele.get("enable_cluster", "0").strip())
#        cluster_cfg_info.virtual_cluster_ip  = info_ele.get("virtual_cluster_ip", "").strip()
#        cluster_cfg_info.virtual_cluster_mask= info_ele.get("virtual_cluster_mask", "").strip()
#        cluster_cfg_info.external_NIC           = info_ele.get("external_NIC", "").strip()
#        cluster_cfg_info.my_inner_ip         = info_ele.get("my_inner_ip", "").strip()
#
#        if cluster_cfg_info.enable_cluster:
#            if cluster_cfg_info.my_inner_ip == "":
#                tracelog.error("load cluster information from %s failed. inner_ip is null" % cluster_info_xml)
#                return ret
#    except:
#        tracelog.exception("load cluster information from %s failed." % cluster_info_xml)
#        return ret
#
#    return 0, cluster_cfg_info

    

class ClusterNode:
    """
    Class: ClusterNode
    Description: 集群的节点对象
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method: __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
        """

        self.__cluster_thread = None
                   
    def is_master(self):
        """
        Method: is_master
        Description: 判断该节点是否是master
        Parameter: 无
        Return: 该节点是否是master
        Others: 
        """

        return self.__cluster_thread.is_master()
        
    def is_slave(self):
        """
        Method: is_slave
        Description: 判断该节点是否是slave
        Parameter: 无
        Return: 该节点是否是slave
        Others: 
        """

        return self.__cluster_thread.is_slave()

    def is_only_master(self):
        """
        Method: is_only_master
        Description: 判断当前节点，是否处于only master的状态
        Parameter: 无
        Return: 当前节点，是否处于only master的状态
        Others: 
        """

        # 当前是否仅有master节点在线
        return self.__cluster_thread.is_only_master()

    def get_master_ip(self):
        """
        Method: get_master_ip
        Description: 获取master的ip
        Parameter: 无
        Return: master的ip
        Others: 
        """

        return self.__cluster_thread.get_master_ip()


    def get_all_nodes(self):
        """
        Method: get_all_nodes
        Description: 获取全部的节点
        Parameter: 无
        Return: 全部的节点
        Others: 
        """

        return self.__cluster_thread.get_all_nodes()

    def rmv_node(self, ip):
        """
        Method: rmv_node
        Description: 删除节点
        Parameter: 
            ip: 节点的ip
        Return: 错误码
        Others: 
        """

        return self.__cluster_thread.rmv_node(ip)

        
    def on_start(self, role, state):
        """
        Method: on_start
        Description: "节点启动"的响应接口
        Parameter: 
            role: 节点的角色
            state: 节点的状态
        Return: 
        Others: 
        """

        pass

    def on_state_change(self, old_role, old_stats, new_role, new_state):
        """
        Method: on_state_change
        Description: "节点状态变更"的响应接口
        Parameter: 
            old_role: 变化前的角色
            old_stats: 变化前的状态
            new_role: 变化后的角色
            new_state: 变化后的状态
        Return: 
        Others: 
        """

        pass

    def on_master_change(self, old_master_ip, new_master_ip):
        """
        Method: on_master_change
        Description: "master节点发生了变化"的响应接口
        Parameter: 
            old_master_ip: 变化前的master的ip
            new_master_ip: 变化后的master的ip
        Return: 
        Others: 
        """

        # 如果old_master_ip==new_master_ip，那么说明master发生过复位
        pass

    def on_node_offline(self, node_ip):
        """
        Method: on_node_offline
        Description: "某个节点离线"的响应接口
        Parameter: 
            node_ip: 节点的ip
        Return: 
        Others: 
        """

        # 如果当前是master，那么当其他某个节点离线了，那么会调用本接口
        pass
        
    def on_node_online(self, node_ip):
        """
        Method: on_node_online
        Description: "某个节点上线了"的响应接口
        Parameter: 
            node_ip: 
        Return: 
        Others: 
        """

        # 如果当前是master，那么当其他某个节点上线了，那么会调用本接口
        pass


    def start(self, cluster_cfg_info, app_top_path):
        """
        Method: start
        Description: 启动节点
        Parameter: 
            cluster_cfg_info:集群的配置信息 
            app_top_path: 软件的跟目录
        Return: 错误码
        Others: 
        """

        # out_NIC: 外网网卡 outer Network Interface Card
        
        if self.__cluster_thread is not None:
            tracelog.error("can not start cluster node again when it is running.")
            return  err_code_mgr.ER_CLUSTER_START_FAILED
        
        tracelog.info("the cluster node is starting, cluster_ip:%s, my_ip:%s, "
                     "out_NIC:%s"%(cluster_cfg_info.virtual_cluster_ip
                                , cluster_cfg_info.my_inner_ip
                                , cluster_cfg_info.external_NIC))
                        
        cluster_thread = ClusterThread(self)
        
        # 启动节点
        try:
            ret = cluster_thread.initial_cluster(cluster_cfg_info, app_top_path)
            if ret != 0:
                return ret
        except:
            tracelog.exception("initial_cluster failed")
            return err_code_mgr.ER_CLUSTER_START_FAILED

        self.__cluster_thread = cluster_thread
        cluster_thread.start()

        return 0


    
    def stop(self):
        """
        Method: stop
        Description: 停止该节点
        Parameter: 无
        Return: 
        Others: 
        """

        # 停止当前节点
        if self.__cluster_thread is not None:
            self.__cluster_thread.stop_cluster()
        
        self.__cluster_thread.join(5)
        