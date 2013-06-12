#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-13
Description: event���� worker����Ӧ��handler������
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
   Modification:�½��ļ�
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
    Description: �¼���ѯ������
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: �������������EventQueryRequest�������л��ɹ������б�Ҫ�Ĳ�����飬
                                Ȼ������¼���ѯ����������ѯ�¼���¼������ָ����ҳ�ļ�¼�����ظ���ѯ�ߡ�
        Parameter: 
            frame: ������Ϣ��data��ΪEventQueryRequest����
        Return: ��
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
        
        #���صĽ����Ϣ��ͨ�õ�records��άlist��
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
        Description: ����ԭʼ����frame����datas���͸�������
        Parameter: 
            frame: ԭʼ����frame
            datas: ��Ҫ���͵�data���б�
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
    Description: �¼�����������
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ��Ϣ�����������б�Ҫ�Ĳ�������Ժ�ͨ���¼���������������һ����������е���
        Parameter: 
            frame: ������Ϣ��data��ΪEventExportRequest����
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
        
        #����������    
        result = self.get_worker().get_event_export_manager().new_task(req)
                                    
        self.get_worker().get_app().send_ack(frame, (result.serialize(), )) 
        

class EventExportTaskQueryHandler(bf.CmdHandler):
    """
    Class: EventExportTaskQueryHandler
    Description: ���������ѯ������
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description:�����¼�������������ѯ�¼��������� 
        Parameter: 
            frame: ������Ϣ��data��ΪExportTaskRequest����
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
    Description: ��������ļ���ʱ������
    Base: TimeOutHandler
    Others: 
    """

    def time_out(self):
        """
        Method: time_out
        Description: ��ʱ�������������¼�������������clear_export_file�������������
        Parameter: ��
        Return: 
        Others: 
        """

        self.get_worker().get_event_export_manager().clear_export_file()

class EventFilterListHandler(bf.CmdHandler):
    """
    Class: EventFilterListHandler
    Description: �¼���ѯ�Ĺ��������б�Ĳ�ѯ������
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: �����¼���ѯ����������ѯ���õĹ��������б�
        Parameter: 
            frame: ������Ϣ��data��ΪEventFilterListRequest����
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
    Description: �¼���ѯ������
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method: handle_cmd
        Description: ����������EventImcQueryEauRequest �������л��ɹ������б�Ҫ�Ĳ�����飬
                                Ȼ���͸�ָ����EAU����ѯ��EAU��Event��
        Parameter: 
            frame: ������Ϣ��data��Ϊ EventImcQueryEauRequest ����
        Return: ��
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
        
        #��ȡeau endpoint��pid
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
    Description: �¼�����worker
    Base: CmdWorker
    Others: 
    """

    def __init__(self):
        """
        Method: __init__
        Description: �����ʼ������
        Parameter: ��
        Return: 
        Others: 
            __event_query_processor���¼���ѯ������
            __event_export_manager���¼�����������
        """

        bf.CmdWorker.__init__(self, name = "EventOperationWorker"
                            , min_task_id = worker_taskid_define.EVENT_OPERATION_WORKER_MIN_TASK_ID
                            , max_task_id = worker_taskid_define.EVENT_OPERATION_WORKER_MAX_TASK_ID)
        
        self.__event_query_processor = None
        self.__event_export_manager = None        
    
    def ready_for_work(self):        
        """
        Method: ready_for_work
        Description: ע��handler,���ö�ʱhandlerΪ24Сʱ����һ��
        Parameter: ��
        Return: 0���ɹ�
        Others: 
        """

        self.register_handler(EventQueryHandler(), command_code.EVENT_QUERY_REQUEST, command_code.EVENT_QUERY_TO_IMC_REQUEST)
        self.register_handler(EventExportHandler(), command_code.EVENT_EXPORT_REQUEST)
        self.register_handler(EventExportTaskQueryHandler(), command_code.EVENT_EXPORT_TASK_QUERY_REQUEST)
        self.register_handler(EventFilterListHandler(), command_code.EVENT_FILTER_LIST_REQUEST)
        
        #ֻ��IMC�ϵ�eventmanager����Ҫע���Handler
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
        #���Դ��룬���ڿ��ٴ���
        #handler.start_timer(1, True)
        self.register_time_out_handler(handler)
        
        return 0
    
    def get_event_query_processor(self):
        """
        Method: get_event_query_processor
        Description: ��ȡ�¼���ѯ�������
        Parameter: ��
        Return: __event_query_processor
        Others: 
        """

        return self.__event_query_processor
    
    def get_event_export_manager(self):
        """
        Method: get_event_export_manager
        Description: ��ȡ�¼������������
        Parameter: ��
        Return: __event_export_manager
        Others: 
        """

        return self.__event_export_manager
    
    def get_export_event_path(self):
        """
        Method: get_export_event_path
        Description: ��ȡ�¼�����·��
        Parameter: ��
        Return: 
        Others: 
        """

        export_path = os.path.join(self.get_app().get_app_top_path(), 'data', 'http', 'export_data', 'event')        
        return export_path