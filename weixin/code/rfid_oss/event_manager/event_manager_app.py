#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-15
Description: EventManager APP，负责event的接收，存储，查询和导出
Others:      
Key Class&Method List: 
             1. EventManagerApp
History: 
1. Date:2012-12-15
   Author:ACP2013
   Modification:新建文件
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
    Description: App类，负责worker的注册，mit的初始化，全局参数的初始化
    Base: BasicApp
    Others: 
        __mit_manager，mit管理器
        __global_param，全局参数EventManagerGlobalParam对象
        __event_no_creator，事件流水号生成器
        __event_type_manager，事件类型管理器
        
    """

    def __init__(self):
        """
        Method: __init__
        Description: 对象初始化函数
        Parameter: 无
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
        Description: 获取mit_manager对象实例
        Parameter: 无
        Return: __mit_manager
        Others: 
        """

        return self.__mit_manager
    
    def get_global_param(self):
        """
        Method: get_global_param
        Description: 获取全局参数
        Parameter: 无
        Return: __global_param
        Others: 
        """

        return self.__global_param
    
    def set_global_param(self, global_param):
        """
        Method: set_global_param
        Description: 设置全局参数
        Parameter: 
            global_param: 全局参数EventManagerGlobalParam对象实例
        Return: 
        Others: 
        """

        self.__global_param = global_param
        
    def get_event_sequence_no_creator(self):
        """
        Method: get_event_sequence_no_creator
        Description: 获取event流水号生成器
        Parameter: 无
        Return: __event_no_creator
        Others: 
        """

        return self.__event_no_creator
    
    def get_event_type_manager(self):
        """
        Method: get_event_type_manager
        Description: 获取event类型管理器
        Parameter: 无
        Return: __event_type_manager
        Others: 
        """

        return self.__event_type_manager
     
    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: 父类实现方法，注册MOC对象，加载全局参数 ，
                                    初始化流水号生成器，初始化event类型管理器，
                                    注册EventPersistenceWorker和EventOperationWorker
        Parameter: 无
        Return: 0，成功
                                            其他，失败
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

        #测试时可以使用sqlite
        self.__mit_manager.open_sqlite(db_file)
        #self.__mit_manager.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME)) 
        
        #加载全局参数
        rdms = self.__mit_manager.rdm_find('EventManagerGlobalParam'
                                         , key = 'default')
        if len(rdms)!=1:
            tracelog.error("can't load the default global parameter")
            return 1
        else:
            self.__global_param = copy.copy(rdms[0])
            
        #初始化event no creator, 获取当前MIT中的最大sequence_no
        sequence_no = self.__mit_manager.get_attr_max_value('Event', 'sequence_no')
        if sequence_no is None:
            sequence_no =  0
        self.__event_no_creator.init_creator(2**32, sequence_no)
        
        #初始化event type manager
        self.__event_type_manager.load_event_type(self.__mit_manager)
        
        worker = event_persistence_worker.EventPersistenceWorker()
        self.register_worker(worker)

        worker = event_operation_worker.EventOperationWorker()
        self.register_worker(worker)
        
        return 0   
    
#    def get_callacp_srv(self):
#        """
#        Method: get_callacp_srv
#        Description: 实例化callcsp对象
#        Parameter: 无
#        Return: callcsp对象
#        Others: 
#        """
#
#        callacp_srv = bf.SimpleCallAcpSrv(self, port = 7301)
#        return callacp_srv
    
    def send_ack(self, frame, datas):
        """
        Method: send_ack
        Description: 根据原始请求frame，将datas发送给请求者
        Parameter: 
            frame: 原始请求frame
            datas: 需要发送的data的列表
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