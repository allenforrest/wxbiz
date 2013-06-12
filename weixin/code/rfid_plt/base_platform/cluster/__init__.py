#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


import cluster_error_code
from .cluster_node import ClusterNode, ClusterCfgInfo

from .cluster_const import (CLUSTER_ROLE_UNKNOWN
                            , CLUSTER_ROLE_MASTER
                            , CLUSTER_ROLE_SLAVE
                            , CLUSTER_STATE_NORMAL
                            , CLUSTER_STATE_STARTING
                            , CLUSTER_STATE_NO_MASTER
                            , CLUSTER_STATE_ONLY_MASTER)
                        
