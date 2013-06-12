#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09
Description: 定义各个Python版本的String类型
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""

import sys

major,mior = sys.version_info[:2]
if major >= 3:
    bytes = bytes
    unicode = str
    basestring = (bytes, unicode)
    asbytes = lambda s: s if isinstance(s, bytes) else unicode(s).encode('utf8')

elif major == 2:
    unicode = unicode
    bytes = str
    basestring = basestring
    asbytes = str

b = asbytes

__all__ = ['asbytes', 'bytes', 'unicode', 'basestring', 'b']
