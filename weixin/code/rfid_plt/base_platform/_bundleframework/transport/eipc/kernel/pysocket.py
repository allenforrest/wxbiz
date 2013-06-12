#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09
Description: EIPC �׽��ֵ�python����
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
# ����
#-----------------------------------------------------------------------------

def setsockopt_string(self, option, optval, encoding='utf-8'):
    """
    s.setsockopt_string(option, optval, encoding='utf-8')

    �����׽���ѡ��

    Parameters
    ----------
    option : int
        SUBSCRIBE, UNSUBSCRIBE, IDENTITY
    optval : unicode �ַ���
        Ҫ���õ�ֵ.
    encoding : str
        �����ʽ
    """
    if not isinstance(optval, unicode):
        raise TypeError("unicode strings only")
    return self.setsockopt(option, optval.encode(encoding))

def getsockopt_string(self, option, encoding='utf-8'):
    """
    s.getsockopt_string(option, encoding='utf-8')

    ��ȡ�׽���ѡ��

    Parameters
    ----------
    option : int
        IDENTITY

    Returns
    -------
    optval : unicode �ַ���
        ѡ���ֵ
    """
    
    if option not in constants.bytes_sockopts:
        raise TypeError("option %i will not return a string to be decoded"%option)
    return self.getsockopt(option).decode(encoding)

def bind_to_random_port(self, addr, min_port=49152, max_port=65536, max_tries=100):
    """
    s.bind_to_random_port(addr, min_port=49152, max_port=65536, max_tries=100)

    ���׽��ֵ�һ���Ķ˿ڷ�Χ

    Parameters
    ----------
    addr : str
        IP��ַ
    min_port : int, optional
        ��С�˿ڣ������˶˿�
    max_port : int, optional
        ���˿ڣ��������˶˿�
    max_tries : int, optional
        ����Դ���

    Returns
    -------
    port : int
        ���ö˿�
    
    Raises
    ------
    EIPCBindError
        ���û�л�ȡ�����ö˿�
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
# ���ͽ�����Ϣ
#-------------------------------------------------------------------------

def send_multipart(self, msg_parts, flags=0, copy=True, track=False):
    """
    s.send_multipart(msg_parts, flags=0, copy=True, track=False)

    ����buffer���б�

    Parameters
    ----------
    msg_parts : iterable
        ��Ϣ�б�
    flags : int, optional
        SNDMORE ѡ��Զ������frame
    copy : bool, optional
        copying ���ǲ�copying
    track : bool, optional
        �Ƿ������Ϣ��ɵ���Է������copy=True���������

    Returns
    -------
    None : �����copy����track
    MessageTracker : ����track����no copy        
    """
    for msg in msg_parts[:-1]:
        self.send(msg, SNDMORE|flags, copy=copy, track=track)
    # Send the last part without the extra SNDMORE flag.
    return self.send(msg_parts[-1], flags, copy=copy, track=track)

def recv_multipart(self, flags=0, copy=True, track=False):
    """
    s.recv_multipart(flags=0, copy=True, track=False)

    ���ն�֡��Ϣ

    Parameters
    ----------
    flags : int, optional
        NOBLOCKѡ��. ��� NOBLOCK���ã����������׳�EIPCError�������Ϣû��׼����        
        ��� NOBLOCK û������, ������������ֱ����Ϣ�յ�
    copy : bool, optional
        copying ���ǲ�copying
    track : bool, optional
        �Ƿ������Ϣ��ɵ���Է������copy=True���������
    Returns
    -------
    msg_parts : list
        ��Ϣ�б�    
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

    ���ͱ����ַ���    

    Parameters
    ----------
    u : Python unicode �ַ��� 
        Ҫ���͵�unicode�ַ���
    flags : int, optional
        ���п��õķ���flag
    encoding : str [default: 'utf-8']
        �����ʽ
    """
    if not isinstance(u, basestring):
        raise TypeError("unicode/str objects only")
    return self.send(u.encode(encoding), flags=flags, copy=copy)

def recv_string(self, flags=0, encoding='utf-8'):
    """
    s.recv_string(flags=0, encoding='utf-8')

    ���ձ����ַ���    
    
    Parameters
    ----------
    flags : int
        �κο��õĽ���flag
    encoding : str [default: 'utf-8']
        �����ʽ

    Returns
    -------
    s : unicode �ַ���
        ���յ����ַ���
    """
    msg = self.recv(flags=flags, copy=False)
    return codecs.decode(msg.bytes, encoding)

def send_pyobj(self, obj, flags=0, protocol=-1):
    """
    s.send_pyobj(obj, flags=0, protocol=-1)

    ����py������pickle����

    Parameters
    ----------
    obj : Python object
        Ҫ���͵Ķ���
    flags : int
        ���п��õķ���flag
    protocol : int
        pickle protocol ��ֵ
    """
    msg = pickle.dumps(obj, protocol)
    return self.send(msg, flags)

def recv_pyobj(self, flags=0):
    """
    s.recv_pyobj(flags=0)

    ����py������pickle����

    Parameters
    ----------
    flags : int
        �κο��õĽ���flag

    Returns
    -------
    obj : Python object
        ���յ���py����
    """
    s = self.recv(flags)
    return pickle.loads(s)

def send_json(self, obj, flags=0):
    """
    s.send_json(obj, flags=0)

    ����python ������json����

    Parameters
    ----------
    obj : Python object
        Ҫ���͵�python����
    flags : int
        �κο��õķ���flag
    """
    if jsonapi.jsonmod is None:
        raise ImportError('jsonlib{1,2}, json or simplejson library is required.')
    else:
        msg = jsonapi.dumps(obj)
        return self.send(msg, flags)

def recv_json(self, flags=0):
    """
    s.recv_json(flags=0)

    ����py������json����

    Parameters
    ----------
    flags : int
        �κο��õĽ����ַ���

    Returns
    -------
    obj : Python object
        ���յ���py����
    """
    if jsonapi.jsonmod is None:
        raise ImportError('jsonlib{1,2}, json or simplejson library is required.')
    else:
        msg = self.recv(flags)
        return jsonapi.loads(msg)

def poll(self, timeout=None, flags=POLLIN):
    """
    s.poll(timeout=None, flags=POLLIN)

    Poll �׽����¼�.  ȱʡ���������ָ����ʱΪmilliseconds

    Parameters
    ----------
    timeout : int
        ��ʱʱ�䣬��λmilliseconds
    flags : bitfield (int) 
        poll �¼���ʶ POLLIN��POLLOUT��ȱʡPOLLIN

    Returns
    -------
    events : bitfield (int)
        ��ȡ�����¼�
    """

    if self.closed:
        raise EIPCError(ENOTSUP)

    p = eipc.Poller()
    p.register(self, flags)
    evts = dict(p.poll(timeout))
    # û���¼�������0
    return evts.get(self, 0)
