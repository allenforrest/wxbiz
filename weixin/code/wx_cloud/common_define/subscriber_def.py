#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-18
Description: �����߶����壨���ڶ�����״̬����
Others:      
Key Class&Method List: 
    1. Subscriber
        
History: 
1. Date: 2013-05-18
   Author: Allen
   Modification: �½��ļ�
"""

import time

class Subscriber(object):
    """
    Class: Subscriber
    Description: �������
    Base: 
    Others: 
    """

    def __init__(self, spec, group_ids, state):
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
        self.group_ids = group_ids
        self.last_frame = None
        self.state = state
        self.old_state = None
        self.state_time = time.time()
        self.old_state_time = 0

    def set_fakeid(self, fake_id):
        self.spec.fake_id = fake_id

    def set_detail_info(self, weixin_id, nickname, gender, city):
        self.spec.weixin_id = weixin_id
        self.spec.nickname = nickname
        self.spec.gender = gender
        self.spec.city = city
    
    def set_groups(self, group_ids):
        self.group_ids = group_ids
        
    def set_assoc_member(self, assoc_member_id):
        self.spec.assoc_member_id = assoc_member_id

    def save_frame(self, frame):
        del self.last_frame
        self.last_frame = frame

    def free_frame(self):
        del self.last_frame
        self.last_frame = None

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

    def get_last_frame(self):
        return self.last_frame
    
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

    def get_group_ids(self):
        """
        Method: get_group_ids
        Description: 
        Parameter: ��
        Return: ����
        Others: 
        """

        return self.group_ids
        
    def get_id(self):
        """
        Method: get_id
        Description: ��ȡ�����߶���ID
        Parameter: ��
        Return: ������
        Others: 
        """

        return self.spec.subscriber_open_id
    
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

