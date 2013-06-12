#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-15
Description: 本文实现了mit中用户结果收集的功能类
Others:      
Key Class&Method List: 
             1. RstCollector: mit中用户结果收集的功能类
History: 
1. Date:
   Author:
   Modification:
"""


class RstCollector:
    """
    Class: RstCollector
    Description: mit中用户结果收集的功能类
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
            err_code: 错误码
            msg: 错误信息
            _info: 其他所有的用户自定义的信息
        """

        self.err_code = 0
        self.msg = ""
        
        self._info = {}
       

    def clear(self):
        """
        Method:    clear
        Description: 情况所有的信息
        Parameter: 无
        Return: 
        Others: 
        """

        self.err_code = 0
        self.msg = ""    
        self._info.clear()
        

    def set_err_code(self, err_code):
        """
        Method:    set_err_code
        Description: 设置错误码
        Parameter: 
            err_code: 错误码
        Return: 
        Others: 
        """

        self.err_code = err_code


    def get_err_code(self):
        """
        Method:    get_err_code
        Description: 获取错误码
        Parameter: 无
        Return: 错误码
        Others: 
        """

        return self.err_code


    def set_msg(self, msg):
        """
        Method:    set_msg
        Description: 设置错误信息
        Parameter: 
            msg: 错误信息
        Return: 
        Others: 
        """

        self.msg = msg

    def get_msg(self):
        """
        Method:    get_msg
        Description: 获取错误信息
        Parameter: 无
        Return: 错误信息
        Others: 
        """

        return self.msg
        
        
    def set_field(self, field_name, value):
        """
        Method:    set_field
        Description: 设置一个字段信息
        Parameter: 
            field_name: 字段的名称
            value: 字段的值
        Return: 
        Others: 
        """

        self._info[field_name] = value

    def get_field(self, field_name, default = None):
        """
        Method:    get_field
        Description: 获取一个字段的值
        Parameter: 
            field_name: 字段的名称
            default: 如果字段不存在，则返回该值
        Return: 字段的值或默认值
        Others: 
        """

        return self._info.get(field_name, default)

    def has_field(self, field_name):
        """
        Method:    has_field
        Description: 判断是否存在某个字段
        Parameter: 
            field_name: 字段的名称
        Return: 指定的字段是否存在
        Others: 
        """

        return field_name in self._info
    
