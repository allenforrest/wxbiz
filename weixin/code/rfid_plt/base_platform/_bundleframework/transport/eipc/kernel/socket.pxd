#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-24
Description: EIPC �׽��ֶ�������
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
    """EIPC socket��"""

    cdef void *handle           # �ײ�eipc�����C������.
    cdef public int socket_type # EIPC socket����-REQ,REP��
    # ���ֶ������ĵ�һ�����ã�ָ��socket�����������������
    cdef public Context context # eipc�����Ķ���
    cdef public bint _closed   # �ر��˵�socket��bool����
    cdef dict _attrs   # �����ֵ䣬����������һЩ��sockopt��get/setattr����
    
    # ����ֱ��cython���ʵ�cpdef����
    cpdef object send(self, object data, int flags=*, copy=*, track=*)
    cpdef object recv(self, int flags=*, copy=*, track=*)

