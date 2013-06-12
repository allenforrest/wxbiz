#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-24
Description: EIPC 套接字对象声明
Others:      
Key Class&Method List: 
History: 
1. Date:
   Author:
   Modification:
"""


#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from context cimport Context

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------


cdef class Socket:
    """EIPC socket类"""

    cdef void *handle           # 底层eipc对象的C处理函数.
    cdef public int socket_type # EIPC socket类型-REQ,REP等
    # 保持对上下文的一个引用，指导socket处理完后再垃圾回收
    cdef public Context context # eipc上下文对象
    cdef public bint _closed   # 关闭了的socket的bool类型
    cdef dict _attrs   # 参数字典，用于子类中一些非sockopt的get/setattr方法
    
    # 用于直接cython访问的cpdef方法
    cpdef object send(self, object data, int flags=*, copy=*, track=*)
    cpdef object recv(self, int flags=*, copy=*, track=*)

