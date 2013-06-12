#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09
Description: EIPC polling ��غ�������
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

import eipc
from eipc.kernel._poll import _poll
from eipc.kernel.constants import POLLIN, POLLOUT, POLLERR

#-----------------------------------------------------------------------------
# Polling ��غ���
#-----------------------------------------------------------------------------


class Poller(object):
    """
    Poller()

    һ����״̬��poll�ӿ�
    """

    def __init__(self):
        self.sockets = {}

    def register(self, socket, flags=POLLIN|POLLOUT):
        """
        p.register(socket, flags=POLLIN|POLLOUT)

        ע�� a EIPC �׽��ֻ���ԭʼ�׽��� 
        
        register(s,0) ���� unregister(s).

        Parameters
        ----------
        socket : eipc�׽��ֻ���ԭʼ�׽���            
        flags : int
            POLLIN, POLLOUT ���� POLLIN|POLLOUT.
            ���=0������unregister
        """
        if flags:
            self.sockets[socket] = flags
        elif socket in self.sockets:
            # uregister �׽��� 
            self.unregister(socket)
        else:
            # ����
            pass

    def modify(self, socket, flags=POLLIN|POLLOUT):
        """
        p.modify(socket, flags=POLLIN|POLLOUT)

        �޸�flag
        """
        self.register(socket, flags)

    def unregister(self, socket):
        """
        p.unregister(socket)

        ע��

        Parameters
        ----------
        socket : eipc�׽��ֻ���ԭʼ�׽���             
        """
        del self.sockets[socket]

    def poll(self, timeout=None):
        """
        poll(timeout=None)

        Poll �׽���

        Parameters
        ----------
        timeout : float, int
            ��λmilliseconds�����ΪNone��û�г�ʱ            
        """
        if timeout is None:
            timeout = -1
        
        timeout = int(timeout)
        if timeout < 0:
            timeout = -1
        return _poll(list(self.sockets.items()), timeout=timeout)


def select(rlist, wlist, xlist, timeout=None):
    """
    select(rlist, wlist, xlist, timeout=None) -> (rlist, wlist, xlist)

    ���� �ɶ�����д���쳣���׽����б�    

    Parameters
    ----------
    timeout : float, int, optional
       ��λseconds�����ΪNone��û�г�ʱ            
    rlist : ���׽����б�        
    wlist : д�׽����б�
    xlist : �쳣�׽����б�
    
    Returns
    -------
    (rlist, wlist, xlist) : �ɶ�����д���쳣���׽����б� 
    """
    if timeout is None:
        timeout = -1
    # ʱ�䵥λת��
    timeout = int(timeout*1000.0)
    if timeout < 0:
        timeout = -1
    sockets = []
    for s in set(rlist + wlist + xlist):
        flags = 0
        if s in rlist:
            flags |= POLLIN
        if s in wlist:
            flags |= POLLOUT
        if s in xlist:
            flags |= POLLERR
        sockets.append((s, flags))
    return_sockets = _poll(sockets, timeout)
    rlist, wlist, xlist = [], [], []
    for s, flags in return_sockets:
        if flags & POLLIN:
            rlist.append(s)
        if flags & POLLOUT:
            wlist.append(s)
        if flags & POLLERR:
            xlist.append(s)
    return rlist, wlist, xlist


__all__ = [ 'Poller', 'select' ]
