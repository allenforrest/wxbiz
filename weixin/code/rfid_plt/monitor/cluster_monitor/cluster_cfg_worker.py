#coding=gbk

import bundleframework as bf
import tracelog
import err_code_mgr
import cluster_msg_def
import monitor_cmd_code
import cluster

class QueryClusterNodeHandler(bf.CmdHandler):
    """
    Class: QueryClusterNodeHandler
    Description: 查询cluster的节点信息
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理消息
        Parameter: 
            frame: AppFrame
        Return: 无
        Others: 
        """

        rep = cluster_msg_def.QueryClusterNodeResponse()
        rep.node_list = []

        cur_cluster = self.get_worker().get_cur_cluster()

        if cur_cluster is None:
            # cur_cluster is None说明当前没有启用cluster
            # 那么只需要返回当前节点的信息
            one_node = cluster_msg_def.ClusterNodeInfo()
            one_node.ip = self.get_worker().get_app().get_device_cfg_info().get_device_internal_ip()
            one_node.is_online = 1
            one_node.role = cluster.CLUSTER_ROLE_MASTER
            rep.node_list.append(one_node)
        else:
            all_nodes = cur_cluster.get_all_nodes()
            for node in all_nodes:
                one_node = cluster_msg_def.ClusterNodeInfo()
                one_node.ip = node.get_ip()
                one_node.is_online = 1 if node.is_online() else 0
                one_node.role = node.get_role()
                rep.node_list.append(one_node)
        

        # 发送应答
        self.get_worker().send_ack(frame,rep.serialize())
        


class RmvClusterNodeHandler(bf.CmdHandler):
    """
    Class: QueryClusterNodeHandler
    Description: 查询cluster的节点信息
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理消息
        Parameter: 
            frame: AppFrame
        Return: 无
        Others: 
        """
        
        para = cluster_msg_def.RmvClusterNodeRequest.deserialize(frame.get_data())

        if para is None:
            tracelog.error("invalid request! frame:%s" %(frame))
            return

        
        rep = cluster_msg_def.RmvClusterNodeResponse()        
        cur_cluster = self.get_worker().get_cur_cluster()
        if cur_cluster is None:
            rep.return_code = err_code_mgr.ER_CLUSTER_IS_DISABLE
            rep.description = err_code_mgr.get_error_msg(err_code_mgr.ER_CLUSTER_IS_DISABLE)
        else:
            rep.return_code, rep.description = cur_cluster.rmv_node(para.ip)

        # 发送应答
        self.get_worker().send_ack(frame,rep.serialize())
        
        

class ClusterCfgWorker(bf.CmdWorker):

    def __init__(self, cluster_node):
        """
        Method: __init__
        Description: 初始化函数
        Parameter: 无
        Return: 
        Others: 
        """

        bf.CmdWorker.__init__(self, name = "ClusterCfgWorker"
                            , min_task_id = 4001
                            , max_task_id = 6000)
        

        self.__cur_cluster_node = cluster_node


      
        
    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: 注册Handler处理函数
        Parameter: 无
        Return: 
            0,成功
            非0，不成功
        Others: 
        """        
        
        
        self.register_handler(QueryClusterNodeHandler(), monitor_cmd_code.CMD_QUERY_CLUSTER_NODE )
        self.register_handler(RmvClusterNodeHandler(), monitor_cmd_code.CMD_RMV_CLUSTER_NODE)
        
        
        return 0


    def get_cur_cluster(self):
        return self.__cur_cluster_node

