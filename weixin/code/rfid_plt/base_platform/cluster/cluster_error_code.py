#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 
Others:      
Key Class&Method List: 
             1. 本文件中定义了cluster的错误码
History: 
1. Date:
   Author:
   Modification:
"""

import err_code_mgr

# cluster错误码: 3601~3700

error_defs = {

  # 集群错误码
    "ER_CLUSTER_START_FAILED":  (3601, "启动分布式集群节点失败", "Start the cluster node failed")
  , "ER_CLUSTER_LOAD_CFG_FAILED":  (3602, "加载集群配置文件失败", "Load cluster configuration failed")                                            
  , "ER_CLUSTER_IS_DISABLED":  (3603, "当前集群节点被禁用", "The current cluster node is disabled")
  , "ER_CANNOT_RMV_ONLINE_CLUSTER_NODE": (3604, "不能删除在线的集群节点", "Can not remove online cluster node")
  , "ER_CLUSTER_REACH_MAX": (3605, "当前集群的节点已经达到了最大数目", "The number of cluster nodes has reached the maximum")
             }
             
err_code_mgr.regist_errors(error_defs)

