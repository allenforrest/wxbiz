#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-18
Description: 订阅者状态机相关定义
Others:      
Key Class&Method List: 
        
History: 
1. Date:2012-05-18
   Author:Allen
   Modification:新建文件
"""
import time
import tracelog

# 订阅者状态定义
INIT_STATE        = 'INIT SUBSCRIBE'
#GET_SUBSCRIBER_INFO_STATE  = 'GET SUBSCRIBER INFO'
SESSION_STATE     = 'NORMAL SESSION'
MENU_SELECT_STATE = 'MENU SELECT'

# 事件定义
#SUBSCRIBE_EVENT             = 'SUBSCRIBE'
#UNSUBSCRIBE_EVENT           = 'UNSUBSCRIBE'
SUBSCRIBER_MESSAGE_EVENT    = 'SUBSCRIBER MESSAGE'
DELIVERY_MENU_SELECT_EVENT  = 'DELIVERY MENU SELECT' 


class FsmEvent(object):
    """
    Class: FsmEvent
    Description: 状态机事件类定义
    Base: 
    Others: 
    """

    def __init__(self, event_type, target_id, other_info = None):
        """
        Method: __init__
        Description: 
        Parameter: 
            event_type: 事件类型 
            target_id: 状态机关联的对象ID
            other_info: 其他参数
        Return: 
        Others: 
        """

        self.event_id = time.time()
        self.event_type = event_type
        self.target_id = target_id
        self.other_info = other_info


class FsmHandler(object):
    """
    Class: FsmHandler
    Description: 状态机事件处理方法基类
    Base: 
    Others: 
    """

    def handle(self, obj, event):
        """
        Method: handle
        Description: 状态事件处理虚方法
        Parameter: 
            obj: 状态机对象
            event: 事件
        Return: 
        Others: 
        """

        raise NotImplementedError()
    
    
class BaseStateHandler(object):
    """
    Class: BaseStateHandler
    Description: 状态机状态处理方法基类
    Base: 
    Others: 
    """

    def __init__(self, processor):
        """
        Method: __init__
        Description: 类初始化 
        Parameter: 
            processor: 状态机处理器对象
        Return: 
        Others: 
        """

        self._processor = processor

    def enter_state(self):
        """
        Method: enter_state
        Description: 进入状态处理方法
        Parameter: 无
        Return: 
        Others: 
        """

        raise NotImplementedError()
    
    def exec_state(self):
        """
        Method: exec_state
        Description: 维持当前状态处理方法
        Parameter: 无
        Return: 
        Others: 
        """

        raise NotImplementedError()
    
    def exit_state(self):
        """
        Method: exit_state
        Description: 退出当前状态处理方法
        Parameter: 无
        Return: 
        Others: 
        """

        raise NotImplementedError()
    
    
class SubscriberStateProcessor(object):
    """
    Class: SubscriberStateProcessor
    Description: 订阅者状态处理器类
    Base: 
    Others: 
    """

    def __init__(self, task, worker):
        """
        Method: __init__
        Description: 类初始化 
        Parameter: 
            task: 任务
            worker: 任务宿主worker
        Return: 
        Others: 
        """

        self._task = task
        self._worker = worker
        self._state_handlers = {}

    def register_state_handler(self, state, handler):
        """
        Method: register_state_handler
        Description: 注册状态处理方法类
        Parameter: 
            state: 状态
            handler: 状态处理方法类
        Return: 
        Others: 
        """

        self._state_handlers[state] = handler

    def unregister_state_handler(self, state):
        """
        Method: unregister_state_handler
        Description: 去注册状态处理方法类
        Parameter: 
            state: 状态
        Return: 
        Others: 
        """

        if self._state_handlers.has_key(state) is True:
            del self._state_handlers[state]
        
    def init_state(self):
        """
        Method: init_state
        Description: 状态初始化
        Parameter: 无
        Return: 
        Others: 
        """

        self._state_handlers[self._task.get_state()].enter_state()
        self._state_handlers[self._task.get_state()].exec_state()

    def change_state(self, new_state):
        """
        Method: change_state
        Description: 状态切换
        Parameter: 
            new_state: 新状态
        Return: 
        Others: 
        """

        self._state_handlers[self._task.get_state()].exit_state()
        self._task.set_state(new_state)
        self._state_handlers[self._task.get_state()].enter_state()
        self._state_handlers[self._task.get_state()].exec_state()

    def keep_state(self):
        """
        Method: keep_state
        Description: 保持状态
        Parameter: 无
        Return: 
        Others: 
        """

        self._state_handlers[self._task.get_state()].exec_state()

    def attach_worker(self, worker):
        """
        Method: attach_worker
        Description: 配置宿主Worker
        Parameter: 
            worker: 宿主Worker
        Return: 
        Others: 
        """

        self._worker = worker

    def get_target(self):
        """
        Method: get_target
        Description: 获取状态机处理器的任务
        Parameter: 无
        Return: 
        Others: 
        """

        return self._task
    
    def get_worker(self):
        """
        Method: get_worker
        Description: 获取宿主Worker
        Parameter: 无
        Return: 
        Others: 
        """

        return self._worker


class FsmManager():
    """
    Class: FsmManager
    Description: 状态机管理器类
    Base: 
    Others: 
    """

    def __init__(self):        
        """
        Method: __init__
        Description: 类初始化
        Parameter: 无
        Return: 
        Others: 
        """

        self._processors = {}
        self._event_handlers = {}

    def add_processor(self, processor):        
        """
        Method: add_processor
        Description: 增加状态机处理器
        Parameter: 
            processor: 状态机处理器
        Return: 
        Others: 
        """

        processor.init_state()
        self._processors[processor.get_target().get_id()] = processor

    def remove_processor(self, processor):        
        """
        Method: remove_processor
        Description: 删除状态机处理器
        Parameter: 
            processor: 状态机处理器
        Return: 
        Others: 
        """

        if self._processors.has_key(processor.get_target().get_id()):
            del self._processors[processor.get_target().get_id()]

    def get_processor(self, obj_id):
        """
        Method: get_processor
        Description: 获取状态机处理器
        Parameter: 
            obj_id: 对象ID
        Return: 
        Others: 
        """

        if self._processors.has_key(obj_id):
            return self._processors[obj_id]
        else:
            return None

    def get_processors(self):
        """
        Method: get_processor
        Description: 获取所有状态机处理器
        Parameter: 
        Return: 
        Others: 
        """

        return self._processors.values()

    def process_event(self, event):
        """
        Method: process_event
        Description: 处理状态机事件
        Parameter: 
            event: 事件
        Return: 
        Others: 
        """

        if self._processors.has_key(event.target_id) is not True:
            tracelog.error("the object %s in the state management does't exist " % event.target_id)
            return
        else:
            processor = self._processors[event.target_id]
        if (self._event_handlers.has_key(processor.get_target().state) is not True or
            self._event_handlers[processor.get_target().state].has_key(event.event_type) is not True):
            tracelog.error("can not find the handler of %s state and %s event" % (processor.get_target().state
                                                                                , event.event_type))
            return
        
        new_state = (self._event_handlers[processor.get_target().state][event.event_type].handle(processor, event))
        tracelog.info('FSM: object(%s), old_state(%s), event(%s), new_state(%s)' %(processor.get_target().get_id(), processor.get_target().state, event.event_type, new_state))
        processor.change_state(new_state)

    def register_event_handler(self, state, event_type, handler):
        """
        Method: register_event_handler
        Description: 注册事件处理方法类 
        Parameter: 
            state: 状态
            event_type: 事件类型 
            handler: 事件处理方法类
        Return: 
        Others: 
        """

        if self._event_handlers.has_key(state) is not True:
            self._event_handlers[state] = {}
        self._event_handlers[state][event_type] = handler

    def unregister_event_handler(self, state, event_type):
        """
        Method: unregister_event_handler
        Description: 去注册事件处理方法类 
        Parameter: 
            state: 状态
            event_type: 事件类型 
        Return: 
        Others:         """

        if self._event_handlers.has_key(state) and self._event_handlers[state].has_key(event_type):        
            del self._event_handlers[state][event_type]        

