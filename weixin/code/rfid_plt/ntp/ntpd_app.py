#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTPD NTP服务配置的APP，该APP负责配置NTPD服务设置，打开关闭NTP服务，获取NTPD服务设置的信息
Others: 无     
Key Class&Method List: 
             1. NtpdApp：APP类，负责worker的注册  
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:新建文件
"""

if __name__ == "__main__":
    import import_paths
    
import bundleframework as bf
import tracelog

import ntpd_worker

class NtpdApp(bf.BasicApp):  
    """
    Class: NtpdApp
    Description: NTPD NTP服务配置的APP，该APP负责配置NTPD服务设置，打开关闭NTP服务，获取NTPD服务设置的信息
    Base: BasicApp
    Others: 无
    """

    def __init__(self):
        """
        Method: __init__
        Description: 初始化
        Parameter: 无
        Return: 无
        Others: 无
        """

        bf.BasicApp.__init__(self, "NtpdApp")
    
    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: 注册NtpdWorker
        Parameter: 无
        Return: 0
        Others: 无
        """

        bf.BasicApp._ready_for_work(self)        
        worker = ntpd_worker.NtpdWorker()        
        self.register_worker(worker)     
        return 0
        
NtpdApp().run()
