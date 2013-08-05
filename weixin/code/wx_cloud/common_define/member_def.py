#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-18
Description: 会员对象定义（用于会员状态机）
Others:      
Key Class&Method List: 
    1. Member
        
History: 
1. Date: 2013-07-05
   Author: Allen
   Modification: 新建文件
"""

import time

class Member(object):
    """
    Class: Member
    Description: 任务基类
    Base: 
    Others: 
    """

    def __init__(self, spec, state):
        """
        Method: __init__
        Description: 类初始化
        Parameter: 
            spec: 订阅者对象参数
            state: 订阅者对象初始状态
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
        Description: 设置对象状态
        Parameter: 
            state: 状态
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
        Description: 获取对象当前状态
        Parameter: 无
        Return: 状态
        Others: 
        """

        return self.state

    def get_old_state(self):
        """
        Method: get_old_state
        Description: 获取对象上一次状态
        Parameter: 无
        Return: 状态
        Others: 
        """

        return self.old_state

    def get_spec(self):
        """
        Method: get_spec
        Description: 获取订阅者对象参数
        Parameter: 无
        Return: 对象
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
        Description: 获取订阅者对象ID
        Parameter: 无
        Return: 对象名
        Others: 
        """

        return self.spec.member_id
    
    def get_state_time(self):
        """
        Method: get_state_time
        Description: 获取切换到当前状态的时间
        Parameter: 无
        Return: 时间
        Others: 
        """

        return self.state_time

    def get_old_state_time(self):
        """
        Method: get_old_state_time
        Description: 获取切换到上一次状态的时间
        Parameter: 无
        Return: 时间
        Others: 
        """

        return self.old_state_time

