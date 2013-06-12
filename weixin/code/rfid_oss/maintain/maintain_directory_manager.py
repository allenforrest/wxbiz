#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: 目录directory的定时维护：目录directory超过设定大小，按照修改时间顺序删除旧文档
Others:无
Key Class&Method List: 
             1. MaintainDirectoryManager： 目录directory的定时维护：目录directory超过设定大小，按照修改时间顺序删除旧文档
History: 
1. Date:2013-3-19
   Author:ACP2013
   Modification:新建文件
"""

import os

import tracelog
import err_code_mgr
import sequence_no_creator

import event_sender
import bundleframework as bf

class MaintainDirectoryManager():
    """
    Class: MaintainLogManager
    Description: log的定时维护，log按日期打包，log打包任务情况查询的管理
    Base: 无
    Others: 无
    """

    def __init__(self, worker, param, top_path):
        """
        Method: __init__
        Description: 初始化
        Parameter: 
            directory_path: 监控目录路径
            max_size: 监控目录最大大小
            whether_to_report: 是否上报
        Return: 无
        Others: 无
        """

        self.__worker = worker
        self.__directory_info = param
        self.__top_path = top_path
        #print "top path = ", repr(self.__top_path)


    def monitor_directorysize(self):
        """
        Method: monitor_directorysize
        Description: 目录的定时维护
        Parameter: 无
        Return: 无
        Others: 无
        """

        #print "Hello, world!" # for test

        for directory_info in self.__directory_info:
            directory_path = os.path.join(self.__top_path, directory_info.directory_path)
            #unit is M
            directory_maxsize = directory_info.max_size << 20
            directory_whether_to_report = directory_info.whether_to_report

            ## 返回监控目录的大小
            directory_size = self.__get_directorysize(directory_path)
            #print "directory_size = ", directory_size

            ## 检查监控目录大小是否超过设定大小
            if (directory_size > directory_maxsize):
                exceed_size = directory_size - 0.7 * directory_maxsize
                ## 将监控目录排序，并且删除旧文件，将大小控制在70%，如果需要上报就报告给monitor
                self.__maintain_directory(directory_path, exceed_size,directory_whether_to_report)


    def __send_event(self, dirname, filename):
        """
       Method: __send_event
       Description: 发送消息指数据库
       Parameter: dirname, filename
       Return: 无
       Others: 无
       """
        event_data = event_sender.EventData()
        event_data.set_event_id('event.MaintainApp.0')
        event_data.set_object_id("maintain_app")
        event_data.set_device_id(self.__worker.get_app().get_device_id())
        
        # dirname是从数据库中读取出来的，已经是utf-8编码的，无需再次编码
        # 另外，目前我们Linux系统默认使用了utf-8编码，windows默认使用了gbk
        try:
            filename = filename.decode("gbk").encode("UTF-8")
        except:
            pass
        params = {'file_name': filename, 'dir_name': dirname}
        event_data.set_params(params)
        event_sender.send_event(event_data)


    def __maintain_directory(self, directory_path, exceed_size, directory_whether_to_report):
        """
        :param directory_path:
        :param exceed_size:
        Method: sort_directory
        Description: 递归得到目录下所有文件，包括子目录
        Parameter: directory_path, exceed_size
        Return: 目录及子目录下所有文件
        Others: 无
        """

        # 得到监控目录下文件并且排序
        total_files = self.__get_files_in_directory(directory_path)
        total_files.sort()

        """print "after sorted: "

        for filename in total_files:
            print "file:", filename[2]"""

        filesize = 0
        count = 0
        while (filesize < exceed_size):

            filepath = total_files[count][2]
            # print "what to be removed: ", filepath
            try:
                os.remove(filepath)
                tracelog.info("%s was be deleted successfully!" % filepath)

                filesize += total_files[count][1]
                ## 事件上报：将成功删除文件的消息上报至数据库
                if directory_whether_to_report:
                    self.__send_event(directory_path, filepath)
            except:
                # 如果失败删除就将这条消息打印到日志log中
                tracelog.exception("%s failed to be deleted" % filepath)
            count += 1


    def __get_files_in_directory(self, directory_path):
        """
        :param directory_path:
        Method: __get_files_in_directory
        Description: 递归得到目录下所有文件，包括子目录
        Parameter: directory_path
        Return: 目录及子目录下所有文件
         Others: 无
        """

        # 将total_file初始化
        total_files = []

        # 递归将子目录下的文件增加到"total_file"中
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                #print "filepath =", filepath  ### for test
                var = (os.path.getmtime(filepath), os.path.getsize(filepath), filepath)
                total_files.append(var)

        return total_files


    def __get_directorysize(self, directory_path):
        """

        :param directory_path:
        Method: get_directorysize
        Description: 递归计算目录大小
        Parameter: directory_path
        Return: 文件夹大小
        Others: 无
        """

        # 将文件总大小total_size初始化
        total_size = 0
        # print "directory_path = ", directory_path
        # 递归将子目录下文件大小累计至"total_size"
        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                #print "filepath = ", filepath
                total_size += os.path.getsize(filepath)

        return total_size

    """##recursively add the size of files in subdirectories of "directory_path" to "total_size"
            for item in os.listdir(directory_path)
                itempath = os.path.join(directory_path, item)
                if(os.path.isfile(itempath))
                   total_size += os.path.getsize(itempath)
                elif(os.path.isdir(itempath))
                   total_size += __get_directorysize(itempath)
            return total_size
    """
        
