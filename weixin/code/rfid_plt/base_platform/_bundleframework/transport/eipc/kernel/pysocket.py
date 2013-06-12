#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09
Description: EIPC 套接字的python方法
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""

#-----------------------------------------------------------------------------
# Python Imports
#-----------------------------------------------------------------------------

import random
import codecs

import eipc
from eipc.kernel import constants
from eipc.kernel.constants import *
from eipc.kernel.error import EIPCError, EIPCBindError
from eipc.utils import jsonapi
from eipc.utils.strtypes import bytes,unicode,basestring

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

#-----------------------------------------------------------------------------
# 编码
#-----------------------------------------------------------------------------

def setsockopt_string(self, option, optval, encoding='utf-8'):
    """
    s.setsockopt_string(option, optval, encoding='utf-8')

    设置套接字选项

    Parameters
    ----------
    option : int
        SUBSCRIBE, UNSUBSCRIBE, IDENTITY
    optval : unicode 字符串
        要设置的值.
    encoding : str
        编码格式
    """
    if not isinstance(optval, unicode):
        raise TypeError("unicode strings only")
    return self.setsockopt(option, optval.encode(encoding))

def getsockopt_string(self, option, encoding='utf-8'):
    """
    s.getsockopt_string(option, encoding='utf-8')

    获取套接字选项

    Parameters
    ----------
    option : int
        IDENTITY

    Returns
    -------
    optval : unicode 字符串
        选项的值
    """
    
    if option not in constants.bytes_sockopts:
        raise TypeError("option %i will not return a string to be decoded"%option)
    return self.getsockopt(option).decode(encoding)

def bind_to_random_port(self, addr, min_port=49152, max_port=65536, max_tries=100):
    """
    s.bind_to_random_port(addr, min_port=49152, max_port=65536, max_tries=100)

    绑定套接字到一定的端口范围

    Parameters
    ----------
    addr : str
        IP地址
    min_port : int, optional
        最小端口，包含此端口
    max_port : int, optional
        最大端口，不包含此端口
    max_tries : int, optional
        最大尝试次数

    Returns
    -------
    port : int
        可用端口
    
    Raises
    ------
    EIPCBindError
        如果没有获取到可用端口
    """
    for i in range(max_tries):
        try:
            port = random.randrange(min_port, max_port)
            self.bind('%s:%s' % (addr, port))
        except EIPCError:
            pass
        else:
            return port
    raise EIPCBindError("Could not bind socket to random port.")

#-------------------------------------------------------------------------
# 发送接收消息
#-------------------------------------------------------------------------

def send_multipart(self, msg_parts, flags=0, copy=True, track=False):
    """
    s.send_multipart(msg_parts, flags=0, copy=True, track=False)

    发送buffer的列表

    Parameters
    ----------
    msg_parts : iterable
        消息列表
    flags : int, optional
        SNDMORE 选项，自动处理多frame
    copy : bool, optional
        copying 还是不copying
    track : bool, optional
        是否跟踪消息完成到达对方，如果copy=True，则忽略它

    Returns
    -------
    None : 如果是copy或者track
    MessageTracker : 加入track并且no copy        
    """
    for msg in msg_parts[:-1]:
        self.send(msg, SNDMORE|flags, copy=copy, track=track)
    # Send the last part without the extra SNDMORE flag.
    return self.send(msg_parts[-1], flags, copy=copy, track=track)

def recv_multipart(self, flags=0, copy=True, track=False):
    """
    s.recv_multipart(flags=0, copy=True, track=False)

    接收多帧消息

    Parameters
    ----------
    flags : int, optional
        NOBLOCK选项. 如果 NOBLOCK设置，本方法会抛出EIPCError，如果消息没有准备好        
        如果 NOBLOCK 没有设置, 本方法会阻塞直到消息收到
    copy : bool, optional
        copying 还是不copying
    track : bool, optional
        是否跟踪消息完成到达对方，如果copy=True，则忽略它
    Returns
    -------
    msg_parts : list
        消息列表    
    """
    parts = [self.recv(flags, copy=copy, track=track)]
    # have first part already, only loop while more to receive
    while self.getsockopt(eipc.RCVMORE):
        part = self.recv(flags, copy=copy, track=track)
        parts.append(part)
    
    return parts

def send_string(self, u, flags=0, copy=False, encoding='utf-8'):
    """
    s.send_string(u, flags=0, copy=False, encoding='utf-8')

    发送编码字符串    

    Parameters
    ----------
    u : Python unicode 字符串 
        要发送的unicode字符串
    flags : int, optional
        所有可用的发送flag
    encoding : str [default: 'utf-8']
        编码格式
    """
    if not isinstance(u, basestring):
        raise TypeError("unicode/str objects only")
    return self.send(u.encode(encoding), flags=flags, copy=copy)

def recv_string(self, flags=0, encoding='utf-8'):
    """
    s.recv_string(flags=0, encoding='utf-8')

    接收编码字符串    
    
    Parameters
    ----------
    flags : int
        任何可用的接收flag
    encoding : str [default: 'utf-8']
        编码格式

    Returns
    -------
    s : unicode 字符串
        接收到的字符串
    """
    msg = self.recv(flags=flags, copy=False)
    return codecs.decode(msg.bytes, encoding)

def send_pyobj(self, obj, flags=0, protocol=-1):
    """
    s.send_pyobj(obj, flags=0, protocol=-1)

    发送py对象，用pickle编码

    Parameters
    ----------
    obj : Python object
        要发送的对象
    flags : int
        所有可用的发送flag
    protocol : int
        pickle protocol 数值
    """
    msg = pickle.dumps(obj, protocol)
    return self.send(msg, flags)

def recv_pyobj(self, flags=0):
    """
    s.recv_pyobj(flags=0)

    接收py对象，用pickle解码

    Parameters
    ----------
    flags : int
        任何可用的接收flag

    Returns
    -------
    obj : Python object
        接收到的py对象
    """
    s = self.recv(flags)
    return pickle.loads(s)

def send_json(self, obj, flags=0):
    """
    s.send_json(obj, flags=0)

    发送python 对象，用json编码

    Parameters
    ----------
    obj : Python object
        要发送的python对象
    flags : int
        任何可用的发送flag
    """
    if jsonapi.jsonmod is None:
        raise ImportError('jsonlib{1,2}, json or simplejson library is required.')
    else:
        msg = jsonapi.dumps(obj)
        return self.send(msg, flags)

def recv_json(self, flags=0):
    """
    s.recv_json(flags=0)

    接收py对象，用json解码

    Parameters
    ----------
    flags : int
        任何可用的接收字符串

    Returns
    -------
    obj : Python object
        接收到的py对象
    """
    if jsonapi.jsonmod is None:
        raise ImportError('jsonlib{1,2}, json or simplejson library is required.')
    else:
        msg = self.recv(flags)
        return jsonapi.loads(msg)

def poll(self, timeout=None, flags=POLLIN):
    """
    s.poll(timeout=None, flags=POLLIN)

    Poll 套接字事件.  缺省阻塞，如果指定超时为milliseconds

    Parameters
    ----------
    timeout : int
        超时时间，单位milliseconds
    flags : bitfield (int) 
        poll 事件标识 POLLIN或POLLOUT，缺省POLLIN

    Returns
    -------
    events : bitfield (int)
        获取到的事件
    """

    if self.closed:
        raise EIPCError(ENOTSUP)

    p = eipc.Poller()
    p.register(self, flags)
    evts = dict(p.poll(timeout))
    # 没有事件，返回0
    return evts.get(self, 0)
