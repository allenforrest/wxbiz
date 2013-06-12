#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-11
Description: ���ļ��У�ʵ����CmdHandler
Others:      
Key Class&Method List: 
             1. CmdRound: ����ִ��ʱ������round
             2. TimeOutHandler: ��ʱhandler
             3. CmdHandler: ������handler
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
    Description: ����ִ��ʱ������round
    Base: 
    Others: 
    """

    def __init__(self, request_frame):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            request_frame: ������Ϣ
        Return: 
            __request_frame: ������Ϣ
            __response_frames: Ӧ����Ϣ�б�
            __over: �Ƿ��Ѿ�����
            __result: ������
            __send_yet: ������Ϣ�Ƿ��Ѿ�����
            __data: �Զ��������
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
        Description: ��ȡ������Ϣ
        Parameter: ��
        Return: ������Ϣ
        Others: 
        """

        return self.__request_frame

    def add_response_frame(self, response_frame):
        """
        Method:    add_response_frame
        Description: ����Ӧ����Ϣ
        Parameter: 
            response_frame: Ӧ����Ϣ
        Return: 
        Others: 
        """

        self.__response_frames.append(response_frame)
        if response_frame.is_last():
            # �����frameʱ�Ƿ���������
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
        Description: ��ȡ���е�Ӧ����Ϣ
        Parameter: ��
        Return: ���е�Ӧ����Ϣ
        Others: 
        """

        return self.__response_frames

    def get_response_frame(self):
        """
        Method:    get_response_frame
        Description: ��ȡ��һ��Ӧ����Ϣ
        Parameter: ��
        Return: 
            None: û��Ӧ����Ϣ
            ��None: ��һ��Ӧ����Ϣ
        Others: 
        """

        if len(self.__response_frames) > 0:
            return self.__response_frames[0]
        else:
            return None

    def set_data(self, data):
        """
        Method:    set_data
        Description: �����Զ�������
        Parameter: 
            data: �Զ�������
        Return: 
        Others: 
        """

        self.__data = data

    def get_data(self):
        """
        Method:    get_data
        Description: ��ȡ�Զ�������
        Parameter: ��
        Return: �Զ�������
        Others: 
        """

        return self.__data

    def over(self, result):
        """
        Method:    over
        Description: ��round����Ϊ����״̬���������ô�����
        Parameter: 
            result: ������
        Return: 
        Others: 
        """

        self.__over   = True
        self.__result = result

    def is_over(self):
        """
        Method:    is_over
        Description: �ж��Ƿ��Ѿ�����
        Parameter: ��
        Return: �Ƿ��Ѿ�����
        Others: 
        """

        return self.__over

    def get_result(self):
        """
        Method:    get_result
        Description: ��ȡ������
        Parameter: ��
        Return: ������
        Others: 
        """

        return self.__result

    def set_send_yet(self, s):
        """
        Method:    set_send_yet
        Description: �����Ƿ��Ѿ�������������Ϣ
        Parameter: 
            s: Ture����False
        Return: 
        Others: 
        """

        self.__send_yet = s

    def send_yet(self):
        """
        Method:    send_yet
        Description: �ж��Ƿ��Ѿ�������������Ϣ
        Parameter: ��
        Return: �Ƿ��Ѿ�������������Ϣ
        Others: 
        """

        return self.__send_yet

    def is_wait_for_ack(self):
        """
        Method:    is_wait_for_ack
        Description: �ж��Ƿ��ڵȴ�Ӧ����Ϣ��״̬
        Parameter: ��
        Return: �Ƿ��ڵȴ�Ӧ����Ϣ��״̬
        Others: 
        """

        return not self.__over and self.__send_yet


class TimeOutHandlerBase(object):
    """
    Class: TimeOutHandlerBase
    Description: ��ʱhandler
    Base: object
    Others: 
        _once: �Ƿ�ֻ����1�γ�ʱ
        _worker: handler���ڵ�workers
    """
    
    def __init__(self):
        self._once = False
        self._worker = None
        
    def is_time(self, now_second):
        return False

    def time_out(self):
        """
        Method:    time_out
        Description: ��ʱʱ�䵽���Ժ󣬵��ñ��ӿڴ�����ص�����
        Parameter: ��
        Return: 
        Others: ���ӿڹ���������
        """

        pass

        
    def stop_timer(self):
        """
        Method:    stop_timer
        Description: ֹͣʱ������ʽ�ļ�ʱ��
        Parameter: ��
        Return: 
        Others: 
        """
        pass


    def set_worker(self, wrkr):
        """
        Method:    set_worker
        Description: ����Worker����
        Parameter: 
            wrkr: Worker����
        Return: 
        Others: 
        """

        self._worker = wrkr

    def get_worker(self):
        """
        Method:    get_worker
        Description: ��ȡWorker����
        Parameter: ��
        Return: Worker����
        Others: 
        """

        return self._worker


        
class TimeOutHandler(TimeOutHandlerBase):
    """
    Class: TimeOutHandler
    Description: ��ʱhandler
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
            __last_time: �ϴγ�ʱ��ʱ��(��)
            __interval_time:ÿ�γ�ʱ������(��)
        """
        TimeOutHandlerBase.__init__(self)

        # ���չ̶������ʱ
        self.__last_time = 0
        self.__interval_time = 0
              
        
    def is_time(self, now_second):
        """
        Method:    is_time
        Description: �ж��Ƿ��˳�ʱʱ��
        Parameter: 
            ticks: ��ǰϵͳʱ��
        Return: �Ƿ��˳�ʱʱ��
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
        Description: ������ʱ��������������һ����ʱ����
        Parameter: 
            ticks: ��ʱ�������ڳ���(��)
            once: �Ƿ�ֻ����һ�γ�ʱ
        Return: 
        Others: 
        """

        self.__last_time = 0
        self.__interval_time = interval_time
        self._once = once
                

    def stop_timer(self):
        """
        Method:    stop_timer
        Description: ֹͣʱ������ʽ�ļ�ʱ��
        Parameter: ��
        Return: 
        Others: 
        """

        self.__last_time = 0
        self.__interval_time = 0
        

        
class FixedTimeOutHandler(TimeOutHandlerBase):
    """
    Class: FixedTimeOutHandler
    Description: ��ʱhandler
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
        """
        TimeOutHandlerBase.__init__(self)

        # ���չ̶���ʱ����ʱ
        self.__year = None
        self.__month = None
        self.__day = None
        self.__hour = None
        self.__minute = None
        self.__second = None

        # �ϴμ���ʱ���
        self.__last_time = None

        # �ϴ�������ʱ���
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
        Description: �ж��Ƿ��˳�ʱʱ��
        Parameter: 
            ticks: ��ǰϵͳʱ��
        Return: �Ƿ��˳�ʱʱ��
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
        Description: ������ʱ�������������ǹ̶���ʱ���
        Parameter: 
            
            once: �Ƿ�ֻ����һ�γ�ʱ
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
        Description: ֹͣ�̶�ʱ���ļ�ʱ��
        Parameter: ��
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
    Description: ������handler 
    Base: TimeOutHandler
    Others: 
    """

    invalid_round_id = 0

    min_round_id = 1
    max_round_id = 0xfffffffe

    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
            __time_of_new: ��ǰhandler������ʱ��
            __parent: ��handler
            __children: ���е���handler
            __over: �Ƿ��Ѿ�����
            __result: ������
            __task_id: �����
            __rounds: ���е�round
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
        Description: ����round���Ʋ���
        Parameter: 
            strategy: round���Ʋ���
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
        Description: ���ø�handler
        Parameter: 
            parent: ��handler
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
        Description: ��ȡ��handler
        Parameter: ��
        Return: 
        Others: 
        """

        return self.__parent

    def add_child(self, child):
        """
        Method:    add_child
        Description: ������handler
        Parameter: 
            child: ��handler
        Return: 
        Others: 
        """

        if child and not child in self.__children:
            self.__children.append(child)

        return self

    def get_time_of_new(self):
        """
        Method:    get_time_of_new
        Description: ��ȡhandler����ʱ��ʱ��
        Parameter: ��
        Return: handler����ʱ��ʱ��
        Others: 
        """

        return self.__time_of_new

    def is_my_duty(self, frame):
        """
        Method:    is_my_duty
        Description: �ж�ָ������Ϣ�Ƿ��ǵ�ǰhandler����
        Parameter: 
            frame: AppFrame
        Return: ָ������Ϣ�Ƿ��ǵ�ǰhandler����
        Others: 
        """

        return False

    def is_busy(self, frame):
        """
        Method:    is_busy
        Description: �ж�ָ������Ϣ�Ƿ��뵱ǰhandlerͬʱִ��
        Parameter: 
            frame: AppFrame
        Return: ָ������Ϣ�Ƿ��뵱ǰhandlerͬʱִ��
        Others: 
        """

        return False

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: ������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """

        pass

    def get_all_rounds(self):
        """
        Method:    get_all_rounds
        Description: ��ȡ���е�round
        Parameter: ��
        Return: ���е�round
        Others: 
        """

        return self.__rounds
        
    def _new_round(self, round):
        """
        Method:    _new_round
        Description: �¼���һ��round
        Parameter: 
            round: �����ĵ�round
        Return: �Զ������round��id
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
        Description: ע�ᵱǰhandlerΪack_handle���Ա����Ӧ����Ϣ
        Parameter: ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
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
        Description: ����������Ϣ���ͳ�ȥ�����ҵȴ�Ӧ��
        Parameter: 
            frame: ��Ҫ���ͳ�ȥ������
            time_out: �ȴ�Ӧ��ĳ�ʱʱ��
        Return: ���ͳ�ȥ��round�ĸ���
        Others: 
        """

        self._new_round(CmdRound(frame))
        return self.wait_for_all_rounds_ack(time_out)

    def wait_for_all_rounds_ack(self, time_out):
        """
        Method:    wait_for_all_rounds_ack
        Description: �����е����е�round���ͳ�ȥ�����ҵȴ�Ӧ�� 
        Parameter: 
            time_out: �ȴ�Ӧ��ĳ�ʱʱ��
        Return: ���ͳ�ȥ��round�ĸ���
        Others: 
        """

        if self.__regist_as_ack_handle() != 0:
            return 0

        total_rounds_send = self.send_all_rounds()

        # bug fix: ���������Ƿ�������Ϣ��Ҫ������ʱ����
        # ����ᵼ��handler��ʱ����worker�У�taskid��ռ�ã��Ұװ��˷ѿռ�
        #if total_rounds_send > 0:
        self.start_timer(time_out, True)

        return total_rounds_send

    def wait_for_child_ack(self, frame, time_out):
        """
        Method:    wait_for_child_ack
        Description: ��ָ����frame��Ϊ��handlerִ�У����ҵȴ�����handler��Ӧ��
        Parameter: 
            frame: ������Ϣ
            time_out: ��ʱʱ��
        Return: ���ͳ�ȥ��round�ĸ���
        Others: 
        """

        self._new_round(CmdRound(frame))
        return self.wait_for_all_children_ack(time_out)

    def wait_for_all_children_ack(self, time_out):
        """
        Method:    wait_for_all_children_ack
        Description: �����е�����round����Ϊ��handlerִ�У����ҵȴ�����handler��Ӧ��
        Parameter: 
            time_out: �ȴ���handler�����ĳ�ʱʱ��
        Return: ���ͳ�ȥ��round�ĸ���
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
        Description: �����е�����round���ͳ�ȥ
        Parameter: ��
        Return: ���ͳ�ȥ��round�ĸ���
        Others: 
        """

        return self.__send_all_rounds_to(False)

    def send_all_rounds_to_children(self):
        """
        Method:    send_all_rounds_to_children
        Description: �����е����е�round���͸���handler
        Parameter: ��
        Return: ���ͳ�ȥ��round�ĸ���
        Others: 
        """

        return self.__send_all_rounds_to(True)

    def __send_all_rounds_to(self, to_children):
        """
        Method:    __send_all_rounds_to
        Description: �����е����е�round���ͳ�ȥ
        Parameter: 
            to_children: �Ƿ��͸���handler
        Return: ���ͳ�ȥ��round�ĸ���
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
        Description: ����Ӧ����Ϣ
        Parameter: 
            frame: appframeӦ����Ϣ
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
        Description: �ж��Ƿ��Ѿ�����
        Parameter: ��
        Return: �Ƿ��Ѿ�����
        Others: 
        """

        return self.__over

    def __is_all_rounds_over(self):
        """
        Method:    __is_all_rounds_over
        Description: �ж��Ƿ����е�round���Ѿ�����
        Parameter: ��
        Return: �Ƿ����е�round���Ѿ�����
        Others: 
        """

        for r in self.__rounds.itervalues():
            if not r.is_over():
                return False

        return True

    def time_out(self):
        """
        Method:    time_out
        Description: ��ʱ����µĴ���
        Parameter: ��
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
        Description: ��handler����Ϊ����״̬
        Parameter: 
            result: ������
            args: ������Ϣ����Ҫ�õ���һЩ����
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
        Description: ��Ӧ��handler�������¼�
        Parameter: 
            child: ��handler
        Return: 
        Others: 
        """

        pass

    def _on_round_over(self, round_id, r):
        """
        Method:    _on_round_over
        Description: ��Ӧround�������¼�
        Parameter: 
            round_id: round��id
            r: round����
        Return: 
        Others: 
        """

        """
        ��round�յ�Ӧ����Ϣ, ���ô˽ӿ�
        """
        pass

    def _on_all_rounds_over(self, rounds):
        """
        Method:    _on_all_rounds_over
        Description: ��Ӧ����round�������˵��¼�
        Parameter: 
            rounds: ���е�round
        Return: 
        Others: 
        """

        self.over(0)


    def _on_round_timeout(self, round_id, r):
        """
        Method:    _on_round_timeout
        Description: ��Ӧround��ʱ�¼�
        Parameter: 
            round_id: round��id
            r: round����
        Return: 
        Others: 
        """

        pass

    
    def _on_over(self, result, **args):
        """
        Method:    _on_over
        Description: ��Ӧhandler�����¼�
        Parameter: 
            result: ������
            args: ������Ϣ����Ҫ�õ���һЩ����
        Return: 
        Others: 
        """

        pass

        

