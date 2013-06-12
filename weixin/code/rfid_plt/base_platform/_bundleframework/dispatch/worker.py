#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-12
Description: ���ļ���ʵ����Worker�࣬��������������worker�Ļ���
Others:      
Key Class&Method List: 
             1. Worker: �������࣬��������������worker�Ļ���
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
    Description: �������࣬��������������worker�Ļ���
    Base: object
    Others: 
    """

    def __init__(self, name):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            name: worker������
        Return: 
        Others: 
            __name: worker������
            __app: app����
            __time_out_handlers: ���ж�ʱhandler(�ȴ���ʱ��handler)
        """

        self.__name = name
        self.__app  = None
        self.__time_out_handlers = []


    def set_app(self, app):
        """
        Method:    set_app
        Description: ����app����
        Parameter: 
            app: app����
        Return: 
        Others: 
        """

        self.__app = app

    def get_app(self):
        """
        Method:    get_app
        Description: ��ȡapp����
        Parameter: ��
        Return: app���� 
        Others: 
        """

        return self.__app

    def is_my_duty(self, frame):
        """
        Method:    is_my_duty
        Description: �ж��Ƿ��ǵ�ǰworker��Ҫ���������
        Parameter: 
            frame: ������Ϣ
        Return: �Ƿ��ǵ�ǰworker��Ҫ���������
        Others: 
        """

        return False

    #def is_my_duty_ts(self, frame):
    #    return -1

    def get_name(self):
        """
        Method:    get_name
        Description: ��ȡworker������
        Parameter: ��
        Return: worker������
        Others: 
        """

        return self.__name


    def get_my_pid(self):
        """
        Method:    get_my_pid
        Description: ��ȡapp��pid
        Parameter: ��
        Return: app��pid
        Others: 
        """

        if self.__app:
            return self.__app.get_my_pid()
        else:
            return -1

    def get_pid(self, name, strategy=FIRSTLOCAL_PID):
        """
        Method:    get_pid
        Description: ��ȡָ�����Ƶ�app��pid
        Parameter: 
            name: app������
            strategy:ѡ�����
        Return: app��pid
        Others: 
        """

        if self.__app:
            return self.__app.get_pid(name, strategy)
        else:
            return -1

    def get_peer_pid(self, name):
        """
        Method:    get_peer_pid
        Description: ����˫������£���ȡ�Զ�ϵͳ��ָ�����Ƶ�app��pid
        Parameter: 
            name: �Զ�ϵͳ��app������
        Return: �Զ�ϵͳ��ָ�����Ƶ�app��pid
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
        Description: �ж��Ƿ���ڵȴ���ʱ��handler
        Parameter: ��
        Return: �Ƿ���ڵȴ���ʱ��handler
        Others: 
        """

        return len(self.__time_out_handlers) > 0

    def time_out(self, ticks):
        """
        Method:    time_out
        Description: ��鶨ʱ���Ĵ���
        Parameter: 
            ticks: ��ǰʱ��
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
        Description: ע�ᶨʱhandler
        Parameter: 
            handler: ��Ҫע��Ϊ��ʱ����handler
        Return: 
        Others: 
        """

        if not (handler in self.__time_out_handlers):
            self.__time_out_handlers.append(handler)
            handler.set_worker(self)

    def unregister_time_out_handler(self, handler):
        """
        Method:    unregister_time_out_handler
        Description: ע����ʱhandler
        Parameter: 
            handler: ��ʱhandler
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
        Description: ���д�����
        Parameter: 
            total_ready_frames: ���еȴ�������Ϣ�ĸ���
        Return: 
        Others: 
        """

        pass

    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker��ʼ������
        Parameter: ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
        Others: 
            �����Worker��CmdWorker�̳е������У���Ҫ��worker����ǰ��Щ��ʼ������
            ��ô����ready_for_work����ɣ����磬ע��handler��
            ע�⣬ready_for_work����0��ʾִ�гɹ�������Ϊʧ�ܡ���ready_for_work
            ʧ�ܵ�����£����̻��˳�(�����˳���monitor���Զ������ý���)
        """

        return 0

    def get_max_busy_ticks_ts(self):
        """
        Method:    get_max_busy_ticks_ts
        Description: ��ȡ���ķ�æʱ������
        Parameter: ��
        Return: ���ķ�æʱ������
        Others: 
            ���worker�ڴ������ڣ��߳�û��ι��������Ϊworker�������쳣
        """

        return 600

    def get_max_wait_ticks_ts(self):
        """
        Method:    get_max_wait_ticks_ts
        Description: ��ȡÿ�εȴ��µ���Ϣ��ʱ��
        Parameter: ��
        Return: ÿ�εȴ��µ���Ϣ��ʱ��
        Others: 
        """

        return 0.8


    def is_busy(self, frame):
        """
        Method:    is_busy
        Description: �ж�ִ�е���Ϣ�Ƿ��뵱ǰ����ִ�е������
        Parameter: 
            frame: AppFrame
        Return: ִ�е���Ϣ�Ƿ��뵱ǰ����ִ�е������
        Others: 
        """

        return (False, 0)

    def priority(self, frame):
        """
        Method:    priority
        Description: ��ȡָ����Ϣ�����ȼ�
        Parameter: 
            frame: AppFrame
        Return: ��Ϣ�����ȼ�
        Others: 
        """

        return AppFrame.medium_priority

    def work(self, frame, total_ready_frames):
        """
        Method:    work
        Description: ����һ����Ϣ
        Parameter: 
            frame: AppFrame
            total_ready_frames: ���д��������Ϣ����
        Return: 
        Others: 
        """

        pass

    def on_event(self, e):
        """
        Method:    on_event
        Description: �����¼���Ϣ
        Parameter: 
            e: �¼���Ϣ
        Return: 
            0: �ɹ�
            ��0: ʧ��
        Others: 
        """

        return 0

    def exit_work(self):
        """
        Method:    exit_work
        Description: worker�˳�ǰ�Ĵ�����
        Parameter: ��
        Return: 
        Others: 
        """

        pass

    def dispatch_frame_to_process(self, process_name, frame):
        """
        Method:    dispatch_frame_to_process
        Description: ������Ϣ��ָ�����ƵĽ���
        Parameter: 
            process_name: ������Ϣ�Ľ��̵�����
            frame: AppFrame
        Return: 
        Others: 
        """

        if self.__app:
            self.__app.dispatch_frame_to_process(process_name, frame)

    def dispatch_frame_to_process_by_pid(self, pid, frame):
        """
        Method:    dispatch_frame_to_process_by_pid
        Description: ������Ϣ��ָ��pid�Ľ���
        Parameter: 
            pid: ������Ϣ�Ľ��̵�pid
            frame: 
        Return: 
        Others: 
        """

        if self.__app:
            self.__app.dispatch_frame_to_process_by_pid(pid, frame)

    def dispatch_frame_to_worker(self, worker_name, frame):
        """
        Method:    dispatch_frame_to_worker
        Description: ������Ϣ��ָ����worker
        Parameter: 
            worker_name: ������Ϣ��worker
            frame: AppFrame
        Return: 
        Others: 
        """

        if self.__app:
            self.__app.dispatch_frame_to_worker(worker_name, frame)

    def dispatch_frame_to_all_workers(self, frame):
        """
        Method:    dispatch_frame_to_all_workers
        Description: ������Ϣ���������ڵ�����worker
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
        Description:������Ϣ�����е��������� 
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
        Description:����Ӧ����Ϣ
        Parameter: 
            frame: AppFrameʵ������Ӧ��������Ϣ
            datas: Ӧ����Ϣ�壬�ַ�������������ݣ�������һ���ַ�������������ݵ��б�
        Return: 
        Others: 
        """
        if self.__app:
            self.__app.send_ack(frame, datas)
        
    #def dispatch_frame_to_callacp(self, frame):
    #    """
    #    Method:    dispatch_frame_to_callacp
    #    Description:������Ϣ��callacp�Ŀͻ���
    #    Parameter: 
    #        frame: AppFrame
    #    Return: 
    #    Others: 
    #    """
    #    if self.__app:
    #        self.__app.dispatch_frame_to_callacp(frame)


