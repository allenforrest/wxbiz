#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-12
Description: 本文件中实现了MOC属性的定义
Others:      
Key Class&Method List: 
             1. MocAttrDef: 普通的MOC属性定义
             2. ComplexAttrDef: 复合属性类型定义
History: 
1. Date:
   Author:
   Modification:
"""


class MocAttrDef:
    """
    Class: MocAttrDef
    Description: 普通的MOC属性定义
    Base: 
    Others: 
    """

    def __init__(self, name, is_key, attr_type, max_len = 0, primary_key = False):
        """
        Method:    __init__
        Description: 构造函数
        Parameter:     
            name:       属性名称
            is_key:     是否是关键字
            attr_type:  属性的类型(原子的类型, 例如整型、字符串等
            max_len:    最大长度，当属性类型是字符串时有意义
            primary_key: 主键
        Return: 
        Others: 
        """

        self.name = name
        self.attr_type = attr_type
        self.is_key = is_key
        self.max_len = max_len
        self.primary_key = primary_key
        
        
class ComplexAttrDef:
    """
    Class: ComplexAttrDef
    Description: 复合属性类型定义
    Base: 
    Others: 
    """

    
    def __init__(self, name, attr_type, is_list, max_len = 0):        
        """
        Method:    __init__
        Description: 构造函数
        Parameter:     
            name:       属性名称
            attr_type:  属性的类型
            max_len:    最大长度，当属性类型是is_list为True时有意义
            is_list:    是否是列表

        Return: 
        Others: 
        """

        self.name = name
        self.attr_type = attr_type
        self.is_list = is_list
        self.max_len = max_len



