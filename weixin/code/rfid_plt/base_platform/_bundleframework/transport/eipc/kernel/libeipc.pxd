#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-30
Description: EIPC所有的C引用
Others:      
Key Class&Method List: 
History: 
1. Date:
   Author:
   Modification:
"""

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# C头文件引用
#-----------------------------------------------------------------------------

cdef extern from *:
    ctypedef void* const_void_ptr "const void *"

cdef extern from "allocate.h":
    object allocate(size_t n, void **pp)

cdef extern from "errno.h" nogil:
    enum: EIPC_EINVAL "EINVAL"
    enum: EIPC_EAGAIN "EAGAIN"
    enum: EIPC_EFAULT "EFAULT"
    enum: EIPC_ENOMEM "ENOMEM"
    enum: EIPC_ENODEV "ENODEV"

cdef extern from "string.h" nogil:
    void *memcpy(void *dest, void *src, size_t n)
    size_t strlen(char *s)

cdef extern from "eipc_compat.h":
    ctypedef signed long long int64_t "pyeipc_int64_t"

cdef extern from "eipc.h" nogil:

    void _eipc_version "eipc_version"(int *major, int *minor, int *patch)
    
    ctypedef int fd_t "EIPC_FD_T"
    
    enum: EIPC_VERSION_MAJOR
    enum: EIPC_VERSION_MINOR
    enum: EIPC_VERSION_PATCH
    enum: EIPC_VERSION

    enum: EIPC_HAUSNUMERO
    enum: EIPC_ENOTSUP "ENOTSUP"
    enum: EIPC_EPROTONOSUPPORT "EPROTONOSUPPORT"
    enum: EIPC_ENOBUFS "ENOBUFS"
    enum: EIPC_ENETDOWN "ENETDOWN"
    enum: EIPC_EADDRINUSE "EADDRINUSE"
    enum: EIPC_EADDRNOTAVAIL "EADDRNOTAVAIL"
    enum: EIPC_ECONNREFUSED "ECONNREFUSED"
    enum: EIPC_EINPROGRESS "EINPROGRESS"
    enum: EIPC_ENOTSOCK "ENOTSOCK"
    enum: EIPC_EAFNOSUPPORT "EAFNOSUPPORT"
    enum: EIPC_EHOSTUNREACH "EHOSTUNREACH"

    enum: EIPC_EFSM "EFSM"
    enum: EIPC_ENOCOMPATPROTO "ENOCOMPATPROTO"
    enum: EIPC_ETERM "ETERM"
    enum: EIPC_ECANTROUTE "ECANTROUTE"
    enum: EIPC_EMTHREAD "EMTHREAD"
    
    enum: errno
    char *eipc_strerror (int errnum)
    int eipc_errno()

    enum: EIPC_MAX_VSM_SIZE # 30
    enum: EIPC_DELIMITER # 31
    enum: EIPC_VSM # 32
    enum: EIPC_MSG_MORE # 1
    enum: EIPC_MSG_SHARED # 128
    
    # eipc_msg_t的黑盒定义
    ctypedef void * eipc_msg_t "eipc_msg_t"
    
    ctypedef void eipc_free_fn(void *data, void *hint)
    
    int eipc_msg_init (eipc_msg_t *msg)
    int eipc_msg_init_size (eipc_msg_t *msg, size_t size)
    int eipc_msg_init_data (eipc_msg_t *msg, void *data,
        size_t size, eipc_free_fn *ffn, void *hint)
    int eipc_msg_close (eipc_msg_t *msg)
    int eipc_msg_move (eipc_msg_t *dest, eipc_msg_t *src)
    int eipc_msg_copy (eipc_msg_t *dest, eipc_msg_t *src)
    void *eipc_msg_data (eipc_msg_t *msg)
    size_t eipc_msg_size (eipc_msg_t *msg)

    void *eipc_init (int io_threads)
    int eipc_term (void *context)

    enum: EIPC_PAIR # 0
    enum: EIPC_PUB # 1
    enum: EIPC_SUB # 2
    enum: EIPC_REQ # 3
    enum: EIPC_REP # 4
    enum: EIPC_XREQ # 5
    enum: EIPC_DEALER # 5 or 12
    enum: EIPC_XREP # 6
    enum: EIPC_ROUTER # 6 or 11 or 13
    enum: EIPC_PULL # 7
    enum: EIPC_PUSH # 8
    enum: EIPC_XPUB # 9
    enum: EIPC_XSUB # 10
    enum: EIPC_UPSTREAM # 7
    enum: EIPC_DOWNSTREAM # 8

    enum: EIPC_HWM # 1
    enum: EIPC_SWAP # 3
    enum: EIPC_AFFINITY # 4
    enum: EIPC_IDENTITY # 5
    enum: EIPC_SUBSCRIBE # 6
    enum: EIPC_UNSUBSCRIBE # 7
    enum: EIPC_RATE # 8
    enum: EIPC_RECOVERY_IVL # 9
    enum: EIPC_MCAST_LOOP # 10
    enum: EIPC_SNDBUF # 11
    enum: EIPC_RCVBUF # 12
    enum: EIPC_RCVMORE # 13
    enum: EIPC_FD # 14
    enum: EIPC_EVENTS # 15
    enum: EIPC_TYPE # 16
    enum: EIPC_LINGER # 17
    enum: EIPC_RECONNECT_IVL # 18
    enum: EIPC_BACKLOG # 19
    enum: EIPC_RECOVERY_IVL_MSEC # 20
    enum: EIPC_RECONNECT_IVL_MAX # 21
    enum: EIPC_MAXMSGSIZE # 22
    enum: EIPC_SNDHWM # 23
    enum: EIPC_RCVHWM # 24
    enum: EIPC_MULTICAST_HOPS # 25
    enum: EIPC_RCVTIMEO # 27
    enum: EIPC_SNDTIMEO # 28
    enum: EIPC_RCVLABEL # 29
    enum: EIPC_RCVCMD # 30
    enum: EIPC_IPV4ONLY # 31
    enum: EIPC_LAST_ENDPOINT # 32
    enum: EIPC_FAIL_UNROUTABLE # 33

    enum: EIPC_NOBLOCK # 1
    enum: EIPC_DONTWAIT # 1
    enum: EIPC_SNDMORE # 2
    enum: EIPC_SNDLABEL # 4
    enum: EIPC_SNDCMD # 8

    void *eipc_socket (void *context, int type)
    int eipc_close (void *s)
    int eipc_setsockopt (void *s, int option, void *optval, size_t optvallen)
    int eipc_getsockopt (void *s, int option, void *optval, size_t *optvallen)
    int eipc_bind (void *s, char *addr)
    int eipc_connect (void *s, char *addr)
    # send/recv
    int eipc_sendmsg (void *s, eipc_msg_t *msg, int flags)
    int eipc_recvmsg (void *s, eipc_msg_t *msg, int flags)
    int eipc_sendbuf (void *s, const_void_ptr buf, size_t n, int flags)
    int eipc_recvbuf (void *s, void *buf, size_t n, int flags)

    enum: EIPC_POLLIN # 1
    enum: EIPC_POLLOUT # 2
    enum: EIPC_POLLERR # 4

    ctypedef struct eipc_pollitem_t:
        void *socket
        int fd
        # #if defined _WIN32
        #     SOCKET fd;
        short events
        short revents

    int eipc_poll (eipc_pollitem_t *items, int nitems, long timeout)

    enum: EIPC_STREAMER
    enum: EIPC_FORWARDER
    enum: EIPC_QUEUE
    # libeipc中删除
    int eipc_device (int device_, void *insocket_, void *outsocket_)

cdef extern from "eipc_utils.h" nogil:

    void *eipc_stopwatch_start ()
    unsigned long eipc_stopwatch_stop (void *watch_)
    void eipc_sleep (int seconds_)

