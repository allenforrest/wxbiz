#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-10
Description: 本文中实现了规则校验失败的异常类
Others:      
Key Class&Method List: 
             1. RuleException: 规则校验失败的异常类
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
    Description: 规则校验失败的异常类
    Base: Exception
    Others: 
    """

    def __init__(self, err_code, **kw):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            err_code: 错误码
            **kw: 错误信息中需要的动态参数的值
        Return: 
        Others: 
        """

        Exception.__init__(self, "rule check error")
        self.err_code = err_code
        self.kw = kw
        

    def get_err_code(self):
        """
        Method:    get_err_code
        Description: 获取错误码
        Parameter: 无
        Return: 错误码
        Others: 
        """

        return self.err_code
        
    def get_msg(self):
        """
        Method:    get_msg
        Description: 获取错误信息
        Parameter: 无
        Return: 错误信息
        Others: 
        """

        try:
            return err_code_mgr.get_error_msg(self.err_code, **self.kw)
        except:
            tracelog.exception("RuleException: get_error_msg failed, err_code:%s, kw:%s" % (repr(self.err_code), repr(self.kw)))
            return "RuleException: err_code:%s, err_msg:unknow!" % repr(self.err_code)


        