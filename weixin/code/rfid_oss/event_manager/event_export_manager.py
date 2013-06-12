#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-10
Description: event���������࣬�������event��������
Others:      
Key Class&Method List: 
             1. EventExportManager
             2. EventExportTaskThread
History: 
1. Date:2012-12-10
   Author:ACP2013
   Modification:�½��ļ�
"""

import os
import os.path
import time
import threading
import copy
import csv
import glob
import collections

import tracelog
import err_code_mgr

import sequence_no_creator
import message_across_app

#����CSV�ļ����ļ�ͷ                    
CSV_FILE_HEADER = ['event_sequence_no'
                 , 'event_id'
                 , 'name'
                 , 'level'
                 , 'time'
                 , 'device_type'
                 , 'device_id'
                 , 'object_type'
                 , 'object_id'
                 , 'description'
                 , 'cause'                 
                ]

class EventExportManager():    
    """
    Class: EventExportManager
    Description: event���������࣬���Դ����µĵ������񣬲�ѯ�������������״̬�����ݹ���������������ļ�
    Base: ��
    Others: 
        __event_query_processor���¼���ѯ����������
        __running_task_no����ǰ���е������
        __task_no_creator�������������
        __export_path��������Ŀ¼
        __max_running_export_task��������ͬʱ���е�������
        __exported_file_nums_policy�������ļ��İ���������Ĺ���
        __exported_file_days_policy�������ļ��İ���������Ĺ���
        __lock�������������ڱ�֤��ͬ�����̸߳�������״̬ʱ����
    """

    def __init__(self, event_query_processor, export_path
                 , max_running_export_task, exported_file_nums_policy, exported_file_days_policy):
        self.__event_query_processor = event_query_processor
        
        self.__task_info_map = {}
        self.__running_task_no = set()
        
        self.__task_no_creator = sequence_no_creator.SequenceNoCreator()        
        self.__task_no_creator.init_creator(2**32, int(time.time()))
        self.__export_path = export_path
        self.__max_running_export_task = max_running_export_task
        self.__exported_file_nums_policy = exported_file_nums_policy
        self.__exported_file_days_policy = exported_file_days_policy
        
        
        self.__lock = threading.RLock()

    def get_event_query_processor(self):
        """
        Method: get_event_query_processor
        Description: ����__event_query_processor����
        Parameter: ��
        Return: __event_query_processor
        Others: 
        """

        return self.__event_query_processor
    
    def new_task(self, event_export_request):
        """
        Method: new_task
        Description: ����һ���µĵ����������ж��Ƿ��Ѿ��ﵽ�������������ˣ��ٴ���һ���µ�EventExportTaskThread���󣬲��������߳̽���������
        Parameter: 
            event_export_request: ���������������
        Return: EventExportResponse����
        Others: 
        """

        result = message_across_app.EventExportResponse()
        result.init_all_attr()
        result.user_session = event_export_request.user_session
        
        if len(self.__running_task_no)>=self.__max_running_export_task:
            result.return_code = err_code_mgr.ER_MAX_EXPORT_TASK_LIMIT
            
            #������Ϣ�ı����Ժ�Ҫ��ΪUTF-8��������ﲻ�ٿ���ת��
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_MAX_EXPORT_TASK_LIMIT)
            result.task_no = 0
            return result
        
        task_info = message_across_app.ExportTask()
        task_info.init_all_attr()
        task_info.task_no = self.__task_no_creator.get_new_no()
        task_info.status = 'running'
        file_name = 'export_event_%s_task_%d.csv'%(time.strftime('%Y-%m-%d-%H-%M-%S'), task_info.task_no)
        task_info.location = os.path.join(self.__export_path, file_name)
        
        with self.__lock:
            self.__task_info_map[task_info.task_no] = task_info
            self.__running_task_no.add(task_info.task_no)
        
        export_thd = EventExportTaskThread(self, event_export_request, copy.copy(task_info))
        export_thd.start()
        
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.task_no = task_info.task_no
        
        return result
    
    def update_task_status(self, task_info):
        """
        Method: update_task_status
        Description: ��������״̬��__task_info_map����������Ѿ���ɣ���__running_task_no�����
        Parameter: 
            task_info: ������Ϣ
        Return: ��
        Others: 
        """

        with self.__lock:
            if self.__task_info_map.has_key(task_info.task_no):
                self.__task_info_map[task_info.task_no] = task_info
            
            if task_info.status in ('finished', 'failed', 'file_empty') :
                self.__running_task_no.discard(task_info.task_no)
    
    def query_export_task(self, export_task_request):
        """
        Method: query_export_task
        Description: ��ѯ����������Ϣ�����Բ�ѯָ��task_no������Ҳ���Բ�ѯ�������񣬲��Ұ���__task_info_map���Ѿ������ڣ����ǵ���Ŀ¼�����ļ���������Ϣ
        Parameter: 
            export_task_request: ��ѯ����
        Return: ExportTaskResponse����
        Others: 
        """

        result = message_across_app.ExportTaskResponse()
        result.init_all_attr()
        result.user_session = export_task_request.user_session
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.tasks = []
        
        with self.__lock:
            #��ѯָ������
            if isinstance(export_task_request.task_nos, list) and len(export_task_request.task_nos)>0:
                for task_no in export_task_request.task_nos:
                    if self.__task_info_map.has_key(task_no):
                        result.tasks.append(copy.copy(self.__task_info_map[task_no]))
                    else:
                        task_info = message_across_app.ExportTask()
                        task_info.init_all_attr()
                        task_info.task_no = task_no
                        task_info.status = 'unknown'
                        task_info.location = ''
                        result.tasks.append(task_info)
                        
            #��ѯȫ�������Լ������ļ�                
            else:
                locations = glob.glob(os.path.join(self.__export_path,'export_event_*_task_*.csv'))                
                locations_set = set(locations)
                
                for task_info in self.__task_info_map.itervalues():
                    result.tasks.append(copy.copy(task_info))                    
                    locations_set.discard(task_info.location)
                    
                for location in locations_set:
                    task_info = message_across_app.ExportTask()
                    task_info.init_all_attr()
                    task_info.task_no = 0
                    task_info.status = 'unknown'
                    task_info.location = location
                    result.tasks.append(task_info)
                    
        # ��ѯ����У���Ҫ���ļ�·�����޸�Ϊhttp�����·��
        for task_info in result.tasks:
            file_name = os.path.basename(task_info.location)

            # ���ﲻʹ��os.path.join����Ϊwebֻ��'/'
            new_path = "export_data/event/" + file_name
            task_info.location = new_path
        return result
    
    def clear_export_file(self):
        """
        Method: clear_export_file
        Description: ���������������������ļ��������ֲ��ԣ�һ���Ǹ����ļ������������ǰ���ļ�����һ���Ǹ���ʱ���������ǰ���ļ�
        Parameter: ��
        Return: ��
        Others: 
        """

        locations = glob.glob(os.path.join(self.__export_path,'export_event_*_task_*.csv'))
        tmp_locations = {}        
        
        #��ʱ��ɾ��        
        exported_second = self.__exported_file_days_policy*24*60*60
        
        #���Դ��룬���ڴ�������
        #exported_second = 4*60*60
        current_time = time.time()
        for location in locations:
            try:
                file_name = os.path.basename(location)                
                st_ctime = time.mktime(time.strptime(file_name.split('_')[2], '%Y-%m-%d-%H-%M-%S'))
                if (current_time-st_ctime)>=exported_second:
                    os.remove(location)
                else:
                    tmp_locations[location] = st_ctime                    
            except Exception, err:
                tracelog.error('clear export file exception %s'% err)
        
        #������ɾ��ɾ����ɵ�
        clear_num = len(tmp_locations)-self.__exported_file_nums_policy
        if clear_num>0:
            #����ʱ���������
            ordered_locations = collections.OrderedDict(sorted(tmp_locations.items(), key=lambda t: t[1]))            
            rmv_locations = ordered_locations.keys()[:clear_num]            
            for location in rmv_locations:
                try:
                    os.remove(location)                
                except Exception, err:
                    tracelog.error('clear export file exception %s'% err)
            

class EventExportTaskThread(threading.Thread):
    """
    Class: EventExportTaskThread
    Description: �����������̣߳���Ҫ����event��Ϣ��ѯ���Լ�����ѯ�����Ϣд�뵽CSV�ļ��С�
    Base: threading.Thread
    Others: 
    """

    def __init__(self, manager, event_export_request, task_info):
        """
        Method: __init__
        Description: 
        Parameter: 
            manager: 
            event_export_request: 
            task_info: 
        Return: 
        Others: 
            __manager����������manager
            __request,�����������
            __task_info��������Ϣ
        """

        threading.Thread.__init__(self)
        self.__manager = manager
        self.__request = event_export_request
        self.__task_info = task_info
        
    def run(self):
        """
        Method: run
        Description: �̹߳�����������Ҫ����event��Ϣ��ѯ���Լ�����ѯ�����Ϣд�뵽CSV�ļ���
        Parameter: ��
        Return: 
        Others: 
        """

        #��ѯ 
        ret = self.__manager.get_event_query_processor().export_event_from_db(self.__request.event_filter)
        if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
            task_info = copy.copy(self.__task_info)
            task_info.status = 'failed'
            self.__manager.update_task_status(task_info)
            tracelog.error('export task %d %s %s'%(task_info.task_no, task_info.status, ret.get_msg()))
            return
        
        records = ret.get_field('records')
        
        #дCSV�ļ�
        try:
            writer=csv.writer(open(self.__task_info.location, 'wb'))
            writer.writerow(CSV_FILE_HEADER)
            writer.writerows(records)
        except Exception, err:
            task_info = copy.copy(self.__task_info)
            task_info.status = 'failed'
            self.__manager.update_task_status(task_info)
            tracelog.error('export task %d %s %s'%(task_info.task_no, task_info.status, err))
            return
        
        task_info = copy.copy(self.__task_info)
        task_info.status = 'finished'
        self.__manager.update_task_status(task_info)
        
        return
        
        
        
    
    
