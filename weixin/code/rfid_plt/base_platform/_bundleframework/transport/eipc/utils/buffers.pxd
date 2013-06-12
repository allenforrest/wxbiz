#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-31
Description: eipc基础模块: C/Python buffer相关方法(python版本无关)
Others:      
Key Class&Method List: 
             1. asbuffer: python对象对应的C buffer
             2. frombuffer: C buffer对应的python buffer/view
             3. viewfromobject: python对象对应的python buffer/view

History: 
1. Date:
   Author:
   Modification:
"""

#-----------------------------------------------------------------------------
# Python includes.
#-----------------------------------------------------------------------------

# 获取版本无关的别名
cdef extern from "pyversion_compat.h":
    pass

# Python 3 buffer接口
cdef extern from "Python.h":
    int PY_MAJOR_VERSION
    int PY_MINOR_VERSION
    ctypedef int Py_ssize_t
    ctypedef struct PyMemoryViewObject:
        pass
    ctypedef struct Py_buffer:
        void *buf
        Py_ssize_t len
        int readonly
        char *format
        int ndim
        Py_ssize_t *shape
        Py_ssize_t *strides
        Py_ssize_t *suboffsets
        Py_ssize_t itemsize
        void *internal
    cdef enum:
        PyBUF_SIMPLE
        PyBUF_WRITABLE
        PyBUF_FORMAT
        PyBUF_ANY_CONTIGUOUS
    int  PyObject_CheckBuffer(object)
    int  PyObject_GetBuffer(object, Py_buffer *, int) except -1
    void PyBuffer_Release(Py_buffer *)
    
    int PyBuffer_FillInfo(Py_buffer *view, object obj, void *buf,
                Py_ssize_t len, int readonly, int infoflags) except -1
    object PyMemoryView_FromBuffer(Py_buffer *info)
    
    object PyMemoryView_FromObject(object)

# Python 2 buffer接口
cdef extern from "Python.h":
    ctypedef void const_void "const void"
    Py_ssize_t Py_END_OF_BUFFER
    int PyObject_CheckReadBuffer(object)
    int PyObject_AsReadBuffer (object, const_void **, Py_ssize_t *) except -1
    int PyObject_AsWriteBuffer(object, void **, Py_ssize_t *) except -1
    
    object PyBuffer_FromMemory(void *ptr, Py_ssize_t s)
    object PyBuffer_FromReadWriteMemory(void *ptr, Py_ssize_t s)

    object PyBuffer_FromObject(object, Py_ssize_t offset, Py_ssize_t size)
    object PyBuffer_FromReadWriteObject(object, Py_ssize_t offset, Py_ssize_t size)


#-----------------------------------------------------------------------------
# asbuffer: python对象对应的C buffer
#-----------------------------------------------------------------------------


cdef inline int memoryview_available():
    return PY_MAJOR_VERSION >= 3 or (PY_MAJOR_VERSION >=2 and PY_MINOR_VERSION >= 7)

cdef inline int oldstyle_available():
    return PY_MAJOR_VERSION < 3


cdef inline int check_buffer(object ob):
    """
    检查对象是否是一个buffer(python版本无关)

    参数    
    ----------
    object : object
        任何python对象

    返回值
    -------
    int : 0: 非buffer接口, 3: 新风格的buffer接口, 3: 老风格的buffer接口
    """
    if PyObject_CheckBuffer(ob):
        return 3
    if oldstyle_available():
        return PyObject_CheckReadBuffer(ob) and 2
    return 0


cdef inline object asbuffer(object ob, int writable, int format,
                            void **base, Py_ssize_t *size,
                            Py_ssize_t *itemsize):
    """
    转换python对象到C buffer(转换方式python版本无关)
    
    参数    
    ----------
    ob : object
        准备转换为c buffer的python对象
    writable : int
        转换成的buffer是否可写(写入原对象)
    format : int
        buffer格式
    base : void **
        转换成的c buffer指针
    size : Py_ssize_t *
        buffer大小
    itemsize : Py_ssize_t *
        如果buffer不相邻，一个子项的大小
    
    返回值
    -------
    描述buffer格式的对象，通常是字符串，例如'B'
    """

    cdef void *bptr = NULL
    cdef Py_ssize_t blen = 0, bitemlen = 0
    cdef str bfmt = None
    cdef Py_buffer view
    cdef int flags = PyBUF_SIMPLE
    cdef int mode = 0

    mode = check_buffer(ob)
    if mode == 0:
        raise TypeError("%r does not provide a buffer interface."%ob)

    if mode == 3:
        flags = PyBUF_ANY_CONTIGUOUS
        if writable:
            flags |= PyBUF_WRITABLE
        if format:
            flags |= PyBUF_FORMAT
        PyObject_GetBuffer(ob, &view, flags)
        bptr = view.buf
        blen = view.len
        if format:
            if view.format != NULL:
                bfmt = view.format
                bitemlen = view.itemsize
        PyBuffer_Release(&view)
    else: # oldstyle
        if writable:
            PyObject_AsWriteBuffer(ob, &bptr, &blen)
        else:
            PyObject_AsReadBuffer(ob, <const_void **>&bptr, &blen)
        if format:
            try: # numpy.ndarray
                dtype = ob.dtype
                bfmt = dtype.char
                bitemlen = dtype.itemsize
            except AttributeError:
                try: # array.array
                    bfmt = ob.typecode
                    bitemlen = ob.itemsize
                except AttributeError:
                    if isinstance(ob, bytes):
                        bfmt = "B"
                        bitemlen = 1
                    else:
                        # 什么都没找到
                        bfmt = None
                        bitemlen = 0
    if base: base[0] = <void *>bptr
    if size: size[0] = <Py_ssize_t>blen
    if itemsize: itemsize[0] = <Py_ssize_t>bitemlen
    return bfmt


cdef inline object asbuffer_r(object ob, void **base, Py_ssize_t *size):
    """Wrapper for standard calls to asbuffer with a readonly buffer."""
    asbuffer(ob, 0, 0, base, size, NULL)
    return ob


cdef inline object asbuffer_w(object ob, void **base, Py_ssize_t *size):
    """Wrapper for standard calls to asbuffer with a writable buffer."""
    asbuffer(ob, 1, 0, base, size, NULL)
    return ob

#------------------------------------------------------------------------------
# frombuffer: C buffer对应的python buffer/view
#------------------------------------------------------------------------------


cdef inline object frombuffer_3(void *ptr, Py_ssize_t s, int readonly):
    """
    Python 3版本的frombuffer.
    (Python 2.6应该也可以运行，目前主要用于3.0以上版本)
    """
    cdef Py_buffer pybuf
    cdef Py_ssize_t *shape = [s]
    cdef str astr=""
    PyBuffer_FillInfo(&pybuf, astr, ptr, s, readonly, PyBUF_SIMPLE)
    pybuf.format = "B"
    pybuf.shape = shape
    return PyMemoryView_FromBuffer(&pybuf)


cdef inline object frombuffer_2(void *ptr, Py_ssize_t s, int readonly):
    """
    Python 2版本的frombuffer. 
    (必须用在2.6以下版本，目前主要用于所有3.0以下版本)
    """
    
    if oldstyle_available():
        if readonly:
            return PyBuffer_FromMemory(ptr, s)
        else:
            return PyBuffer_FromReadWriteMemory(ptr, s)
    else:
        raise NotImplementedError("Old style buffers not available.")


cdef inline object frombuffer(void *ptr, Py_ssize_t s, int readonly):
    """
    从C的数组创建一个python buffer/view
    
    参数
    ----------
    ptr : void *
        指向数组的指针
    s : size_t
        buffer长度
    readonly : int
        转换后的对象是否可写(写回原buffer)
    
    返回值
    -------
    转换后的Python Buffer/View
    """
    # oldstyle优先
    if oldstyle_available():
        return frombuffer_2(ptr, s, readonly)
    else:
        return frombuffer_3(ptr, s, readonly)


cdef inline object frombuffer_r(void *ptr, Py_ssize_t s):
    """Wrapper for readonly view frombuffer."""
    return frombuffer(ptr, s, 1)


cdef inline object frombuffer_w(void *ptr, Py_ssize_t s):
    """Wrapper for writable view frombuffer."""
    return frombuffer(ptr, s, 0)

#------------------------------------------------------------------------------
# viewfromobject: python对象对应的python buffer/view(包含完整的引用计数)
# frombuffer(asbuffer(obj))不会跟踪引用情况
#------------------------------------------------------------------------------

cdef inline object viewfromobject(object obj, int readonly):
    """
    从另一个python对象创建一个python buffer/view
    (版本无关的方式实现)
    
    参数
    ----------
    obj : object
        转换为buffer的输入对象
    readonly : int
        转换后的buffer是否只读(是否会覆盖原对象)
    
    返回值
    -------
    源对象转换后的Buffer/View
    """
    if not memoryview_available():
        if readonly:
            return PyBuffer_FromObject(obj, 0, Py_END_OF_BUFFER)
        else:
            return PyBuffer_FromReadWriteObject(obj, 0, Py_END_OF_BUFFER)
    else:
        return PyMemoryView_FromObject(obj)


cdef inline object viewfromobject_r(object obj):
    """只读viewfromobject的封装"""
    return viewfromobject(obj, 1)


cdef inline object viewfromobject_w(object obj):
    """可写viewfromobject的封装"""
    return viewfromobject(obj, 0)
