#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-18
Description: ������״̬����ض���
Others:      
Key Class&Method List: 
        
History: 
1. Date:2012-05-18
   Author:Allen
   Modification:�½��ļ�
"""
import time
import tracelog

# ������״̬����
INIT_STATE        = 'INIT SUBSCRIBE'
#GET_SUBSCRIBER_INFO_STATE  = 'GET SUBSCRIBER INFO'
SESSION_STATE     = 'NORMAL SESSION'
MENU_SELECT_STATE = 'MENU SELECT'

# �¼�����
#SUBSCRIBE_EVENT             = 'SUBSCRIBE'
#UNSUBSCRIBE_EVENT           = 'UNSUBSCRIBE'
SUBSCRIBER_MESSAGE_EVENT    = 'SUBSCRIBER MESSAGE'
DELIVERY_MENU_SELECT_EVENT  = 'DELIVERY MENU SELECT' 


class FsmEvent(object):
    """
    Class: FsmEvent
    Description: ״̬���¼��ඨ��
    Base: 
    Others: 
    """

    def __init__(self, event_type, target_id, other_info = None):
        """
        Method: __init__
        Description: 
        Parameter: 
            event_type: �¼����� 
            target_id: ״̬�������Ķ���ID
            other_info: ��������
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
    Description: ״̬���¼�����������
    Base: 
    Others: 
    """

    def handle(self, obj, event):
        """
        Method: handle
        Description: ״̬�¼������鷽��
        Parameter: 
            obj: ״̬������
            event: �¼�
        Return: 
        Others: 
        """

        raise NotImplementedError()
    
    
class BaseStateHandler(object):
    """
    Class: BaseStateHandler
    Description: ״̬��״̬����������
    Base: 
    Others: 
    """

    def __init__(self, processor):
        """
        Method: __init__
        Description: ���ʼ�� 
        Parameter: 
            processor: ״̬������������
        Return: 
        Others: 
        """

        self._processor = processor

    def enter_state(self):
        """
        Method: enter_state
        Description: ����״̬������
        Parameter: ��
        Return: 
        Others: 
        """

        raise NotImplementedError()
    
    def exec_state(self):
        """
        Method: exec_state
        Description: ά�ֵ�ǰ״̬������
        Parameter: ��
        Return: 
        Others: 
        """

        raise NotImplementedError()
    
    def exit_state(self):
        """
        Method: exit_state
        Description: �˳���ǰ״̬������
        Parameter: ��
        Return: 
        Others: 
        """

        raise NotImplementedError()
    
    
class SubscriberStateProcessor(object):
    """
    Class: SubscriberStateProcessor
    Description: ������״̬��������
    Base: 
    Others: 
    """

    def __init__(self, task, worker):
        """
        Method: __init__
        Description: ���ʼ�� 
        Parameter: 
            task: ����
            worker: ��������worker
        Return: 
        Others: 
        """

        self._task = task
        self._worker = worker
        self._state_handlers = {}

    def register_state_handler(self, state, handler):
        """
        Method: register_state_handler
        Description: ע��״̬��������
        Parameter: 
            state: ״̬
            handler: ״̬��������
        Return: 
        Others: 
        """

        self._state_handlers[state] = handler

    def unregister_state_handler(self, state):
        """
        Method: unregister_state_handler
        Description: ȥע��״̬��������
        Parameter: 
            state: ״̬
        Return: 
        Others: 
        """

        if self._state_handlers.has_key(state) is True:
            del self._state_handlers[state]
        
    def init_state(self):
        """
        Method: init_state
        Description: ״̬��ʼ��
        Parameter: ��
        Return: 
        Others: 
        """

        self._state_handlers[self._task.get_state()].enter_state()
        self._state_handlers[self._task.get_state()].exec_state()

    def change_state(self, new_state):
        """
        Method: change_state
        Description: ״̬�л�
        Parameter: 
            new_state: ��״̬
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
        Description: ����״̬
        Parameter: ��
        Return: 
        Others: 
        """

        self._state_handlers[self._task.get_state()].exec_state()

    def attach_worker(self, worker):
        """
        Method: attach_worker
        Description: ��������Worker
        Parameter: 
            worker: ����Worker
        Return: 
        Others: 
        """

        self._worker = worker

    def get_target(self):
        """
        Method: get_target
        Description: ��ȡ״̬��������������
        Parameter: ��
        Return: 
        Others: 
        """

        return self._task
    
    def get_worker(self):
        """
        Method: get_worker
        Description: ��ȡ����Worker
        Parameter: ��
        Return: 
        Others: 
        """

        return self._worker


class FsmManager():
    """
    Class: FsmManager
    Description: ״̬����������
    Base: 
    Others: 
    """

    def __init__(self):        
        """
        Method: __init__
        Description: ���ʼ��
        Parameter: ��
        Return: 
        Others: 
        """

        self._processors = {}
        self._event_handlers = {}

    def add_processor(self, processor):        
        """
        Method: add_processor
        Description: ����״̬��������
        Parameter: 
            processor: ״̬��������
        Return: 
        Others: 
        """

        processor.init_state()
        self._processors[processor.get_target().get_id()] = processor

    def remove_processor(self, processor):        
        """
        Method: remove_processor
        Description: ɾ��״̬��������
        Parameter: 
            processor: ״̬��������
        Return: 
        Others: 
        """

        if self._processors.has_key(processor.get_target().get_id()):
            del self._processors[processor.get_target().get_id()]

    def get_processor(self, obj_id):
        """
        Method: get_processor
        Description: ��ȡ״̬��������
        Parameter: 
            obj_id: ����ID
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
        Description: ��ȡ����״̬��������
        Parameter: 
        Return: 
        Others: 
        """

        return self._processors.values()

    def process_event(self, event):
        """
        Method: process_event
        Description: ����״̬���¼�
        Parameter: 
            event: �¼�
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
        Description: ע���¼��������� 
        Parameter: 
            state: ״̬
            event_type: �¼����� 
            handler: �¼���������
        Return: 
        Others: 
        """

        if self._event_handlers.has_key(state) is not True:
            self._event_handlers[state] = {}
        self._event_handlers[state][event_type] = handler

    def unregister_event_handler(self, state, event_type):
        """
        Method: unregister_event_handler
        Description: ȥע���¼��������� 
        Parameter: 
            state: ״̬
            event_type: �¼����� 
        Return: 
        Others:         """

        if self._event_handlers.has_key(state) and self._event_handlers[state].has_key(event_type):        
            del self._event_handlers[state][event_type]        

