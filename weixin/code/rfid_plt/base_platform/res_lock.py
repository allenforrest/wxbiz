#coding=gbk

"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-24
Description: 本文件中实现了统一的资源锁功能
Others:      
Key Class&Method List: 
             
History: 
1. Date:
   Author:
   Modification:
"""

import threading

g_all_res = {}


class ResLock:
    """
    Class: ResLock
    Description: 资源的锁
    Base: 
    Others: 
    """
    def __init__(self):
        self.__lock = threading.Lock()

        # 资源是否已经被占用
        self.__is_locked = False 

    def __enter__(self):
        self.acquire(False)
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def acquire(self, blocking = True):
        """
        Method:    acquire
        Description: 占用指定资源的锁
        Parameter: 
            blocking: 当资源被已经被占用时，是否一直等待
        Return: 
            True: 获取到了资源的锁
            False: 没有获取到资源的锁
        Others: 
        """
    
        ret = self.__lock.acquire(blocking)
        if ret:
            self.__is_locked = True

        return ret

    def release(self):
        """
        Method:    release
        Description: 释放指定资源的锁
        Parameter: 
        Return: 
        Others: 
        """

        if self.__is_locked:
            self.__lock.release()
            self.__is_locked = False

    def is_locked(self):
        return self.__is_locked
    
        
def init_res_lock(res_name):
    """
    Method:    init_res_lock
    Description: 初始化一个资源锁
    Parameter: 
        res_name: 资源的名称
    Return: 
    Others: 
        资源初始化后，默认锁是可用状态
        须及时销毁不存在的资源的锁
    """
    global g_all_res
    g_all_res[res_name] = ResLock()

def destroy_res_lock(res_name):
    """
    Method:    destroy_res_lock
    Description: 销毁指定资源的锁
    Parameter: 
        res_name: 资源的名称
    Return: 
    Others: 
    """
    global g_all_res
    lock = g_all_res.pop(res_name, None)
    
    if lock is not None:
        del lock
        
def get_res_lock(res_name):
    """
    Method:    get_res_lock
    Description: 获取指定资源的锁
    Parameter: 
        res_name: 资源的名称
    Return: 指定资源的锁
    Others: 
    """
    global g_all_res

    return g_all_res.get(res_name)


def is_res_locked(res_name):
    lock = g_all_res.get(res_name)
    return lock.is_locked()
        

def acquire(res_name, blocking = True):
    """
    Method:    acquire
    Description: 占用指定资源的锁
    Parameter: 
        res_name: 资源的名称
        blocking: 当资源被已经被占用时，是否一直等待
    Return: 
        True: 获取到了资源的锁
        False: 没有获取到资源的锁
    Others: 
    """
    global g_all_res

    lock = g_all_res.get(res_name)
    return lock.acquire(blocking)

def release(res_name):
    """
    Method:    release
    Description: 释放指定资源的锁
    Parameter: 
        res_name: 资源的名称
    Return: 
    Others: 
    """
    global g_all_res
    
    lock = g_all_res.get(res_name)
    lock.release()
    
    


