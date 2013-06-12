#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��ж����˼�Ⱥ�ڵ����Ϣ����
Others:      
Key Class&Method List: 
             1. ClusterNodeInfo: ��Ⱥ�ڵ����Ϣ����
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
    Description: ��Ⱥ�ڵ����Ϣ����
    Base: 
    Others: 
    """

    def __init__(self, ip):
        """
        Method: __init__
        Description: ���캯��
        Parameter: 
            ip: �ڵ��ip
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
        Description: �������
        Parameter: ��
        Return: 
        Others: 
        """

        # master���slave�ĳ�ʱʱ�� > slave���master�ĳ�ʱʱ��
        # Ϊ�˷�ֹ��������£�master��Ϊslave�Ѿ����ߣ�slaveȴ��Ϊmaster���ߵ�����£�
        # slave�����ֱ�ע��������slave�Լ�ȴ��֪������������ע�����ַ���
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
        Description: �յ������Ĵ���ӿ�
        Parameter: 
            msg: ������Ϣ
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
        Description: ��ȡ״̬����ı�ǣ��������øñ��
        Parameter: ��
        Return: ״̬����ı��
        Others: 
        """

        tmp = self.__stat_change_flag
        self.__stat_change_flag = CLUSTER_NODE_STATE_NOCHANGE
        return tmp
        
        
    def reset_heartbeat(self, set_nodes_to_offline):
        """
        Method: reset_heartbeat
        Description: ��������
        Parameter: 
            set_nodes_to_offline: �Ƿ�ͬʱ����Ϊ����
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
        Description: ��ȡ�ڵ��ip
        Parameter: ��
        Return: 
            �ڵ��ip
        Others: 
        """

        return self.__ip

    def set_ip(self, ip):
        """
        Method: set_ip
        Description: ���ýڵ��ip
        Parameter: 
            ip: �ڵ��ip
        Return: 
        Others: 
        """

        self.__ip = ip

    def get_start_time(self):
        """
        Method: get_start_time
        Description: ��ȡ����ʱ��
        Parameter: ��
        Return: �ڵ������ʱ��
        Others: 
        """

        return self.__start_time
        
    def set_enable(self, is_enable):
        """
        Method: set_enable
        Description: �����Ƿ�����
        Parameter: 
            is_enable: �Ƿ�����
        Return: 
        Others: 
        """

        self.__is_enable = is_enable

    def is_enable(self):
        """
        Method: is_enable
        Description: �жϽڵ��Ƿ�����
        Parameter: ��
        Return: �ڵ��Ƿ�����
        Others: 
        """

        return self.__is_enable


    def set_role(self, role):
        """
        Method: set_role
        Description: ���ýڵ��ɫ
        Parameter: 
            role: �ڵ�Ľ�ɫ
        Return: 
        Others: 
        """

        self.__role = role
        
    def get_role(self):
        """
        Method: get_role
        Description: ��ȡ�ڵ�Ľ�ɫ
        Parameter: ��
        Return: �ڵ�Ľ�ɫ
        Others: 
        """

        return self.__role

    def is_role_unknown(self):
        """
        Method: is_role_unknown
        Description: �жϸýڵ�Ľ�ɫ�Ƿ���δ֪״̬
        Parameter: ��
        Return: �ýڵ�Ľ�ɫ�Ƿ���δ֪״̬
        Others: 
        """

        return self.__role == CLUSTER_ROLE_UNKNOWN


    def is_role_master(self):
        """
        Method: is_role_master
        Description: �жϸýڵ��Ƿ���master
        Parameter: ��
        Return: �ýڵ��Ƿ���master
        Others: 
        """

        return self.__role == CLUSTER_ROLE_MASTER

    
    def is_role_slave(self):
        """
        Method: is_role_slave
        Description: �жϸýڵ��Ƿ���slave
        Parameter: ��
        Return: �ýڵ��Ƿ���slave
        Others: 
        """

        return self.__role == CLUSTER_ROLE_SLAVE
        
    def is_online(self):
        """
        Method: is_online
        Description: �жϸýڵ��Ƿ�����
        Parameter: ��
        Return: �ýڵ��Ƿ�����
        Others: 
        """

        return self.__is_online


    def set_online(self, is_online):
        """
        Method: set_online
        Description: ���øýڵ��Ƿ�����
        Parameter: 
            is_online: �Ƿ�����
        Return: 
        Others: 
        """

        self.__is_online = is_online
