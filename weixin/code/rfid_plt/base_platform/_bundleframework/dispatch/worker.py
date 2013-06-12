#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-12
Description: 本文件中实现了Worker类，是其他各种派生worker的基类
Others:      
Key Class&Method List: 
             1. Worker: 工作者类，是其他各种派生worker的基类
History: 
1. Date:
   Author:
   Modification:
"""


from copy import copy
import threading

from _bundleframework.protocol.appframe import AppFrame
from _bundleframework.local_const_def import FIRSTLOCAL_PID

class Worker(object):
    """
    Class: Worker
    Description: 工作者类，是其他各种派生worker的基类
    Base: object
    Others: 
    """

    def __init__(self, name):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            name: worker的名字
        Return: 
        Others: 
            __name: worker的名字
            __app: app对象
            __time_out_handlers: 所有定时handler(等待超时的handler)
        """

        self.__name = name
        self.__app  = None
        self.__time_out_handlers = []


    def set_app(self, app):
        """
        Method:    set_app
        Description: 设置app对象
        Parameter: 
            app: app对象
        Return: 
        Others: 
        """

        self.__app = app

    def get_app(self):
        """
        Method:    get_app
        Description: 获取app对象
        Parameter: 无
        Return: app对象 
        Others: 
        """

        return self.__app

    def is_my_duty(self, frame):
        """
        Method:    is_my_duty
        Description: 判断是否是当前worker需要处理的命令
        Parameter: 
            frame: 命令消息
        Return: 是否是当前worker需要处理的命令
        Others: 
        """

        return False

    #def is_my_duty_ts(self, frame):
    #    return -1

    def get_name(self):
        """
        Method:    get_name
        Description: 获取worker的名字
        Parameter: 无
        Return: worker的名字
        Others: 
        """

        return self.__name


    def get_my_pid(self):
        """
        Method:    get_my_pid
        Description: 获取app的pid
        Parameter: 无
        Return: app的pid
        Others: 
        """

        if self.__app:
            return self.__app.get_my_pid()
        else:
            return -1

    def get_pid(self, name, strategy=FIRSTLOCAL_PID):
        """
        Method:    get_pid
        Description: 获取指定名称的app的pid
        Parameter: 
            name: app的名称
            strategy:选择策略
        Return: app的pid
        Others: 
        """

        if self.__app:
            return self.__app.get_pid(name, strategy)
        else:
            return -1

    def get_peer_pid(self, name):
        """
        Method:    get_peer_pid
        Description: 主备双机情况下，获取对端系统上指定名称的app的pid
        Parameter: 
            name: 对端系统上app的名称
        Return: 对端系统上指定名称的app的pid
        Others: 
        """

        if self.__app:
            pass #return self.__app.get_pid(name, True)
            1/0
        else:
            return -1

    def has_time_out_handler(self):
        """
        Method:    has_time_out_handler
        Description: 判断是否存在等待超时的handler
        Parameter: 无
        Return: 是否存在等待超时的handler
        Others: 
        """

        return len(self.__time_out_handlers) > 0

    def time_out(self, ticks):
        """
        Method:    time_out
        Description: 检查定时器的处理
        Parameter: 
            ticks: 当前时间
        Return: 
        Others: 
        """

        time_out_handlers = copy(self.__time_out_handlers)
        for time_out_hander in time_out_handlers:
            if time_out_hander.is_time(ticks):
                time_out_hander.time_out()

    def register_time_out_handler(self, handler):
        """
        Method:    register_time_out_handler
        Description: 注册定时handler
        Parameter: 
            handler: 需要注册为定时器的handler
        Return: 
        Others: 
        """

        if not (handler in self.__time_out_handlers):
            self.__time_out_handlers.append(handler)
            handler.set_worker(self)

    def unregister_time_out_handler(self, handler):
        """
        Method:    unregister_time_out_handler
        Description: 注销定时handler
        Parameter: 
            handler: 定时handler
        Return: 
        Others: 
        """

        try:
            self.__time_out_handlers.remove(handler)
        except:
            pass

    def idle(self, total_ready_frames):
        """
        Method:    idle
        Description: 空闲处理函数
        Parameter: 
            total_ready_frames: 所有等待处理消息的个数
        Return: 
        Others: 
        """

        pass

    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker初始化函数
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
            如果从Worker或CmdWorker继承的子类中，需要在worker运行前做些初始化动作
            那么就在ready_for_work中完成，例如，注册handler等
            注意，ready_for_work返回0表示执行成功，否认为失败。在ready_for_work
            失败的情况下，进程会退出(进程退出后，monitor会自动重启该进程)
        """

        return 0

    def get_max_busy_ticks_ts(self):
        """
        Method:    get_max_busy_ticks_ts
        Description: 获取最大的繁忙时间周期
        Parameter: 无
        Return: 最大的繁忙时间周期
        Others: 
            如果worker在此周期内，线程没有喂狗，则认为worker出现了异常
        """

        return 600

    def get_max_wait_ticks_ts(self):
        """
        Method:    get_max_wait_ticks_ts
        Description: 获取每次等待新的消息的时间
        Parameter: 无
        Return: 每次等待新的消息的时间
        Others: 
        """

        return 0.8


    def is_busy(self, frame):
        """
        Method:    is_busy
        Description: 判断执行的消息是否与当前正在执行的命令互斥
        Parameter: 
            frame: AppFrame
        Return: 执行的消息是否与当前正在执行的命令互斥
        Others: 
        """

        return (False, 0)

    def priority(self, frame):
        """
        Method:    priority
        Description: 获取指定消息的优先级
        Parameter: 
            frame: AppFrame
        Return: 消息的优先级
        Others: 
        """

        return AppFrame.medium_priority

    def work(self, frame, total_ready_frames):
        """
        Method:    work
        Description: 处理一条消息
        Parameter: 
            frame: AppFrame
            total_ready_frames: 所有待处理的消息总数
        Return: 
        Others: 
        """

        pass

    def on_event(self, e):
        """
        Method:    on_event
        Description: 处理事件消息
        Parameter: 
            e: 事件消息
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        return 0

    def exit_work(self):
        """
        Method:    exit_work
        Description: worker退出前的处理函数
        Parameter: 无
        Return: 
        Others: 
        """

        pass

    def dispatch_frame_to_process(self, process_name, frame):
        """
        Method:    dispatch_frame_to_process
        Description: 发送消息到指定名称的进程
        Parameter: 
            process_name: 接收消息的进程的名称
            frame: AppFrame
        Return: 
        Others: 
        """

        if self.__app:
            self.__app.dispatch_frame_to_process(process_name, frame)

    def dispatch_frame_to_process_by_pid(self, pid, frame):
        """
        Method:    dispatch_frame_to_process_by_pid
        Description: 发送消息到指定pid的进程
        Parameter: 
            pid: 接收消息的进程的pid
            frame: 
        Return: 
        Others: 
        """

        if self.__app:
            self.__app.dispatch_frame_to_process_by_pid(pid, frame)

    def dispatch_frame_to_worker(self, worker_name, frame):
        """
        Method:    dispatch_frame_to_worker
        Description: 发送消息到指定的worker
        Parameter: 
            worker_name: 接收消息的worker
            frame: AppFrame
        Return: 
        Others: 
        """

        if self.__app:
            self.__app.dispatch_frame_to_worker(worker_name, frame)

    def dispatch_frame_to_all_workers(self, frame):
        """
        Method:    dispatch_frame_to_all_workers
        Description: 发送消息到本进程内的所有worker
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """

        if self.__app:
            self.__app.dispatch_frame_to_all_workers(frame)

    def dispatch_frame_to_any_other_processes(self, frame):
        """
        Method:    dispatch_frame_to_any_other_processes
        Description:发送消息到所有的其他进程 
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """

        if self.__app:
            self.__app.dispatch_frame_to_any_other_processes(frame)

    def send_ack(self, frame, datas):
        """
        Method:    send_ack
        Description:发送应答消息
        Parameter: 
            frame: AppFrame实例，对应的请求消息
            datas: 应答消息体，字符串或二进制数据，可以是一个字符串或二进制数据的列表
        Return: 
        Others: 
        """
        if self.__app:
            self.__app.send_ack(frame, datas)
        
    #def dispatch_frame_to_callacp(self, frame):
    #    """
    #    Method:    dispatch_frame_to_callacp
    #    Description:发送消息到callacp的客户端
    #    Parameter: 
    #        frame: AppFrame
    #    Return: 
    #    Others: 
    #    """
    #    if self.__app:
    #        self.__app.dispatch_frame_to_callacp(frame)


