#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-19
Description: EIPC 秒表对象
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


cdef class Stopwatch:
    """定义一个简单的秒表指针"""

    cdef void *watch 

