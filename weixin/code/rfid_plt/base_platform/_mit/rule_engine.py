#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-18
Description: ���ļ�ʵ���˹���������
Others:      
Key Class&Method List: 
             1. RuleEngine: ����������
History: 
1. Date:
   Author:
   Modification:
"""



from _mit.rule_exception import  RuleException

class RuleEngine:
    """
    Class: RuleEngine
    Description: У�����������
    Base: 
    Others: 
    """

    def __init__(self):

        pass
        
    def check(self, is_True, err_code, **msg_paras):
        """
        Method:    check
        Description: У��һ������
        Parameter: 
            is_True: ����ֵ����ʾ�����Ƿ�����
            err_code: ������Ϣ
            **msg_paras: ������Ϣ�еĶ�̬������ֵ
        Return: 
        Others: 
        """

        if is_True:
            pass

        else:
            raise RuleException(err_code, **msg_paras)

    

