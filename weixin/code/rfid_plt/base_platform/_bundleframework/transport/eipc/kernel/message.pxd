#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-30
Description: EIPC消息相关的类定义
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
    跟踪EIPC是否处理完了某条或多条消息的类
    """

    cdef set events  # 跟踪的消息时间对象
    cdef set peers   # 其他消息或消息跟踪器对象
    

cdef class Frame:
    """
    无copy的收发消息框架类
    """

    cdef eipc_msg_t eipc_msg
    cdef object _data      # 作为python对象的实际消息数据
    cdef object _buffer    # 消息内容对应的python Buffer/View
    cdef object _bytes     # 消息的字节/字符串拷贝
    cdef bint _failed_init # eipc_msg_init处理失败的标记
    cdef public object tracker_event  # 使用eipc_free_fn事件
    cdef public object tracker        # MessageTracker对象.
    cdef public bint more             # RCVMORE标记是否设置

    cdef Frame fast_copy(self) # 创建消息对象的浅复制
    cdef object _getbuffer(self) # 构造self._buffer.

cdef inline object copy_eipc_msg_bytes(eipc_msg_t *eipc_msg)
