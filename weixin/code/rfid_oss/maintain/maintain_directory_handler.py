#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: 定期检查监控目录占用空间是否超过设定大小，超过预期大小就依次删除最旧文件
Others:无
Key Class&Method List: 
             1. MonitorFileSizeTimeoutHandler：定期检查监控目录占用空间是否超过设定大小，超过预期大小就依次删除最旧文件
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:新建文件
"""


import bundleframework as bf

        
class MonitorFileSizeTimeoutHandler(bf.TimeOutHandler):
    """
    Class: DetectLogFileTimeoutHandler
    Description: 定期检查监控目录占用空间是否超过设定大小，超过预期大小就依次删除最旧文件
    Base: TimeOutHandler
    Others: 无
    """

    def time_out(self):
        """
        Method: time_out
        Description: 定期检查监控目录占用空间是否超过设定大小，超过预期大小就依次删除最旧文件
        Parameter: 无
        Return: 无
        Others: 无
        """

        self.get_worker().get_maintain_directory_manager().monitor_directorysize()
     