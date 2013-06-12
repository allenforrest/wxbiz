#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-10
Description: event导出管理类，负责管理event导出任务
Others:      
Key Class&Method List: 
             1. EventExportManager
             2. EventExportTaskThread
History: 
1. Date:2012-12-10
   Author:ACP2013
   Modification:新建文件
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

#导出CSV文件的文件头                    
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
    Description: event导出管理类，可以创建新的导出任务，查询导出任务的运行状态，根据规则定期清除导出的文件
    Base: 无
    Others: 
        __event_query_processor，事件查询处理器对象
        __running_task_no，当前运行的任务号
        __task_no_creator，任务号生成器
        __export_path，导出的目录
        __max_running_export_task，最大可以同时运行的任务数
        __exported_file_nums_policy，导出文件的按数量清理的规则
        __exported_file_days_policy，导出文件的按日期清理的规则
        __lock，互斥锁，用于保证不同任务线程更新任务状态时互斥
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
        Description: 返回__event_query_processor对象
        Parameter: 无
        Return: __event_query_processor
        Others: 
        """

        return self.__event_query_processor
    
    def new_task(self, event_export_request):
        """
        Method: new_task
        Description: 创建一个新的导出任务，先判断是否已经达到任务的最大限制了，再创建一个新的EventExportTaskThread对象，并且启动线程进行任务处理
        Parameter: 
            event_export_request: 导出任务请求参数
        Return: EventExportResponse对象
        Others: 
        """

        result = message_across_app.EventExportResponse()
        result.init_all_attr()
        result.user_session = event_export_request.user_session
        
        if len(self.__running_task_no)>=self.__max_running_export_task:
            result.return_code = err_code_mgr.ER_MAX_EXPORT_TASK_LIMIT
            
            #错误信息的编码以后要改为UTF-8，因此这里不再考虑转码
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
        Description: 更新任务状态到__task_info_map，如果任务已经完成，从__running_task_no中清除
        Parameter: 
            task_info: 任务信息
        Return: 无
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
        Description: 查询导出任务信息，可以查询指定task_no的任务，也可以查询所有任务，并且包含__task_info_map中已经不存在，但是导出目录中有文件的任务信息
        Parameter: 
            export_task_request: 查询参数
        Return: ExportTaskResponse对象
        Others: 
        """

        result = message_across_app.ExportTaskResponse()
        result.init_all_attr()
        result.user_session = export_task_request.user_session
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.tasks = []
        
        with self.__lock:
            #查询指定任务
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
                        
            #查询全部任务，以及其他文件                
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
                    
        # 查询结果中，需要将文件路径，修改为http的相对路径
        for task_info in result.tasks:
            file_name = os.path.basename(task_info.location)

            # 这里不使用os.path.join，因为web只认'/'
            new_path = "export_data/event/" + file_name
            task_info.location = new_path
        return result
    
    def clear_export_file(self):
        """
        Method: clear_export_file
        Description: 根据清除策略清除导出的文件，有两种策略，一种是根据文件数量来清除早前的文件；另一种是根据时间来清除早前的文件
        Parameter: 无
        Return: 无
        Others: 
        """

        locations = glob.glob(os.path.join(self.__export_path,'export_event_*_task_*.csv'))
        tmp_locations = {}        
        
        #按时间删除        
        exported_second = self.__exported_file_days_policy*24*60*60
        
        #测试代码，便于触发条件
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
        
        #按数量删除删除最旧的
        clear_num = len(tmp_locations)-self.__exported_file_nums_policy
        if clear_num>0:
            #根据时间进行排序
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
    Description: 导出任务处理线程，主要包括event信息查询，以及将查询后的信息写入到CSV文件中。
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
            __manager，导出任务manager
            __request,导出请求参数
            __task_info，任务信息
        """

        threading.Thread.__init__(self)
        self.__manager = manager
        self.__request = event_export_request
        self.__task_info = task_info
        
    def run(self):
        """
        Method: run
        Description: 线程工作函数，主要包括event信息查询，以及将查询后的信息写入到CSV文件中
        Parameter: 无
        Return: 
        Others: 
        """

        #查询 
        ret = self.__manager.get_event_query_processor().export_event_from_db(self.__request.event_filter)
        if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
            task_info = copy.copy(self.__task_info)
            task_info.status = 'failed'
            self.__manager.update_task_status(task_info)
            tracelog.error('export task %d %s %s'%(task_info.task_no, task_info.status, ret.get_msg()))
            return
        
        records = ret.get_field('records')
        
        #写CSV文件
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
        
        
        
    
    
