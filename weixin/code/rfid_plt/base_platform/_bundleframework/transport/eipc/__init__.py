#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09
Description: 用Python加载链接库
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
import sys

if sys.platform.startswith('win'):
    import os, ctypes
    here = os.path.dirname(__file__)
    libeipc = os.path.join(here, 'libeipc.dll')
    if os.path.exists(libeipc):
        ctypes.cdll.LoadLibrary(libeipc)
    del here, libeipc, ctypes, os

from eipc.utils import initthreads # 初始化线程
initthreads.init_threads()

from eipc import kernel
from eipc.kernel import *

def get_includes():
    """返回要链接的目录列表""" 
    from os.path import join, dirname, abspath, pardir
    base = dirname(__file__)
    parent = abspath(join(base, pardir))
    return [ parent ] + [ join(parent, base, subdir) for subdir in ('utils',) ]


__all__ = ['get_includes'] + kernel.__all__

