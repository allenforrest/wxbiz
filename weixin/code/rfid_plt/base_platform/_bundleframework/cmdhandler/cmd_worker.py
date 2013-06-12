#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-19
Description: ���ļ���ʵ���˴�������ִ�е�worker
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


import time

import tracelog
import err_code_mgr

from _bundleframework.protocol.appframe import AppFrame
from _bundleframework.dispatch.worker import Worker

class CmdWorker(Worker):
    """
    Class: CmdWorker
    Description: ����ִ�е�worker
    Base: Worker
    Others: 
    """

    invalid_task_id = 0

    def __init__(self, name, min_task_id, max_task_id):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            name: worker������
            min_task_id: 
            max_task_id: 
        Return: 
        Others: 
             һ��app�е�worker���Ʋ��ܳ�ͻ
             ÿ��app�е�����worker������Ҫ���Լ���taskid�����Σ��Ҳ��ܻ����غ�
             min_task_id����С�� 1
             max_task_id���ܴ���0xFFFFFFFE
             taskid�� unsigned int����

             ע: RpcWorker�Ѿ��̶�ʹ��0xFFFF0000~0xFFFFFFFE
                ��������workerֻ��ʹ��1~0xFFFEFFFF
                
        """
        
        Worker.__init__(self, name)

        self.__min_task_id = min(min(0xFFFFFFFF, max(1, min_task_id)), min(0xFFFFFFFF, max(1, max_task_id)))
        self.__max_task_id = max(min(0xFFFFFFFF, max(1, min_task_id)), min(0xFFFFFFFF, max(1, max_task_id)))
        self.__current_task_id = self.__min_task_id

        self.__ack_handlers = {}

        self.set_dispatch_handler_strategy(CmdCodeDispatchHandlerStrategy())
        self.set_busy_strategy(NoBusyStrategy())

    def set_dispatch_handler_strategy(self, strategy):
        """
        Method:    set_dispatch_handler_strategy
        Description: ����handler���ҵĲ���
        Parameter: 
            strategy: handler���ҵĲ���
        Return: 
        Others: 
        """

        if strategy is None:
            self.__dispatch_handler_strategy = CmdCodeDispatchHandlerStrategy()
        else:
            self.__dispatch_handler_strategy = strategy

    def get_dispatch_handler_strategy(self):
        return self.__dispatch_handler_strategy
        
    
    def set_busy_strategy(self, strategy):
        """
        Method:    set_busy_strategy
        Description: ����handler�����Ĳ���
        Parameter: 
            strategy: handler�����Ĳ���
        Return: 
        Others: 
        """

        if strategy:
            self.__busy_strategy = strategy
        else:
            self.__busy_strategy = NoBusyStrategy()

    def register_handler(self, handler, *args):
        """
        Method:    register_handler
        Description: ע��handler
        Parameter: 
            handler: handler����
            *args: ���ݸ�handler���ҵĲ��Զ���Ĳ���
        Return: 
        Others: 
        """

        if handler is not None:
            handler.set_worker(self)
            self.__dispatch_handler_strategy.register_handler(handler, *args)
        else:
            tracelog.error("handler is None for %s " % self.get_name())

    def register_ack_handler(self, handler):
        """
        Method:    register_ack_handler
        Description: ��handlerע��Ϊ�ȴ�Ӧ����Ϣ��״̬
        Parameter: 
            handler: handler����
        Return: �����
        Others: 
        """

        return self.register_ack_handler_again(handler, CmdWorker.invalid_task_id)

    def register_ack_handler_again(self, handler, task_id):
        """
        Method:    register_ack_handler_again
        Description: ���½�handlerע��Ϊ�ȴ�Ӧ����Ϣ��״̬
        Parameter: 
            handler: handler����
            task_id: �����
        Return: �����
        Others: 
        """

        if handler is None:
            tracelog.error("register ack in worker %s handler is null!" % self.get_name())
            return CmdWorker.invalid_task_id

        if task_id == CmdWorker.invalid_task_id:
            task_id = self.__new_task_id()

        if task_id < self.__min_task_id or task_id > self.__max_task_id:
            tracelog.error("worker %s task_id %d is out of range(%d, %d)!" % (self.get_name(), task_id, self.__min_task_id, self.__max_task_id))
            return CmdWorker.invalid_task_id

        self.__ack_handlers[task_id] = handler
        self.register_time_out_handler(handler)

        return task_id

    def __check_over_handles(self):
        """
        Method:    __check_over_handles
        Description: ���handler�Ƿ��Ѿ�����������Ѿ���������ɾ��֮
        Parameter: ��
        Return: 
        Others: 
        """

        for task_id, handler in self.__ack_handlers.items(): # ע:����ʹ��iteritems
            if handler.is_over():
                self.__ack_handlers.pop(task_id)
            else:
                if time.time() - handler.get_time_of_new() > 24 * 60 * 60:
                    tracelog.error("handler %s in worker %s last 24 hours!" % (handler, self.get_name()))
                    handler.over(err_code_mgr.ER_TIMEOUT)
                    self.__ack_handlers.pop(task_id)
        
        
    def __new_task_id(self):
        """
        Method:    __new_task_id
        Description: ����һ���µ������
        Parameter: ��
        Return: �����
        Others: 
        """

        if len(self.__ack_handlers) >= (self.__max_task_id - self.__min_task_id + 1):
            self.__check_over_handles()
            
            if len(self.__ack_handlers) >= (self.__max_task_id - self.__min_task_id + 1):
                return CmdWorker.invalid_task_id

        task_id = self.__current_task_id + 1
        while task_id in self.__ack_handlers and task_id <= self.__max_task_id:
            task_id += 1

        if task_id > self.__max_task_id:
            task_id = self.__min_task_id
            while task_id in self.__ack_handlers and task_id <= self.__current_task_id:
                task_id += 1

            if task_id > self.__current_task_id:
                return self.invalid_task_id
        
        self.__current_task_id = task_id
        return task_id

    def is_my_duty(self, frame):
        """
        Method:    is_my_duty
        Description: �жϸ���������Ƿ����ڵ�ǰworker����
        Parameter: 
            frame: ���appframe����
        Return: ����������Ƿ����ڵ�ǰworker����
        Others: 
        """

        if frame.is_ack_frame() and self.__ack_handlers.has_key(frame.get_task_id()):
            return True
        else:
            return self.__dispatch_handler_strategy.get_duty_cmd_handler(frame)

    def is_busy(self, frame):
        """
        Method:    is_busy
        Description: �жϸ�������Ƿ������ڵȴ�Ӧ����Ϣ��handler����ͬʱִ��
        Parameter: 
            frame: ���appframe����
        Return: 
        Others: 
        """

        return self.__busy_strategy.is_busy(self.__ack_handlers, frame)

    def priority(self, frame):
        """
        Method:    priority
        Description: ��ȡָ����Ϣ�����ȼ�
        Parameter: 
            frame: AppFrame
        Return: ���ȼ�
        Others: 
        """

        if self.__ack_handlers.has_key(frame.get_task_id()):
            return AppFrame.high_priority
        else:
            return AppFrame.medium_priority

    def work(self, frame, total_ready_frames):
        """
        Method:    work
        Description: ִ��һ������
        Parameter: 
            frame: AppFrame
            total_ready_frames: �ܹ��ȴ�ִ�е�����
        Return: 
        Others: 
        """

        if frame.is_ack_frame():
            handler = self.__get_duty_ack_handler(frame)
            if handler is not None and not handler.is_over():                
                 handler.handle_ack(frame)
            
        else:
            handler = self.__dispatch_handler_strategy.get_duty_cmd_handler(frame)
            if handler:
                new_handler = handler.__class__()
                new_handler.set_worker(self)
                new_handler.handle_cmd(frame)
            else:
                tracelog.error("frame %s is not %s's duty" % (frame, self.get_name()))

    def idle(self, total_ready_to_process_frames):
        """
        Method:    idle
        Description: ����״̬�¼�������handler
        Parameter: 
            total_ready_to_process_frames: �ȴ�ִ�е�������Ŀ
        Return: 
        Others: 
        """

        self.__check_over_handles()

    def __get_duty_ack_handler(self, frame):
        """
        Method:    __get_duty_ack_handler
        Description: ��ȡӦ����Ϣ��Ӧ��handler
        Parameter: 
            frame: Ӧ����Ϣ
        Return: Ӧ����Ϣ��Ӧ��handler
        Others: 
        """


        return self.__ack_handlers.get(frame.get_task_id())


    def dispatch_child_frame(self, parent, frame):
        """
        Method:    dispatch_child_frame
        Description: �����������handler����
        Parameter: 
            parent: ��handler
            frame: ������Ϣ
        Return: 
            0: �ҵ��˶�Ӧ����handler
            ��0:û���ҵ���Ӧ����handler
        Others: 
        """

        child = self.__dispatch_handler_strategy.get_duty_cmd_handler(frame)
        if child:
            child.set_parent(parent).handle_cmd(frame)
            return 0
        else:
            return -1

class CmdCodeDispatchHandlerStrategy(object):
    """
    Class: CmdCodeDispatchHandlerStrategy
    Description: handler���Ҳ���: �������������
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 
        Parameter: ��
        Return: 
        Others: 
            __template_cmd_handlers: ���е�ģ��handler
        """

        self.__template_cmd_handlers = {}

    def register_handler(self, handler, *args):
        """
        Method:    register_handler
        Description: ע��ģ��handler
        Parameter: 
            handler: handler����
            *args: ��handler�����������
        Return: 
        Others: 
            �����������int���͵���ֵ����ʾ����������
            Ҳ����������int��ɵ�Ԫ�飬��ʾһ����Χ�ڵ�������(������)
            
            ����: 
                register_handler(handler, (100, 200))
                register_handler(handler, 100) 
                register_handler(handler, 100, 103, ...)
        """

        if len(args) == 0:
            tracelog.error("no cmd range for handler %s" % handler)
            return

        for cmd_code_range in args:
            if isinstance(cmd_code_range, int):
                self.__template_cmd_handlers[cmd_code_range] = handler

            else:
                code1, code2 = cmd_code_range
                if code1 <= code2:
                    for cmd_code in xrange(code1, code2 + 1):
                        self.__template_cmd_handlers[cmd_code] = handler
                else:
                    for cmd_code in xrange(code2, code1+ 1):
                        self.__template_cmd_handlers[cmd_code] = handler
                    
    def get_duty_cmd_handler(self, frame):
        """
        Method:    get_duty_cmd_handler
        Description: ��ȡ����ָ�������handler
        Parameter: 
            frame: ������Ϣ
        Return: 
            None: û���ҵ���ص�handler
            ��None: ����ָ�������handler
        Others:             
        """

        try:
            return self.__template_cmd_handlers[frame.get_cmd_code()]
        except:
            return None

class DutyDispatchHandlerStrategy(object):
    """
    Class: DutyDispatchHandlerStrategy
    Description: handler���Ҳ���: ����handler��is_my_duty������
    Base: object
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
            __template_cmd_handlers: ���е�ģ��handler
        """

        self.__template_cmd_handlers = []

    def register_handler(self, handler, *args):
        """
        Method:    register_handler
        Description: ע��ģ��handler
        Parameter: 
            handler: ģ��handler
            *args: δʹ��. Ϊ�˱���������������ӿڼ���.
        Return: 
        Others: 
        """

        self.__template_cmd_handlers.append(handler)

    def get_duty_cmd_handler(self, frame):
        """
        Method:    get_duty_cmd_handler
        Description: ��ȡ����ָ�������handler
        Parameter: 
            frame: ������Ϣ
        Return: 
            None: û���ҵ���ص�handler
            ��None: ����ָ�������handler
        Others:             
        """

        for handler in self.__template_cmd_handlers:
            if handler.is_my_duty(frame):
                return handler

        return None

class NoBusyStrategy(object):
    """
    Class: NoBusyStrategy
    Description: ͬһ��worker��handler���ǲ���:����������
    Base: 
    Others: 
    """

    def is_busy(self, ack_handlers, frame):
        return (False, 0)

class BusyStrategy(object):
    """
    Class: BusyStrategy
    Description: ͬһ��worker��handler���ǲ���:�жϴ��ڵȴ�Ӧ����Ϣ��handler�Ƿ�����ĳ������ͬ��ִ��
    Base: 
    Others: 
    """

    def is_busy(self, ack_handlers, frame):

        if len(ack_handlers) == 0 or ack_handlers.has_key(frame.get_task_id()):
            return (False, 0)

        for handler in ack_handlers.itervalues():
            if handler and not handler.is_over() and handler.is_busy(frame):
                return (True, 0)

        return (False, 0)


