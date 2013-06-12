/*************************************************
Copyright (C), 2012-2015, Anything Connected Possibilities
Author:   ACP team
Version:  1.0
Date:     2012/09
Description:   eipc涉及版本和平台兼容性相关宏定义
History: 
1. Date:        2012/09    
   Author:      ACP team
2. ...
*************************************************/

#if defined(_MSC_VER)
#define pyeipc_int64_t __int64
#else
#include <stdint.h>
#define pyeipc_int64_t int64_t
#endif


// 版本兼容
#include "eipc.h"

#define _missing (PyErr_SetString(PyExc_NotImplementedError, \
                "Not available in current efctipc."), -1)

#ifndef EIPC_RCVTIMEO
    #define EIPC_RCVTIMEO (-1)
#endif
#ifndef EIPC_SNDTIMEO
    #define EIPC_SNDTIMEO (-1)
#endif

#ifndef EAFNOSUPPORT
    #define EAFNOSUPPORT (-1)
#endif
#ifndef EHOSTUNREACH
    #define EHOSTUNREACH (-1)
#endif

#ifndef EIPC_MAXMSGSIZE
    #define EIPC_MAXMSGSIZE (-1)
#endif
#ifndef EIPC_SNDHWM
    #define EIPC_SNDHWM (-1)
#endif
#ifndef EIPC_RCVHWM
    #define EIPC_RCVHWM (-1)
#endif
#ifndef EIPC_MULTICAST_HOPS
    #define EIPC_MULTICAST_HOPS (-1)
#endif
#ifndef EIPC_DONTWAIT
    #define EIPC_DONTWAIT (-1)
#endif
#ifndef EIPC_RCVLABEL
    #define EIPC_RCVLABEL (-1)
#endif
#ifndef EIPC_SNDLABEL
    #define EIPC_SNDLABEL (-1)
#endif
#ifndef EIPC_IPV4ONLY
    #define EIPC_IPV4ONLY (-1)
#endif
#ifndef EIPC_LAST_ENDPOINT
    #define EIPC_LAST_ENDPOINT (-1)
#endif
#ifndef EIPC_FAIL_UNROUTABLE
    #define EIPC_FAIL_UNROUTABLE (-1)
#endif


#ifndef EIPC_MAX_VSM_SIZE
    #define EIPC_MAX_VSM_SIZE (-1)
#endif
#ifndef EIPC_DELIMITER
    #define EIPC_DELIMITER (-1)
#endif
#ifndef EIPC_MSG_MORE
    #define EIPC_MSG_MORE (-1)
#endif
#ifndef EIPC_MSG_SHARED
    #define EIPC_MSG_SHARED (-1)
#endif

#ifndef EIPC_UPSTREAM
    #define EIPC_UPSTREAM (-1)
#endif
#ifndef EIPC_DOWNSTREAM
    #define EIPC_DOWNSTREAM (-1)
#endif

#ifndef EIPC_HWM
    #define EIPC_HWM (-1)
#endif
#ifndef EIPC_SWAP
    #define EIPC_SWAP (-1)
#endif
#ifndef EIPC_MCAST_LOOP
    #define EIPC_MCAST_LOOP (-1)
#endif
#ifndef EIPC_RECOVERY_IVL_MSEC
    #define EIPC_RECOVERY_IVL_MSEC (-1)
#endif

#ifndef EIPC_NOBLOCK
    #define EIPC_NOBLOCK (-1)
#endif


#ifndef EIPC_STREAMER
    #define EIPC_STREAMER 1
#endif
#ifndef EIPC_FORWARDER
    #define EIPC_FORWARDER 2
#endif
#ifndef EIPC_QUEUE
    #define EIPC_QUEUE 3
#endif


#ifndef ECANTROUTE
    #define ECANTROUTE (-1)
#endif

#ifndef EIPC_RCVCMD
    #define EIPC_RCVCMD (-1)
#endif
#ifndef EIPC_SNDCMD
    #define EIPC_SNDCMD (-1)
#endif

#ifndef EIPC_XREQ
    #define EIPC_XREQ (-1)
#endif
#ifndef EIPC_XREP
    #define EIPC_XREP (-1)
#endif
#ifndef EIPC_DEALER
    #define EIPC_DEALER (-1)
#endif

#ifndef EIPC_IDENTITY
    #define EIPC_IDENTITY (-1)
#endif

// 定义 套接字类型 
#ifdef _WIN32
  #ifdef _MSC_VER && _MSC_VER <= 1400
    #define EIPC_FD_T UINT_PTR
  #else
    #define EIPC_FD_T SOCKET
  #endif
#else
    #define EIPC_FD_T int
#endif

#if EIPC_VERSION_MAJOR >= 3
    #define eipc_sendbuf eipc_send
    #define eipc_recvbuf eipc_recv
    #define eipc_device(type,in,out) _missing
#else
    #define eipc_sendmsg eipc_send
    #define eipc_recvmsg eipc_recv
    #define eipc_sendbuf (void *s, const void *buf, size_t len, int flags) _missing
    #define eipc_recvbuf (void *s, void *buf, size_t len, int flags) _missing
#endif
