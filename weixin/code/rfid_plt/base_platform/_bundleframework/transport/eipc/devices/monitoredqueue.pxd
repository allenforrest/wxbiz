"""MonitoredQueue class declarations."""


#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from libeipc cimport *

#-----------------------------------------------------------------------------
# MonitoredQueue C functions
#-----------------------------------------------------------------------------

cdef inline int _relay(void *insocket_, void *outsocket_, void *sidesocket_, 
                eipc_msg_t msg, eipc_msg_t side_msg, eipc_msg_t id_msg,
                bint swap_ids) nogil:
    cdef int rc
    cdef int64_t flag_2
    cdef int flag_3
    cdef int flags
    cdef bint more
    cdef size_t flagsz
    cdef void * flag_ptr
    
    if EIPC_VERSION_MAJOR < 3:
        flagsz = sizeof (int64_t)
        flag_ptr = &flag_2
    else:
        flagsz = sizeof (int)
        flag_ptr = &flag_3
    
    if swap_ids:# both router, must send second identity first
        # recv two ids into msg, id_msg
        rc = eipc_recvmsg (insocket_, &msg, 0)
        rc = eipc_recvmsg (insocket_, &id_msg, 0)

        # send second id (id_msg) first
        #!!!! always send a copy before the original !!!!
        rc = eipc_msg_copy(&side_msg, &id_msg)
        rc = eipc_sendmsg (outsocket_, &side_msg, EIPC_SNDMORE)
        rc = eipc_sendmsg (sidesocket_, &id_msg, EIPC_SNDMORE)
        # send first id (msg) second
        rc = eipc_msg_copy(&side_msg, &msg)
        rc = eipc_sendmsg (outsocket_, &side_msg, EIPC_SNDMORE)
        rc = eipc_sendmsg (sidesocket_, &msg, EIPC_SNDMORE)
        if rc < 0:
            return rc
    while (True):
        rc = eipc_recvmsg (insocket_, &msg, 0)
        # assert (rc == 0)
        rc = eipc_getsockopt (insocket_, EIPC_RCVMORE, flag_ptr, &flagsz)
        flags = 0
        if EIPC_VERSION_MAJOR < 3:
            if flag_2:
                flags |= EIPC_SNDMORE
        else:
            if flag_3:
                flags |= EIPC_SNDMORE
            # LABEL has been removed:
            # rc = eipc_getsockopt (insocket_, EIPC_RCVLABEL, flag_ptr, &flagsz)
            # if flag_3:
            #     flags |= EIPC_SNDLABEL
        # assert (rc == 0)

        rc = eipc_msg_copy(&side_msg, &msg)
        if flags:
            rc = eipc_sendmsg (outsocket_, &side_msg, flags)
            # only SNDMORE for side-socket
            rc = eipc_sendmsg (sidesocket_, &msg, EIPC_SNDMORE)
        else:
            rc = eipc_sendmsg (outsocket_, &side_msg, 0)
            rc = eipc_sendmsg (sidesocket_, &msg, 0)
            break
    return rc

# the MonitoredQueue C function, adapted from eipc::queue.cpp :
cdef inline int c_monitored_queue (void *insocket_, void *outsocket_,
                        void *sidesocket_, eipc_msg_t *in_msg_ptr, 
                        eipc_msg_t *out_msg_ptr, int swap_ids) nogil:
    """The actual C function for a monitored queue device. 

    See ``monitored_queue()`` for details.
    """
    
    cdef eipc_msg_t msg
    cdef int rc = eipc_msg_init (&msg)
    cdef eipc_msg_t id_msg
    rc = eipc_msg_init (&id_msg)
    cdef eipc_msg_t side_msg
    rc = eipc_msg_init (&side_msg)
    # assert (rc == 0)
    
    
    cdef eipc_pollitem_t items [2]
    items [0].socket = insocket_
    items [0].fd = 0
    items [0].events = EIPC_POLLIN
    items [0].revents = 0
    items [1].socket = outsocket_
    items [1].fd = 0
    items [1].events = EIPC_POLLIN
    items [1].revents = 0
    # I don't think sidesocket should be polled?
    # items [2].socket = sidesocket_
    # items [2].fd = 0
    # items [2].events = EIPC_POLLIN
    # items [2].revents = 0
    
    while (True):
    
        # //  Wait while there are either requests or replies to process.
        rc = eipc_poll (&items [0], 2, -1)
        if rc < 0:
            return rc
        # //  The algorithm below asumes ratio of request and replies processed
        # //  under full load to be 1:1. Although processing requests replies
        # //  first is tempting it is suspectible to DoS attacks (overloading
        # //  the system with unsolicited replies).
        # 
        # //  Process a request.
        if (items [0].revents & EIPC_POLLIN):
            # send in_prefix to side socket
            rc = eipc_msg_copy(&side_msg, in_msg_ptr)
            rc = eipc_sendmsg (sidesocket_, &side_msg, EIPC_SNDMORE)
            if rc < 0:
                return rc
            # relay the rest of the message
            rc = _relay(insocket_, outsocket_, sidesocket_, msg, side_msg, id_msg, swap_ids)
            if rc < 0:
                return rc
        if (items [1].revents & EIPC_POLLIN):
            # send out_prefix to side socket
            rc = eipc_msg_copy(&side_msg, out_msg_ptr)
            rc = eipc_sendmsg (sidesocket_, &side_msg, EIPC_SNDMORE)
            if rc < 0:
                return rc
            # relay the rest of the message
            rc = _relay(outsocket_, insocket_, sidesocket_, msg, side_msg, id_msg, swap_ids)
            if rc < 0:
                return rc
    return 0
