#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: Ŀ¼directory�Ķ�ʱά����Ŀ¼directory�����趨��С�������޸�ʱ��˳��ɾ�����ĵ�
Others:��
Key Class&Method List: 
             1. MaintainDirectoryManager�� Ŀ¼directory�Ķ�ʱά����Ŀ¼directory�����趨��С�������޸�ʱ��˳��ɾ�����ĵ�
History: 
1. Date:2013-3-19
   Author:ACP2013
   Modification:�½��ļ�
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
    Description: log�Ķ�ʱά����log�����ڴ����log������������ѯ�Ĺ���
    Base: ��
    Others: ��
    """

    def __init__(self, worker, param, top_path):
        """
        Method: __init__
        Description: ��ʼ��
        Parameter: 
            directory_path: ���Ŀ¼·��
            max_size: ���Ŀ¼����С
            whether_to_report: �Ƿ��ϱ�
        Return: ��
        Others: ��
        """

        self.__worker = worker
        self.__directory_info = param
        self.__top_path = top_path
        #print "top path = ", repr(self.__top_path)


    def monitor_directorysize(self):
        """
        Method: monitor_directorysize
        Description: Ŀ¼�Ķ�ʱά��
        Parameter: ��
        Return: ��
        Others: ��
        """

        #print "Hello, world!" # for test

        for directory_info in self.__directory_info:
            directory_path = os.path.join(self.__top_path, directory_info.directory_path)
            #unit is M
            directory_maxsize = directory_info.max_size << 20
            directory_whether_to_report = directory_info.whether_to_report

            ## ���ؼ��Ŀ¼�Ĵ�С
            directory_size = self.__get_directorysize(directory_path)
            #print "directory_size = ", directory_size

            ## �����Ŀ¼��С�Ƿ񳬹��趨��С
            if (directory_size > directory_maxsize):
                exceed_size = directory_size - 0.7 * directory_maxsize
                ## �����Ŀ¼���򣬲���ɾ�����ļ�������С������70%�������Ҫ�ϱ��ͱ����monitor
                self.__maintain_directory(directory_path, exceed_size,directory_whether_to_report)


    def __send_event(self, dirname, filename):
        """
       Method: __send_event
       Description: ������Ϣָ���ݿ�
       Parameter: dirname, filename
       Return: ��
       Others: ��
       """
        event_data = event_sender.EventData()
        event_data.set_event_id('event.MaintainApp.0')
        event_data.set_object_id("maintain_app")
        event_data.set_device_id(self.__worker.get_app().get_device_id())
        
        # dirname�Ǵ����ݿ��ж�ȡ�����ģ��Ѿ���utf-8����ģ������ٴα���
        # ���⣬Ŀǰ����LinuxϵͳĬ��ʹ����utf-8���룬windowsĬ��ʹ����gbk
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
        Description: �ݹ�õ�Ŀ¼�������ļ���������Ŀ¼
        Parameter: directory_path, exceed_size
        Return: Ŀ¼����Ŀ¼�������ļ�
        Others: ��
        """

        # �õ����Ŀ¼���ļ���������
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
                ## �¼��ϱ������ɹ�ɾ���ļ�����Ϣ�ϱ������ݿ�
                if directory_whether_to_report:
                    self.__send_event(directory_path, filepath)
            except:
                # ���ʧ��ɾ���ͽ�������Ϣ��ӡ����־log��
                tracelog.exception("%s failed to be deleted" % filepath)
            count += 1


    def __get_files_in_directory(self, directory_path):
        """
        :param directory_path:
        Method: __get_files_in_directory
        Description: �ݹ�õ�Ŀ¼�������ļ���������Ŀ¼
        Parameter: directory_path
        Return: Ŀ¼����Ŀ¼�������ļ�
         Others: ��
        """

        # ��total_file��ʼ��
        total_files = []

        # �ݹ齫��Ŀ¼�µ��ļ����ӵ�"total_file"��
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
        Description: �ݹ����Ŀ¼��С
        Parameter: directory_path
        Return: �ļ��д�С
        Others: ��
        """

        # ���ļ��ܴ�Сtotal_size��ʼ��
        total_size = 0
        # print "directory_path = ", directory_path
        # �ݹ齫��Ŀ¼���ļ���С�ۼ���"total_size"
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
        
