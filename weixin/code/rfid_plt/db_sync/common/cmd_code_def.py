#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��ж���������ͬ������ʹ�õ���������
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


#3701~3800 ����ͬ��ʹ��

DB_SYNC_BASE = 3700

########################################################################
#DB SYNC COMMAND CODE
########################################################################
"""
CMD_SYNC_DATA
��������ͬ��֪ͨ��Ϣ
"""
CMD_SYNC_DATA = DB_SYNC_BASE + 1

# ȫͬ��֪ͨ
CMD_NOTIFY_SYNC_FULL = DB_SYNC_BASE + 2


# ���ܷ�����Ԫ���������ϴ�ȫ������
CMD_SYNC_NE_EXP_FULL = DB_SYNC_BASE + 3

CMD_START_EXP_FULL = DB_SYNC_BASE + 4
CMD_START_IMP_FULL = DB_SYNC_BASE + 5

# imc_device_mgr��������EAU��������Ϣ
CMD_NTF_NE_ID_PID = DB_SYNC_BASE + 6

# ��imc_device_mgr���Ͳ�ѯ����
CMD_QUERY_NE_ID_PID = 0x02001009


