#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-30
Description: EIPC��Ϣ��ص��ඨ��
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

from libeipc cimport eipc_msg_t

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------

cdef class MessageTracker(object):
    """
    ����EIPC�Ƿ�������ĳ���������Ϣ����
    """

    cdef set events  # ���ٵ���Ϣʱ�����
    cdef set peers   # ������Ϣ����Ϣ����������
    

cdef class Frame:
    """
    ��copy���շ���Ϣ�����
    """

    cdef eipc_msg_t eipc_msg
    cdef object _data      # ��Ϊpython�����ʵ����Ϣ����
    cdef object _buffer    # ��Ϣ���ݶ�Ӧ��python Buffer/View
    cdef object _bytes     # ��Ϣ���ֽ�/�ַ�������
    cdef bint _failed_init # eipc_msg_init����ʧ�ܵı��
    cdef public object tracker_event  # ʹ��eipc_free_fn�¼�
    cdef public object tracker        # MessageTracker����.
    cdef public bint more             # RCVMORE����Ƿ�����

    cdef Frame fast_copy(self) # ������Ϣ�����ǳ����
    cdef object _getbuffer(self) # ����self._buffer.

cdef inline object copy_eipc_msg_bytes(eipc_msg_t *eipc_msg)
