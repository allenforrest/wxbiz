#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ���ʵ����ά����Ⱥ�ڵ�״̬���߳�
Others:      
Key Class&Method List: 
             1. ClusterServerEventHandler: �ڵ��ͨ��callacpͨ��ʱʹ�õ�EventHandler
             2. MasterNodeInfo: master�Ľڵ���Ϣ
             3. ClusterThread: ά����Ⱥ�ڵ�״̬���߳�
History: 
1. Date:
   Author:
   Modification:
"""

import os.path
import threading
import copy
import time
import multiprocessing

import tracelog
import pycallacp
import err_code_mgr
import utility



from cluster_const import *

from cluster.cluster_node_info import ClusterNodeInfo
from cluster.cluster_mit import ClusterMit
from cluster import cluster_cmd_code
from cluster.cluster_struct_def import ClusterStateMsg
from cluster.virtual_ip import bind_virtual_ip, unbind_virtual_ip





class ClusterServerEventHandler(pycallacp.AcpEventHandler):
    """
    Class: ClusterServerEventHandler
    Description: �ڵ��ͨ��callacpͨ��ʱʹ�õ�EventHandler
    Base: 
    Others: 
    """

    def __init__(self, cluster_thread):
        """
        Method: __init__
        Description: ���캯��
        Parameter: 
            cluster_thread: ClusterThread����
        Return: 
        Others: 
        """

        pycallacp.AcpEventHandler.__init__(self)
        self.__cluster_thread = cluster_thread
        
    def on_msg_received(self, url_or_srv_name, msg):
        """
        Method: on_msg_received
        Description: "�յ���Ϣ"�Ĵ���ӿ�
        Parameter: 
            url_or_srv_name: ��Ϣ�����ߵ�url
            msg: ��Ϣ
        Return: 
        Others: 
        """

        #print "on_msg_received", msg.get_cmd_code()
        
        cmd_code = msg.get_cmd_code()        
        if (cmd_code != cluster_cmd_code.CMD_CLUSTER_QUERY_STATE
           and cmd_code != cluster_cmd_code.CMD_CLUSTER_ACK_STATE):
           tracelog.error("ClusterServerEventHandler receved invalid msg:%d" % cmd_code)
           return
            
        try:
            state_msg = ClusterStateMsg.deserialize(msg.get_data())
            if state_msg is None:
                tracelog.error("ClusterStateMsg.deserialize failed. "
                                "msg:%d, %r" % (cmd_code, msg.get_data()))
                return
                
            if cmd_code == cluster_cmd_code.CMD_CLUSTER_QUERY_STATE:                
                self.__cluster_thread.on_query_state(url_or_srv_name, state_msg)
                
            elif cmd_code == cluster_cmd_code.CMD_CLUSTER_ACK_STATE:
                self.__cluster_thread.on_ack_state(state_msg)            
                
        except:
            tracelog.exception("handler msg(%d) failed" % cmd_code)
            
class MasterNodeInfo:
    """
    Class: MasterNodeInfo
    Description: master�Ľڵ���Ϣ
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method: __init__
        Description: 
        Parameter: ��
        Return: 
        Others: 
            master_ip: master��ip
            start_time: master������ʱ��
        """

        self.__master_ip = ""
        self.__start_time = ""

    def update(self, ip, start_time):
        """
        Method: update
        Description: ����master��ip������ʱ��
        Parameter: 
            ip: master��ip
            start_time: master������ʱ��
        Return: master����Ϣ�Ƿ����˱仯
        Others: 
        """

        is_change = False
        
        if self.__master_ip != ip or self.__start_time != start_time:
            is_change = True

        self.__master_ip = ip
        self.__start_time = start_time

        return is_change

    def get_ip(self):
        """
        Method: get_ip
        Description: ��ȡmaster��IP
        Parameter: ��
        Return: master��IP
        Others: 
        """

        return self.__master_ip

        
class ClusterThread(threading.Thread):
    """
    Class: ClusterThread
    Description: ά����Ⱥ�ڵ�״̬���߳�
    Base: threading.Thread
    Others: 
    """

    def __init__(self, cluster_node):
        """
        Method: __init__
        Description: ά����ǰ��Ⱥ�ڵ�״̬���߳�
        Parameter: 
            cluster_node: ClusterNode�Ķ���ʵ��
        Return: 
        Others: 
        """

        threading.Thread.__init__(self)
        self.daemon = True # �������߳�һ���˳�

        self.__cluster_node = cluster_node
        
        # ���ڼ�Ⱥ֮��ͨ�ŵ�callacpʵ��
        self.__callacp_srv = None
        self.__callacp_client = None

        # ��Ⱥ��������Ϣ
        self.__cluster_cfg_info = None

        # ���������нڵ�
        self.__other_nodes = []

        # ͨ��mit��ȡ��Ⱥ�ڵ����Ϣ
        self.__mit = None

        # �����װ�ĸ�Ŀ¼
        self.__app_top_path = ""

        self.__lock = threading.RLock()

        # ����������ѯ����ļ�����
        self.__query_counter = 0

        # ��ǰ�Ľ�ɫ
        self.__role = CLUSTER_ROLE_UNKNOWN
        
        # ��ǰ��״̬
        self.__state = CLUSTER_STATE_STARTING

        # �Ƿ��Ѿ���ֹͣ
        self.__stoped_event = multiprocessing.Event()

        # master����Ϣ
        self.__mater_node_info = MasterNodeInfo()
        
        # ������ʱ��
        self.__start_time = str(time.time())
  
    def __clear(self):
        """
        Method: __clear
        Description: ����ڲ�������
        Parameter: ��
        Return: 
        Others: 
        """

        if self.__callacp_srv is not None:
            self.__callacp_srv.clear()
            self.__callacp_srv = None
        
        if self.__callacp_client is not None:
            self.__callacp_client.clear()
            self.__callacp_client = None

        self.__cluster_cfg_info = None
        self.__other_nodes = []

        if self.__mit is not None:
            self.__mit.close()
            self.__mit = None
        
        self.__app_top_path = ""


    def is_master(self):   
        """
        Method: is_master
        Description: �жϵ�ǰ��ɫ�Ƿ���master
        Parameter: ��
        Return: ��ǰ��ɫ�Ƿ���master
        Others: 
        """

        with self.__lock:
            return self.__role == CLUSTER_ROLE_MASTER

    def is_only_master(self):
        """
        Method: is_only_master
        Description: �жϵ�ǰ�ڵ�Ľ�ɫ�Ƿ���mater�����ҽ���master�ڵ�û������slave�ڵ�
        Parameter: ��
        Return: ��ǰ�Ľ�ɫ�Ƿ���mater�����ҽ���master�ڵ�û������slave�ڵ�
        Others: 
        """

        with self.__lock:
            return self.__state == CLUSTER_STATE_ONLY_MASTER
    
    def is_slave(self):
        """
        Method: is_slave
        Description: �жϵ�ǰ�Ľڵ��ɫ�Ƿ���slave
        Parameter: ��
        Return: ��ǰ�Ľڵ��ɫ�Ƿ���slave
        Others: 
        """

        with self.__lock:
            return self.__role == CLUSTER_ROLE_SLAVE

    def get_role(self):
        """
        Method: get_role
        Description: ��ȡ��ǰ�ڵ�Ľ�ɫ
        Parameter: ��
        Return: ��ǰ�ڵ�Ľ�ɫ
        Others: 
        """

        with self.__lock:
            return self.__role

    def get_master_ip(self):
        """
        Method: get_master_ip
        Description: ��ȡmaster��ip
        Parameter: ��
        Return: master��ip
        Others: 
        """

        return self.__mater_node_info.get_ip()
        

    def get_all_nodes(self):
        """
        Method: get_all_nodes
        Description: ��ȡ���еĽڵ���Ϣ
        Parameter: ��
        Return: ���еĽڵ���Ϣ
        Others: 
        """

        # ��ȡ���е�nodes����Ϣ
        with self.__lock:
            all_nodes = copy.deepcopy(self.__other_nodes)
            
            myself = ClusterNodeInfo(self.__cluster_cfg_info.my_inner_ip)       
            myself.set_role(self.__role)  
            myself.set_online(True)            
            all_nodes.append(myself)

        return all_nodes

    def rmv_node(self, ip):
        """
        Method: rmv_node
        Description: ɾ��ָ���Ľڵ�
        Parameter: 
            ip: ָ���Ľڵ��ip
        Return: �����룬������Ϣ
        Others: 
        """

        online_err = (err_code_mgr.ER_CANNOT_RMV_ONLINE_CLUSTER_NODE
                        , err_code_mgr.get_error_msg(err_code_mgr.ER_CANNOT_RMV_ONLINE_CLUSTER_NODE))
                        
        with self.__lock:
            # ֻ����ɾ�����ߵĽڵ�
            if ip == self.__cluster_cfg_info.my_inner_ip:
                return online_err

            for node in self.__other_nodes:
                if node.get_ip() == ip and node.is_online():
                    return online_err
            
            # ��ɾ��mit�е���Ϣ
            ret_code, err_msg = self.__mit.rmv_node(ip)

            if ret_code == 0:
                # ɾ���ڴ��е���Ϣ
                self.__rmv_node(ip)
                
                tracelog.info("remvoe node %s." % ip)
            else:
                tracelog.error("remvoe node %s failed." % ip)

        return ret_code, err_msg
        
    def initial_cluster(self, cluster_cfg_info, app_top_path):
        """
        Method: initial_cluster
        Description: ��ʼ����Ⱥ
        Parameter: 
            cluster_cfg_info: ��Ⱥ��������Ϣ
            app_top_path: �����װ�ĸ�Ŀ¼
        Return: ������
        Others: 
        """

        # out_NIC: �������� outer Network Interface Card
                
        self.__clear()
        
        self.__cluster_cfg_info = cluster_cfg_info
        self.__app_top_path = app_top_path
        

        # ����callacp�ķ���˺Ϳͻ���
        self.__callacp_srv = pycallacp.CallAcpServer()
        self.__callacp_client = pycallacp.CallAcpClient()
        
        self.__callacp_srv.set_event_handler(ClusterServerEventHandler(self))
        self.__callacp_client.set_event_handler(ClusterServerEventHandler(self))

        self.__callacp_srv.set_msg_buf_max_num(3)
        self.__callacp_client.set_msg_buf_max_num(3)
        
        my_ip = cluster_cfg_info.my_inner_ip
        
        ret_code = self.__callacp_srv.bind(my_ip, CLUSTER_LISTEN_PORT)
        if ret_code != 0:
            tracelog.error("cluster: listen on (%s, %d) failed." % (
                            my_ip
                            , CLUSTER_LISTEN_PORT))
            return ret_code
        else:
            tracelog.info("cluster: listen on (%s, %d) ok." % (
                            my_ip
                            , CLUSTER_LISTEN_PORT))


        # ���¼���
        ret_code, cur_node = self.reload_nodes(True)
        if ret_code != 0:
            tracelog.error("load cluster nodes from DB failed. ret:%d" % ret_code)
            return ret_code

        # �ж��Լ��Ƿ��Ѿ�������DB�У���������������DB
        if cur_node is None:

            # �����ǰ��Ⱥ�ڵ��Ѿ��ﵽ������������ô�ͷ���ʧ��
            if len(self.__other_nodes) >= cluster_cfg_info.max_nodes_num:
                tracelog.error("The number of cluster nodes has reached the "
                                "maximum(%d)" % cluster_cfg_info.max_nodes_num)
                return err_code_mgr.ER_CLUSTER_REACH_MAX
                
            ret_code = self.__mit.save_node(my_ip, True)
            if ret_code != 0:
                tracelog.error("save current nodes to DB failed. ret:%d" % ret_code)
                return ret_code
        else:
            # �ж��Լ��Ƿ񱻽�����
            if not cur_node.is_enable():
                tracelog.error("the current node is disabled, can not start.")
                return err_code_mgr.ER_CLUSTER_IS_DISABLED
                
        # ����������ip
        self.__unbind_virtual_ip(False)

        return ret_code
                
    def stop_cluster(self):
        """
        Method: stop_cluster
        Description: ֹͣ��ǰ�Ľڵ�
        Parameter: ��
        Return: ��
        Others: 
        """

        # ֹͣ��ǰ�ڵ�
        self.__stoped_event.set()
    
        # ȡ��ip��
        if self.is_master():
            self.__unbind_virtual_ip(True)

    def is_node_prior(self, node):
        """
        Method: is_node_prior
        Description: �ж�ָ���Ľڵ���о����ȼ����Ƿ�ȵ�ǰ�ڵ�����ȼ���
        Parameter: 
            node: ���ȽϵĽڵ�
        Return: ָ���Ľڵ���о����ȼ����Ƿ�ȵ�ǰ�ڵ�����ȼ���
        Others: 
        """

        # �ڵ�node�����ȼ��Ƿ�ȵ�ǰ�ڵ��
        return node.get_ip() < self.__cluster_cfg_info.my_inner_ip

    def __get_url(self, node_ip):
        """
        Method: __get_url
        Description: ����ip��ȡ�ڵ��url
        Parameter: 
            node_ip: �ڵ��ip
        Return: �ڵ��url
        Others: 
        """

        return  "tcp://%s:%d" %(node_ip, CLUSTER_LISTEN_PORT)
        
    def __add_node(self, node_ip, is_enable):
        """
        Method: __add_node
        Description: ���ӽڵ�
        Parameter: 
            node_ip: �ڵ��ip
            is_enable: �Ƿ�������
        Return: ������
        Others: 
        """

        ret = 0
        
        if node_ip == self.__cluster_cfg_info.my_inner_ip:
            return ret

        for node in self.__other_nodes:
            if node.get_ip() == node_ip:
                break
        else:
            node_info = ClusterNodeInfo(node_ip)                
            if is_enable == 0:                    
                node_info.set_enable(False)

            self.__other_nodes.append(node_info)
            url = self.__get_url(node_ip)
            ret = self.__callacp_client.new_connect(url)
            if ret != 0:
                tracelog.error("new connection to cluster node failed. %s" % url)
                
        return ret

    def __rmv_node(self, node_ip):
        """
        Method: __rmv_node
        Description: ɾ���ڵ�
        Parameter: 
            node_ip: �ڵ��ip
        Return: 
        Others: 
        """

        for i, node in enumerate(self.__other_nodes):
            if node.get_ip() != node_ip:
                continue

            self.__other_nodes.pop(i)

            url = self.__get_url(node_ip)
            self.__callacp_client.rmv_connect(url)

    def reload_nodes(self, log_all_nodes = False):
        """
        Method: reload_nodes
        Description: �����ݿ������¼��ؽڵ���Ϣ
        Parameter: 
            log_all_nodes: �Ƿ����еĽڵ���Ϣ��¼��־
        Return: �����룬��ǰ�Ľڵ���Ϣ
        Others: 
        """

        # ��DB�ж�ȡ���нڵ����Ϣ
        # ����ֵ: ������, ��ǰnode
        cur_node = None
        
        with self.__lock:
            if self.__mit is None:
                try:
                    db_file = os.path.join(self.__app_top_path, "data", "sqlite", "cluster.db")
                    self.__mit = ClusterMit(db_file)
                except:
                    tracelog.exception("reload cluster node failed.")
                    return err_code_mgr.ER_CLUSTER_START_FAILED, None

            
            # �������еĽڵ���Ϣ
            other_nodes_ips = set([node.get_ip() for node in self.__other_nodes])
            
            nodes = self.__mit.get_all_nodes()
            for node in nodes:
                                                    
                if node.ip == self.__cluster_cfg_info.my_inner_ip:
                    cur_node = ClusterNodeInfo(node.ip)                
                    if node.is_enable == 0:                    
                        cur_node.set_enable(False)
                else:
                    other_nodes_ips.discard(node.ip)
                    ret = self.__add_node(node.ip, node.is_enable)
                    if ret != 0:
                        tracelog.error("add cluster node %s failed." % node.ip)
                        return err_code_mgr.ER_CLUSTER_START_FAILED, None

                if log_all_nodes is True:
                    tracelog.info("load cluster node: %s" % node.ip)

            # ɾ���Ѿ������ڵĽڵ�
            for node_ip in other_nodes_ips:
                self.__rmv_node(node_ip)
                
        return 0, cur_node

        
    def __when_starting(self):
        """
        Method: __when_starting
        Description: �����������еĴ�����
        Parameter: ��
        Return: 
        Others: 
        """

        has_other_enable_nodes = False
        has_other_online_nodes = False
        
        # ����Ƿ��нڵ㷵����Ӧ����Ϣ
        for node in self.__other_nodes:
            if not node.is_enable():
                continue

            has_other_enable_nodes = True
            
            if node.is_online():
                # ��slave��ʽ����
                has_other_online_nodes = True

                if node.is_role_master() and self.__mater_node_info.get_ip() == "":
                    self.__mater_node_info.update(node.get_ip(), node.get_start_time())
                    

        if has_other_online_nodes is True:
            self.__start_with_slave()
            return
    
        if has_other_enable_nodes is False:
            # û���������õĽڵ㣬��master��ʽ����
            tracelog.info("the current cluster node is the only enabled node.")            
            self.__start_with_master(CLUSTER_STATE_ONLY_MASTER)
            return
            
        # �������������CLUSTER_JUDGE_STATE_HAERTBEAT����������Ͳ�ѯ����
        # ������master��ʽ����
        if self.__query_counter < CLUSTER_JUDGE_STATE_HAERTBEAT:
            self.__query_other_node_state()
        else:
            tracelog.info("other cluster nodes didn't respond for state query command.")
            self.__start_with_master(CLUSTER_STATE_ONLY_MASTER)
            
    def __when_now_master(self):
        """
        Method: __when_now_master
        Description: ������master�Ĵ�����
        Parameter: ��
        Return: 
        Others: 
        """

        is_any_other_node_online = False

        with self.__lock:
            for node in self.__other_nodes:
                if not node.is_enable():
                    continue

                # ���ڵ��״̬���
                state_change = node.fetch_change_flag()
                if state_change == CLUSTER_NODE_STATE_CHANGE_ONLINE:
                    tracelog.info("cluster node %s is online" % node.get_ip())
                    # ��⵽�ڵ������ˣ�֪ͨ�ϲ�
                    self.__cluster_node.on_node_online(node.get_ip())
                    
                elif state_change == CLUSTER_NODE_STATE_CHANGE_OFFLINE:
                    tracelog.info("cluster node %s is offline" % node.get_ip())         
                    
                    # ��⵽�ڵ������ˣ�֪ͨ�ϲ�
                    self.__cluster_node.on_node_offline(node.get_ip())
                
                if not node.is_online():
                    continue

                is_any_other_node_online = True
                
                if node.is_role_master():              
                    # ����յ���ip��С��master�Ĳ�ѯ�����ô���л�Ϊslave
                    # ע�⣬����ip�Ƚ����ַ����ıȽϣ�ֻҪ���нڵ���㷨��һ�µľ�OK
                    if self.is_node_prior(node):
                        tracelog.info("cluster node %s is also master, this node will goto slave" % node.get_ip())
                        self.__mater_node_info.update(node.get_ip(), node.get_start_time())
                        self.__switch_to_slave()
                        return
                    else:
                        tracelog.info("cluster node %s is also master, that node will goto slave" % node.get_ip())
                else:
                    if self.__state == CLUSTER_STATE_ONLY_MASTER:
                        self.__change_state(CLUSTER_STATE_NORMAL)
                
        if is_any_other_node_online is False and self.__state == CLUSTER_STATE_NORMAL:
            self.__change_state(CLUSTER_STATE_ONLY_MASTER)
                        
        self.__query_other_node_state()
            
    def __when_now_slave(self):
        """
        Method: __when_now_slave
        Description: ������slave�Ĵ�����
        Parameter: ��
        Return: 
        Others: 
        """

        # û���յ�master�Ĳ�ѯ������û�������ڵ㣬��û���յ�ip��С��Ӧ��
        # ��ôתΪmaster   
        with self.__lock:
            for node in self.__other_nodes:
                if not node.is_enable():
                    continue
                
                if node.is_role_master():
                    node.check_heartbeat()
                    
                    if node.is_online():   
                        old_master_ip = self.__mater_node_info.get_ip()
                        if self.__mater_node_info.update(node.get_ip(), node.get_start_time()):
                            self.__cluster_node.on_master_change(old_master_ip, self.__mater_node_info.get_ip())
                            
                        return
                

        tracelog.info("the master cluster node is offline.")

        
        # �л�Ϊ����״̬
        self.__change_state(CLUSTER_STATE_NO_MASTER)
        self.__reset_query_counter(True)
        self.reload_nodes()

        
    def __when_now_no_master(self):
        """
        Method: __when_now_no_master
        Description: ������û��master�ڵ�״̬�Ĵ�����
        Parameter: ��
        Return: 
        Others: 
        """

        # ������״̬�£����û�������ڵ㣬����û���յ�ip��С��Ӧ��
        # ��ôתΪmaster
        # �Ƿ�����������ߵĽڵ�
        has_other_online_node = False

        # �Ƿ�������ȼ����ߡ��������ߵĽڵ�
        has_prior_online_node = False
        
        self.__query_other_node_state()

        with self.__lock:
            for node in self.__other_nodes:
                if not node.is_enable():
                    continue
                            
                if not node.is_online():
                    continue

                has_other_online_node = True
                
                if node.is_role_master():
                    tracelog.info("the cluster node %s become to master" % node.get_ip())
                    self.__mater_node_info.update(node.get_ip(), node.get_start_time())
                    self.__change_state(CLUSTER_STATE_NORMAL)
                    return
                
                if self.is_node_prior(node):
                    has_prior_online_node = True

        if has_prior_online_node is True:   
            # �ȴ������ڵ��Ϊmaster
            return

        if self.__query_counter >= CLUSTER_JUDGE_STATE_HAERTBEAT:
            tracelog.info("no higher priority cluster node respond for state query command.")

            if has_other_online_node:
                self.__switch_to_master(CLUSTER_STATE_NORMAL)
            else:
                self.__switch_to_master(CLUSTER_STATE_ONLY_MASTER)
            
        
    def run(self):
        """
        Method: run
        Description: �̵߳�run�ӿ�
        Parameter: ��
        Return: 
        Others: 
        """

        self.__reset_query_counter(True)

        reload_counter = 0
        reload_times = 30
        
        while 1:
            try:
                if self.__role == CLUSTER_ROLE_UNKNOWN:            
                    if self.__state == CLUSTER_STATE_STARTING:
                        self.__when_starting()
                        
                elif self.is_master():       
                    self.__when_now_master()
                    
                elif self.is_slave():
                    if self.__state == CLUSTER_STATE_NO_MASTER:
                        self.__when_now_no_master()
                    else:
                        self.__when_now_slave()
            except:
                tracelog.exception("error occur")
                
            if self.__stoped_event.wait(2) is True:                
                break

            reload_counter += 1
            
            if reload_counter == reload_times:
                self.reload_nodes()
                
                if self.is_master():
                    # ���ڳ��԰�ip
                    self.__bind_virtual_ip(False)
                    
                elif self.is_slave():
                    # ���ڳ���ȡ����ip
                    self.__unbind_virtual_ip(False)
                    
                reload_counter = 0

        self.__clear()
        tracelog.info("cluster node stoped.")
        
        
    def __bind_virtual_ip(self, write_log):
        """
        Method: __bind_virtual_ip
        Description: ������ip��ַ
        Parameter: 
            write_log: ����ʧ��ʱ���Ƿ��¼��־
        Return: ������
        Others: 
        """

        if self.__cluster_cfg_info.virtual_cluster_ip == "":
            return
        
        ret, msg = bind_virtual_ip(self.__cluster_cfg_info.virtual_cluster_ip
                            , self.__cluster_cfg_info.virtual_cluster_mask
                            , self.__cluster_cfg_info.external_NIC)
                            
        if ret != 0 and write_log:
            tracelog.error("bind_virtual_ip(%s/%s on %s) failed:%d, %s" % (
                            self.__cluster_cfg_info.virtual_cluster_ip
                            , self.__cluster_cfg_info.virtual_cluster_mask
                            , self.__cluster_cfg_info.external_NIC
                            , ret
                            , msg))
            
        return ret

    def __unbind_virtual_ip(self, write_log):
        """
        Method: __unbind_virtual_ip
        Description: ����󶨵�����ip
        Parameter: 
            write_log: ���������ipʧ��ʱ���Ƿ���Ҫ��¼��־
        Return: ������
        Others: 
        """

        if self.__cluster_cfg_info.virtual_cluster_ip == "":
            return

        ret, msg = unbind_virtual_ip(self.__cluster_cfg_info.virtual_cluster_ip
                                , self.__cluster_cfg_info.virtual_cluster_mask
                                , self.__cluster_cfg_info.external_NIC)
                                
        if ret != 0 and write_log:
            tracelog.error("unbind_virtual_ip(%s/%s on %s) failed:%d, %s" % (
                            self.__cluster_cfg_info.virtual_cluster_ip
                            , self.__cluster_cfg_info.virtual_cluster_mask
                            , self.__cluster_cfg_info.external_NIC
                            , ret
                            , msg))
            
        return ret


       

    def __start_with_master(self, state):
        """
        Method: __start_with_master
        Description: ʹ��master��ɫ������ǰ�ڵ�
        Parameter: 
            state: ״̬
        Return: 
        Others: 
        """

        # ��master����
        self.__role = CLUSTER_ROLE_MASTER
        self.__state = state
        self.__mater_node_info.update(self.__cluster_cfg_info.my_inner_ip, self.__start_time)
        
        tracelog.info("the current cluster node %s start with master, state:%d." % (
                          self.__cluster_cfg_info.my_inner_ip
                        , state))
        
        self.__cluster_node.on_start(self.__role, state)

        # ����master״̬���������������ڵ��״̬
        self.__reset_query_counter(True)
        

    def __start_with_slave(self):
        """
        Method: __start_with_slave
        Description: ʹ��slave��ɫ������ǰ�ڵ�
        Parameter: ��
        Return: 
        Others: 
        """

        # ��slave����
        self.__role = CLUSTER_ROLE_SLAVE
        self.__state = CLUSTER_STATE_NORMAL
        self.__mater_node_info.update("", "")
        
        tracelog.info("the current cluster node %s start with slave." % self.__cluster_cfg_info.my_inner_ip)

        self.__cluster_node.on_start(self.__role, self.__state)

    def __switch_to_master(self, state):
        """
        Method: __switch_to_master
        Description: ����ɫ�л���master
        Parameter: 
            state: ״̬
        Return: 
        Others: 
        """

        # �л���master

        old_role = self.__role
        old_state = self.__state
        self.__mater_node_info.update(self.__cluster_cfg_info.my_inner_ip, self.__start_time)
        
        self.__role = CLUSTER_ROLE_MASTER
        self.__state = state
        tracelog.info("the current cluster node %s switch to master. state:%d" % (
                          self.__cluster_cfg_info.my_inner_ip
                        , state))

        ret_code  = self.__bind_virtual_ip(True)
        if ret_code != 0:
            tracelog.error("bind virtual ip faild. ret_code:%d" % ret_code)

        self.__cluster_node.on_state_change(old_role, old_state, self.__role, state)

        # ����master״̬���������������ڵ��״̬
        self.__reset_query_counter(True)
        
    def __switch_to_slave(self):
        """
        Method: __switch_to_slave
        Description: ����ɫ�л���slave
        Parameter: ��
        Return: 
        Others: 
        """

        # �л���slave

        old_role = self.__role
        old_state = self.__state
        
        self.__role = CLUSTER_ROLE_SLAVE
        self.__state = CLUSTER_STATE_NORMAL
        tracelog.info("the current cluster node %s switch to slave. state:%d" % (
                            self.__cluster_cfg_info.my_inner_ip
                           , state))

        ret_code  = self.__unbind_virtual_ip(True)
        if ret_code != 0:
            tracelog.error("unbind virtual ip faild. ret_code:%d" % ret_code)
            
        self.__cluster_node.on_state_change(old_role, old_state, self.__role, state)
        
    def __change_state(self, state):
        """
        Method: __change_state
        Description: �л���ǰ��״̬
        Parameter: 
            state: 
        Return: 
        Others: 
        """

        old_state = self.__state
        
        self.__state = state
        tracelog.info("the current cluster node %s change state:%d" % (
                            self.__cluster_cfg_info.my_inner_ip
                           , state))

        self.__cluster_node.on_state_change(self.__role, old_state, self.__role, state)
        
    def __query_other_node_state(self):
        """
        Method: __query_other_node_state
        Description: ��ѯ�����ڵ��״̬
        Parameter: ��
        Return: 
        Others: 
        """

        req_msg = self.__get_state_msg(cluster_cmd_code.CMD_CLUSTER_QUERY_STATE)

        
        with self.__lock:
            for node in self.__other_nodes:
                # ����״̬��ѯ������ڵ�
                url = self.__get_url(node.get_ip())
                self.__callacp_client.send(url, req_msg)                    
                
                # ���½ڵ����������
                node.check_heartbeat()


        self.__query_counter += 1
        
    def __reset_query_counter(self, set_nodes_to_offline):
        """
        Method: __reset_query_counter
        Description: ����������ѯ�ļ�����
        Parameter: 
            set_nodes_to_offline: �Ƿ�ͬʱ���ýڵ�Ϊ����
        Return: 
        Others: 
        """

        self.__query_counter = 0

        for node in self.__other_nodes:
            node.reset_heartbeat(set_nodes_to_offline)



    def __get_state_msg(self, cmd_code):
        """
        Method: __get_state_msg
        Description: ����״̬Ӧ����Ϣ
        Parameter: 
            cmd_code: ������
        Return: 
        Others: 
        """

        state = ClusterStateMsg()
        state.ip = self.__cluster_cfg_info.my_inner_ip
        state.role = self.get_role()
        state.start_time = self.__start_time
        msg = pycallacp.AcpMessage(cmd_code
                                 , state.serialize())
        return msg
        
    def on_query_state(self, url, msg):
        """
        Method: on_query_state
        Description: "��ѯ״̬"�Ĵ���ӿ�
        Parameter: 
            url: ���Ͳ�ѯ�ߵ�url(�Զ˵�url)
            msg: ��ѯ��Ϣ
        Return: 
        Others: 
        """


        try_times = 1
        
        with self.__lock:
            while try_times <= 2:
                for node in self.__other_nodes:
                    if node.get_ip() == msg.ip:
                        node.on_heartbeat(msg)  
                        try_times = 3
                        break
                else:                    
                    if try_times == 2:
                        tracelog.error("the cluster node %s is unknown" % msg.ip)
                    else:
                        # ���´�DB�м��ؽڵ���Ϣ
                        tracelog.error("receive state query cmd from unknown "
                                "node:%s now try to reload nodes" % msg.ip)
                        self.reload_nodes()
                        
                    try_times += 1

        # ����Ӧ����Ϣ
        ack_msg = self.__get_state_msg(cluster_cmd_code.CMD_CLUSTER_ACK_STATE)
        self.__callacp_srv.send(url, ack_msg)

    def on_ack_state(self,  msg):
        """
        Method: on_ack_state
        Description: �յ�״̬��ѯ��Ӧ����Ϣ
        Parameter: 
            msg: ״̬��ѯ��Ӧ����Ϣ
        Return: 
        Others: 
        """

        with self.__lock:
            for node in self.__other_nodes:
                if node.get_ip() == msg.ip:
                    node.on_heartbeat(msg)
                    break
            else:
                tracelog.error("receive state ack cmd from unknown node:%s" % msg.ip)
        
