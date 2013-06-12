#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-12
Description: ���ļ���ʵ����MOC���ԵĶ���
Others:      
Key Class&Method List: 
             1. MocAttrDef: ��ͨ��MOC���Զ���
             2. ComplexAttrDef: �����������Ͷ���
History: 
1. Date:
   Author:
   Modification:
"""


class MocAttrDef:
    """
    Class: MocAttrDef
    Description: ��ͨ��MOC���Զ���
    Base: 
    Others: 
    """

    def __init__(self, name, is_key, attr_type, max_len = 0, primary_key = False):
        """
        Method:    __init__
        Description: ���캯��
        Parameter:     
            name:       ��������
            is_key:     �Ƿ��ǹؼ���
            attr_type:  ���Ե�����(ԭ�ӵ�����, �������͡��ַ�����
            max_len:    ��󳤶ȣ��������������ַ���ʱ������
            primary_key: ����
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
    Description: �����������Ͷ���
    Base: 
    Others: 
    """

    
    def __init__(self, name, attr_type, is_list, max_len = 0):        
        """
        Method:    __init__
        Description: ���캯��
        Parameter:     
            name:       ��������
            attr_type:  ���Ե�����
            max_len:    ��󳤶ȣ�������������is_listΪTrueʱ������
            is_list:    �Ƿ����б�

        Return: 
        Others: 
        """

        self.name = name
        self.attr_type = attr_type
        self.is_list = is_list
        self.max_len = max_len



