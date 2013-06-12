#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09
Description: EIPC Context class declaration
Others:      
Key Class&Method List: 

History: 
1. Date:
   Author:
   Modification:
"""

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------

cdef class Context:
    """
    管理EIPC Context的生命周期.
    """

    cdef void *handle
    cdef void ** _sockets
    cdef size_t n_sockets
    cdef size_t max_sockets
    cdef public object closed
   
    cdef inline void _add_socket(self, void* handle)
    cdef inline void _remove_socket(self, void* handle)
    
    cdef public dict sockopts
    cdef dict _attrs

