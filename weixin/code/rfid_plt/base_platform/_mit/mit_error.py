#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-31
Description: ���ļ��ж�����mit��ʹ�õĴ�������Ϣ
Others:      
Key Class&Method List: 
History: 
1. Date:
   Author:
   Modification:
"""


# mit�����뷶Χ: [2001, 3000]


error_defs = {
    "ER_MIT_UNKNOWN_ERROR"      :(1501, "mit�з���δ֪����", "mit unknown error")
  , "ER_OBJECT_ADD_CONFLICT"  : (1502, "����%(moid)s�Ѿ�����", "The Object %(moid)s already exists")
  , "ER_OBJECT_NOT_EXIST"      :(1503, "����%(moid)s������", "The Object %(moid)s does not exists")
  , "ER_OPEN_DB_FAILED"         :(1504, "�����ݿ�ʧ��", "Open DB failed")
  , "ER_MIT_TRANSACTION_ALREADY_EXISTS" : (1505, "mit�����Ѿ����ڣ������ٿ�ʼ������", "Can not start new transaction when the mit is already in transaction")
  , "ER_OBJECT_IS_READ_ONLY" : (1506, "mit�ж�����ֻ����", "The MOC %(mocname)s is read-only in mit.")

  }





