#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-31
Description: 本文件中定义了mit中使用的错误码信息
Others:      
Key Class&Method List: 
History: 
1. Date:
   Author:
   Modification:
"""


# mit错误码范围: [2001, 3000]


error_defs = {
    "ER_MIT_UNKNOWN_ERROR"      :(1501, "mit中发生未知错误", "mit unknown error")
  , "ER_OBJECT_ADD_CONFLICT"  : (1502, "对象%(moid)s已经存在", "The Object %(moid)s already exists")
  , "ER_OBJECT_NOT_EXIST"      :(1503, "对象%(moid)s不存在", "The Object %(moid)s does not exists")
  , "ER_OPEN_DB_FAILED"         :(1504, "打开数据库失败", "Open DB failed")
  , "ER_MIT_TRANSACTION_ALREADY_EXISTS" : (1505, "mit事务已经存在，不能再开始新事务", "Can not start new transaction when the mit is already in transaction")
  , "ER_OBJECT_IS_READ_ONLY" : (1506, "mit中对象是只读的", "The MOC %(mocname)s is read-only in mit.")

  }





