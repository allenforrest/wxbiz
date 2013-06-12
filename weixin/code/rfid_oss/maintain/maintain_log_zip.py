#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: maintian_log_managerʹ�õĺ�����װ
Others:��
Key Class&Method List: 
             1. maintain_log_find 
             2. maintain_log_dumpfile_zip
             3. maintain_log_currentfile_zip
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:�½��ļ�
"""

import os
import time
import re
import zipfile

import tracelog

def maintain_log_find(log_path,start_time,end_time):
    """
    Function: maintain_log_find
    Description: ������־Ŀ¼�µķ���Ҫ�����־�ļ������ҷ���Ϊת����־�͵�ǰ��־
    Parameter: 
        log_path: ��־�ļ�·��
        start_time: ��ʼʱ��
        end_time: ����ʱ��
    Return: current_file,dumpfile ����ǰ�ļ��б�ת���ļ��б�
    Others: ��
    """

    current_file = []
    dumpfile_map = {}
    dumpmatch = r'\w+_\d+_(\d{4}_(\d{2}_){4}\d{2})\.(log|zip)$'
    for f in os.listdir(log_path):
        dumptemp = re.match(dumpmatch,f)
        if dumptemp is not None:
            try:
                filetime = time.strptime(dumptemp.group(1), '%Y_%m_%d_%H_%M_%S')
                filetime = time.mktime(filetime)
                dumpfile_map[f] = filetime
            except Exception, err:
                tracelog.error('find unknow log: (%s)and exception %s'% (dumptemp.group(1),err))
        else:
            current_file.append(f)
    
    if start_time is not None:
        for key in dumpfile_map.keys():
            if dumpfile_map[key]<start_time:
                del dumpfile_map[key]
                         
    if end_time is not None and end_time<time.time():
        current_file = []
        for key in dumpfile_map.keys():
            if dumpfile_map[key]>end_time:
                del dumpfile_map[key]
    return current_file,dumpfile_map.keys()

def maintain_log_dumpfile_zip(location,log_path,task_no,dump_file):
    """
    Function: maintain_log_dumpfile_zip
    Description: ���ѹ��ת����־
    Parameter: 
        location: ѹ���ļ�·��
        log_path: ��־�ļ�·��
        task_no: ��������
        dump_file: ת���ļ��б�
    Return: ��
    Others: ��
    """

    openzipfile = None
    for f in dump_file:  
        try:
            openzipfile = zipfile.ZipFile(location, 'a', zipfile.ZIP_DEFLATED)
            openzipfile.write(os.path.join(log_path,f),f)
        except Exception, err:
            tracelog.error('log export task %d %s'%(task_no,err))
        finally:
            if openzipfile is not None:
                openzipfile.close()
    
def maintain_log_currentfile_zip(location,log_path,task_no,current_file): 
    """
    Function: maintain_log_currentfile_zip
    Description: ���ѹ����ǰ��־�ļ�
    Parameter: 
        location: ѹ���ļ�·��
        log_path: ��־�ļ�·��
        task_no: ��������
        current_file: ��ǰ�ļ��б�
    Return: ��
    Others: ��
    """

    openfile = None
    openzipfile = None
    log_file = None
    for f in current_file:
        try:
            temp_file_name = '%s_%s.log'%(f[:-4],time.strftime("%Y_%m_%d_%H_%M_%S"))
            openfile = open(os.path.join(log_path,f),'r')
            log_file = openfile.read()
        except Exception, err:
            tracelog.error('log export task %d %s'%(task_no,err))
            continue
        finally:
            if openfile is not None:
                openfile.close()
            
        try:
            openzipfile = zipfile.ZipFile(location, 'a', zipfile.ZIP_DEFLATED)
            openzipfile.writestr(os.path.join(temp_file_name), log_file)
        except Exception, err:
            tracelog.error('log export task %d %s'%(task_no,err))
        finally:
            if openzipfile is not None:
                openzipfile.close()
                
    