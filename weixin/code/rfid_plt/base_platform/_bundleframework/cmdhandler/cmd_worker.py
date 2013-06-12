#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-19
Description: 本文件中实现了处理命令执行的worker
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
    Description: 命令执行的worker
    Base: Worker
    Others: 
    """

    invalid_task_id = 0

    def __init__(self, name, min_task_id, max_task_id):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            name: worker的名称
            min_task_id: 
            max_task_id: 
        Return: 
        Others: 
             一个app中的worker名称不能冲突
             每个app中的所有worker，都需要有自己的taskid的区段，且不能互相重合
             min_task_id不能小于 1
             max_task_id不能大于0xFFFFFFFE
             taskid是 unsigned int类型

             注: RpcWorker已经固定使用0xFFFF0000~0xFFFFFFFE
                所以其他worker只能使用1~0xFFFEFFFF
                
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
        Description: 设置handler查找的策略
        Parameter: 
            strategy: handler查找的策略
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
        Description: 设置handler并发的策略
        Parameter: 
            strategy: handler并发的策略
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
        Description: 注册handler
        Parameter: 
            handler: handler对象
            *args: 传递给handler查找的策略对象的参数
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
        Description: 将handler注册为等待应答消息的状态
        Parameter: 
            handler: handler对象
        Return: 任务号
        Others: 
        """

        return self.register_ack_handler_again(handler, CmdWorker.invalid_task_id)

    def register_ack_handler_again(self, handler, task_id):
        """
        Method:    register_ack_handler_again
        Description: 重新将handler注册为等待应答消息的状态
        Parameter: 
            handler: handler对象
            task_id: 任务号
        Return: 任务号
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
        Description: 检查handler是否已经结束，如果已经结束，则删除之
        Parameter: 无
        Return: 
        Others: 
        """

        for task_id, handler in self.__ack_handlers.items(): # 注:不能使用iteritems
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
        Description: 分配一个新的任务号
        Parameter: 无
        Return: 任务号
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
        Description: 判断给定的命令，是否属于当前worker处理
        Parameter: 
            frame: 命令，appframe对象
        Return: 给定的命令，是否属于当前worker处理
        Others: 
        """

        if frame.is_ack_frame() and self.__ack_handlers.has_key(frame.get_task_id()):
            return True
        else:
            return self.__dispatch_handler_strategy.get_duty_cmd_handler(frame)

    def is_busy(self, frame):
        """
        Method:    is_busy
        Description: 判断给定命令，是否与正在等待应答消息的handler不能同时执行
        Parameter: 
            frame: 命令，appframe对象
        Return: 
        Others: 
        """

        return self.__busy_strategy.is_busy(self.__ack_handlers, frame)

    def priority(self, frame):
        """
        Method:    priority
        Description: 获取指定消息的优先级
        Parameter: 
            frame: AppFrame
        Return: 优先级
        Others: 
        """

        if self.__ack_handlers.has_key(frame.get_task_id()):
            return AppFrame.high_priority
        else:
            return AppFrame.medium_priority

    def work(self, frame, total_ready_frames):
        """
        Method:    work
        Description: 执行一个命令
        Parameter: 
            frame: AppFrame
            total_ready_frames: 总共等待执行的命令
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
        Description: 空闲状态下检查结束的handler
        Parameter: 
            total_ready_to_process_frames: 等待执行的命令数目
        Return: 
        Others: 
        """

        self.__check_over_handles()

    def __get_duty_ack_handler(self, frame):
        """
        Method:    __get_duty_ack_handler
        Description: 获取应答消息对应的handler
        Parameter: 
            frame: 应答消息
        Return: 应答消息对应的handler
        Others: 
        """


        return self.__ack_handlers.get(frame.get_task_id())


    def dispatch_child_frame(self, parent, frame):
        """
        Method:    dispatch_child_frame
        Description: 发送命令给子handler处理
        Parameter: 
            parent: 父handler
            frame: 命令消息
        Return: 
            0: 找到了对应的子handler
            非0:没有找到对应的子handler
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
    Description: handler查找策略: 根据命令码查找
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 
        Parameter: 无
        Return: 
        Others: 
            __template_cmd_handlers: 所有的模板handler
        """

        self.__template_cmd_handlers = {}

    def register_handler(self, handler, *args):
        """
        Method:    register_handler
        Description: 注册模板handler
        Parameter: 
            handler: handler对象
            *args: 该handler处理的命令码
        Return: 
        Others: 
            命令码可以是int类型的数值，表示单个命令码
            也可以是两个int组成的元组，表示一个范围内的命令码(闭区间)
            
            例如: 
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
        Description: 获取处理指定命令的handler
        Parameter: 
            frame: 命令消息
        Return: 
            None: 没有找到相关的handler
            非None: 处理指定命令的handler
        Others:             
        """

        try:
            return self.__template_cmd_handlers[frame.get_cmd_code()]
        except:
            return None

class DutyDispatchHandlerStrategy(object):
    """
    Class: DutyDispatchHandlerStrategy
    Description: handler查找策略: 根据handler的is_my_duty来查找
    Base: object
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
            __template_cmd_handlers: 所有的模板handler
        """

        self.__template_cmd_handlers = []

    def register_handler(self, handler, *args):
        """
        Method:    register_handler
        Description: 注册模板handler
        Parameter: 
            handler: 模板handler
            *args: 未使用. 为了保持与其他策略类接口兼容.
        Return: 
        Others: 
        """

        self.__template_cmd_handlers.append(handler)

    def get_duty_cmd_handler(self, frame):
        """
        Method:    get_duty_cmd_handler
        Description: 获取处理指定命令的handler
        Parameter: 
            frame: 命令消息
        Return: 
            None: 没有找到相关的handler
            非None: 处理指定命令的handler
        Others:             
        """

        for handler in self.__template_cmd_handlers:
            if handler.is_my_duty(frame):
                return handler

        return None

class NoBusyStrategy(object):
    """
    Class: NoBusyStrategy
    Description: 同一个worker中handler并非策略:无条件并发
    Base: 
    Others: 
    """

    def is_busy(self, ack_handlers, frame):
        return (False, 0)

class BusyStrategy(object):
    """
    Class: BusyStrategy
    Description: 同一个worker中handler并非策略:判断处于等待应答消息的handler是否允许某个命令同步执行
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


