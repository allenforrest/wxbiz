#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-13
Description: �¼�����ģ��app
Key Class&Method List: 
             1. EventCenterApp -- ������
History:
1. Date: 2013-5-16
   Author: Allen
   Modification: create
"""

import os.path
import sys
import time
import collections
import Queue

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import mit
import tracelog
import sequence_no_creator

import err_code_def
import cmd_code_def
import msg_params_def
import event_man_worker

from moc_wx import Event, Subject, Group

class EventCenterApp(bf.BasicApp):
    """
    Class:    EventCenterApp
    Description: EventCenterAppģ��Ľ�����
    Base: BasicApp    
    Others: ��
    """

    def __init__(self):
        """
        Method: __init__
        Description: ���ʼ��
        Parameter: ��
        Return: 
        Others: 
        """

        bf.BasicApp.__init__(self, "EventCenterApp")
        self._mit_manager = mit.Mit()
        self._event_seq_no_creator = sequence_no_creator.SequenceNoCreator()
            
    def _ready_for_work(self):
        """
        Method:    _ready_for_work
        Description: ��������ʱ�ĳ�ʼ��������ע���̺߳�worker
        Parameter:  ��
        Return: 
                0   -- �ɹ�
                                      ��0 -- ʧ��
        Others: ��
        """
        bf.BasicApp._ready_for_work(self)        
        
        self._mit_manager.init_mit_lock()
        
        self._mit_manager.regist_moc(Event.Event, Event.EventRule)
        self._mit_manager.regist_moc(Subject.Subject, Subject.SubjectRule)
        self._mit_manager.regist_moc(Group.Group, Group.GroupRule)
        
        self._mit_manager.open_sqlite("../../data/sqlite/wx_cloud.db")

        worker = event_man_worker.EventManWorker(min_task_id = 1, max_task_id = 9999)
        self.register_worker(worker)

        event_seq_no = self.get_mit_manager().get_attr_max_value('Event', 'event_id')
        if event_seq_no is None:
            event_seq_no =  0
        self._event_seq_no_creator.init_creator(2 ** 32, event_seq_no)

        return 0

    def get_mit_manager(self):
        """
        Method: get_mit_manager
        Description: ��ȡ���̵�mit������
        Parameter: ��
        Return: mit������
        Others: 
        """

        return self._mit_manager
    
    def get_event_seq_no_creater(self):
        return self._event_seq_no_creator
    
    def send_ack_dispatch(self, frame, datas):
        """
        Method: send_ack_dispatch
        Description: �������Ӧ��Ϣ
        Parameter: 
            frame: ��Ϣ֡
            datas: ��������
        Return: 
        Others: 
        """

        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(frame)        
        for data in datas:
            frame_ack.add_data(data)

        tracelog.info('event center app send ack frame: %s' % frame_ack)
        tracelog.info('frame buf: %s' % frame_ack.get_data())
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)
            

if __name__ == "__main__":
    EventCenterApp().run()