/*************************************************
Copyright (C), 2012-2015, Anything Connected Possibilities
Author:   ACP team
Version:  1.0
Date:     2012/09
Description:   eipc基础功能模块: 分配字节数组buffer
Others:      
Key Class&Method List: 
			allocate        分配大小为n的空字节数组

History: 
1. Date:        2012/09    
   Author:      ACP team
2. ...
*************************************************/

#include "Python.h"

static PyObject * allocate(Py_ssize_t n, void **pp){
  PyObject *ob;
  if (n > PY_SSIZE_T_MAX)
    return PyErr_NoMemory();
  else if (n < 0) {
    PyErr_SetString(PyExc_RuntimeError,
                    "memory allocation with negative size");
    return NULL;
  }
  ob = PyByteArray_FromStringAndSize(NULL, (n==0) ? 1 : n);
  if (ob && n==0 && (PyByteArray_Resize(ob, 0) < 0)) {
    Py_DECREF(ob);
    return NULL;
  }
  if (ob && pp)
    *pp = (void *)PyByteArray_AS_STRING(ob);
  return ob;
}