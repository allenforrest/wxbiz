#coding=gbk
"""
���ļ����ڴ������ļ��м������ݿ��������Ϣ
"""

#todo...������װ��ʱ��һ���ع�

#import oradb

_configure = {}

# Ĭ�ϵ�oracle������������Ϣ
ORACLE_DEFAULT_CON_NAME = "default oracle"

# Ĭ�ϵ�oracle������������Ϣ
ORACLE_SYNC_CON_NAME = "oracle sync"

def load_configure():
    # TODO... �������ļ��ж�ȡ��Ϣ�����������н��ܣ�
    pass

def get_configure(cfg_name):
    if cfg_name == ORACLE_DEFAULT_CON_NAME:
        # TODO... ���Ѿ���ȡ��������Ϣ�в���  
        # ��ʱ���ֹ��̶�      
        return dict(host="localhost", port = 1521, username="user_acp", password="user_acp", db="orcl", sysdba=False)
        
    if cfg_name == ORACLE_SYNC_CON_NAME:
        # TODO... ���Ѿ���ȡ��������Ϣ�в���  
        # ��ʱ���ֹ��̶�      
        return dict(host="localhost", port = 1521, username="user_sync", password="user_sync", db="orcl", sysdba=False)
    
    
    return None