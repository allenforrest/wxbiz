#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-24
Description: 本文件中实现了工作者线程基类
Others:      
Key Class&Method List: 
             1. WatchedThread: 可以被app监控的线程
             2. WorkThread: 工作者线程的基类
             3. CommunicationThread: 在WorkThread类的基础上实现了发送接收消息的线程
History: 
1. Date:
   Author:
   Modification:
"""


from __future__ import with_statement

from collections import deque
from Queue import Empty
from threading import Thread
from threading import Event
from threading import RLock
import time
import multiprocessing

from _bundleframework.protocol.appframe import AppFrame
from _bundleframework.protocol.appframe import AppEvent

import tracelog
import err_code_mgr

class WatchedThread(Thread):
    """
    Class: WatchedThread
    Description: 可以被app监控的线程
    Base: threading.Thread
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
            这里将daemon设置为True，使得子线程可以跟随主线程一起退出
        """

        Thread.__init__(self)
        
        self.daemon = True # 跟随主线程一起退出
                
        self.__base_thread_mutex = RLock()
        self.__busy_ticks = 0
        self.__over = False
        self.__stopped = False

    def feed_dog(self):
        """
        Method:    feed_dog
        Description: 喂软件狗
        Parameter: 无
        Return: 
        Others: 在线程的运行过程中，需要及时喂狗，
                如果狗被饿死，则认为出现了异常情况，会重启进程
        """

        with self.__base_thread_mutex:
            self.__busy_ticks = 0
            return self.__stopped

    def is_over(self):
        """
        Method:    is_over
        Description: 判断当前线程是否已经结束
        Parameter: 无
        Return: 当前线程是否已经结束
        Others: 
        """

        with self.__base_thread_mutex:
            return self.__over

    def over(self):
        """
        Method:    over
        Description: 设置进程为结束状态
        Parameter: 无
        Return: 
        Others: 
        """

        with self.__base_thread_mutex:
            self.__over = True

    def is_stopped(self):
        """
        Method:    is_stopped
        Description: 判断当前线程是否已经被设置为停止
        Parameter: 无
        Return: 当前线程是否已经被设置为停止
        Others: 
        """

        with self.__base_thread_mutex:
            return self.__stopped

    def start_me(self):
        """
        Method:    start_me
        Description: 启动线程
        Parameter: 无
        Return: 
        Others: 
        """

        if self._pre_start() != 0:
            return

        self.start()

        self._post_start()

    def _pre_start(self):
        """
        Method:    _pre_start
        Description: 在线程启动前的预处理
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        return 0

    def _post_start(self):
        """
        Method:    _post_start
        Description: 线程启动后的后处理
        Parameter: 无
        Return: 
        Others: 
        """

        pass

    def stop(self):
        """
        Method:    stop
        Description: 停止线程的运行
        Parameter: 无
        Return: 
        Others: 
        """

        if self._pre_stop() == 0:
            with self.__base_thread_mutex:
                self.__stopped = True

        self._post_stop()

    def _pre_stop(self):
        """
        Method:    _pre_stop
        Description: 线程停止前的预处理
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        return 0

    def _post_stop(self):
        """
        Method:    _post_stop
        Description: 线程停止后的后处理
        Parameter: 无
        Return: 
        Others: 
        """

        pass



    def get_max_busy_ticks_ts(self):
        """
        Method:    get_max_busy_ticks_ts
        Description: 获取最大的繁忙周期
        Parameter: 无
        Return: 最大的繁忙周期
        Others: 
        """

        return 7200    # 1秒 * 7200

    def overflow_max_busy_ticks(self):
        """
        Method:    overflow_max_busy_ticks
        Description: 周期检查，判断是否超过了最大繁忙周期
        Parameter: 无
        Return: 是否超过了最大繁忙周期
        Others: 
        """

        with self.__base_thread_mutex:
            self.__busy_ticks += 1
            if self.__busy_ticks <= self.get_max_busy_ticks_ts():
                return False

            self._log_after_overflow_max_busy_ticsk()
            return True;

    def _log_after_overflow_max_busy_ticsk(self):
        """
        Method:    _log_after_overflow_max_busy_ticsk
        Description: 当超过最大繁忙周期后，记录日志
        Parameter: 无
        Return: 
        Others: 
        """

        tracelog.error("thread %s over %d ticks" % (self.get_name(), self.get_max_busy_ticks_ts()))

    def get_name(self):
        """
        Method:    get_name
        Description: 获取线程的名称
        Parameter: 无
        Return: 线程的名称
        Others: 
        """

        return "watched_thread_" + str(self)

    @classmethod
    def sleep(cls, seconds):
        """
        Method:    sleep
        Description: 使得调用本函数的线程休眠一定的时间
        Parameter: 
            seconds: 休眠的时间长度(秒)
        Return: 
        Others: 
        """

        time.sleep(seconds)


class WorkThread(WatchedThread):
    """
    Class: WorkThread
    Description: 工作者线程的基类
    Base: WatchedThread
    Others: 
    """

    doing_none              = 0
    doing_ready_for_work    = 1
    doing_work              = 2
    doing_time_out          = 3
    doing_on_event          = 4
    doing_idle              = 5
    doing_exit_work         = 6

    def __init__(self, wrkr = None):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            wrkr: 默认绑定的worker
        Return: 
        Others: 
        """

        WatchedThread.__init__(self)

        # 绑定在当前线程上所有的worker
        self.__workers = []
        if wrkr is not None:
            self.__workers.append(wrkr)

        # 信号量，用来检查是否有消息等待执行
        # 不使用threading.Event,因为它内部使用了sleep，实时性差，新消息会延长几十毫秒才能被调度        
        self._has_work_to_do_sema = multiprocessing.Event()
        self._has_work_to_do_sema.clear()

        # 所有优先级队列的初始的权重
        # weight值越大，优先级就会越低
        self.__weight = [8, 4, 1, 0]

        # 所有优先级队列的权重
        self.__weight_of_priority = [8, 4, 1, 0]

        # 所有的优先级
        self.__priorities = [AppFrame.event_priority, AppFrame.high_priority, AppFrame.medium_priority, AppFrame.low_priority]

        # 命令请求消息队列
        self.__frame_buffer = {}
        self.__frame_buffer[AppFrame.low_priority]    = deque()
        self.__frame_buffer[AppFrame.medium_priority] = deque()
        self.__frame_buffer[AppFrame.high_priority]   = deque()
        self.__frame_buffer[AppFrame.event_priority]  = deque()

        # 应答消息队列
        # 将应答消息与命令消息区分开，可以保证应答消息被及时处理，不至于被阻塞在队列中
        self.__ack_frame_buffer = deque()

        # 所有等待处理的消息的总数
        self._total_ready_to_process_frames = 0

        # 每个优先级队列被丢弃的消息的数目
        self.__total_frames_discarded = [0, 0, 0, 0]

        # 每个优先级队列最大的消息数目
        self.__max_frames_in_buffer = [0, 0, 0, 0]        
        for i in xrange(AppFrame.low_priority, AppFrame.event_priority + 1):
            self.__max_frames_in_buffer[i] = self.get_frame_queue_max_size(i)

        # 空闲处理函数没有被调用的次数
        self.__idle_not_run_times = 0

        # 标识当前线程正在执行什么动作
        # 以便当线程的软件狗触发后可以定位分析问题
        self.__doing_what = WorkThread.doing_none

        # 当前正在处理的消息
        self.__doing_what_frame = None

    def get_name(self):
        """
        Method:    get_name
        Description: 获取线程的名称
        Parameter: 无
        Return: 线程的名称
        Others: 
        """

        return "work_thread_" + str(self)

    def get_workers(self):
        """
        Method:    get_workers
        Description: 获取所有的worker
        Parameter: 无
        Return: worker列表
        Others: 
        """

        return self.__workers

    def get_worker(self, worker_name):
        """
        Method:    get_worker
        Description: 获取指定名字的worker
        Parameter: 
            worker_name: worker的名字
        Return: 
            None: 没有找到指定的worker
            非None: 指定名字的worker
        Others: 
        """

        for worker in self.__workers:
            if worker.get_name() == worker_name:
                return worker

        return None
            
    def append_worker(self, wrkr):
        """
        Method:    append_worker
        Description: 增加绑定到当前线程的worker
        Parameter: 
            wrkr: worker
        Return: 
        Others: 
        """

        self.__workers.append(wrkr)
    
    def remove_worker(self, wrkr):
        """
        Method:    append_worker
        Description: 取消worker与当前线程的绑定关系
        Parameter: 
            wrkr: worker
        Return: 
        Others: 
        """

        self.__workers.remove(wrkr)
        
    def run(self):
        """
        Method:    run
        Description: 线程的主函数
        Parameter: 无
        Return: 
        Others: 
        """


        
        if len(self.__workers) == 0:
            self.over()
            return
        
        if self._ready_for_work() != 0:
            self.over()
            return




        # worker中，由于time_out_handler是动态加入的，所以不能在这里先判断是否有
        #has_time_out_workerLst = [ w for w in self.__workers if w.has_time_out_handler()]
        #if len(has_time_out_workerLst)>0 :
        #    has_time_out_handler = True
        #else:
        #    has_time_out_handler = False


        try:
            current_seconds = 0
            last_seconds = 0

            while True:
                #if has_time_out_handler:
                elapsed_seconds = time.time()
                
                self._work()

                #if has_time_out_handler:
                elapsed_seconds = time.time() - elapsed_seconds;
                current_seconds += elapsed_seconds;

                if current_seconds < last_seconds:
                    last_seconds = current_seconds

                if current_seconds - last_seconds > 1:
                    self.__doing_what = WorkThread.doing_time_out

                    for wrkr in self.__workers:
                        try:
                            wrkr.time_out(current_seconds)
                        except:
                            tracelog.exception("worker.time_out() failed.")
                    last_seconds = current_seconds

                if self.feed_dog():
                    break

            for i in xrange(AppFrame.low_priority, AppFrame.event_priority):
                if self.__total_frames_discarded[i] > 0:
                    tracelog.info("%s discards %d frames on priority %d" % (self.get_name(), self.__total_frames_discarded[i], i))

            self.__doing_what = WorkThread.doing_exit_work

            for worker in self.__workers:
                worker.exit_work()
                tracelog.info("%s is over normally." %worker.get_name())

            msg = ",".join(["[%d]%d" % (i, len(frame_buffer)) for i, frame_buffer in self.__frame_buffer.iteritems()])

            tracelog.info("%s go to stop, total_ready_to_process_frames:%d, frame_buffer:%s" % (
                      self.get_name()
                    , self._total_ready_to_process_frames
                    , msg))
        except:
            tracelog.exception("WorkThread.run() failed.")
            
        self.over()

    def get_frame_queue_max_size(self, priority):
        """
        Method:    get_frame_queue_max_size
        Description: 获取指定优先级的frame队列的最大长度
        Parameter: 
            priority: 队列的优先级
        Return: 指定优先级的frame队列的最大长度
        Others: 当存放AppFrame的队列达到最大后，将会丢弃最早的消息
        """
        return 50000
        
        
    def push_frame(self, frame):
        """
        Method:    push_frame
        Description: 将消息加入到缓存队列中
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        
        if frame.is_ack_frame():
            self.__ack_frame_buffer.append(frame)
            self._total_ready_to_process_frames += 1
        else:
            priority = frame.get_priority()
            queue = self.__frame_buffer.get(priority)
        
            if queue is not None:

                # 判断是否超过了队列的最大长度
                max_num = self.__max_frames_in_buffer[priority]
                if len(queue) >= max_num:
                    queue.popleft()
                    queue.append(frame)
                    self.__total_frames_discarded[priority] += 1                      
                    
                else:
                    queue.append(frame)
                    self._total_ready_to_process_frames += 1

        self._has_work_to_do_sema.set()
    
        
    def _pop_frame(self, wait_seconds):
        """
        Method:    _pop_frame
        Description: 从消息缓队列中取出一条消息
        Parameter: 
            wait_seconds: 当队列中没有消息时，等待新消息的时间
        Return: 消息，消息的优先级
        Others: 
        """

      
        if self._has_work_to_do_sema.wait(wait_seconds) is not True:
            return (None, AppFrame.invalid_priority)

        
        self._has_work_to_do_sema.clear() 

        # 先处理应答消息，否则容易导致handler超时
        if len(self.__ack_frame_buffer) > 0:
            self._total_ready_to_process_frames -= 1
            self._has_work_to_do_sema.set()
            return (self.__ack_frame_buffer.popleft(), AppFrame.high_priority)
            
        
        for priority in self.__priorities:
            if len(self.__frame_buffer[priority]) > 0:
                self._total_ready_to_process_frames -= 1

                # 使得下次仍然可以取到后续的消息
                self._has_work_to_do_sema.set()
                return (self.__frame_buffer[priority].popleft(), priority)

        return (None, AppFrame.invalid_priority)


    def get_max_busy_ticks_ts(self):
        """
        Method:    get_max_busy_ticks_ts
        Description: 获取当前线程的最大的繁忙周期
        Parameter: 无
        Return: 当前线程的最大的繁忙周期
        Others: 如果线程在此周期内，线程没有喂狗，则认为出现了异常
        """

        if len(self.__workers) > 0:
            return max([i.get_max_busy_ticks_ts() for i in self.__workers])
        else:
            return 600

    def _log_after_overflow_max_busy_ticsk(self):
        """
        Method:    _log_after_overflow_max_busy_ticsk
        Description: 当超过最大繁忙周期后，记录日志
        Parameter: 无
        Return: 
        Others: 
        """

        doing_what = ["none", "ready_for_work", "work", "time_out", "on_event", "idle", "exit_work"]
        tracelog.error("thread %s over %d ticks when doing %s" % (self.get_name(), self.get_max_busy_ticks_ts(), doing_what[self.__doing_what]))
        if self.__doing_what_frame:
            tracelog.error("self.__doing_what_frame: %s" % self.__doing_what_frame)

    def _pre_start(self):
        """
        Method:    _pre_start
        Description: 在线程启动前的预处理
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        if len(self.__workers) > 0:
            return 0
        else:
            self.over()
            return -1

    def _post_stop(self):
        """
        Method:    _post_stop
        Description: 线程停止后的后处理
        Parameter: 无
        Return: 
        Others: 
        """

        self._has_work_to_do_sema.set()

    def _idle(self):
        """
        Method:    _idle
        Description: 空闲处理函数
        Parameter: 无
        Return: 
        Others: 
        """

        for wrkr in self.__workers:
            wrkr.idle(self._total_ready_to_process_frames)

    def _ready_for_work(self):
        """
        Method:    _ready_for_work
        Description: 线程工作前的初始化函数
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        self.__doing_what = WorkThread.doing_ready_for_work
        
        for wrkr in self.__workers:
            try:
                ret = wrkr.ready_for_work()
            except:
                tracelog.exception("worker %s ready_for_work failed." % wrkr.get_name())
                return -1
                
                
            if ret == 0:
                tracelog.info("%s is ready for work." % wrkr.get_name())
            else:
                tracelog.error("%s is not ready." % wrkr.get_name())
                return ret
                
        return 0
        
    def __adjust_priority(self, priority, weight):
        """
        Method:    __adjust_priority
        Description: 调整队列的优先级
        Parameter: 
            priority: 被调整的队列的优先级
            weight: 权重
        Return: 
        Others: 
        """

        if weight == 0:
            return

        self.__weight_of_priority[priority] += weight

        adjust = False
        for i in xrange(AppFrame.low_priority, AppFrame.event_priority):
            if self.__priorities[i] == priority:
                adjust = True

            if adjust:
                if self.__weight_of_priority[self.__priorities[i]] > self.__weight_of_priority[self.__priorities[i + 1]]:
                    t = self.__priorities[i]
                    self.__priorities[i] = self.__priorities[i + 1]
                    self.__priorities[i + 1] = t
                else:
                    return

    def _when_worker_is_busy(self, priority, frame, busy_reason):
        """
        Method:    _when_worker_is_busy
        Description: 当worker处于忙状态时的处理
        Parameter: 
            priority: 消息的优先级
            frame: AppFrame
            busy_reason: 忙的原因。如果原因不为0，则丢弃该消息
        Return: 
        Others: 
        """

        if busy_reason == 0:
            self.__frame_buffer[priority].appendleft(frame)
            self._total_ready_to_process_frames += 1

    def _work(self):
        """
        Method:    _work
        Description: 处理一次任务
        Parameter: 无
        Return: 
        Others: 
        """


        try:
            if not self._handle_frames(0.8) or self.__idle_not_run_times > 10:
                self.__idle_not_run_times = 0

                self.__doing_what = WorkThread.doing_idle

                self._idle()
            else:
                self.__idle_not_run_times += 1
        except:
            tracelog.exception("WorkThread._work failed.")
            
            
    def _handle_frames(self, wait_seconds):
        """
        Method:    _handle_frames
        Description: 处理消息
        Parameter: 
            wait_seconds: 等待新消息的时间(秒)
        Return: 
        Others: 
        """


        frame, priority = self._pop_frame(wait_seconds)

        if frame is None:
            return False

        self._handle_one_frame(frame, priority)
      
        return True


    def _handle_one_frame(self, frame, priority):
        """
        Method:    _handle_one_frame
        Description: 处理一条消息
        Parameter: 
            frame: AppFrame
            priority: 消息的优先级
        Return: 是否处理了消息
        Others: 
        """

        
        self.__doing_what_frame = frame

        if frame is None:
            return False


        do_something = True
        
        for wrkr in self.__workers:
            handler = wrkr.is_my_duty(frame)
            if handler is None:
                continue

            if frame.is_ack_frame():
                self.__doing_what = WorkThread.doing_work                        
                wrkr.work(frame, self._total_ready_to_process_frames)
            else:
                if AppFrame.event_priority != priority:
                    (busy, busy_reason) = wrkr.is_busy(frame)
                    if busy:
                        self._when_worker_is_busy(priority, frame, busy_reason)

                        do_something = False

                        self.__adjust_priority(priority, self.__weight[AppFrame.low_priority])
                    else:
                        self.__doing_what = WorkThread.doing_work
                        
                        wrkr.work(frame, self._total_ready_to_process_frames)

                        self.__adjust_priority(priority, self.__weight[priority])
                else:
                    e = AppEvent.from_frame(frame)
                    if e is not None:
                        self.__doing_what = WorkThread.doing_on_event
                        if wrkr.on_event(e) != 0:
                            tracelog.error("WorkThread %s can't process event.\r\n%s" %(self.get_name(), e))
                    else:
                        tracelog.error("WorkThread %s can't process event.\r\n%s"%(self.get_name(), frame))

            break

        return do_something

class CommunicationThread(WorkThread):
    """
    Class: CommunicationThread
    Description: 在WorkThread类的基础上实现了发送接收消息的线程
    Base: 
    Others: 
    """

    def __init__(self, wrkr):
        WorkThread.__init__(self, wrkr)

    def run(self):
        if self._ready_for_work() == 0:
            wrkr = self.get_workers()[0]
            if wrkr:
                while True:
                    wrkr.idle(0)
                    if self.feed_dog():
                        break
        self.over()


#class DispatchThread(WorkThread):
#    pass
    
