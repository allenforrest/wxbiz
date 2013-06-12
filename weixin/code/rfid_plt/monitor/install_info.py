#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-27
Description: 读取配置文件中的配置信息
Others:      
Key Class&Method List: 
             1. AppInfo: python开发的各个进程的信息
             2. BinInfo: 其他可以直接运行的可执行程序的信息
             3. InstallInfo: 读取配置文件的类
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
    Description: python开发的各个进程的信息
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
        Description: 构造函数
        Parameter: 
            service_name: 服务的名称
            auto_run: 是否是自动运行
            is_exclude: 启动时是否是独占方式的
            program_path: app所在路径            
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
        Description: 获取 service_name
        Parameter: 无
        Return: service_name
        Others: 
        """

        return self._service_name
    
    def get_instance_num(self):
        """
        Method:    get_instance_num
        Description: 获取 instance_num
        Parameter: 无
        Return: instance_num
        Others: 
        """

        return self._instance_num

    def is_auto_run_on_master(self):
        """
        Method:    is_auto_run_on_master
        Description: 判断在master上，是否自动运行
        Parameter: 无
        Return: 是否自动运行
        Others: 
        """

        return self._run_on_master

    def is_auto_run_on_slave(self):
        """
        Method:    is_auto_run_on_slave
        Description: 判断在salve上，是否自动运行
        Parameter: 无
        Return: 是否自动运行
        Others: 
        """

        return self._run_on_slave

    def is_exclude(self):
        """
        Method:    is_exclude
        Description: 判断启动时是否是独占方式的
        Parameter: 无
        Return: 启动时是否是独占方式的
        Others: 
        """

        return self._is_exclude

    def get_program_path(self):
        """
        Method:    get_program_path
        Description: 获取app所在的路径
        Parameter: 无
        Return: app所在的路径
        Others: 
        """

        return self._program_path
    


class BinInfo:
    """
    Class: BinInfo
    Description: 其他可以直接运行的可执行程序的信息
    Base: 
    Others: 
    """

    def __init__(self, program, arg, work_dir, lib_path):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            program: 程序所在的路径
            arg: 程序启动时传递给它的参数
            work_dir: 程序的工作路径
            lib_path: 程序需要的动态库所在的目录(linux有效)
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
        Description: 获取程序所在的路径
        Parameter: 无
        Return: 程序所在的路径
        Others: 
        """

        return self._program

    def get_arg(self):
        """
        Method:    get_arg
        Description: 获取程序启动时传递给它的参数
        Parameter: 无
        Return: 程序启动时传递给它的参数
        Others: 
        """

        return self._arg

    def get_work_dir(self):
        """
        Method:    get_work_dir
        Description: 获取工作路径
        Parameter: 无
        Return: 工作路径
        Others: 
        """

        return self._work_dir

    def get_lib_path(self):
        """
        Method:    get_lib_path
        Description: 获取程序需要的动态库所在的目录
        Parameter: 无
        Return: 程序需要的动态库所在的目录
        Others: 
        """

        return self._lib_path
        
        
        
class InstallInfo:
    """
    Class: InstallInfo
    Description: 负责读取整个配置文件信息
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
            _apps: 所有的AppInfo的列表
            _bins: 所有的BinInfo的列表
        """

        self._apps = []
        self._bins = []


    def _load_app_info(self, xmlroot):
        """
        Method:    _load_app_info
        Description: 加载python开发的各个进程的信息
        Parameter: 
            xmlroot: xml根节点
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
        Description: 加载其他可以直接运行的可执行程序的信息
        Parameter: 
            xmlroot: xml根节点
        Return: 
        Others: 
        """

        # 配置文件中，区分了win和linux
        # 其中windows下，没有lib_path参数
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
        Description: 读取配置文件
        Parameter: 
            cfg_file_path: 
        Return: 
            0: 成功
            非0: 失败
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
        Description: 获取python开发的各个进程的信息
        Parameter: 无
        Return: python开发的各个进程的信息
        Others: 
        """

        return self._apps


    def get_bin_info(self):
        """
        Method:    get_bin_info
        Description: 获取其他可以直接运行的可执行程序的信息
        Parameter: 无
        Return: 其他可以直接运行的可执行程序的信息
        Others: 
        """

        return self._bins
        
