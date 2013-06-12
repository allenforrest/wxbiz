#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-25
Description: �����ж�����mit���ⲿ����ʹ�õ���������
Others:      
Key Class&Method List: 
             1. RawDataMoi: mit���ⲿ����ʹ�õ���������
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
    Description: mit���ⲿ����ʹ�õ���������
    Base: 
    Others: 
        ��mit֮�⣬ͳһʹ��RawDataMoi����ʾһ�������ʵ��
        ��ʹ��mit��MOC��ʵ�����������Ա����ⲿʹ�ö���ʱ�����ö��󷽷���ɻ���
        RawDataMoi��ֻ�ж�������Ժ�ֵ��û�������ķ���

        ���⣬RawDataMoiҲ��Ϊmit���޸����ݵĲ�����

        ����:
            # mit is instance of Mit
            obj = mit.gen_rmd("PhysicalReader")
            obj.readerId = "12-34-56"
            print obj.NumGPIs
            mit.add_obj(obj)         
    """
    
    def __init__(self, moc_class_name, **attr_values):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            moc_class_name: MOC��������
            **attr_values: ��ʼ������ֵ
        Return: 
        Others: 
        """

       
        self.__moc_class_name = moc_class_name

        if len(attr_values) > 0:
            self.__dict__.update(attr_values)
        

    def set_moc_name(self, moc_name):
        """
        Method:    set_moc_name
        Description: ����MOC��������
        Parameter: 
            moc_name: MOC��������
        Return: 
        Others: 
        """

        self.__moc_class_name = moc_name
        
    def get_moc_name(self):
        """
        Method:    get_moc_name
        Description: ��ȡMOC��������
        Parameter: ��
        Return: MOC��������
        Others: 
        """

        return self.__moc_class_name

        
    def clone(self):
        """
        Method:    clone
        Description: ��¡��ǰ��ʵ��
        Parameter: ��
        Return: ��¡������ʵ��
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
        Description: ���л�
        Parameter: ��
        Return: ���л������
        Others: 
        """

        return cPickle.dumps(self)

    @classmethod
    def deserialize(cls, bin_value):        
        """
        Method:    deserialize
        Description: �����л�
        Parameter: 
            bin_value: ������������
        Return: �����л������Ķ���ʵ��
        Others: 
        """

        return cPickle.loads(bin_value)

    
