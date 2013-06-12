#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-25
Description: 本文中定义了mit与外部交互使用的数据类型
Others:      
Key Class&Method List: 
             1. RawDataMoi: mit与外部交互使用的数据类型
History: 
1. Date:
   Author:
   Modification:
"""

import copy

import cPickle

class RawDataMoi:
    """
    Class: RawDataMoi
    Description: mit与外部交互使用的数据类型
    Base: 
    Others: 
        在mit之外，统一使用RawDataMoi来表示一个对象的实例
        不使用mit中MOC的实例，这样可以避免外部使用对象时，调用对象方法造成混乱
        RawDataMoi中只有对象的属性和值，没有其他的方法

        另外，RawDataMoi也作为mit中修改数据的参数，

        举例:
            # mit is instance of Mit
            obj = mit.gen_rmd("PhysicalReader")
            obj.readerId = "12-34-56"
            print obj.NumGPIs
            mit.add_obj(obj)         
    """
    
    def __init__(self, moc_class_name, **attr_values):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            moc_class_name: MOC的类名称
            **attr_values: 初始的属性值
        Return: 
        Others: 
        """

       
        self.__moc_class_name = moc_class_name

        if len(attr_values) > 0:
            self.__dict__.update(attr_values)
        

    def set_moc_name(self, moc_name):
        """
        Method:    set_moc_name
        Description: 设置MOC的类名称
        Parameter: 
            moc_name: MOC的类名称
        Return: 
        Others: 
        """

        self.__moc_class_name = moc_name
        
    def get_moc_name(self):
        """
        Method:    get_moc_name
        Description: 获取MOC的类名称
        Parameter: 无
        Return: MOC的类名称
        Others: 
        """

        return self.__moc_class_name

        
    def clone(self):
        """
        Method:    clone
        Description: 克隆当前的实例
        Parameter: 无
        Return: 克隆出来的实例
        Others: 
        """

        return copy.deepcopy(self)
        
    def __str__(self):
        attrs = ["%s=%s" % (repr(attr_name), repr(value)) for attr_name, value in self.__dict__.iteritems()]
        return "rdm(%s, %s)" % (self.__moc_class_name, ", ".join(attrs))

    def __repr__(self):
        return str(self)

    def serialize(self):
        """
        Method:    serialize
        Description: 序列化
        Parameter: 无
        Return: 序列化后的流
        Others: 
        """

        return cPickle.dumps(self)

    @classmethod
    def deserialize(cls, bin_value):        
        """
        Method:    deserialize
        Description: 反序列化
        Parameter: 
            bin_value: 二进制数据流
        Return: 反序列化出来的对象实例
        Others: 
        """

        return cPickle.loads(bin_value)

    
