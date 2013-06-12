#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-10
Description: ������ʵ���˹���У��ʧ�ܵ��쳣��
Others:      
Key Class&Method List: 
             1. RuleException: ����У��ʧ�ܵ��쳣��
History: 
1. Date:
   Author:
   Modification:
"""

import err_code_mgr
import tracelog

class RuleException(Exception):
    """
    Class: RuleException
    Description: ����У��ʧ�ܵ��쳣��
    Base: Exception
    Others: 
    """

    def __init__(self, err_code, **kw):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            err_code: ������
            **kw: ������Ϣ����Ҫ�Ķ�̬������ֵ
        Return: 
        Others: 
        """

        Exception.__init__(self, "rule check error")
        self.err_code = err_code
        self.kw = kw
        

    def get_err_code(self):
        """
        Method:    get_err_code
        Description: ��ȡ������
        Parameter: ��
        Return: ������
        Others: 
        """

        return self.err_code
        
    def get_msg(self):
        """
        Method:    get_msg
        Description: ��ȡ������Ϣ
        Parameter: ��
        Return: ������Ϣ
        Others: 
        """

        try:
            return err_code_mgr.get_error_msg(self.err_code, **self.kw)
        except:
            tracelog.exception("RuleException: get_error_msg failed, err_code:%s, kw:%s" % (repr(self.err_code), repr(self.kw)))
            return "RuleException: err_code:%s, err_msg:unknow!" % repr(self.err_code)


        