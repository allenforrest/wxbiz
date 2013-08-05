#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-18
Description: ��Ա�����壨���ڻ�Ա״̬����
Others:      
Key Class&Method List: 
    1. Member
        
History: 
1. Date: 2013-07-05
   Author: Allen
   Modification: �½��ļ�
"""

import time

class Member(object):
    """
    Class: Member
    Description: �������
    Base: 
    Others: 
    """

    def __init__(self, spec, state):
        """
        Method: __init__
        Description: ���ʼ��
        Parameter: 
            spec: �����߶������
            state: �����߶����ʼ״̬
        Return: 
        Others: 
        """
        self.spec = spec
        self.assoc_sub_spec = None
        self.delivery_id = None
        self.today = time.time()
        self.state = state
        self.old_state = None
        self.state_time = time.time()
        self.old_state_time = 0

    def set_delivery_id(self, delivery_id):
        self.delivery_id = delivery_id

    def set_assoc_subscriber(self, sub_spec):
        self.assoc_sub_spec = sub_spec
        
    def set_today(self, today):
        self.today = today

    def set_state(self, state):
        """
        Method: set_state
        Description: ���ö���״̬
        Parameter: 
            state: ״̬
        Return: 
        Others: 
        """
        if self.old_state is None:
            self.first_create = True

        self.old_state = self.state
        self.state = state
        self.old_state_time = self.state_time
        self.state_time = time.time()

    def get_state(self):
        """
        Method: get_state
        Description: ��ȡ����ǰ״̬
        Parameter: ��
        Return: ״̬
        Others: 
        """

        return self.state

    def get_old_state(self):
        """
        Method: get_old_state
        Description: ��ȡ������һ��״̬
        Parameter: ��
        Return: ״̬
        Others: 
        """

        return self.old_state

    def get_spec(self):
        """
        Method: get_spec
        Description: ��ȡ�����߶������
        Parameter: ��
        Return: ����
        Others: 
        """

        return self.spec

    def get_delivery_id(self):
        return self.delivery_id

    def get_assoc_subscriber(self):
        return self.assoc_sub_spec

    def get_today(self):
        return self.today

    def get_id(self):
        """
        Method: get_id
        Description: ��ȡ�����߶���ID
        Parameter: ��
        Return: ������
        Others: 
        """

        return self.spec.member_id
    
    def get_state_time(self):
        """
        Method: get_state_time
        Description: ��ȡ�л�����ǰ״̬��ʱ��
        Parameter: ��
        Return: ʱ��
        Others: 
        """

        return self.state_time

    def get_old_state_time(self):
        """
        Method: get_old_state_time
        Description: ��ȡ�л�����һ��״̬��ʱ��
        Parameter: ��
        Return: ʱ��
        Others: 
        """

        return self.old_state_time

