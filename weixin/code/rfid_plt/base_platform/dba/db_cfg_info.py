#coding=gbk
"""
本文件用于从配置文件中加载数据库的配置信息
"""

#todo...开发安装盘时再一起重构

#import oradb

_configure = {}

# 默认的oracle连续的配置信息
ORACLE_DEFAULT_CON_NAME = "default oracle"

# 默认的oracle连续的配置信息
ORACLE_SYNC_CON_NAME = "oracle sync"

def load_configure():
    # TODO... 从配置文件中读取信息（需对密码进行解密）
    pass

def get_configure(cfg_name):
    if cfg_name == ORACLE_DEFAULT_CON_NAME:
        # TODO... 从已经读取出来的信息中查找  
        # 暂时先手工固定      
        return dict(host="localhost", port = 1521, username="user_acp", password="user_acp", db="orcl", sysdba=False)
        
    if cfg_name == ORACLE_SYNC_CON_NAME:
        # TODO... 从已经读取出来的信息中查找  
        # 暂时先手工固定      
        return dict(host="localhost", port = 1521, username="user_sync", password="user_sync", db="orcl", sysdba=False)
    
    
    return None