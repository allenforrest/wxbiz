#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 
Others:      
Key Class&Method List: 
             1. 本文件中定义了cluster模块用到的常量
History: 
1. Date:
   Author:
   Modification:
"""


CLUSTER_ROLE_UNKNOWN = 0
CLUSTER_ROLE_MASTER = 1
CLUSTER_ROLE_SLAVE = 2

CLUSTER_STATE_NORMAL = 0        # 当前有主、从的正常状态
CLUSTER_STATE_STARTING = 1      # 当前节点处于启动状态
CLUSTER_STATE_NO_MASTER = 2     # 集群处于无master状态
CLUSTER_STATE_ONLY_MASTER = 3   # 当前只有master

CLUSTER_LISTEN_PORT = 7004

# master监控slave的超时时间 > slave监控master的超时时间
# 为了防止极端情况下，master认为slave已经离线，slave却认为master在线的情况下，
# slave的名字被注销，但是slave自己却不知道（不会重新注册名字服务）
CLUSTER_SLAVE_MAX_HAERTBEAT = 10 # 10*2 = 20秒
CLUSTER_MASTER_MAX_HAERTBEAT = 7 # 7*2 ≈ 15秒

CLUSTER_JUDGE_STATE_HAERTBEAT = 5  # 5*2 = 10秒


CLUSTER_NODE_STATE_NOCHANGE = 0
CLUSTER_NODE_STATE_CHANGE_ONLINE = 1
CLUSTER_NODE_STATE_CHANGE_OFFLINE = 2