class NoRoundsControlStrategy:
    """
    Class: NoRoundsControlStrategy
    Description: round���Ʋ���-�����κο���
    Base: 
    Others: 
    """

    def not_control(self, rounds, round_id, r):
        """
        Method:    not_control
        Description: �ж�ָ����round�Ƿ���Է��ͳ�ȥ
        Parameter: 
            rounds: ���е�round
            round_id: ��ǰ��round id
            r: round����
        Return: ָ����round�Ƿ���Է��ͳ�ȥ            
        Others: ��Ӧ�����ԣ������κο���
        """

        return True

class SequenceRoundsControlStrategy:
    """
    Class: SequenceRoundsControlStrategy
    Description: round���Ʋ���-�������е�roundֻ��˳��ִ��
                ��ǰ��һ��round�����󣬲���ִ�к���һ��round
    Base: 
    Others: 
    """

    def not_control(self, rounds, round_id, r):
        """
        Method:    not_control
        Description: �ж�ָ����round�Ƿ���Է��ͳ�ȥ
        Parameter: 
            rounds: ���е�round
            round_id: ��ǰ��round id
            r: round����
        Return: ָ����round�Ƿ���Է��ͳ�ȥ            
        Others:  
            ��Ӧ�����ԣ���Ҫ����Ƿ���round���ڵȴ�Ӧ���״̬��
            ����У�������ǰ��round���ͳ�ȥ
        """

        for i in rounds.itervalues:
            if i.is_wait_for_ack():
                return False

        return True



