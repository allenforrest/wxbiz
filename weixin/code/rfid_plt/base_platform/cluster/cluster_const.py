#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 
Others:      
Key Class&Method List: 
             1. ���ļ��ж�����clusterģ���õ��ĳ���
History: 
1. Date:
   Author:
   Modification:
"""


CLUSTER_ROLE_UNKNOWN = 0
CLUSTER_ROLE_MASTER = 1
CLUSTER_ROLE_SLAVE = 2

CLUSTER_STATE_NORMAL = 0        # ��ǰ�������ӵ�����״̬
CLUSTER_STATE_STARTING = 1      # ��ǰ�ڵ㴦������״̬
CLUSTER_STATE_NO_MASTER = 2     # ��Ⱥ������master״̬
CLUSTER_STATE_ONLY_MASTER = 3   # ��ǰֻ��master

CLUSTER_LISTEN_PORT = 7004

# master���slave�ĳ�ʱʱ�� > slave���master�ĳ�ʱʱ��
# Ϊ�˷�ֹ��������£�master��Ϊslave�Ѿ����ߣ�slaveȴ��Ϊmaster���ߵ�����£�
# slave�����ֱ�ע��������slave�Լ�ȴ��֪������������ע�����ַ���
CLUSTER_SLAVE_MAX_HAERTBEAT = 10 # 10*2 = 20��
CLUSTER_MASTER_MAX_HAERTBEAT = 7 # 7*2 �� 15��

CLUSTER_JUDGE_STATE_HAERTBEAT = 5  # 5*2 = 10��


CLUSTER_NODE_STATE_NOCHANGE = 0
CLUSTER_NODE_STATE_CHANGE_ONLINE = 1
CLUSTER_NODE_STATE_CHANGE_OFFLINE = 2
