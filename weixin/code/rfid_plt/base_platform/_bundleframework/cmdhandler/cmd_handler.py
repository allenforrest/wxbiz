#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-11
Description: 本文件中，实现了CmdHandler
Others:      
Key Class&Method List: 
             1. CmdRound: 命令执行时交互的round
             2. TimeOutHandler: 定时handler
             3. CmdHandler: 命令处理的handler
History: 
1. Date:
   Author:
   Modification:
"""


import time, datetime

import tracelog
import err_code_mgr

from cmd_worker import CmdWorker

from _bundleframework.protocol.appframe import AppFrame

class CmdRound():
    """
    Class: CmdRound
    Description: 命令执行时交互的round
    Base: 
    Others: 
    """

    def __init__(self, request_frame):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            request_frame: 请求消息
        Return: 
            __request_frame: 请求消息
            __response_frames: 应答消息列表
            __over: 是否已经结束
            __result: 错误码
            __send_yet: 请求消息是否已经发送
            __data: 自定义的数据
        Others: 
        """

        self.__request_frame   = request_frame
        self.__response_frames = []

        self.__over         = False
        self.__result       = err_code_mgr.ER_TIMEOUT
        self.__send_yet     = False

        self.__data         = None

    def get_request_frame(self):
        """
        Method:    get_request_frame
        Description: 获取请求消息
        Parameter: 无
        Return: 请求消息
        Others: 
        """

        return self.__request_frame

    def add_response_frame(self, response_frame):
        """
        Method:    add_response_frame
        Description: 增加应答消息
        Parameter: 
            response_frame: 应答消息
        Return: 
        Others: 
        """

        self.__response_frames.append(response_frame)
        if response_frame.is_last():
            # 检查多个frame时是否是完整的
            if response_frame.get_tag() == AppFrame.end:
                frame_no = 0
                for f in self.__response_frames:
                    if f.get_frame_no() != frame_no:
                        self.over(err_code_mgr.ER_RECEIVE_FRAME_FAILED)
                        return
                        
                    frame_no += 1
            self.over(err_code_mgr.ER_SUCCESS)

    def get_response_frames(self):
        """
        Method:    get_response_frames
        Description: 获取所有的应答消息
        Parameter: 无
        Return: 所有的应答消息
        Others: 
        """

        return self.__response_frames

    def get_response_frame(self):
        """
        Method:    get_response_frame
        Description: 获取第一个应答消息
        Parameter: 无
        Return: 
            None: 没有应答消息
            非None: 第一个应答消息
        Others: 
        """

        if len(self.__response_frames) > 0:
            return self.__response_frames[0]
        else:
            return None

    def set_data(self, data):
        """
        Method:    set_data
        Description: 设置自定义数据
        Parameter: 
            data: 自定义数据
        Return: 
        Others: 
        """

        self.__data = data

    def get_data(self):
        """
        Method:    get_data
        Description: 获取自定义数据
        Parameter: 无
        Return: 自定义数据
        Others: 
        """

        return self.__data

    def over(self, result):
        """
        Method:    over
        Description: 将round设置为结束状态，并且设置错误码
        Parameter: 
            result: 错误码
        Return: 
        Others: 
        """

        self.__over   = True
        self.__result = result

    def is_over(self):
        """
        Method:    is_over
        Description: 判断是否已经结束
        Parameter: 无
        Return: 是否已经结束
        Others: 
        """

        return self.__over

    def get_result(self):
        """
        Method:    get_result
        Description: 获取错误码
        Parameter: 无
        Return: 错误码
        Others: 
        """

        return self.__result

    def set_send_yet(self, s):
        """
        Method:    set_send_yet
        Description: 设置是否已经发送了请求消息
        Parameter: 
            s: Ture或者False
        Return: 
        Others: 
        """

        self.__send_yet = s

    def send_yet(self):
        """
        Method:    send_yet
        Description: 判断是否已经发送了请求消息
        Parameter: 无
        Return: 是否已经发送了请求消息
        Others: 
        """

        return self.__send_yet

    def is_wait_for_ack(self):
        """
        Method:    is_wait_for_ack
        Description: 判断是否处于等待应答消息的状态
        Parameter: 无
        Return: 是否处于等待应答消息的状态
        Others: 
        """

        return not self.__over and self.__send_yet


