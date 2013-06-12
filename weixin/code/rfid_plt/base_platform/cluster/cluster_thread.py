#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中实现了维护集群节点状态的线程
Others:      
Key Class&Method List: 
             1. ClusterServerEventHandler: 节点间通过callacp通信时使用的EventHandler
             2. MasterNodeInfo: master的节点信息
             3. ClusterThread: 维护集群节点状态的线程
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
    Description: 节点间通过callacp通信时使用的EventHandler
    Base: 
    Others: 
    """

    def __init__(self, cluster_thread):
        """
        Method: __init__
        Description: 构造函数
        Parameter: 
            cluster_thread: ClusterThread对象
        Return: 
        Others: 
        """

        pycallacp.AcpEventHandler.__init__(self)
        self.__cluster_thread = cluster_thread
        
    def on_msg_received(self, url_or_srv_name, msg):
        """
        Method: on_msg_received
        Description: "收到消息"的处理接口
        Parameter: 
            url_or_srv_name: 消息发送者的url
            msg: 消息
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
    Description: master的节点信息
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method: __init__
        Description: 
        Parameter: 无
        Return: 
        Others: 
            master_ip: master的ip
            start_time: master的启动时间
        """

        self.__master_ip = ""
        self.__start_time = ""

    def update(self, ip, start_time):
        """
        Method: update
        Description: 更新master的ip和启动时间
        Parameter: 
            ip: master的ip
            start_time: master的启动时间
        Return: master的信息是否发生了变化
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
        Description: 获取master的IP
        Parameter: 无
        Return: master的IP
        Others: 
        """

        return self.__master_ip

        
class ClusterThread(threading.Thread):
    """
    Class: ClusterThread
    Description: 维护集群节点状态的线程
    Base: threading.Thread
    Others: 
    """

    def __init__(self, cluster_node):
        """
        Method: __init__
        Description: 维护当前集群节点状态的线程
        Parameter: 
            cluster_node: ClusterNode的对象实例
        Return: 
        Others: 
        """

        threading.Thread.__init__(self)
        self.daemon = True # 跟随主线程一起退出

        self.__cluster_node = cluster_node
        
        # 用于集群之间通信的callacp实例
        self.__callacp_srv = None
        self.__callacp_client = None

        # 集群的配置信息
        self.__cluster_cfg_info = None

        # 其他的所有节点
        self.__other_nodes = []

        # 通过mit获取集群节点的信息
        self.__mit = None

        # 软件安装的根目录
        self.__app_top_path = ""

        self.__lock = threading.RLock()

        # 发送心跳查询命令的计数器
        self.__query_counter = 0

        # 当前的角色
        self.__role = CLUSTER_ROLE_UNKNOWN
        
        # 当前的状态
        self.__state = CLUSTER_STATE_STARTING

        # 是否已经被停止
        self.__stoped_event = multiprocessing.Event()

        # master的信息
        self.__mater_node_info = MasterNodeInfo()
        
        # 启动的时间
        self.__start_time = str(time.time())
  
    def __clear(self):
        """
        Method: __clear
        Description: 情况内部的数据
        Parameter: 无
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
        Description: 判断当前角色是否是master
        Parameter: 无
        Return: 当前角色是否是master
        Others: 
        """

        with self.__lock:
            return self.__role == CLUSTER_ROLE_MASTER

    def is_only_master(self):
        """
        Method: is_only_master
        Description: 判断当前节点的角色是否是mater，并且仅有master节点没有其他slave节点
        Parameter: 无
        Return: 当前的角色是否是mater，并且仅有master节点没有其他slave节点
        Others: 
        """

        with self.__lock:
            return self.__state == CLUSTER_STATE_ONLY_MASTER
    
    def is_slave(self):
        """
        Method: is_slave
        Description: 判断当前的节点角色是否是slave
        Parameter: 无
        Return: 当前的节点角色是否是slave
        Others: 
        """

        with self.__lock:
            return self.__role == CLUSTER_ROLE_SLAVE

    def get_role(self):
        """
        Method: get_role
        Description: 获取当前节点的角色
        Parameter: 无
        Return: 当前节点的角色
        Others: 
        """

        with self.__lock:
            return self.__role

    def get_master_ip(self):
        """
        Method: get_master_ip
        Description: 获取master的ip
        Parameter: 无
        Return: master的ip
        Others: 
        """

        return self.__mater_node_info.get_ip()
        

    def get_all_nodes(self):
        """
        Method: get_all_nodes
        Description: 获取所有的节点信息
        Parameter: 无
        Return: 所有的节点信息
        Others: 
        """

        # 获取所有的nodes的信息
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
        Description: 删除指定的节点
        Parameter: 
            ip: 指定的节点的ip
        Return: 错误码，错误信息
        Others: 
        """

        online_err = (err_code_mgr.ER_CANNOT_RMV_ONLINE_CLUSTER_NODE
                        , err_code_mgr.get_error_msg(err_code_mgr.ER_CANNOT_RMV_ONLINE_CLUSTER_NODE))
                        
        with self.__lock:
            # 只允许删除离线的节点
            if ip == self.__cluster_cfg_info.my_inner_ip:
                return online_err

            for node in self.__other_nodes:
                if node.get_ip() == ip and node.is_online():
                    return online_err
            
            # 先删除mit中的信息
            ret_code, err_msg = self.__mit.rmv_node(ip)

            if ret_code == 0:
                # 删除内存中的信息
                self.__rmv_node(ip)
                
                tracelog.info("remvoe node %s." % ip)
            else:
                tracelog.error("remvoe node %s failed." % ip)

        return ret_code, err_msg
        
    def initial_cluster(self, cluster_cfg_info, app_top_path):
        """
        Method: initial_cluster
        Description: 初始化集群
        Parameter: 
            cluster_cfg_info: 集群的配置信息
            app_top_path: 软件安装的根目录
        Return: 错误码
        Others: 
        """

        # out_NIC: 外网网卡 outer Network Interface Card
                
        self.__clear()
        
        self.__cluster_cfg_info = cluster_cfg_info
        self.__app_top_path = app_top_path
        

        # 启动callacp的服务端和客户端
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


        # 重新加载
        ret_code, cur_node = self.reload_nodes(True)
        if ret_code != 0:
            tracelog.error("load cluster nodes from DB failed. ret:%d" % ret_code)
            return ret_code

        # 判断自己是否已经存在于DB中，如果不存在则插入DB
        if cur_node is None:

            # 如果当前集群节点已经达到了最大个数，那么就返回失败
            if len(self.__other_nodes) >= cluster_cfg_info.max_nodes_num:
                tracelog.error("The number of cluster nodes has reached the "
                                "maximum(%d)" % cluster_cfg_info.max_nodes_num)
                return err_code_mgr.ER_CLUSTER_REACH_MAX
                
            ret_code = self.__mit.save_node(my_ip, True)
            if ret_code != 0:
                tracelog.error("save current nodes to DB failed. ret:%d" % ret_code)
                return ret_code
        else:
            # 判断自己是否被禁用了
            if not cur_node.is_enable():
                tracelog.error("the current node is disabled, can not start.")
                return err_code_mgr.ER_CLUSTER_IS_DISABLED
                
        # 绑定网卡虚拟ip
        self.__unbind_virtual_ip(False)

        return ret_code
                
    def stop_cluster(self):
        """
        Method: stop_cluster
        Description: 停止当前的节点
        Parameter: 无
        Return: 无
        Others: 
        """

        # 停止当前节点
        self.__stoped_event.set()
    
        # 取消ip绑定
        if self.is_master():
            self.__unbind_virtual_ip(True)

    def is_node_prior(self, node):
        """
        Method: is_node_prior
        Description: 判断指定的节点的判决优先级，是否比当前节点的优先级高
        Parameter: 
            node: 待比较的节点
        Return: 指定的节点的判决优先级，是否比当前节点的优先级高
        Others: 
        """

        # 节点node的优先级是否比当前节点高
        return node.get_ip() < self.__cluster_cfg_info.my_inner_ip

    def __get_url(self, node_ip):
        """
        Method: __get_url
        Description: 根据ip获取节点的url
        Parameter: 
            node_ip: 节点的ip
        Return: 节点的url
        Others: 
        """

        return  "tcp://%s:%d" %(node_ip, CLUSTER_LISTEN_PORT)
        
    def __add_node(self, node_ip, is_enable):
        """
        Method: __add_node
        Description: 增加节点
        Parameter: 
            node_ip: 节点的ip
            is_enable: 是否启用了
        Return: 错误码
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
        Description: 删除节点
        Parameter: 
            node_ip: 节点的ip
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
        Description: 从数据库中重新记载节点信息
        Parameter: 
            log_all_nodes: 是否将所有的节点信息记录日志
        Return: 错误码，当前的节点信息
        Others: 
        """

        # 从DB中读取所有节点的信息
        # 返回值: 错误码, 当前node
        cur_node = None
        
        with self.__lock:
            if self.__mit is None:
                try:
                    db_file = os.path.join(self.__app_top_path, "data", "sqlite", "cluster.db")
                    self.__mit = ClusterMit(db_file)
                except:
                    tracelog.exception("reload cluster node failed.")
                    return err_code_mgr.ER_CLUSTER_START_FAILED, None

            
            # 加载所有的节点信息
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

            # 删除已经不存在的节点
            for node_ip in other_nodes_ips:
                self.__rmv_node(node_ip)
                
        return 0, cur_node

        
    def __when_starting(self):
        """
        Method: __when_starting
        Description: 当处于启动中的处理函数
        Parameter: 无
        Return: 
        Others: 
        """

        has_other_enable_nodes = False
        has_other_online_nodes = False
        
        # 检查是否有节点返回了应答消息
        for node in self.__other_nodes:
            if not node.is_enable():
                continue

            has_other_enable_nodes = True
            
            if node.is_online():
                # 以slave方式启动
                has_other_online_nodes = True

                if node.is_role_master() and self.__mater_node_info.get_ip() == "":
                    self.__mater_node_info.update(node.get_ip(), node.get_start_time())
                    

        if has_other_online_nodes is True:
            self.__start_with_slave()
            return
    
        if has_other_enable_nodes is False:
            # 没有其他可用的节点，以master方式启动
            tracelog.info("the current cluster node is the only enabled node.")            
            self.__start_with_master(CLUSTER_STATE_ONLY_MASTER)
            return
            
        # 如果计数器少于CLUSTER_JUDGE_STATE_HAERTBEAT，则继续发送查询命令
        # 否则，以master方式启动
        if self.__query_counter < CLUSTER_JUDGE_STATE_HAERTBEAT:
            self.__query_other_node_state()
        else:
            tracelog.info("other cluster nodes didn't respond for state query command.")
            self.__start_with_master(CLUSTER_STATE_ONLY_MASTER)
            
    def __when_now_master(self):
        """
        Method: __when_now_master
        Description: 当处于master的处理函数
        Parameter: 无
        Return: 
        Others: 
        """

        is_any_other_node_online = False

        with self.__lock:
            for node in self.__other_nodes:
                if not node.is_enable():
                    continue

                # 检查节点的状态变更
                state_change = node.fetch_change_flag()
                if state_change == CLUSTER_NODE_STATE_CHANGE_ONLINE:
                    tracelog.info("cluster node %s is online" % node.get_ip())
                    # 监测到节点离线了，通知上层
                    self.__cluster_node.on_node_online(node.get_ip())
                    
                elif state_change == CLUSTER_NODE_STATE_CHANGE_OFFLINE:
                    tracelog.info("cluster node %s is offline" % node.get_ip())         
                    
                    # 监测到节点离线了，通知上层
                    self.__cluster_node.on_node_offline(node.get_ip())
                
                if not node.is_online():
                    continue

                is_any_other_node_online = True
                
                if node.is_role_master():              
                    # 如果收到了ip更小的master的查询命令，那么就切换为slave
                    # 注意，这里ip比较是字符串的比较，只要所有节点的算法是一致的就OK
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
        Description: 当处于slave的处理函数
        Parameter: 无
        Return: 
        Others: 
        """

        # 没有收到master的查询，并且没有其他节点，或没有收到ip更小的应答
        # 那么转为master   
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

        
        # 切换为无主状态
        self.__change_state(CLUSTER_STATE_NO_MASTER)
        self.__reset_query_counter(True)
        self.reload_nodes()

        
    def __when_now_no_master(self):
        """
        Method: __when_now_no_master
        Description: 当处于没有master节点状态的处理函数
        Parameter: 无
        Return: 
        Others: 
        """

        # 当无主状态下，如果没有其他节点，或者没有收到ip更小的应答
        # 那么转为master
        # 是否存在其他在线的节点
        has_other_online_node = False

        # 是否存在优先级更高、并且在线的节点
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
            # 等待其他节点成为master
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
        Description: 线程的run接口
        Parameter: 无
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
                    # 定期尝试绑定ip
                    self.__bind_virtual_ip(False)
                    
                elif self.is_slave():
                    # 定期尝试取消绑定ip
                    self.__unbind_virtual_ip(False)
                    
                reload_counter = 0

        self.__clear()
        tracelog.info("cluster node stoped.")
        
        
    def __bind_virtual_ip(self, write_log):
        """
        Method: __bind_virtual_ip
        Description: 绑定虚拟ip地址
        Parameter: 
            write_log: 当绑定失败时，是否记录日志
        Return: 错误码
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
        Description: 解除绑定的虚拟ip
        Parameter: 
            write_log: 解除绑定虚拟ip失败时，是否需要记录日志
        Return: 错误码
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
        Description: 使用master角色启动当前节点
        Parameter: 
            state: 状态
        Return: 
        Others: 
        """

        # 以master启动
        self.__role = CLUSTER_ROLE_MASTER
        self.__state = state
        self.__mater_node_info.update(self.__cluster_cfg_info.my_inner_ip, self.__start_time)
        
        tracelog.info("the current cluster node %s start with master, state:%d." % (
                          self.__cluster_cfg_info.my_inner_ip
                        , state))
        
        self.__cluster_node.on_start(self.__role, state)

        # 进入master状态后，重新设置其他节点的状态
        self.__reset_query_counter(True)
        

    def __start_with_slave(self):
        """
        Method: __start_with_slave
        Description: 使用slave角色启动当前节点
        Parameter: 无
        Return: 
        Others: 
        """

        # 以slave启动
        self.__role = CLUSTER_ROLE_SLAVE
        self.__state = CLUSTER_STATE_NORMAL
        self.__mater_node_info.update("", "")
        
        tracelog.info("the current cluster node %s start with slave." % self.__cluster_cfg_info.my_inner_ip)

        self.__cluster_node.on_start(self.__role, self.__state)

    def __switch_to_master(self, state):
        """
        Method: __switch_to_master
        Description: 将角色切换到master
        Parameter: 
            state: 状态
        Return: 
        Others: 
        """

        # 切换到master

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

        # 进入master状态后，重新设置其他节点的状态
        self.__reset_query_counter(True)
        
    def __switch_to_slave(self):
        """
        Method: __switch_to_slave
        Description: 将角色切换到slave
        Parameter: 无
        Return: 
        Others: 
        """

        # 切换到slave

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
        Description: 切换当前的状态
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
        Description: 查询其他节点的状态
        Parameter: 无
        Return: 
        Others: 
        """

        req_msg = self.__get_state_msg(cluster_cmd_code.CMD_CLUSTER_QUERY_STATE)

        
        with self.__lock:
            for node in self.__other_nodes:
                # 发送状态查询命令给节点
                url = self.__get_url(node.get_ip())
                self.__callacp_client.send(url, req_msg)                    
                
                # 更新节点的心跳计数
                node.check_heartbeat()


        self.__query_counter += 1
        
    def __reset_query_counter(self, set_nodes_to_offline):
        """
        Method: __reset_query_counter
        Description: 重置心跳查询的计数器
        Parameter: 
            set_nodes_to_offline: 是否同时设置节点为离线
        Return: 
        Others: 
        """

        self.__query_counter = 0

        for node in self.__other_nodes:
            node.reset_heartbeat(set_nodes_to_offline)



    def __get_state_msg(self, cmd_code):
        """
        Method: __get_state_msg
        Description: 生成状态应答消息
        Parameter: 
            cmd_code: 命令码
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
        Description: "查询状态"的处理接口
        Parameter: 
            url: 发送查询者的url(对端的url)
            msg: 查询消息
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
                        # 重新从DB中加载节点信息
                        tracelog.error("receive state query cmd from unknown "
                                "node:%s now try to reload nodes" % msg.ip)
                        self.reload_nodes()
                        
                    try_times += 1

        # 发送应答消息
        ack_msg = self.__get_state_msg(cluster_cmd_code.CMD_CLUSTER_ACK_STATE)
        self.__callacp_srv.send(url, ack_msg)

    def on_ack_state(self,  msg):
        """
        Method: on_ack_state
        Description: 收到状态查询的应答消息
        Parameter: 
            msg: 状态查询的应答消息
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
        
