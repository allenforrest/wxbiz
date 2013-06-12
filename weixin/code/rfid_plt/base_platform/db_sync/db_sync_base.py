#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��ж���������ͬ��������Ҫ�õ���һЩ���ݽṹ
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""

import serializable_obj
import type_def

class DBSyncStatus():
    """
    Class: DBSyncStatus
    Description: ͬ��״̬
    Others:
    """
    ERROR_SUCCESS           = 0
    ERROR_NETWORK           = 1
    ERROR_CONFLICT          = 2
    ERROR_FAILED            = 3

class DBSyncType:
    """
    Class: DBSyncType
    Description: ͬ������
    Others:
    """
    FULL = 0
    INCREMENTAL = 1
    
class DBSyncOperationType:
    """
    Class: DBSyncOperationType
    Description: ͬ����������
    Others:
    """
    INSERT = 0
    UPDATE = 1
    DELETE = 2

class DBSyncResult(serializable_obj.BsonSerializableObj):
    """
    Class: DBSyncResult
    Description: ͬ�������
    Base: serializable_obj.BsonSerializableObj
    Others:
    """
    __ATTR_DEF__ = {
         'id': type_def.TYPE_UINT32
        ,'return_code': type_def.TYPE_UINT32
        ,'error_message': type_def.TYPE_STRING
        ,'event_ids': [type_def.TYPE_UINT32]
        }
    def __init__(self):
        """
        Method: __init__
        Description: ��ʼ������
        """
        self.id = 0
        self.return_code = DBSyncStatus.ERROR_SUCCESS
        self.error_message = ''
        self.event_ids = []

class DBSyncEvent(serializable_obj.BsonSerializableObj):
    """
    Class: DBSyncEvent
    Description: ��������ͬ���¼�
    Base: serializable_obj.BsonSerializableObj
    Others:
    """
    
    __ATTR_DEF__ = {
         "id": type_def.TYPE_UINT32
        ,"type": type_def.TYPE_UINT32
        ,"priority": type_def.TYPE_UINT32
        ,"target": type_def.TYPE_STRING
        ,"operation": type_def.TYPE_UINT32
        ,"data": type_def.TYPE_STRING
        ,"condition": type_def.TYPE_STRING
        }

class DBSyncObject(serializable_obj.BsonSerializableObj):
    """
    Class: DBSyncObject
    Description: ͬ��������
    Base: serializable_obj.BsonSerializableObj
    Others:
    """
    __ATTR_DEF__ = {
         'id': type_def.TYPE_UINT32
        ,'sync_events': [DBSyncEvent]
        }

class SyncFullRequest(serializable_obj.BsonSerializableObj):
    """
    Class: SyncFullRequest
    Description: ���ܷ�����Ԫȫͬ��������
    Base: serializable_obj.BsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
          "ne_id": type_def.TYPE_INT32
        , "ftp_ip": type_def.TYPE_STRING
        , "ftp_port": type_def.TYPE_INT32
        , "file_path": type_def.TYPE_STRING
        , "ftp_user": type_def.TYPE_STRING
        , "ftp_pwd": type_def.TYPE_STRING
        }

class SyncFullResponse(serializable_obj.BsonSerializableObj):
    """
    Class: SyncFullResponse
    Description: ��Ԫ�ظ���ȫͬ�������Ӧ����Ϣ
    Base: serializable_obj.BsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
          "ne_id": type_def.TYPE_INT32
        , "return_code": type_def.TYPE_UINT32
        , "description": type_def.TYPE_STRING

        }

class NEIDAndPidNotification(serializable_obj.BsonSerializableObj):
    """
    Class: NEIDAndPidNotification
    Description: ��IMCDeviceMgr��������Ԫ��pid��id��Ϣ
    Base: serializable_obj.BsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "ne_id_pids": []
                }
                


    
    
if __name__=="__main__":
    buf = '{"id":1,"return_code":1000}'
    try:
        result = DBSyncResult.deserialize(buf)
        print(result)
    except Exception, e:
        print(e)
