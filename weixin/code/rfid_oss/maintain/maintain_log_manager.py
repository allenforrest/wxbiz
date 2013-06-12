#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: log�Ķ�ʱά����log�����ڴ����log������������ѯ�Ĺ���
Others:��
Key Class&Method List: 
             1. MaintainLogManager�� log�Ķ�ʱά����log�����ڴ����log������������ѯ�Ĺ���
             2. MaintainLogExportTaskThread�� log�����ڴ��ʱ���̴߳���
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:�½��ļ�
"""

import os, os.path
import time
import threading
import copy
import zipfile
import glob
import re
import collections

import tracelog
import err_code_mgr
import sequence_no_creator

import maintain_log_params
import maintain_log_zip

class MaintainLogManager():
    """
    Class: MaintainLogManager
    Description: log�Ķ�ʱά����log�����ڴ����log������������ѯ�Ĺ���
    Base: ��
    Others: ��
    """

    def __init__(self, log_path,export_log_path,max_running_export_task):
        """
        Method: __init__
        Description: ��ʼ��
        Parameter: 
            log_path: ��־·��
            export_log_path: �����־���·��
            max_running_export_task: ���������
        Return: ��
        Others: ��
        """

        self.__task_info_map = {}
        self.__running_task_no = set()
        
        self.__task_no_creator = sequence_no_creator.SequenceNoCreator()        
        self.__task_no_creator.init_creator(2**32, int(time.time()))
        self.__log_path = log_path  
        self.__export_log_path = export_log_path
        self.__max_running_export_task = max_running_export_task
        self.__lock = threading.RLock()
        
    def new_task(self, event_export_request):
        """
        Method: new_task
        Description: �����־
        Parameter: 
            event_export_request:�����־����������Ǹ�PackageLog����
        Return: result������ţ�
        Others: ��
        """

        result = maintain_log_params.PackageLogHandlerResult()
        result.init_all_attr()
        
        if len(self.__running_task_no)>=self.__max_running_export_task:
            result.prepare_for_ack(event_export_request
                                   , err_code_mgr.ER_MAINTAINGLOG_MAX_EXPORT_TASK_LIMIT
                                   , err_code_mgr.get_error_msg(err_code_mgr.ER_MAINTAINGLOG_MAX_EXPORT_TASK_LIMIT))            
            result.task_no = 0
            return result
              
        task_info = maintain_log_params.PackageLogExportTask()
        task_info.init_all_attr()
        task_info.task_no = self.__task_no_creator.get_new_no()
        task_info.status = 'running'
        file_name = 'PACKAGE_LOG_%s.zip'%(time.strftime("%Y_%m_%d_%H_%M_%S"))
        task_info.location = os.path.join(self.__export_log_path, file_name)
        
        with self.__lock:
            self.__task_info_map[task_info.task_no] = task_info
            self.__running_task_no.add(task_info.task_no)
        
        export_thd = MaintainLogExportTaskThread(self,event_export_request,copy.copy(task_info),self.__log_path)
        export_thd.start()
        
        result.prepare_for_ack(event_export_request
                               , err_code_mgr.ER_SUCCESS
                               , err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS))        
        result.task_no = task_info.task_no
        
        return result
    
    def update_task_status(self, task_info):
        """
        Method: update_task_status
        Description: ��������״̬
        Parameter: 
            task_info: �����
        Return: ��
        Others: ��
        """

        with self.__lock:
            if self.__task_info_map.has_key(task_info.task_no):
                self.__task_info_map[task_info.task_no] = task_info
            
            if task_info.status in ('finished', 'failed', 'file_empty') :
                self.__running_task_no.discard(task_info.task_no)
                
    def query_export_task(self, export_task_request):
        """
        Method: query_export_task
        Description: log������������ѯ
        Parameter: 
            export_task_request: �鿴��������������Ǹ�PackageLogExportTaskRequest����
        Return: result�����������Ϣ���Ǹ�PackageLogExportTaskResponse����
        Others: ��
        """

        result = maintain_log_params.PackageLogExportTaskResponse()
        result.init_all_attr()
        result.prepare_for_ack(export_task_request
                               , err_code_mgr.ER_SUCCESS
                               , err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS))        
        result.tasks = []
        
        with self.__lock:
            #��ѯָ������
            if isinstance(export_task_request.task_nos, list) and len(export_task_request.task_nos)>0:
                for task_no in export_task_request.task_nos:
                    if self.__task_info_map.has_key(task_no):
                        result.tasks.append(copy.copy(self.__task_info_map[task_no]))
                    else:
                        task_info = maintain_log_params.PackageLogExportTask()
                        task_info.init_all_attr()
                        task_info.task_no = task_no
                        task_info.status = 'unknown'
                        task_info.location = ''
                        result.tasks.append(task_info)
                        
            #��ѯȫ�������Լ������ļ�                
            else:
                locations = glob.glob(os.path.join(self.__export_log_path,'*.zip'))                
                locations_set = set(locations)
                
                for task_info in self.__task_info_map.itervalues():
                    result.tasks.append(copy.copy(task_info))                    
                    locations_set.discard(task_info.location)
                    
                for location in locations_set:
                    task_info = maintain_log_params.PackageLogExportTask()
                    task_info.init_all_attr()
                    task_info.task_no = 0
                    task_info.status = 'unknown'
                    task_info.location = location
                    result.tasks.append(task_info)

        # ��ѯ����У���Ҫ���ļ�·�����޸�Ϊhttp�����·��
        for task_info in result.tasks:
            file_name = os.path.basename(task_info.location)

            # ���ﲻʹ��os.path.join����Ϊwebֻ��'/'
            new_path = "export_data/log/" + file_name
            task_info.location = new_path
        
        return result
    
    def zip_file(self):
        """
        Method: zip_file
        Description: log�Ķ�ʱά��
        Parameter: ��
        Return: ��
        Others: ��
        """

        dumpfile_map = {}
        dumpmatch = r'\w+_\d+_(\d{4}_(\d{2}_){4}\d{2})\.log$'
        for f in os.listdir(self.__log_path):
            dumptemp = re.match(dumpmatch,f)
            if dumptemp is not None:
                try:
                    filetime = time.strptime(dumptemp.group(1), '%Y_%m_%d_%H_%M_%S')
                    filetime = time.mktime(filetime)
                    dumpfile_map[f] = filetime
                except Exception, err:
                    tracelog.error('find unknow log: (%s) and exception %s'% (dumptemp.group(1),err))     
        
        #����ɵ�
        if len(dumpfile_map)>0:
            ordered = collections.OrderedDict(sorted(dumpfile_map.items(), key=lambda t: t[1]))            
            rmv = ordered.popitem(False)[0]
            openzipfile = None
            try:
                zip_file_name = '%s.zip' % rmv[:-4]
                openzipfile = zipfile.ZipFile(os.path.join(self.__log_path,zip_file_name), 'w', zipfile.ZIP_DEFLATED)
                openzipfile.write(os.path.join(self.__log_path,rmv),rmv)
                os.remove(os.path.join(self.__log_path,rmv))
            except Exception, err:
                tracelog.error('zip_file exception %s'% err)
            finally:
                if openzipfile is not None:
                    openzipfile.close()     
			


class MaintainLogExportTaskThread(threading.Thread):
    """
    Class: MaintainLogExportTaskThread
    Description: log�����ڴ��ʱ���̴߳���
    Base: Thread
    Others: ��
    """

    def __init__(self,manager,event_export_request,task_info,log_path):
        """
        Method: __init__
        Description: ��ʼ��
        Parameter: 
            manager: ��������־��manager����
            event_export_request: �����־����������Ǹ�PackageLog����
            task_info: �����
            log_path: ��־·��
        Return: ��
        Others: ��
        """

        threading.Thread.__init__(self)
        self.__manager = manager
        self.__request = event_export_request
        self.__task_info = task_info
        self.__log_path = log_path
        
    def run(self):
        """
        Method: run
        Description: �߳�����
        Parameter: ��
        Return: ��
        Others: ��
        """

        current_file,dump_file = maintain_log_zip.maintain_log_find(self.__log_path
                                                                       ,self.__request.start_time
                                                                       ,self.__request.end_time)
        task_info = self.__task_info
        
        #û���ļ���Ҫ���
        if len(current_file)==0 and len(dump_file)==0:
            task_info.status = 'file_empty'
            task_info.location = ''
            self.__manager.update_task_status(task_info)
            tracelog.info('no log files between the requested time')
            return
            
        maintain_log_zip.maintain_log_dumpfile_zip(task_info.location
                                                   , self.__log_path, task_info.task_no
                                                   , dump_file)    
        
        maintain_log_zip.maintain_log_currentfile_zip(task_info.location
                                                   , self.__log_path, task_info.task_no
                                                   , current_file)
        
        try:
            mytestzip = zipfile.ZipFile(task_info.location, 'r')
            if mytestzip.testzip() is not None:
                task_info.status = 'failed'
                self.__manager.update_task_status(task_info)
                tracelog.error('log export task %d %s'%(task_info.task_no,"Zip File have been damaged"))
            mytestzip.close()
        except Exception, err:
            task_info.status = 'failed'
            self.__manager.update_task_status(task_info)
            tracelog.error('log export task %d %s'%(task_info.task_no,err))
            return
        
        task_info.status = 'finished'
        self.__manager.update_task_status(task_info)
        return
                
