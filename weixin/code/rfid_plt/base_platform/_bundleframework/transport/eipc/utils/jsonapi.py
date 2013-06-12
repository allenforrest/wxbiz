#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09
Description: 基于优先级的json library导入
             使用jsonapi.loads()和jsonapi.dumps()保证对齐
             优先级: simplejson > jsonlib2 > json
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""

from eipc.utils.strtypes import bytes, unicode

jsonmod = None

priority = ['simplejson', 'jsonlib2', 'json']
for mod in priority:
    try:
        jsonmod = __import__(mod)
    except ImportError:
        pass
    else:
        break

def _squash_unicode(s):
    if isinstance(s, unicode):
        return s.encode('utf8')
    else:
        return s

def dumps(o, **kwargs):
    """
    序列化对象为JSON bytes
    """
    
    if 'separators' not in kwargs:
        kwargs['separators'] = (',', ':')
    
    return _squash_unicode(jsonmod.dumps(o, **kwargs))

def loads(s, **kwargs):
    """
    从JSON导入对象
    """
    
    if str is unicode and isinstance(s, bytes):
        s = s.decode('utf8')
    return jsonmod.loads(s, **kwargs)

__all__ = ['jsonmod', 'dumps', 'loads']

