#coding=gbk
import threading

import cluster

from process_monitor.process_stat_mgr import ProcessStatMgr


class MonitorCluster(cluster.ClusterNode):
    def __init__(self, app):
        cluster.ClusterNode.__init__(self)
        self.__app = app
        self.__start_event = threading.Event()

        
                
    def on_start(self, role, state):
        self.__notify_state(cluster.CLUSTER_ROLE_UNKNOWN, cluster.CLUSTER_STATE_STARTING, role, state)
        
        if len(self.get_master_ip()) > 0:
            self.__start_event.set()
        
    def on_state_change(self, old_role, old_stats, new_role, new_state):
        if (old_role == new_role ==  cluster.CLUSTER_ROLE_SLAVE) and (new_state == cluster.CLUSTER_STATE_NO_MASTER):
            # ����Ǵ�������slave״̬���л���no master״̬������Ҫ֪ͨ�ϲ�   
            # ��Ϊ��ʱ����Ҫ�������̵Ȳ���
            return
            
        self.__notify_state(old_role, old_stats, new_role, new_state)
        
        if len(self.get_master_ip()) > 0:
            self.__start_event.set()
            
    def on_master_change(self, old_master_ip, new_master_ip):
        self.__app.on_master_change(old_master_ip, new_master_ip)

        if len(self.get_master_ip()) > 0:
            self.__start_event.set()
            
    def on_node_offline(self, node_ip):
        # �����ǰ��master����ô������ĳ���ڵ������ˣ���ô����ñ��ӿ�
        # ֪ͨ���ַ���ע����Ӧ��������Ϣ
        self.__app.on_node_offline(node_ip)

    def on_node_online(self, node_ip):
        # �����ǰ��master����ô������ĳ���ڵ������ˣ���ô����ñ��ӿ�
        self.__app.on_node_online(node_ip)

                
    def wait_until_start(self):
        # �ȴ�cluster�����о�״̬��ͨ����20���ڿ������
        # �ȴ�60���Ѿ��㹻
        return self.__start_event.wait(60)
        
    def __notify_state(self, old_role, old_stats, new_role, new_state):
    
        self.__app.on_cluster_state_change(old_role, old_stats, new_role, new_state, self.get_master_ip())
        
        
        
