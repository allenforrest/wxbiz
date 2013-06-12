#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-15
Description: EventManager APP������event�Ľ��գ��洢����ѯ�͵���
Others:      
Key Class&Method List: 
             1. EventManagerApp
History: 
1. Date:2012-12-15
   Author:ACP2013
   Modification:�½��ļ�
"""



import os.path
import sys

if __name__ == "__main__":
    import import_paths
    
import copy

import bundleframework as bf
import mit
import tracelog
from dba import db_cfg_info

import err_code_mgr
import error_code

import sequence_no_creator
import event_type_manager
import event_persistence_worker
import event_operation_worker

from moc_event_manager import EventType 
from moc_event_manager import EventTypeDetail
from moc_event_manager import Event
from moc_event_manager import EventDetail
from moc_event_manager import EventManagerGlobalParam

class EventManagerApp(bf.BasicApp):    
    """
    Class: EventManagerApp
    Description: App�࣬����worker��ע�ᣬmit�ĳ�ʼ����ȫ�ֲ����ĳ�ʼ��
    Base: BasicApp
    Others: 
        __mit_manager��mit������
        __global_param��ȫ�ֲ���EventManagerGlobalParam����
        __event_no_creator���¼���ˮ��������
        __event_type_manager���¼����͹�����
        
    """

    def __init__(self):
        """
        Method: __init__
        Description: �����ʼ������
        Parameter: ��
        Return: 
        Others: 
        """

        bf.BasicApp.__init__(self, "EventManagerApp")
        self.__mit_manager = mit.Mit()
        self.__global_param = None
        self.__event_no_creator = sequence_no_creator.SequenceNoCreator()
        self.__event_type_manager = event_type_manager.EventTypeManager()
        
    
    def get_mit_manager(self):
        """
        Method: get_mit_manager
        Description: ��ȡmit_manager����ʵ��
        Parameter: ��
        Return: __mit_manager
        Others: 
        """

        return self.__mit_manager
    
    def get_global_param(self):
        """
        Method: get_global_param
        Description: ��ȡȫ�ֲ���
        Parameter: ��
        Return: __global_param
        Others: 
        """

        return self.__global_param
    
    def set_global_param(self, global_param):
        """
        Method: set_global_param
        Description: ����ȫ�ֲ���
        Parameter: 
            global_param: ȫ�ֲ���EventManagerGlobalParam����ʵ��
        Return: 
        Others: 
        """

        self.__global_param = global_param
        
    def get_event_sequence_no_creator(self):
        """
        Method: get_event_sequence_no_creator
        Description: ��ȡevent��ˮ��������
        Parameter: ��
        Return: __event_no_creator
        Others: 
        """

        return self.__event_no_creator
    
    def get_event_type_manager(self):
        """
        Method: get_event_type_manager
        Description: ��ȡevent���͹�����
        Parameter: ��
        Return: __event_type_manager
        Others: 
        """

        return self.__event_type_manager
     
    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: ����ʵ�ַ�����ע��MOC���󣬼���ȫ�ֲ��� ��
                                    ��ʼ����ˮ������������ʼ��event���͹�������
                                    ע��EventPersistenceWorker��EventOperationWorker
        Parameter: ��
        Return: 0���ɹ�
                                            ������ʧ��
        Others: 
        """

        bf.BasicApp._ready_for_work(self)        
        
        self.__mit_manager.init_mit_lock()
        
        self.__mit_manager.regist_moc(EventType.EventType, EventType.EventTypeRule)
        self.__mit_manager.regist_moc(EventTypeDetail.EventTypeDetail, EventTypeDetail.EventTypeDetailRule)
        self.__mit_manager.regist_moc(Event.Event, Event.EventRule)
        self.__mit_manager.regist_moc(EventDetail.EventDetail, EventDetail.EventDetailRule)
        self.__mit_manager.regist_moc(EventManagerGlobalParam.EventManagerGlobalParam, EventManagerGlobalParam.EventManagerGlobalParamRule)

        db_file = os.path.join(self.get_app_top_path()
                                , "data"
                                , "sqlite"
                                , "event_manager.db")

        #����ʱ����ʹ��sqlite
        self.__mit_manager.open_sqlite(db_file)
        #self.__mit_manager.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME)) 
        
        #����ȫ�ֲ���
        rdms = self.__mit_manager.rdm_find('EventManagerGlobalParam'
                                         , key = 'default')
        if len(rdms)!=1:
            tracelog.error("can't load the default global parameter")
            return 1
        else:
            self.__global_param = copy.copy(rdms[0])
            
        #��ʼ��event no creator, ��ȡ��ǰMIT�е����sequence_no
        sequence_no = self.__mit_manager.get_attr_max_value('Event', 'sequence_no')
        if sequence_no is None:
            sequence_no =  0
        self.__event_no_creator.init_creator(2**32, sequence_no)
        
        #��ʼ��event type manager
        self.__event_type_manager.load_event_type(self.__mit_manager)
        
        worker = event_persistence_worker.EventPersistenceWorker()
        self.register_worker(worker)

        worker = event_operation_worker.EventOperationWorker()
        self.register_worker(worker)
        
        return 0   
    
#    def get_callacp_srv(self):
#        """
#        Method: get_callacp_srv
#        Description: ʵ����callcsp����
#        Parameter: ��
#        Return: callcsp����
#        Others: 
#        """
#
#        callacp_srv = bf.SimpleCallAcpSrv(self, port = 7301)
#        return callacp_srv
    
    def send_ack(self, frame, datas):
        """
        Method: send_ack
        Description: ����ԭʼ����frame����datas���͸�������
        Parameter: 
            frame: ԭʼ����frame
            datas: ��Ҫ���͵�data���б�
        Return: 
        Others: 
        """

        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(frame)        
        for data in datas:
            frame_ack.add_data(data)        
        
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)
        
if __name__=='__main__':        
    EventManagerApp().run()