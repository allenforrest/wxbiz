#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: db sync�����붨���ļ�
Others:      
Key Class&Method List: 
    1. ....
History: 
1. Date:2013-03-23
   Author:ACP2013
   Modification:�½��ļ�
"""

import err_code_mgr

#OSS ������
DB_SYNC_ERROR_BASE = 3700

db_sync_error_defs = {"ER_SYNC_FAILED" : (DB_SYNC_ERROR_BASE + 1
                                        , "ִ������ͬ���쳣�� �쳣��Ϣ : %(err)s"
                                        , "execute db sync exception. Exception information: %(err)s")
                    , "ER_SYNC_HOST_NOT_FOUND" : (DB_SYNC_ERROR_BASE + 2
                                        , "ͬ���������Ҳ���"
                                        , "sync host was not found.")
                    , "ER_SYNC_TABLE_NOT_FOUND" : (DB_SYNC_ERROR_BASE + 3
                                        , "ͬ�����ݱ���"
                                        , "sync table was not found.")

                    , "ER_SYNC_NO_TABLE_NEED_SYNC" : (DB_SYNC_ERROR_BASE + 4
                                        , "��������Ҫͬ�������ݱ�"
                                        , "There is no table need to sync")     
                                        
                    , "ER_SYNC_EXPORT_DATA_FAILED" : (DB_SYNC_ERROR_BASE + 5
                                        , "��������ʧ��"
                                        , "Export data failed")   
                                        
                    , "ER_SYNC_UPLOAD_DATA_FAILED" : (DB_SYNC_ERROR_BASE + 6
                                        , "��������ʧ��"
                                        , "Upload data failed")  
                    }
err_code_mgr.regist_errors(db_sync_error_defs)
