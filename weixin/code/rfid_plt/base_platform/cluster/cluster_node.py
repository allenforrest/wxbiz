#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ��Ⱥ������Ϣ
Others:      
Key Class&Method List: 
             1. ClusterCfgInfo: ��Ⱥ��������Ϣ
             2. ClusterNode:��Ⱥ�Ľڵ�
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


# ��Ⱥ�����ļ��е���Ϣ
class ClusterCfgInfo:
    """
    Class: ClusterCfgInfo
    Description: ��Ⱥ��������Ϣ
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method: __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
        """


        # ���⼯Ⱥip
        self.virtual_cluster_ip = ""

        # ���⼯Ⱥip����
        self.virtual_cluster_mask = ""

        # ����ip���ڵ���������
        self.external_NIC = ""

        # �ڲ�ip
        self.my_inner_ip = ""

        self.max_nodes_num = 0


#def load_cur_cluster_node_info(app_top_path):
#    # �������ļ��м��ص�ǰ�ڵ��������Ϣ
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
    Description: ��Ⱥ�Ľڵ����
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method: __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
        """

        self.__cluster_thread = None
                   
    def is_master(self):
        """
        Method: is_master
        Description: �жϸýڵ��Ƿ���master
        Parameter: ��
        Return: �ýڵ��Ƿ���master
        Others: 
        """

        return self.__cluster_thread.is_master()
        
    def is_slave(self):
        """
        Method: is_slave
        Description: �жϸýڵ��Ƿ���slave
        Parameter: ��
        Return: �ýڵ��Ƿ���slave
        Others: 
        """

        return self.__cluster_thread.is_slave()

    def is_only_master(self):
        """
        Method: is_only_master
        Description: �жϵ�ǰ�ڵ㣬�Ƿ���only master��״̬
        Parameter: ��
        Return: ��ǰ�ڵ㣬�Ƿ���only master��״̬
        Others: 
        """

        # ��ǰ�Ƿ����master�ڵ�����
        return self.__cluster_thread.is_only_master()

    def get_master_ip(self):
        """
        Method: get_master_ip
        Description: ��ȡmaster��ip
        Parameter: ��
        Return: master��ip
        Others: 
        """

        return self.__cluster_thread.get_master_ip()


    def get_all_nodes(self):
        """
        Method: get_all_nodes
        Description: ��ȡȫ���Ľڵ�
        Parameter: ��
        Return: ȫ���Ľڵ�
        Others: 
        """

        return self.__cluster_thread.get_all_nodes()

    def rmv_node(self, ip):
        """
        Method: rmv_node
        Description: ɾ���ڵ�
        Parameter: 
            ip: �ڵ��ip
        Return: ������
        Others: 
        """

        return self.__cluster_thread.rmv_node(ip)

        
    def on_start(self, role, state):
        """
        Method: on_start
        Description: "�ڵ�����"����Ӧ�ӿ�
        Parameter: 
            role: �ڵ�Ľ�ɫ
            state: �ڵ��״̬
        Return: 
        Others: 
        """

        pass

    def on_state_change(self, old_role, old_stats, new_role, new_state):
        """
        Method: on_state_change
        Description: "�ڵ�״̬���"����Ӧ�ӿ�
        Parameter: 
            old_role: �仯ǰ�Ľ�ɫ
            old_stats: �仯ǰ��״̬
            new_role: �仯��Ľ�ɫ
            new_state: �仯���״̬
        Return: 
        Others: 
        """

        pass

    def on_master_change(self, old_master_ip, new_master_ip):
        """
        Method: on_master_change
        Description: "master�ڵ㷢���˱仯"����Ӧ�ӿ�
        Parameter: 
            old_master_ip: �仯ǰ��master��ip
            new_master_ip: �仯���master��ip
        Return: 
        Others: 
        """

        # ���old_master_ip==new_master_ip����ô˵��master��������λ
        pass

    def on_node_offline(self, node_ip):
        """
        Method: on_node_offline
        Description: "ĳ���ڵ�����"����Ӧ�ӿ�
        Parameter: 
            node_ip: �ڵ��ip
        Return: 
        Others: 
        """

        # �����ǰ��master����ô������ĳ���ڵ������ˣ���ô����ñ��ӿ�
        pass
        
    def on_node_online(self, node_ip):
        """
        Method: on_node_online
        Description: "ĳ���ڵ�������"����Ӧ�ӿ�
        Parameter: 
            node_ip: 
        Return: 
        Others: 
        """

        # �����ǰ��master����ô������ĳ���ڵ������ˣ���ô����ñ��ӿ�
        pass


    def start(self, cluster_cfg_info, app_top_path):
        """
        Method: start
        Description: �����ڵ�
        Parameter: 
            cluster_cfg_info:��Ⱥ��������Ϣ 
            app_top_path: ����ĸ�Ŀ¼
        Return: ������
        Others: 
        """

        # out_NIC: �������� outer Network Interface Card
        
        if self.__cluster_thread is not None:
            tracelog.error("can not start cluster node again when it is running.")
            return  err_code_mgr.ER_CLUSTER_START_FAILED
        
        tracelog.info("the cluster node is starting, cluster_ip:%s, my_ip:%s, "
                     "out_NIC:%s"%(cluster_cfg_info.virtual_cluster_ip
                                , cluster_cfg_info.my_inner_ip
                                , cluster_cfg_info.external_NIC))
                        
        cluster_thread = ClusterThread(self)
        
        # �����ڵ�
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
        Description: ֹͣ�ýڵ�
        Parameter: ��
        Return: 
        Others: 
        """

        # ֹͣ��ǰ�ڵ�
        if self.__cluster_thread is not None:
            self.__cluster_thread.stop_cluster()
        
        self.__cluster_thread.join(5)
        