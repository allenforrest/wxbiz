#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-27
Description: ��ȡ�����ļ��е�������Ϣ
Others:      
Key Class&Method List: 
             1. AppInfo: python�����ĸ������̵���Ϣ
             2. BinInfo: ��������ֱ�����еĿ�ִ�г������Ϣ
             3. InstallInfo: ��ȡ�����ļ�����
History: 
1. Date:
   Author:
   Modification:
"""

import os, os.path
import copy
import xml.etree.ElementTree as ET   
import tracelog
#import platform

import utility

class AppInfo:
    """
    Class: AppInfo
    Description: python�����ĸ������̵���Ϣ
    Base: 
    Others: 
    """

    def __init__(self                    
                , service_name
                , instance_num                    
                , run_on_master
                , run_on_slave
                , is_exclude
                , program_path):

        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            service_name: ���������
            auto_run: �Ƿ����Զ�����
            is_exclude: ����ʱ�Ƿ��Ƕ�ռ��ʽ��
            program_path: app����·��            
        Return: 
        Others: 
        """
        
        self._service_name = service_name  
        self._instance_num = instance_num        
        self._run_on_master = run_on_master
        self._run_on_slave = run_on_slave
        self._is_exclude = is_exclude
        self._program_path = program_path    
                

    def get_service_name(self):
        """
        Method:    get_service_name
        Description: ��ȡ service_name
        Parameter: ��
        Return: service_name
        Others: 
        """

        return self._service_name
    
    def get_instance_num(self):
        """
        Method:    get_instance_num
        Description: ��ȡ instance_num
        Parameter: ��
        Return: instance_num
        Others: 
        """

        return self._instance_num

    def is_auto_run_on_master(self):
        """
        Method:    is_auto_run_on_master
        Description: �ж���master�ϣ��Ƿ��Զ�����
        Parameter: ��
        Return: �Ƿ��Զ�����
        Others: 
        """

        return self._run_on_master

    def is_auto_run_on_slave(self):
        """
        Method:    is_auto_run_on_slave
        Description: �ж���salve�ϣ��Ƿ��Զ�����
        Parameter: ��
        Return: �Ƿ��Զ�����
        Others: 
        """

        return self._run_on_slave

    def is_exclude(self):
        """
        Method:    is_exclude
        Description: �ж�����ʱ�Ƿ��Ƕ�ռ��ʽ��
        Parameter: ��
        Return: ����ʱ�Ƿ��Ƕ�ռ��ʽ��
        Others: 
        """

        return self._is_exclude

    def get_program_path(self):
        """
        Method:    get_program_path
        Description: ��ȡapp���ڵ�·��
        Parameter: ��
        Return: app���ڵ�·��
        Others: 
        """

        return self._program_path
    


class BinInfo:
    """
    Class: BinInfo
    Description: ��������ֱ�����еĿ�ִ�г������Ϣ
    Base: 
    Others: 
    """

    def __init__(self, program, arg, work_dir, lib_path):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            program: �������ڵ�·��
            arg: ��������ʱ���ݸ����Ĳ���
            work_dir: ����Ĺ���·��
            lib_path: ������Ҫ�Ķ�̬�����ڵ�Ŀ¼(linux��Ч)
        Return: 
        Others: 
        """

        self._program = program
        self._arg = arg
        self._work_dir = work_dir
        self._lib_path = lib_path


    def get_program(self):
        """
        Method:    get_program
        Description: ��ȡ�������ڵ�·��
        Parameter: ��
        Return: �������ڵ�·��
        Others: 
        """

        return self._program

    def get_arg(self):
        """
        Method:    get_arg
        Description: ��ȡ��������ʱ���ݸ����Ĳ���
        Parameter: ��
        Return: ��������ʱ���ݸ����Ĳ���
        Others: 
        """

        return self._arg

    def get_work_dir(self):
        """
        Method:    get_work_dir
        Description: ��ȡ����·��
        Parameter: ��
        Return: ����·��
        Others: 
        """

        return self._work_dir

    def get_lib_path(self):
        """
        Method:    get_lib_path
        Description: ��ȡ������Ҫ�Ķ�̬�����ڵ�Ŀ¼
        Parameter: ��
        Return: ������Ҫ�Ķ�̬�����ڵ�Ŀ¼
        Others: 
        """

        return self._lib_path
        
        
        
class InstallInfo:
    """
    Class: InstallInfo
    Description: �����ȡ���������ļ���Ϣ
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
            _apps: ���е�AppInfo���б�
            _bins: ���е�BinInfo���б�
        """

        self._apps = []
        self._bins = []


    def _load_app_info(self, xmlroot):
        """
        Method:    _load_app_info
        Description: ����python�����ĸ������̵���Ϣ
        Parameter: 
            xmlroot: xml���ڵ�
        Return: 
        Others: 
        """

        for app_ele in xmlroot.iterfind("apps/app"):
            service_name = app_ele.get("service_name")
            if service_name is None:
                continue
            instance_num = int(app_ele.get("instance_num"))
            run_on_master = int(app_ele.get("run_on_master"))
            run_on_slave = int(app_ele.get("run_on_slave"))
            exclude = int(app_ele.get("exclude"))
            program = app_ele.get("program")
            app = AppInfo( service_name
                        , instance_num                        
                        , run_on_master
                        , run_on_slave
                        , exclude
                        , program)
            self._apps.append(app)


    def _load_bin_info(self, xmlroot):
        """
        Method:    _load_bin_info
        Description: ������������ֱ�����еĿ�ִ�г������Ϣ
        Parameter: 
            xmlroot: xml���ڵ�
        Return: 
        Others: 
        """

        # �����ļ��У�������win��linux
        # ����windows�£�û��lib_path����
        #if platform.system().lower() == "windows":
        if utility.is_windows():
            xpath = "bins/bins/win"
            lib_path = ""
        else:
            xpath = "bins/bins/linux"
            lib_path = None
            
        for app_ele in xmlroot.iterfind(xpath):
            if lib_path is None:
                lib_path = app_ele.get("lib_path")
            
            bin = BinInfo(app_ele.get("program")
                        , app_ele.get("arg")
                        , app_ele.get("work_dir")
                        , lib_path)
            self._bins.append(bin)


    def load(self, cfg_file_path):
        """
        Method:    load
        Description: ��ȡ�����ļ�
        Parameter: 
            cfg_file_path: 
        Return: 
            0: �ɹ�
            ��0: ʧ��
        Others: 
        """

        try:
            xmldoc = ET.parse(cfg_file_path)
            xmlroot = xmldoc.getroot()
            
            self._load_app_info(xmlroot)
            self._load_bin_info(xmlroot)

        except:
            tracelog.exception("InstallInfo.load failed. cfg_file_path:%s" % cfg_file_path)
            return -1

        return 0

    def get_app_info(self):
        """
        Method:    get_app_info
        Description: ��ȡpython�����ĸ������̵���Ϣ
        Parameter: ��
        Return: python�����ĸ������̵���Ϣ
        Others: 
        """

        return self._apps


    def get_bin_info(self):
        """
        Method:    get_bin_info
        Description: ��ȡ��������ֱ�����еĿ�ִ�г������Ϣ
        Parameter: ��
        Return: ��������ֱ�����еĿ�ִ�г������Ϣ
        Others: 
        """

        return self._bins
        
