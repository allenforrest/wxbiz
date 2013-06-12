#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ���ʵ���˵���oracle����Ĺ���
Others:      
Key Class&Method List: 
             1. call_expdp: ����expdp����
             2. call_impdp: ����impdp����
History: 
1. Date:
   Author:
   Modification:
"""

import subprocess 
import os.path
import time



if __name__ == "__main__":
    import sys
    sys.path.append("../../../rfid_plt/base_platform")

    
from dba import db_cfg_info
import tracelog

import db_sync_common_const

def __call_oracle_cmd(cmd_line, timeout, log_file_path):
    """
    Function: __call_oracle_cmd
    Description: ���������У��������־��Ϣ
    Parameter: 
        cmd_line: ����Popen��������
        timeout: ��ʱʱ��(��)
        log_file_path: ��־·��
    Return: ������
    Others: ����ڳ�ʱʱ��������û�н�������ô����ֹ���ӽ���
    """

    
    try:                                
        inst = subprocess.Popen(cmd_line
                                , stdin=None #subprocess.PIPE
                                #, stdout=subprocess.PIPE
                                #, stderr=subprocess.STDOUT
                                ) 
    except:
        tracelog.exception("call oracle cmd failed. cmd_line:%s" % " ".join(cmd_line))
        return -1

    while timeout > 0:
        timeout -= 1
        ret = inst.poll()
        if ret is None:  
            time.sleep(1)
            continue
        else:
            break
   
        
    if timeout <= 0:
        tracelog.error("call oracle cmd timeout. cmd_line:%s" % " ".join(cmd_line))
        # ��ʱ������£���Ҫkill������
        try:
            inst.kill()
        except:
            pass
            
        return -1

    if log_file_path is not None:
        try:
            log = file(log_file_path).read()
            tracelog.info(log)
        except:
            pass
    
    if inst.returncode != 0:
        tracelog.error("call oracle cmd failed, return %d, cmd_line:%s" % (
                              inst.returncode
                            , " ".join(cmd_line)))
        return inst.returncode
        
    return 0



def call_expdp(tables, data_dir, timeout = 60*60):
    """
    Function: call_expdp
    Description: ����expdp����
    Parameter: 
        tables: ��Ҫ�����ı�(list)
        data_dir: �������������ڵĴ���Ŀ¼
        timeout: ��ʱʱ��(��)
    Return: ������
    Others: ���ݵ�����ʹ����user_sync�û�
    """

    # expdp user_acp/user_acp@orcl directory=db_sync_dir dumpfile=ne_mocs.dmp  TABLES=user_acp.tbl_TestAntenna,user_acp.tbl_TestPhysicalReader parallel=3 job_name=dbsync  CONTENT=DATA_ONLY 

    # ����ǰ����ɾ�����ļ�
    dmp_file_path = os.path.join(data_dir
                                , db_sync_common_const.DB_SYNC_FILE_NAME)

    try:
        if os.path.exists(dmp_file_path):
            os.remove(dmp_file_path)
    except:
        tracelog.exception("remove out of date file %s failed." % dmp_file_path)
        # ���ﲻ���أ�����ִ�к���ĵ���
    
    oracle_info = db_cfg_info.get_configure("oracle sync")
    conn_string = "%s/%s@%s" % (oracle_info["username"]
                              , oracle_info["password"]
                              , oracle_info["db"])

    cmd_line = ["expdp"
                    , conn_string
                    , "DIRECTORY=db_sync_dir"
                    , "DUMPFILE=%s" % db_sync_common_const.DB_SYNC_FILE_NAME
                    , "TABLES=%s" % ",".join(tables)
                    , "PARALLEL=3"
                    , "CONTENT=DATA_ONLY"]

    
    log_file_path = os.path.join(data_dir, "export.log")        
    ret = __call_oracle_cmd(cmd_line, timeout, log_file_path)
    
    return ret

def call_impdp(tables, data_dir, timeout = 60*60):
    """
    Function: call_impdp
    Description: ����oracle��impdp����
    Parameter: 
        tables: ��Ҫ��������ݱ�(list)
        data_dir: �����ļ����ڴ��̵�·��
        timeout: ��ʱʱ��
    Return: ������
    Others: 
    """

    #impdp user_sync/user_sync@orcl directory=db_sync_dir dumpfile=ne_mocs.dmp TABLES=user_acp.tbl_TestAntenna,user_acp.tbl_TestPhysicalReader TABLE_EXISTS_ACTION=APPEND REMAP_SCHEMA=user_acp:user_sync
    
    oracle_info = db_cfg_info.get_configure("oracle sync")
    conn_string = "%s/%s@%s" % (oracle_info["username"]
                              , oracle_info["password"]
                              , oracle_info["db"])

    cmd_line = ["impdp"
                    , conn_string
                    , "DIRECTORY=db_sync_dir"
                    , "DUMPFILE=%s" % db_sync_common_const.DB_SYNC_FILE_NAME
                    , "TABLES=%s" % ",".join(tables)
                    , "TABLE_EXISTS_ACTION=APPEND"
                    #, "REMAP_SCHEMA=user_acp:user_sync"
                    , "PARALLEL=3"
                    , "CONTENT=DATA_ONLY"]

    
    log_file_path = os.path.join(data_dir, "import.log")            
    ret = __call_oracle_cmd(cmd_line, timeout, log_file_path)
    
    return ret

    
if __name__ == "__main__":
   
    call_expdp(["user_acp.tbl_TestAntenna","user_acp.tbl_TestPhysicalReader"]
                , data_dir = "/work/code_platform/code/data/oracle/db_sync") 
    
