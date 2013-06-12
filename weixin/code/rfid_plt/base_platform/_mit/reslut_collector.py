#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-15
Description: ����ʵ����mit���û�����ռ��Ĺ�����
Others:      
Key Class&Method List: 
             1. RstCollector: mit���û�����ռ��Ĺ�����
History: 
1. Date:
   Author:
   Modification:
"""


class RstCollector:
    """
    Class: RstCollector
    Description: mit���û�����ռ��Ĺ�����
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
            err_code: ������
            msg: ������Ϣ
            _info: �������е��û��Զ������Ϣ
        """

        self.err_code = 0
        self.msg = ""
        
        self._info = {}
       

    def clear(self):
        """
        Method:    clear
        Description: ������е���Ϣ
        Parameter: ��
        Return: 
        Others: 
        """

        self.err_code = 0
        self.msg = ""    
        self._info.clear()
        

    def set_err_code(self, err_code):
        """
        Method:    set_err_code
        Description: ���ô�����
        Parameter: 
            err_code: ������
        Return: 
        Others: 
        """

        self.err_code = err_code


    def get_err_code(self):
        """
        Method:    get_err_code
        Description: ��ȡ������
        Parameter: ��
        Return: ������
        Others: 
        """

        return self.err_code


    def set_msg(self, msg):
        """
        Method:    set_msg
        Description: ���ô�����Ϣ
        Parameter: 
            msg: ������Ϣ
        Return: 
        Others: 
        """

        self.msg = msg

    def get_msg(self):
        """
        Method:    get_msg
        Description: ��ȡ������Ϣ
        Parameter: ��
        Return: ������Ϣ
        Others: 
        """

        return self.msg
        
        
    def set_field(self, field_name, value):
        """
        Method:    set_field
        Description: ����һ���ֶ���Ϣ
        Parameter: 
            field_name: �ֶε�����
            value: �ֶε�ֵ
        Return: 
        Others: 
        """

        self._info[field_name] = value

    def get_field(self, field_name, default = None):
        """
        Method:    get_field
        Description: ��ȡһ���ֶε�ֵ
        Parameter: 
            field_name: �ֶε�����
            default: ����ֶβ����ڣ��򷵻ظ�ֵ
        Return: �ֶε�ֵ��Ĭ��ֵ
        Others: 
        """

        return self._info.get(field_name, default)

    def has_field(self, field_name):
        """
        Method:    has_field
        Description: �ж��Ƿ����ĳ���ֶ�
        Parameter: 
            field_name: �ֶε�����
        Return: ָ�����ֶ��Ƿ����
        Others: 
        """

        return field_name in self._info
    