class TimeOutHandlerBase(object):
    """
    Class: TimeOutHandlerBase
    Description: 定时handler
    Base: object
    Others: 
        _once: 是否只触发1次超时
        _worker: handler所在的workers
    """
    
    def __init__(self):
        self._once = False
        self._worker = None
        
    def is_time(self, now_second):
        return False

    def time_out(self):
        """
        Method:    time_out
        Description: 超时时间到了以后，调用本接口处理相关的任务
        Parameter: 无
        Return: 
        Others: 本接口供子类重载
        """

        pass

        
    def stop_timer(self):
        """
        Method:    stop_timer
        Description: 停止时间间隔方式的计时器
        Parameter: 无
        Return: 
        Others: 
        """
        pass


    def set_worker(self, wrkr):
        """
        Method:    set_worker
        Description: 设置Worker对象
        Parameter: 
            wrkr: Worker对象
        Return: 
        Others: 
        """

        self._worker = wrkr

    def get_worker(self):
        """
        Method:    get_worker
        Description: 获取Worker对象
        Parameter: 无
        Return: Worker对象
        Others: 
        """

        return self._worker


        
class TimeOutHandler(TimeOutHandlerBase):
    """
    Class: TimeOutHandler
    Description: 定时handler
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
            __last_time: 上次超时的时间(秒)
            __interval_time:每次超时的周期(秒)
        """
        TimeOutHandlerBase.__init__(self)

        # 按照固定间隔计时
        self.__last_time = 0
        self.__interval_time = 0
              
        
    def is_time(self, now_second):
        """
        Method:    is_time
        Description: 判断是否到了超时时间
        Parameter: 
            ticks: 当前系统时间
        Return: 是否到了超时时间
        Others: 
        """

        if self.__interval_time == 0:
            return False

        if self.__last_time == 0:
            self.__last_time = now_second
            return False

        if now_second < self.__last_time:
            self.__last_time = now_second

        if now_second - self.__last_time >= self.__interval_time:
            if self._once:
                self.stop_timer()
            else:
                self.__last_time = now_second

            return True

        return False


    def start_timer(self, interval_time, once):
        """
        Method:    start_timer
        Description: 启动定时器，触发条件是一定的时间间隔
        Parameter: 
            ticks: 定时器的周期长度(秒)
            once: 是否只触发一次超时
        Return: 
        Others: 
        """

        self.__last_time = 0
        self.__interval_time = interval_time
        self._once = once
                

    def stop_timer(self):
        """
        Method:    stop_timer
        Description: 停止时间间隔方式的计时器
        Parameter: 无
        Return: 
        Others: 
        """

        self.__last_time = 0
        self.__interval_time = 0
        

        
class FixedTimeOutHandler(TimeOutHandlerBase):
    """
    Class: FixedTimeOutHandler
    Description: 定时handler
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
        """
        TimeOutHandlerBase.__init__(self)

        # 按照固定的时间点计时
        self.__year = None
        self.__month = None
        self.__day = None
        self.__hour = None
        self.__minute = None
        self.__second = None

        # 上次检查的时间点
        self.__last_time = None

        # 上次期望的时间点
        self.__last_expect_time = None


    def __get_time(self):
        now = datetime.datetime.now()

        expect_time = datetime.datetime(year = now.year if self.__year is None else self.__year
                                    , month = now.month if self.__month is None else self.__month
                                    , day = now.day if self.__day is None else self.__day
                                    , hour = now.hour if self.__hour is None else self.__hour
                                    , minute = now.minute if self.__minute is None else self.__minute
                                    , second = now.second if self.__second is None else self.__second
                                    )

        
        return now, expect_time
        
    def is_time(self, now_second):
        """
        Method:    is_time
        Description: 判断是否到了超时时间
        Parameter: 
            ticks: 当前系统时间
        Return: 是否到了超时时间
        Others: 
        """
        if self.__second is None:
            return False

        now, expect_time = self.__get_time()

        ret = False
        if ((self.__last_time <= expect_time <= now)
            or (self.__last_time <= self.__last_expect_time <= now)):            
            if self._once:
                self.stop_timer()

            ret = True

        self.__last_time = now
        self.__last_expect_time = expect_time
        
        
        return ret

    def start_timer(self, year, month, day, hour, minute, second, once):
        """
        Method:    start_timer_ex
        Description: 启动定时器，触发条件是固定的时间点
        Parameter: 
            
            once: 是否只触发一次超时
        Return: 
        Others: 
        """
        if  month is None and year is not None:
            month = 1
            
        if  day is None and month is not None:
            day = 1

        if  hour is None and day is not None:
            hour = 0

        if  minute is None and hour is not None:
            minute = 0

        if  second is None and minute is not None:
            second = 0
        
        self.__year = year
        self.__month = month
        self.__day = day
        self.__hour = hour
        self.__minute = minute
        self.__second = second

        self._once = once
        
        self.__last_time, self.__last_expect_time = self.__get_time()
        
        
    def stop_timer(self):
        """
        Method:    stop_timer
        Description: 停止固定时间点的计时器
        Parameter: 无
        Return: 
        Others: 
        """
        
        self.__year = None
        self.__month = None
        self.__day = None
        self.__hour = None
        self.__minute = None
        self.__second = None
            

        
