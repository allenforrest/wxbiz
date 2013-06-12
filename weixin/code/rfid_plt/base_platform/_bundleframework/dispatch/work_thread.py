#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-24
Description: ���ļ���ʵ���˹������̻߳���
Others:      
Key Class&Method List: 
             1. WatchedThread: ���Ա�app��ص��߳�
             2. WorkThread: �������̵߳Ļ���
             3. CommunicationThread: ��WorkThread��Ļ�����ʵ���˷��ͽ�����Ϣ���߳�
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
    Description: ���Ա�app��ص��߳�
    Base: threading.Thread
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
            ���ｫdaemon����ΪTrue��ʹ�����߳̿��Ը������߳�һ���˳�
        """

        Thread.__init__(self)
        
        self.daemon = True # �������߳�һ���˳�
                
        self.__base_thread_mutex = RLock()
        self.__busy_ticks = 0
        self.__over = False
        self.__stopped = False

    def feed_dog(self):
        """
        Method:    feed_dog
        Description: ι�����
        Parameter: ��
        Return: 
        Others: ���̵߳����й����У���Ҫ��ʱι����
                �����������������Ϊ�������쳣���������������
        """

        with self.__base_thread_mutex:
            self.__busy_ticks = 0
            return self.__stopped

    def is_over(self):
        """
        Method:    is_over
        Description: �жϵ�ǰ�߳��Ƿ��Ѿ�����
        Parameter: ��
        Return: ��ǰ�߳��Ƿ��Ѿ�����
        Others: 
        """

        with self.__base_thread_mutex:
            return self.__over

    def over(self):
        """
        Method:    over
        Description: ���ý���Ϊ����״̬
        Parameter: ��
        Return: 
        Others: 
        """

        with self.__base_thread_mutex:
            self.__over = True

    def is_stopped(self):
        """
        Method:    is_stopped
        Description: �жϵ�ǰ�߳��Ƿ��Ѿ�������Ϊֹͣ
        Parameter: ��
        Return: ��ǰ�߳��Ƿ��Ѿ�������Ϊֹͣ
        Others: 
        """

        with self.__base_thread_mutex:
            return self.__stopped

    def start_me(self):
        """
        Method:    start_me
        Description: �����߳�
        Parameter: ��
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
        Description: ���߳�����ǰ��Ԥ����
        Parameter: ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
        Others: 
        """

        return 0

    def _post_start(self):
        """
        Method:    _post_start
        Description: �߳�������ĺ���
        Parameter: ��
        Return: 
        Others: 
        """

        pass

    def stop(self):
        """
        Method:    stop
        Description: ֹͣ�̵߳�����
        Parameter: ��
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
        Description: �߳�ֹͣǰ��Ԥ����
        Parameter: ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
        Others: 
        """

        return 0

    def _post_stop(self):
        """
        Method:    _post_stop
        Description: �߳�ֹͣ��ĺ���
        Parameter: ��
        Return: 
        Others: 
        """

        pass



    def get_max_busy_ticks_ts(self):
        """
        Method:    get_max_busy_ticks_ts
        Description: ��ȡ���ķ�æ����
        Parameter: ��
        Return: ���ķ�æ����
        Others: 
        """

        return 7200    # 1�� * 7200

    def overflow_max_busy_ticks(self):
        """
        Method:    overflow_max_busy_ticks
        Description: ���ڼ�飬�ж��Ƿ񳬹������æ����
        Parameter: ��
        Return: �Ƿ񳬹������æ����
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
        Description: ���������æ���ں󣬼�¼��־
        Parameter: ��
        Return: 
        Others: 
        """

        tracelog.error("thread %s over %d ticks" % (self.get_name(), self.get_max_busy_ticks_ts()))

    def get_name(self):
        """
        Method:    get_name
        Description: ��ȡ�̵߳�����
        Parameter: ��
        Return: �̵߳�����
        Others: 
        """

        return "watched_thread_" + str(self)

    @classmethod
    def sleep(cls, seconds):
        """
        Method:    sleep
        Description: ʹ�õ��ñ��������߳�����һ����ʱ��
        Parameter: 
            seconds: ���ߵ�ʱ�䳤��(��)
        Return: 
        Others: 
        """

        time.sleep(seconds)


class WorkThread(WatchedThread):
    """
    Class: WorkThread
    Description: �������̵߳Ļ���
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
        Description: ���캯��
        Parameter: 
            wrkr: Ĭ�ϰ󶨵�worker
        Return: 
        Others: 
        """

        WatchedThread.__init__(self)

        # ���ڵ�ǰ�߳������е�worker
        self.__workers = []
        if wrkr is not None:
            self.__workers.append(wrkr)

        # �ź�������������Ƿ�����Ϣ�ȴ�ִ��
        # ��ʹ��threading.Event,��Ϊ���ڲ�ʹ����sleep��ʵʱ�Բ����Ϣ���ӳ���ʮ������ܱ�����        
        self._has_work_to_do_sema = multiprocessing.Event()
        self._has_work_to_do_sema.clear()

        # �������ȼ����еĳ�ʼ��Ȩ��
        # weightֵԽ�����ȼ��ͻ�Խ��
        self.__weight = [8, 4, 1, 0]

        # �������ȼ����е�Ȩ��
        self.__weight_of_priority = [8, 4, 1, 0]

        # ���е����ȼ�
        self.__priorities = [AppFrame.event_priority, AppFrame.high_priority, AppFrame.medium_priority, AppFrame.low_priority]

        # ����������Ϣ����
        self.__frame_buffer = {}
        self.__frame_buffer[AppFrame.low_priority]    = deque()
        self.__frame_buffer[AppFrame.medium_priority] = deque()
        self.__frame_buffer[AppFrame.high_priority]   = deque()
        self.__frame_buffer[AppFrame.event_priority]  = deque()

        # Ӧ����Ϣ����
        # ��Ӧ����Ϣ��������Ϣ���ֿ������Ա�֤Ӧ����Ϣ����ʱ���������ڱ������ڶ�����
        self.__ack_frame_buffer = deque()

        # ���еȴ��������Ϣ������
        self._total_ready_to_process_frames = 0

        # ÿ�����ȼ����б���������Ϣ����Ŀ
        self.__total_frames_discarded = [0, 0, 0, 0]

        # ÿ�����ȼ�����������Ϣ��Ŀ
        self.__max_frames_in_buffer = [0, 0, 0, 0]        
        for i in xrange(AppFrame.low_priority, AppFrame.event_priority + 1):
            self.__max_frames_in_buffer[i] = self.get_frame_queue_max_size(i)

        # ���д�����û�б����õĴ���
        self.__idle_not_run_times = 0

        # ��ʶ��ǰ�߳�����ִ��ʲô����
        # �Ա㵱�̵߳��������������Զ�λ��������
        self.__doing_what = WorkThread.doing_none

        # ��ǰ���ڴ������Ϣ
        self.__doing_what_frame = None

    def get_name(self):
        """
        Method:    get_name
        Description: ��ȡ�̵߳�����
        Parameter: ��
        Return: �̵߳�����
        Others: 
        """

        return "work_thread_" + str(self)

    def get_workers(self):
        """
        Method:    get_workers
        Description: ��ȡ���е�worker
        Parameter: ��
        Return: worker�б�
        Others: 
        """

        return self.__workers

    def get_worker(self, worker_name):
        """
        Method:    get_worker
        Description: ��ȡָ�����ֵ�worker
        Parameter: 
            worker_name: worker������
        Return: 
            None: û���ҵ�ָ����worker
            ��None: ָ�����ֵ�worker
        Others: 
        """

        for worker in self.__workers:
            if worker.get_name() == worker_name:
                return worker

        return None
            
    def append_worker(self, wrkr):
        """
        Method:    append_worker
        Description: ���Ӱ󶨵���ǰ�̵߳�worker
        Parameter: 
            wrkr: worker
        Return: 
        Others: 
        """

        self.__workers.append(wrkr)
    
    def remove_worker(self, wrkr):
        """
        Method:    append_worker
        Description: ȡ��worker�뵱ǰ�̵߳İ󶨹�ϵ
        Parameter: 
            wrkr: worker
        Return: 
        Others: 
        """

        self.__workers.remove(wrkr)
        
    def run(self):
        """
        Method:    run
        Description: �̵߳�������
        Parameter: ��
        Return: 
        Others: 
        """


        
        if len(self.__workers) == 0:
            self.over()
            return
        
        if self._ready_for_work() != 0:
            self.over()
            return




        # worker�У�����time_out_handler�Ƕ�̬����ģ����Բ������������ж��Ƿ���
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
        Description: ��ȡָ�����ȼ���frame���е���󳤶�
        Parameter: 
            priority: ���е����ȼ�
        Return: ָ�����ȼ���frame���е���󳤶�
        Others: �����AppFrame�Ķ��дﵽ���󣬽��ᶪ���������Ϣ
        """
        return 50000
        
        
    def push_frame(self, frame):
        """
        Method:    push_frame
        Description: ����Ϣ���뵽���������
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

                # �ж��Ƿ񳬹��˶��е���󳤶�
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
        Description: ����Ϣ��������ȡ��һ����Ϣ
        Parameter: 
            wait_seconds: ��������û����Ϣʱ���ȴ�����Ϣ��ʱ��
        Return: ��Ϣ����Ϣ�����ȼ�
        Others: 
        """

      
        if self._has_work_to_do_sema.wait(wait_seconds) is not True:
            return (None, AppFrame.invalid_priority)

        
        self._has_work_to_do_sema.clear() 

        # �ȴ���Ӧ����Ϣ���������׵���handler��ʱ
        if len(self.__ack_frame_buffer) > 0:
            self._total_ready_to_process_frames -= 1
            self._has_work_to_do_sema.set()
            return (self.__ack_frame_buffer.popleft(), AppFrame.high_priority)
            
        
        for priority in self.__priorities:
            if len(self.__frame_buffer[priority]) > 0:
                self._total_ready_to_process_frames -= 1

                # ʹ���´���Ȼ����ȡ����������Ϣ
                self._has_work_to_do_sema.set()
                return (self.__frame_buffer[priority].popleft(), priority)

        return (None, AppFrame.invalid_priority)


    def get_max_busy_ticks_ts(self):
        """
        Method:    get_max_busy_ticks_ts
        Description: ��ȡ��ǰ�̵߳����ķ�æ����
        Parameter: ��
        Return: ��ǰ�̵߳����ķ�æ����
        Others: ����߳��ڴ������ڣ��߳�û��ι��������Ϊ�������쳣
        """

        if len(self.__workers) > 0:
            return max([i.get_max_busy_ticks_ts() for i in self.__workers])
        else:
            return 600

    def _log_after_overflow_max_busy_ticsk(self):
        """
        Method:    _log_after_overflow_max_busy_ticsk
        Description: ���������æ���ں󣬼�¼��־
        Parameter: ��
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
        Description: ���߳�����ǰ��Ԥ����
        Parameter: ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
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
        Description: �߳�ֹͣ��ĺ���
        Parameter: ��
        Return: 
        Others: 
        """

        self._has_work_to_do_sema.set()

    def _idle(self):
        """
        Method:    _idle
        Description: ���д�����
        Parameter: ��
        Return: 
        Others: 
        """

        for wrkr in self.__workers:
            wrkr.idle(self._total_ready_to_process_frames)

    def _ready_for_work(self):
        """
        Method:    _ready_for_work
        Description: �̹߳���ǰ�ĳ�ʼ������
        Parameter: ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
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
        Description: �������е����ȼ�
        Parameter: 
            priority: �������Ķ��е����ȼ�
            weight: Ȩ��
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
        Description: ��worker����æ״̬ʱ�Ĵ���
        Parameter: 
            priority: ��Ϣ�����ȼ�
            frame: AppFrame
            busy_reason: æ��ԭ�����ԭ��Ϊ0����������Ϣ
        Return: 
        Others: 
        """

        if busy_reason == 0:
            self.__frame_buffer[priority].appendleft(frame)
            self._total_ready_to_process_frames += 1

    def _work(self):
        """
        Method:    _work
        Description: ����һ������
        Parameter: ��
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
        Description: ������Ϣ
        Parameter: 
            wait_seconds: �ȴ�����Ϣ��ʱ��(��)
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
        Description: ����һ����Ϣ
        Parameter: 
            frame: AppFrame
            priority: ��Ϣ�����ȼ�
        Return: �Ƿ�������Ϣ
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
    Description: ��WorkThread��Ļ�����ʵ���˷��ͽ�����Ϣ���߳�
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
    
