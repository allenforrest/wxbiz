#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-18
Description: 本文件实现了规则引擎类
Others:      
Key Class&Method List: 
             1. RuleEngine: 规则引擎类
History: 
1. Date:
   Author:
   Modification:
"""



from _mit.rule_exception import  RuleException

class RuleEngine:
    """
    Class: RuleEngine
    Description: 校验规则引擎类
    Base: 
    Others: 
    """

    def __init__(self):

        pass
        
    def check(self, is_True, err_code, **msg_paras):
        """
        Method:    check
        Description: 校验一个规则
        Parameter: 
            is_True: 布尔值，表示规则是否满足
            err_code: 错误信息
            **msg_paras: 错误信息中的动态参数的值
        Return: 
        Others: 
        """

        if is_True:
            pass

        else:
            raise RuleException(err_code, **msg_paras)

    

