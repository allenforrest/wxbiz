#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09
Description: EIPC polling 相关函数和类
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
# Polling 相关函数
#-----------------------------------------------------------------------------


class Poller(object):
    """
    Poller()

    一个有状态的poll接口
    """

    def __init__(self):
        self.sockets = {}

    def register(self, socket, flags=POLLIN|POLLOUT):
        """
        p.register(socket, flags=POLLIN|POLLOUT)

        注册 a EIPC 套接字或者原始套接字 
        
        register(s,0) 等于 unregister(s).

        Parameters
        ----------
        socket : eipc套接字或者原始套接字            
        flags : int
            POLLIN, POLLOUT 或者 POLLIN|POLLOUT.
            如果=0，就是unregister
        """
        if flags:
            self.sockets[socket] = flags
        elif socket in self.sockets:
            # uregister 套接字 
            self.unregister(socket)
        else:
            # 忽略
            pass

    def modify(self, socket, flags=POLLIN|POLLOUT):
        """
        p.modify(socket, flags=POLLIN|POLLOUT)

        修改flag
        """
        self.register(socket, flags)

    def unregister(self, socket):
        """
        p.unregister(socket)

        注销

        Parameters
        ----------
        socket : eipc套接字或者原始套接字             
        """
        del self.sockets[socket]

    def poll(self, timeout=None):
        """
        poll(timeout=None)

        Poll 套接字

        Parameters
        ----------
        timeout : float, int
            单位milliseconds。如果为None，没有超时            
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

    返回 可读，可写，异常的套接字列表    

    Parameters
    ----------
    timeout : float, int, optional
       单位seconds。如果为None，没有超时            
    rlist : 读套接字列表        
    wlist : 写套接字列表
    xlist : 异常套接字列表
    
    Returns
    -------
    (rlist, wlist, xlist) : 可读，可写，异常的套接字列表 
    """
    if timeout is None:
        timeout = -1
    # 时间单位转换
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
