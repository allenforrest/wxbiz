#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-23
Description: 事件存储worker和相应的handler处理类
Others:      
Key Class&Method List: 
             1. EventReportHandler
             2. SaveEventTimeoutHandler
             3. EventPersistenceWorker
History: 
1. Date:2012-11-23
   Author:ACP2013
   Modification:新建文件
"""

import cPickle
import Queue

import bundleframework as bf
import tracelog
import err_code_mgr
import event_sender
import basic_rep_to_web

import command_code
import worker_taskid_define

import message_across_app

class EventReportHandler(bf.CmdHandler):
    """
    Class: EventReportHandler
    Description: event接收处理
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 收到event_data，将其增加到worker的队列中去
        Parameter: 
            frame: 请求消息，data中为event_data
        Return: 
        Others: 
        """

        buf = frame.get_data()
        try:
            event_data = cPickle.loads(buf)            
        except Exception, err:
            tracelog.error('illegal data.\n%s'%err)
            return        
        
        if isinstance(event_data, event_sender.EventData) is not True:
            tracelog.error('illegal event data.')
            return
        
        self.get_worker().add_event_data(event_data)
        
        return

class WebEventReportHandler(bf.CmdHandler):
    """
    Class: WebEventReportHandler
    Description: 接收WEB发送的EVENT
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 收到web的消息，转换为event_data，加入到队列中。
        Parameter: 
            frame: 请求消息，data中为EventFromWebRequest对象
        Return: 无
        Others: 
        """

        buf = frame.get_data()
        tracelog.info('WebEventReportHandler data %s'%buf)
        result = basic_rep_to_web.BasicRepToWeb();
        result.init_all_attr()        
        
        buf = frame.get_data()        
        try:
            req = message_across_app.EventFromWebRequest.deserialize(buf)
        except Exception:
            result.user_session = ''            
            result.return_code = err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
                                                            , cmd='WebEventRepor'
                                                            , param_name='EventFromWebRequest')            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return     
        
        event_data = event_sender.EventData()
        event_data.set_event_id(req.event_id)
        event_data.set_event_flag(req.event_flag)
        event_data.set_generate_time(req.generate_time_inner)
        event_data.set_device_id(req.device_id)
        event_data.set_object_id(req.object_id)
        
        params = {}
        #param需要全部转换为utf-8
        for key in req.params:
            if isinstance(req.params[key], unicode):
                params[key.encode('utf-8')] = req.params[key].encode('utf-8')
            else:
                params[key.encode('utf-8')] = req.params[key]
        event_data.set_params(params)        
        
        self.get_worker().add_event_data(event_data)
        
        result.prepare_for_ack(req, err_code_mgr.ER_SUCCESS, err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS))
        self.get_worker().get_app().send_ack(frame, (result.serialize(), ))
        return    

class SaveEventTimeoutHandler(bf.TimeOutHandler):
    """
    Class: SaveEventTimeoutHandler
    Description: 定时处理类，定时存储worker的event队列中的event到mit中去
    Base: TimeOutHandler
    Others: 
    """

    def time_out(self):        
        """
        Method: time_out
        Description: 定时处理函数，从event_queue获取event，通过mit_manager增加Event和EventDetail moc对象
        Parameter: 无
        Return: 
        Others: 
        """

        #手工提交事务
        mit_manager = self.get_worker().get_app().get_mit_manager()
        mit_manager.begin_tran()
        
        event_queue = self.get_worker().get_event_queue()
        no_creator = self.get_worker().get_app().get_event_sequence_no_creator()
        event_type_manager = self.get_worker().get_app().get_event_type_manager()
        
        while event_queue.empty() is not True:                        
            event_data = event_queue.get_nowait()
            event_type_rdm = event_type_manager.get_event_type_by_id(event_data.get_event_id())
            if event_type_rdm is None:
                tracelog.error('the event id %s is not defined'%event_data.get_event_id())
                continue
            
            sequence_no = no_creator.get_new_no()
            
            #由于一个event会生成多个moc对象，为了效率，进行批量事务，因此，单个event的一致性会牺牲。
            event_rdm = mit_manager.gen_rdm("Event")            
            event_rdm.sequence_no = sequence_no
            event_rdm.event_id = event_data.get_event_id()
            event_rdm.device_id = event_data.get_device_id()
            event_rdm.object_id = event_data.get_object_id()
            event_rdm.time_inner, event_rdm.time = event_data.get_generate_time()
            
            event_rdm.event_flag = event_type_rdm.event_flag
            event_rdm.level = event_type_rdm.level
            event_rdm.device_type = event_type_rdm.device_type
            event_rdm.object_type = event_type_rdm.object_type
            
            rst = mit_manager.rdm_add(event_rdm)
            if rst.get_err_code()!=0:
                tracelog.error('insert event %s to mit failed\n%s'%(str(event_rdm), rst.get_msg()))
                continue                
            
            event_type_details = event_type_manager.get_event_type_details_by_id(event_data.get_event_id())
            for type_detail in event_type_details:
                detail_rdm = mit_manager.gen_rdm("EventDetail")
                detail_rdm.sequence_no = sequence_no                 
                detail_rdm.language = type_detail.language
                detail_rdm.name = type_detail.name                
                try:
                    detail_rdm.description = type_detail.description%event_data.get_params()
                    detail_rdm.cause = type_detail.cause%event_data.get_params()
                except Exception,err:
                    tracelog.exception('illegal event params %s.\n %s'%(str(event_data.get_params()),err))
                    continue
                
                rst = mit_manager.rdm_add(detail_rdm)
                if rst.get_err_code()!=0:
                    tracelog.error('insert event detail %s to mit failed\n%s'%(str(detail_rdm), rst.get_msg()))
                    continue
        
        mit_manager.commit_tran()
            

class EventPersistenceWorker(bf.CmdWorker):    
    """
    Class: EventPersistenceWorker
    Description: event存储worker
    Base: CmdWorker
    Others: 
        __current_event_queue,event队列
    """

    def __init__(self):
        """
        Method: __init__
        Description: 
        Parameter: 无
        Return: 
        Others: 
        """

        bf.CmdWorker.__init__(self, name = "EventPersistenceWorker"
                            , min_task_id = worker_taskid_define.EVENT_PERSISTENCE_WORKER_MIN_TASK_ID
                            , max_task_id = worker_taskid_define.EVENT_PERSISTENCE_WORKER_MAX_TASK_ID)
        
        #暂时不考虑多优先级队列
        self.__current_event_queue = Queue.Queue()        
        
    
    def get_event_queue(self):
        """
        Method: get_event_queue
        Description: 获取event队列对象
        Parameter: 无
        Return: __current_event_queue
        Others: 
        """

        return self.__current_event_queue
    
    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: 注册1秒的定时处理SaveEventTimeoutHandler，注册EventReportHandler。
        Parameter: 无
        Return: 
        Others: 
        """

        handler = SaveEventTimeoutHandler()
        handler.start_timer(1, False)
        self.register_time_out_handler(handler)
        
        self.register_handler(EventReportHandler(), command_code.EVENT_REPORT_COMMAND)
        self.register_handler(WebEventReportHandler(), command_code.WEB_EVENT_REPORT_COMMAND)
        
        return 0
    
    def add_event_data(self, event_data):
        """
        Method: add_event_data
        Description: 增加event到队列中去
        Parameter: 
            event_data: event对象
        Return: 
        Others: 
        """

        try:
            self.__current_event_queue.put_nowait(event_data)
        except Queue.Full :            
            tracelog.error('The current_event_queue is full')
    
        
                        
