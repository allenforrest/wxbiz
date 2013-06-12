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
            # 如果是从正常的slave状态，切换到no master状态，则不需要通知上层   
            # 因为此时不需要重启进程等操作
            return
            
        self.__notify_state(old_role, old_stats, new_role, new_state)
        
        if len(self.get_master_ip()) > 0:
            self.__start_event.set()
            
    def on_master_change(self, old_master_ip, new_master_ip):
        self.__app.on_master_change(old_master_ip, new_master_ip)

        if len(self.get_master_ip()) > 0:
            self.__start_event.set()
            
    def on_node_offline(self, node_ip):
        # 如果当前是master，那么当其他某个节点离线了，那么会调用本接口
        # 通知名字服务注销相应的名字信息
        self.__app.on_node_offline(node_ip)

    def on_node_online(self, node_ip):
        # 如果当前是master，那么当其他某个节点上线了，那么会调用本接口
        self.__app.on_node_online(node_ip)

                
    def wait_until_start(self):
        # 等待cluster启动判决状态，通常在20秒内可以完成
        # 等待60秒已经足够
        return self.__start_event.wait(60)
        
    def __notify_state(self, old_role, old_stats, new_role, new_state):
    
        self.__app.on_cluster_state_change(old_role, old_stats, new_role, new_state, self.get_master_ip())
        
        
        
