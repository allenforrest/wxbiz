#coding=gbk

"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-24
Description: ���ļ���ʵ����ͳһ����Դ������
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
    Description: ��Դ����
    Base: 
    Others: 
    """
    def __init__(self):
        self.__lock = threading.Lock()

        # ��Դ�Ƿ��Ѿ���ռ��
        self.__is_locked = False 

    def __enter__(self):
        self.acquire(False)
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def acquire(self, blocking = True):
        """
        Method:    acquire
        Description: ռ��ָ����Դ����
        Parameter: 
            blocking: ����Դ���Ѿ���ռ��ʱ���Ƿ�һֱ�ȴ�
        Return: 
            True: ��ȡ������Դ����
            False: û�л�ȡ����Դ����
        Others: 
        """
    
        ret = self.__lock.acquire(blocking)
        if ret:
            self.__is_locked = True

        return ret

    def release(self):
        """
        Method:    release
        Description: �ͷ�ָ����Դ����
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
    Description: ��ʼ��һ����Դ��
    Parameter: 
        res_name: ��Դ������
    Return: 
    Others: 
        ��Դ��ʼ����Ĭ�����ǿ���״̬
        �뼰ʱ���ٲ����ڵ���Դ����
    """
    global g_all_res
    g_all_res[res_name] = ResLock()

def destroy_res_lock(res_name):
    """
    Method:    destroy_res_lock
    Description: ����ָ����Դ����
    Parameter: 
        res_name: ��Դ������
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
    Description: ��ȡָ����Դ����
    Parameter: 
        res_name: ��Դ������
    Return: ָ����Դ����
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
    Description: ռ��ָ����Դ����
    Parameter: 
        res_name: ��Դ������
        blocking: ����Դ���Ѿ���ռ��ʱ���Ƿ�һֱ�ȴ�
    Return: 
        True: ��ȡ������Դ����
        False: û�л�ȡ����Դ����
    Others: 
    """
    global g_all_res

    lock = g_all_res.get(res_name)
    return lock.acquire(blocking)

def release(res_name):
    """
    Method:    release
    Description: �ͷ�ָ����Դ����
    Parameter: 
        res_name: ��Դ������
    Return: 
    Others: 
    """
    global g_all_res
    
    lock = g_all_res.get(res_name)
    lock.release()
    
    


