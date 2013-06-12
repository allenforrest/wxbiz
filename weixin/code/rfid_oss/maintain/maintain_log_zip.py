#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: maintian_log_manager使用的函数封装
Others:无
Key Class&Method List: 
             1. maintain_log_find 
             2. maintain_log_dumpfile_zip
             3. maintain_log_currentfile_zip
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:新建文件
"""

import os
import time
import re
import zipfile

import tracelog

def maintain_log_find(log_path,start_time,end_time):
    """
    Function: maintain_log_find
    Description: 查找日志目录下的符合要求的日志文件，并且分类为转储日志和当前日志
    Parameter: 
        log_path: 日志文件路径
        start_time: 起始时间
        end_time: 截至时间
    Return: current_file,dumpfile （当前文件列表，转储文件列表）
    Others: 无
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
    Description: 打包压缩转储日志
    Parameter: 
        location: 压缩文件路径
        log_path: 日志文件路径
        task_no: 打包任务号
        dump_file: 转储文件列表
    Return: 无
    Others: 无
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
    Description: 打包压缩当前日志文件
    Parameter: 
        location: 压缩文件路径
        log_path: 日志文件路径
        task_no: 打包任务号
        current_file: 当前文件列表
    Return: 无
    Others: 无
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
                
    