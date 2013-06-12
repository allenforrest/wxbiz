#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 
Others:      
Key Class&Method List: 
             1. ���ļ��ж�����cluster�Ĵ�����
History: 
1. Date:
   Author:
   Modification:
"""

import err_code_mgr

# cluster������: 3601~3700

error_defs = {

  # ��Ⱥ������
    "ER_CLUSTER_START_FAILED":  (3601, "�����ֲ�ʽ��Ⱥ�ڵ�ʧ��", "Start the cluster node failed")
  , "ER_CLUSTER_LOAD_CFG_FAILED":  (3602, "���ؼ�Ⱥ�����ļ�ʧ��", "Load cluster configuration failed")                                            
  , "ER_CLUSTER_IS_DISABLED":  (3603, "��ǰ��Ⱥ�ڵ㱻����", "The current cluster node is disabled")
  , "ER_CANNOT_RMV_ONLINE_CLUSTER_NODE": (3604, "����ɾ�����ߵļ�Ⱥ�ڵ�", "Can not remove online cluster node")
  , "ER_CLUSTER_REACH_MAX": (3605, "��ǰ��Ⱥ�Ľڵ��Ѿ��ﵽ�������Ŀ", "The number of cluster nodes has reached the maximum")
             }
             
err_code_mgr.regist_errors(error_defs)