class CmdHandler(TimeOutHandler):
    """
    Class: CmdHandler
    Description: 命令处理的handler 
    Base: TimeOutHandler
    Others: 
    """

    invalid_round_id = 0

    min_round_id = 1
    max_round_id = 0xfffffffe

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
            __time_of_new: 当前handler创建的时间
            __parent: 父handler
            __children: 所有的子handler
            __over: 是否已经结束
            __result: 错误码
            __task_id: 任务号
            __rounds: 所有的round
        """

        TimeOutHandler.__init__(self)
        
        self.__time_of_new = time.time()

        self.__parent = None
        self.__children = []

        self.__over     = False
        self.__result   = 0
        self.__result_args = None

        self.__task_id = CmdWorker.invalid_task_id

        self.__rounds = {}
        self.__cur_round_id = CmdHandler.min_round_id
        
        self.set_rounds_control_strategy(None)



    def set_rounds_control_strategy(self, strategy):
        """
        Method:    set_rounds_control_strategy
        Description: 设置round控制策略
        Parameter: 
            strategy: round控制策略
        Return: 
        Others: 
        """

        if strategy:
            self.__rounds_control_strategy = strategy
        else:
            self.__rounds_control_strategy = NoRoundsControlStrategy()

    def set_parent(self, parent):
        """
        Method:    set_parent
        Description: 设置父handler
        Parameter: 
            parent: 父handler
        Return: 
        Others: 
        """

        if parent:
            parent.add_child(self)

        self.__parent = parent

        return self

    def get_parent(self):
        """
        Method:    get_parent
        Description: 获取父handler
        Parameter: 无
        Return: 
        Others: 
        """

        return self.__parent

    def add_child(self, child):
        """
        Method:    add_child
        Description: 增加子handler
        Parameter: 
            child: 子handler
        Return: 
        Others: 
        """

        if child and not child in self.__children:
            self.__children.append(child)

        return self

    def get_time_of_new(self):
        """
        Method:    get_time_of_new
        Description: 获取handler创建时的时间
        Parameter: 无
        Return: handler创建时的时间
        Others: 
        """

        return self.__time_of_new

    def is_my_duty(self, frame):
        """
        Method:    is_my_duty
        Description: 判断指定的消息是否是当前handler处理
        Parameter: 
            frame: AppFrame
        Return: 指定的消息是否是当前handler处理
        Others: 
        """

        return False

    def is_busy(self, frame):
        """
        Method:    is_busy
        Description: 判断指定的消息是否与当前handler同时执行
        Parameter: 
            frame: AppFrame
        Return: 指定的消息是否与当前handler同时执行
        Others: 
        """

        return False

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """

        pass

    def get_all_rounds(self):
        """
        Method:    get_all_rounds
        Description: 获取所有的round
        Parameter: 无
        Return: 所有的round
        Others: 
        """

        return self.__rounds
        
    def _new_round(self, round):
        """
        Method:    _new_round
        Description: 新加入一个round
        Parameter: 
            round: 给定的的round
        Return: 自动分配的round的id
        Others: 
        """

        if len(self.__rounds) >= CmdHandler.max_round_id:
            return CmdHandler.invalid_round_id

        round_id = self.__cur_round_id + 1
        while self.__rounds.has_key(round_id) and round_id <= CmdHandler.max_round_id:
            round_id += 1

        if round_id > CmdHandler.max_round_id:
            while self.__rounds.has_key(round_id) and round_id <= self.__cur_round_id:
                round_id += 1

            if round_id > CmdHandler.__cur_round_id:
                return CmdHandler.invalid_round_id

        self.__cur_round_id = round_id
        self.__rounds[round_id] = round

        return round_id

    def _clear_all_round(self):
        self.__rounds.clear()
        

    def __regist_as_ack_handle(self):
        """
        Method:    __regist_as_ack_handle
        Description: 注册当前handler为ack_handle，以便接收应答消息
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        if self.__task_id == CmdWorker.invalid_task_id:
            self.__task_id = self._worker.register_ack_handler(self)
            if self.__task_id == CmdWorker.invalid_task_id:
                self.over(err_code_mgr.ER_TOO_MUCH_COMMANDS_WAITING)
                return -1

        return 0

    def wait_for_ack(self, frame, time_out):
        """
        Method:    wait_for_ack
        Description: 将给定的消息发送出去，并且等待应答
        Parameter: 
            frame: 需要发送出去的命令
            time_out: 等待应答的超时时间
        Return: 发送出去的round的个数
        Others: 
        """

        self._new_round(CmdRound(frame))
        return self.wait_for_all_rounds_ack(time_out)

    def wait_for_all_rounds_ack(self, time_out):
        """
        Method:    wait_for_all_rounds_ack
        Description: 将已有的所有的round发送出去，并且等待应答 
        Parameter: 
            time_out: 等待应答的超时时间
        Return: 发送出去的round的个数
        Others: 
        """

        if self.__regist_as_ack_handle() != 0:
            return 0

        total_rounds_send = self.send_all_rounds()

        # bug fix: 这里无论是否发送了消息都要启动定时器，
        # 否则会导致handler长时间在worker中，taskid被占用，且白白浪费空间
        #if total_rounds_send > 0:
        self.start_timer(time_out, True)

        return total_rounds_send

    def wait_for_child_ack(self, frame, time_out):
        """
        Method:    wait_for_child_ack
        Description: 将指定的frame作为子handler执行，并且等待的子handler的应答
        Parameter: 
            frame: 请求消息
            time_out: 超时时间
        Return: 发送出去的round的个数
        Others: 
        """

        self._new_round(CmdRound(frame))
        return self.wait_for_all_children_ack(time_out)

    def wait_for_all_children_ack(self, time_out):
        """
        Method:    wait_for_all_children_ack
        Description: 将已有的所有round，作为子handler执行，并且等待的子handler的应答
        Parameter: 
            time_out: 等待子handler结束的超时时间
        Return: 发送出去的round的个数
        Others: 
        """

        if self.__regist_as_ack_handle() != 0:
            return 0

        total_rounds_send = self.send_all_rounds_to_children()
        if total_rounds_send > 0:
            self.start_timer(time_out, True)

        return total_rounds_send

    def send_all_rounds(self):
        """
        Method:    send_all_rounds
        Description: 将已有的所有round发送出去
        Parameter: 无
        Return: 发送出去的round的个数
        Others: 
        """

        return self.__send_all_rounds_to(False)

    def send_all_rounds_to_children(self):
        """
        Method:    send_all_rounds_to_children
        Description: 将已有的所有的round发送给子handler
        Parameter: 无
        Return: 发送出去的round的个数
        Others: 
        """

        return self.__send_all_rounds_to(True)

    def __send_all_rounds_to(self, to_children):
        """
        Method:    __send_all_rounds_to
        Description: 将已有的所有的round发送出去
        Parameter: 
            to_children: 是否发送给子handler
        Return: 发送出去的round的个数
        Others: 
        """

        total_rounds_send = 0
        for round_id, r in self.__rounds.iteritems():
            if r is not None and self.__rounds_control_strategy.not_control(self.__rounds, round_id, r):
                frame = r.get_request_frame()
                if frame is None:
                    self.over(err_code_mgr.ER_NO_MEMORY)
                    return total_rounds_send

                if not r.send_yet():
                    frame.set_task_id(self.__task_id)
                    frame.set_round_id(round_id)

                    if to_children:
                        self._worker.dispatch_child_frame(self, frame)
                    else:
                        self._worker.dispatch_frame_to_process_by_pid(frame.get_receiver_pid(), frame)

                    r.set_send_yet(True)
                    total_rounds_send += 1

        return total_rounds_send

    def handle_ack(self, frame):
        """
        Method:    handle_ack
        Description: 处理应答消息
        Parameter: 
            frame: appframe应答消息
        Return: 
        Others: 
        """

        round_id = frame.get_round_id()
        cmd_round = self.__rounds.get(round_id)
        if cmd_round is not None:
            cmd_round.add_response_frame(frame)
            if cmd_round.is_over():
                self._on_round_over(round_id, cmd_round)

                if self.__is_all_rounds_over():
                    self._on_all_rounds_over(self.__rounds)

    def is_over(self):
        """
        Method:    is_over
        Description: 判断是否已经结束
        Parameter: 无
        Return: 是否已经结束
        Others: 
        """

        return self.__over

    def __is_all_rounds_over(self):
        """
        Method:    __is_all_rounds_over
        Description: 判断是否所有的round都已经结束
        Parameter: 无
        Return: 是否所有的round都已经结束
        Others: 
        """

        for r in self.__rounds.itervalues():
            if not r.is_over():
                return False

        return True

    def time_out(self):
        """
        Method:    time_out
        Description: 超时情况下的处理
        Parameter: 无
        Return: 
        Others: 
        """

        for round_id, round in self.__rounds.iteritems():
            if not round.is_over():
                self._on_round_timeout(round_id, round)
                
        return self.over(err_code_mgr.ER_TIMEOUT)

    
    def over(self, result, **args):
        """
        Method:    over
        Description: 将handler设置为结束状态
        Parameter: 
            result: 错误码
            args: 错误信息中需要用到的一些参数
        Return: 
        Others: 
        """

        self._worker.unregister_time_out_handler(self)

        if not self.__over:
            self.__over   = True
            self.__result = result
            self.__result_args = args

            for child in self.__children:
                child.over(result, **args)

            self._on_over(result, **args)
            if self.__parent:
                self.__parent._on_child_over(self)
        else:
            tracelog.error("handler %r is over before, "
                            "result is %d, new result is %d" % (
                            self, self.__result, result))

        return self

    def _on_child_over(self, child):
        """
        Method:    _on_child_over
        Description: 响应子handler结束的事件
        Parameter: 
            child: 子handler
        Return: 
        Others: 
        """

        pass

    def _on_round_over(self, round_id, r):
        """
        Method:    _on_round_over
        Description: 响应round结束的事件
        Parameter: 
            round_id: round的id
            r: round对象
        Return: 
        Others: 
        """

        """
        当round收到应答消息, 调用此接口
        """
        pass

    def _on_all_rounds_over(self, rounds):
        """
        Method:    _on_all_rounds_over
        Description: 响应所有round都结束了的事件
        Parameter: 
            rounds: 所有的round
        Return: 
        Others: 
        """

        self.over(0)


    def _on_round_timeout(self, round_id, r):
        """
        Method:    _on_round_timeout
        Description: 响应round超时事件
        Parameter: 
            round_id: round的id
            r: round对象
        Return: 
        Others: 
        """

        pass

    
    def _on_over(self, result, **args):
        """
        Method:    _on_over
        Description: 响应handler结束事件
        Parameter: 
            result: 错误码
            args: 错误信息中需要用到的一些参数
        Return: 
        Others: 
        """

        pass

        

class NoRoundsControlStrategy:
    """
    Class: NoRoundsControlStrategy
    Description: round控制策略-不作任何控制
    Base: 
    Others: 
    """

    def not_control(self, rounds, round_id, r):
        """
        Method:    not_control
        Description: 判断指定的round是否可以发送出去
        Parameter: 
            rounds: 所有的round
            round_id: 当前的round id
            r: round对象
        Return: 指定的round是否可以发送出去            
        Others: 对应本策略，不作任何控制
        """

        return True

class SequenceRoundsControlStrategy:
    """
    Class: SequenceRoundsControlStrategy
    Description: round控制策略-控制所有的round只能顺序执行
                当前面一个round结束后，才能执行后面一个round
    Base: 
    Others: 
    """

    def not_control(self, rounds, round_id, r):
        """
        Method:    not_control
        Description: 判断指定的round是否可以发送出去
        Parameter: 
            rounds: 所有的round
            round_id: 当前的round id
            r: round对象
        Return: 指定的round是否可以发送出去            
        Others:  
            对应本策略，需要检查是否有round处于等待应答的状态，
            如果有，则不允许当前的round发送出去
        """

        for i in rounds.itervalues:
            if i.is_wait_for_ack():
                return False

        return True



