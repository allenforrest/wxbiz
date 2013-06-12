#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-13
Description: event操作 worker和相应的handler处理类
Others:      
Key Class&Method List: 
             1. EventQueryHandler
             2. EventExportHandler
             3. EventExportTaskQueryHandler
             4. ClearExportFileTimeoutHandler
             5. EventFilterListHandler
             6. EventOperationWorker
History: 
1. Date:2012-12-13
   Author:ACP2013
   Modification:新建文件
"""

import os.path

import bundleframework as bf
import tracelog
import err_code_mgr

import command_code
import worker_taskid_define
import message_across_app
import event_query
import event_export_manager
import param_check
import get_eau_endpoint

class EventQueryHandler(bf.CmdHandler):    
    """
    Class: EventQueryHandler
    Description: 事件查询处理类
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 请求处理函数，如果EventQueryRequest对象反序列化成功，进行必要的参数检查，
                                然后调用事件查询处理器，查询事件记录数，和指定分页的记录，返回给查询者。
        Parameter: 
            frame: 请求消息，data中为EventQueryRequest对象
        Return: 无
        Others: 
        """

        buf = frame.get_data()
        tracelog.info('EventQueryHandler data %s'%buf)
        result = message_across_app.EventQueryResponse()
        result.init_all_attr()
        result.count = 0
        result.event_query_result = []
            
        try:
            req = message_across_app.EventQueryRequest.deserialize(buf)
        except Exception, err:
            tracelog.error('EventQueryHandler deserialize exception: %s'%err)
            result.user_session = ''            
            result.return_code = err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
                                                            , cmd='EventQuery'
                                                            , param_name='EventQueryRequest')
            result.count = 0
            result.event_query_result = []
            self.send_ack(frame, (result.serialize(), ))            
            return
        
        result.user_session = req.user_session
        
        max_query_records_per_page = self.get_worker().get_app().get_global_param().max_query_records_per_page
        return_code, description = param_check.check_page(req.current_page
                                                          , req.num_per_page
                                                          , max_query_records_per_page)  
        
        if return_code!=err_code_mgr.ER_SUCCESS:
            result.return_code = return_code
            result.description = description            
            self.send_ack(frame, (result.serialize(), ))            
            return
        
        return_code, description = param_check.check_filter(req.event_filter)        
        if return_code!=err_code_mgr.ER_SUCCESS:
            result.return_code = return_code
            result.description = description            
            self.send_ack(frame, (result.serialize(), ))            
            return
                
        ret = self.get_worker().get_event_query_processor().count_event_from_db(req.event_filter)
        if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            result.count = 0
            result.event_query_result = []
            self.send_ack(frame, (result.serialize(), ))            
            return
        
        #返回的结果信息在通用的records二维list中
        result.count = ret.get_field('records')[0][0]
        
        ret = self.get_worker().get_event_query_processor().query_event_from_db(req)
        
        if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            result.count = 0
            result.event_query_result = []
            self.send_ack(frame, (result.serialize(), ))            
            return
        
        result.return_code = err_code_mgr.ER_SUCCESS 
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        records = ret.get_field('records')
        count = len(records)
        result.event_query_result = [None]*count
        
        for i in xrange(count):
            display_event = message_across_app.DisplayEvent()
            display_event.init_all_attr()
            display_event.event_sequence_no = records[i][0]
            display_event.event_id = records[i][1]
            display_event.name = records[i][2]
            display_event.level = records[i][3]
            display_event.time = records[i][4]
            display_event.device_type = records[i][5]
            display_event.device_id = records[i][6]
            display_event.object_type = records[i][7]
            display_event.object_id = records[i][8]
            display_event.description = records[i][9]
            display_event.cause = records[i][10]            
            result.event_query_result[i] = display_event
            
        self.send_ack(frame, (result.serialize(), ))
                
        return
    
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
        if frame.get_cmd_code() == command_code.EVENT_QUERY_TO_IMC_REQUEST:
            frame_ack.set_next_pid(self.get_worker().get_pid("IMCGate"))
                    
        for data in datas:
            frame_ack.add_data(data)        
        
        self.get_worker().dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)
        
    
class EventExportHandler(bf.CmdHandler):
    """
    Class: EventExportHandler
    Description: 事件导出处理类
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 消息处理函数，进行必要的参数检查以后，通过事件导出管理器创建一个新任务进行导出
        Parameter: 
            frame: 请求消息，data中为EventExportRequest对象
        Return: 
        Others: 
        """

        buf = frame.get_data()
        result = message_across_app.EventExportResponse()
        result.init_all_attr()
        try:
            req = message_across_app.EventExportRequest.deserialize(buf)
        except Exception:                        
            result.user_session = ''            
            result.return_code = err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
                                                            , cmd='EventExport'
                                                            , param_name='EventExportRequest')
            result.task_no = 0            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return
        
        result.user_session = req.user_session
        
        return_code, description = param_check.check_filter(req.event_filter)        
        if return_code!=err_code_mgr.ER_SUCCESS:
            result.return_code = return_code
            result.description = description            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return
        
        #创建新任务    
        result = self.get_worker().get_event_export_manager().new_task(req)
                                    
        self.get_worker().get_app().send_ack(frame, (result.serialize(), )) 
        

class EventExportTaskQueryHandler(bf.CmdHandler):
    """
    Class: EventExportTaskQueryHandler
    Description: 导出任务查询处理类
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description:调用事件导出管理器查询事件导出任务 
        Parameter: 
            frame: 请求消息，data中为ExportTaskRequest对象
        Return: 
        Others: 
        """

        buf = frame.get_data()
        try:
            req = message_across_app.ExportTaskRequest.deserialize(buf)
        except Exception:
            #
            result = message_across_app.ExportTaskResponse()
            result.init_all_attr()
            result.user_session = ''            
            result.return_code = err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
                                                            , cmd='EventExportTaskQuery'
                                                            , param_name='ExportTaskRequest')
            result.tasks = []            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return        
        
        result = self.get_worker().get_event_export_manager().query_export_task(req)
        
        self.get_worker().get_app().send_ack(frame, (result.serialize(), ))                 

class ClearExportFileTimeoutHandler(bf.TimeOutHandler):
    """
    Class: ClearExportFileTimeoutHandler
    Description: 清除导出文件定时处理类
    Base: TimeOutHandler
    Others: 
    """

    def time_out(self):
        """
        Method: time_out
        Description: 定时处理函数，调用事件导出管理器的clear_export_file函数来进行清除
        Parameter: 无
        Return: 
        Others: 
        """

        self.get_worker().get_event_export_manager().clear_export_file()

class EventFilterListHandler(bf.CmdHandler):
    """
    Class: EventFilterListHandler
    Description: 事件查询的过滤条件列表的查询处理类
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 调用事件查询处理器来查询可用的过滤条件列表
        Parameter: 
            frame: 请求消息，data中为EventFilterListRequest对象
        Return: 
        Others: 
        """

        result = message_across_app.EventFilterListResponse()
        result.init_all_attr()
        
        buf = frame.get_data()        
        try:
            req = message_across_app.EventFilterListRequest.deserialize(buf)
        except Exception:
            result.user_session = ''            
            result.return_code = err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
                                                            , cmd='EventFilterList'
                                                            , param_name='EventFilterListRequest')            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return     
        levels, device_types, object_types = self.get_worker().get_event_query_processor().event_filter_list()
        result.user_session = req.user_session
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.levels = levels
        result.device_types = device_types
        result.object_types = object_types
        
        self.get_worker().get_app().send_ack(frame, (result.serialize(), ))

class EventImcQueryEauHandler(bf.CmdHandler):    
    """
    Class: EventImcQueryEauHandler
    Description: 事件查询处理类
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: 请求处理函数，EventImcQueryEauRequest 对象反序列化成功，进行必要的参数检查，
                                然后发送给指定的EAU，查询该EAU的Event。
        Parameter: 
            frame: 请求消息，data中为 EventImcQueryEauRequest 对象
        Return: 无
        Others: 
        """

        buf = frame.get_data()
        tracelog.info('EventImcQueryEauHandler data %s'%buf)
        result = message_across_app.EventQueryResponse()
        result.init_all_attr()
        result.count = 0
        result.event_query_result = []
        
        
        try:
            req = message_across_app.EventImcQueryEauRequest.deserialize(buf)
        except Exception, err:
            tracelog.error('EventImcQueryEauHandler deserialize exception: %s'%err)
            result.user_session = ''            
            result.return_code = err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_INVALID_DESERIALIZE_STRING_ERROR
                                                            , cmd='EventImcQueryEau'
                                                            , param_name='EventImcQueryEauRequest')            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return
        result.user_session = req.user_session
        
        max_query_records_per_page = self.get_worker().get_app().get_global_param().max_query_records_per_page
        return_code, description = param_check.check_page(req.current_page
                                                          , req.num_per_page
                                                          , max_query_records_per_page)  
        
        if return_code!=err_code_mgr.ER_SUCCESS:
            result.return_code = return_code
            result.description = description            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return
        
        return_code, description = param_check.check_filter(req.event_filter)        
        if return_code!=err_code_mgr.ER_SUCCESS:
            result.return_code = return_code
            result.description = description            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return
        
        #获取eau endpoint的pid
        eau_endpoint = get_eau_endpoint.get_eau_endpoint(req.eau_ip)
        eau_pid = self.get_worker().get_app().get_pid_by_endpiont(eau_endpoint)
        
        if eau_pid==bf.INVALID_PID:
            result.return_code = err_code_mgr.ER_EAU_NOT_REGISTER
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_EAU_NOT_REGISTER, eau_ip=req.eau_ip)            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return
        
        eau_gate_pid = self.get_worker().get_app().get_pid('EAUGate', bf.ONLYLOCAL_PID)
        if eau_gate_pid==bf.INVALID_PID:
            result.return_code = err_code_mgr.ER_EAU_GATE_NOT_ACTIVE
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_EAU_GATE_NOT_ACTIVE)            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return
        
        new_frame = bf.AppFrame()
        new_frame.set_cmd_code(command_code.EVENT_QUERY_TO_IMC_REQUEST)
        new_frame.set_receiver_pid(eau_pid)        
        new_frame.set_next_pid(eau_gate_pid)
        
        eau_req = message_across_app.EventQueryRequest()
        eau_req.init_all_attr()
        eau_req.user_session = req.user_session
        eau_req.current_page = req.current_page
        eau_req.num_per_page = req.num_per_page
        eau_req.event_filter = req.event_filter
        new_frame.add_data(eau_req.serialize())
        
        ack_frames = bf.rpc_request(new_frame, 10)
        if len(ack_frames) == 0:
            result.return_code = err_code_mgr.ER_QUERY_FROM_EAU_TIMEOUT
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_QUERY_FROM_EAU_TIMEOUT, eau_ip=req.eau_ip)            
            self.get_worker().get_app().send_ack(frame, (result.serialize(), ))            
            return
        
        rep = message_across_app.EventQueryResponse.deserialize(ack_frames[0].get_data())
        rep.user_session = req.user_session        
        self.get_worker().get_app().send_ack(frame, (rep.serialize(), ))        
        return

                    
class EventOperationWorker(bf.CmdWorker):    
    """
    Class: EventOperationWorker
    Description: 事件操作worker
    Base: CmdWorker
    Others: 
    """

    def __init__(self):
        """
        Method: __init__
        Description: 对象初始化函数
        Parameter: 无
        Return: 
        Others: 
            __event_query_processor，事件查询处理类
            __event_export_manager，事件导出管理类
        """

        bf.CmdWorker.__init__(self, name = "EventOperationWorker"
                            , min_task_id = worker_taskid_define.EVENT_OPERATION_WORKER_MIN_TASK_ID
                            , max_task_id = worker_taskid_define.EVENT_OPERATION_WORKER_MAX_TASK_ID)
        
        self.__event_query_processor = None
        self.__event_export_manager = None        
    
    def ready_for_work(self):        
        """
        Method: ready_for_work
        Description: 注册handler,设置定时handler为24小时触发一次
        Parameter: 无
        Return: 0，成功
        Others: 
        """

        self.register_handler(EventQueryHandler(), command_code.EVENT_QUERY_REQUEST, command_code.EVENT_QUERY_TO_IMC_REQUEST)
        self.register_handler(EventExportHandler(), command_code.EVENT_EXPORT_REQUEST)
        self.register_handler(EventExportTaskQueryHandler(), command_code.EVENT_EXPORT_TASK_QUERY_REQUEST)
        self.register_handler(EventFilterListHandler(), command_code.EVENT_FILTER_LIST_REQUEST)
        
        #只有IMC上的eventmanager才需要注册该Handler
        #if self.get_app().get_node_type()=='MASTER':
        self.register_handler(EventImcQueryEauHandler(), command_code.EVENT_IMC_QUERY_EAU_REQUEST)
        
        
        param = self.get_app().get_global_param()
        self.__event_query_processor = event_query.EventQueryAndExportProcessor(self.get_app().get_mit_manager()
                                                                                , param.default_language)                
        
        self.get_app().get_mit_manager().regist_custom_function("raw_select_event_from_db"
                                                                , event_query.EventQueryAndExportProcessor.raw_query
                                                                , False)
        
                        
        self.__event_export_manager = event_export_manager.EventExportManager(self.__event_query_processor
                                                                              , self.get_export_event_path()
                                                                              , param.max_running_export_task
                                                                              , param.exported_file_nums_policy
                                                                              , param.exported_file_days_policy
                                                                              )
        
        handler = ClearExportFileTimeoutHandler()
        period = 24*60*60        
        handler.start_timer(period, False)
        #测试代码，便于快速触发
        #handler.start_timer(1, True)
        self.register_time_out_handler(handler)
        
        return 0
    
    def get_event_query_processor(self):
        """
        Method: get_event_query_processor
        Description: 获取事件查询处理对象
        Parameter: 无
        Return: __event_query_processor
        Others: 
        """

        return self.__event_query_processor
    
    def get_event_export_manager(self):
        """
        Method: get_event_export_manager
        Description: 获取事件导出管理对象
        Parameter: 无
        Return: __event_export_manager
        Others: 
        """

        return self.__event_export_manager
    
    def get_export_event_path(self):
        """
        Method: get_export_event_path
        Description: 获取事件导出路径
        Parameter: 无
        Return: 
        Others: 
        """

        export_path = os.path.join(self.get_app().get_app_top_path(), 'data', 'http', 'export_data', 'event')        
        return export_path