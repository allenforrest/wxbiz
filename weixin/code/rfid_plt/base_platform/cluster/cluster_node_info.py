#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中定义了集群节点的信息的类
Others:      
Key Class&Method List: 
             1. ClusterNodeInfo: 集群节点的信息的类
History: 
1. Date:
   Author:
   Modification:
"""

import tracelog

from cluster_const import *

class ClusterNodeInfo:
    """
    Class: ClusterNodeInfo
    Description: 集群节点的信息的类
    Base: 
    Others: 
    """

    def __init__(self, ip):
        """
        Method: __init__
        Description: 构造函数
        Parameter: 
            ip: 节点的ip
        Return: 
        Others: 
        """

        self.__heart_beat = 0
        self.__ip = ip
        self.__role= CLUSTER_ROLE_UNKNOWN
        self.__is_enable = True
        self.__start_time = ""
        
        self.__is_online = False

        self.__stat_change_flag = CLUSTER_NODE_STATE_NOCHANGE


    def check_heartbeat(self):
        """
        Method: check_heartbeat
        Description: 检查心跳
        Parameter: 无
        Return: 
        Others: 
        """

        # master监控slave的超时时间 > slave监控master的超时时间
        # 为了防止极端情况下，master认为slave已经离线，slave却认为master在线的情况下，
        # slave的名字被注销，但是slave自己却不知道（不会重新注册名字服务）
        if self.__role == CLUSTER_ROLE_MASTER:
            max_heartbeat = CLUSTER_MASTER_MAX_HAERTBEAT
        else:
            max_heartbeat = CLUSTER_SLAVE_MAX_HAERTBEAT
            
        if self.__heart_beat == max_heartbeat:
            self.__is_online = False
            self.__role = CLUSTER_ROLE_UNKNOWN
            #tracelog.info("cluster node %s is offline" % self.__ip)

            self.__stat_change_flag = CLUSTER_NODE_STATE_CHANGE_OFFLINE
            
        if self.__heart_beat <= max_heartbeat:
            self.__heart_beat += 1
        
    def on_heartbeat(self, msg):
        """
        Method: on_heartbeat
        Description: 收到心跳的处理接口
        Parameter: 
            msg: 心跳消息
        Return: 
        Others: 
        """

        if self.__is_online is False:
            #tracelog.info("cluster node %s is online" % self.__ip)
            self.__stat_change_flag = CLUSTER_NODE_STATE_CHANGE_ONLINE
            self.__is_online = True
            
        self.__heart_beat = 0
        self.__start_time = msg.start_time
        
        if msg.role in (CLUSTER_ROLE_MASTER, CLUSTER_ROLE_SLAVE, CLUSTER_ROLE_UNKNOWN):
            self.__role = msg.role 
        else:
            tracelog.error("invalid cluster role of node(%s): %d"%(
                      self.__ip
                    , msg.role))
                    
            self.__role = CLUSTER_ROLE_UNKNOWN

    def fetch_change_flag(self):
        """
        Method: fetch_change_flag
        Description: 获取状态变更的标记，并且重置该标记
        Parameter: 无
        Return: 状态变更的标记
        Others: 
        """

        tmp = self.__stat_change_flag
        self.__stat_change_flag = CLUSTER_NODE_STATE_NOCHANGE
        return tmp
        
        
    def reset_heartbeat(self, set_nodes_to_offline):
        """
        Method: reset_heartbeat
        Description: 重置心跳
        Parameter: 
            set_nodes_to_offline: 是否同时设置为离线
        Return: 
        Others: 
        """

        self.__heart_beat = 0

        if set_nodes_to_offline:
            self.__is_online = False
            self.__role = CLUSTER_ROLE_UNKNOWN
        
    def get_ip(self):
        """
        Method: get_ip
        Description: 获取节点的ip
        Parameter: 无
        Return: 
            节点的ip
        Others: 
        """

        return self.__ip

    def set_ip(self, ip):
        """
        Method: set_ip
        Description: 设置节点的ip
        Parameter: 
            ip: 节点的ip
        Return: 
        Others: 
        """

        self.__ip = ip

    def get_start_time(self):
        """
        Method: get_start_time
        Description: 获取启动时间
        Parameter: 无
        Return: 节点的启动时间
        Others: 
        """

        return self.__start_time
        
    def set_enable(self, is_enable):
        """
        Method: set_enable
        Description: 设置是否启用
        Parameter: 
            is_enable: 是否启用
        Return: 
        Others: 
        """

        self.__is_enable = is_enable

    def is_enable(self):
        """
        Method: is_enable
        Description: 判断节点是否启用
        Parameter: 无
        Return: 节点是否启用
        Others: 
        """

        return self.__is_enable


    def set_role(self, role):
        """
        Method: set_role
        Description: 设置节点角色
        Parameter: 
            role: 节点的角色
        Return: 
        Others: 
        """

        self.__role = role
        
    def get_role(self):
        """
        Method: get_role
        Description: 获取节点的角色
        Parameter: 无
        Return: 节点的角色
        Others: 
        """

        return self.__role

    def is_role_unknown(self):
        """
        Method: is_role_unknown
        Description: 判断该节点的角色是否处于未知状态
        Parameter: 无
        Return: 该节点的角色是否处于未知状态
        Others: 
        """

        return self.__role == CLUSTER_ROLE_UNKNOWN


    def is_role_master(self):
        """
        Method: is_role_master
        Description: 判断该节点是否是master
        Parameter: 无
        Return: 该节点是否是master
        Others: 
        """

        return self.__role == CLUSTER_ROLE_MASTER

    
    def is_role_slave(self):
        """
        Method: is_role_slave
        Description: 判断该节点是否是slave
        Parameter: 无
        Return: 该节点是否是slave
        Others: 
        """

        return self.__role == CLUSTER_ROLE_SLAVE
        
    def is_online(self):
        """
        Method: is_online
        Description: 判断该节点是否在线
        Parameter: 无
        Return: 该节点是否在线
        Others: 
        """

        return self.__is_online


    def set_online(self, is_online):
        """
        Method: set_online
        Description: 设置该节点是否在线
        Parameter: 
            is_online: 是否在线
        Return: 
        Others: 
        """

        self.__is_online = is_online
