#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-03
Description: pyEIPC和EIPC版本号相关函数
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

from eipc.kernel._version import eipc_version_info

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------

__version__ = '2.2.0'
__revision__ = ''

def pyeipc_version():
    """
    pyeipc_version()

    以字符串方式返回pyeipc的版本号
    """
    if __revision__:
        return '@'.join([__version__,__revision__[:6]])
    else:
        return __version__

def pyeipc_version_info():
    """
    pyeipc_version_info()
    
    以元组方式返回pyeipc的版本号
    """
    import re
    parts = re.findall('[0-9]+', __version__)
    parts = [ int(p) for p in parts ]
    if 'dev' in __version__:
        parts.append(float('inf'))
    return tuple(parts)


def eipc_version():
    """
    eipc_version()

    以字符串方式返回eipc的版本号
    """
    return "%i.%i.%i" % eipc_version_info()



__all__ = ['eipc_version', 'eipc_version_info',
           'pyeipc_version','pyeipc_version_info',
           '__version__', '__revision__'
]

