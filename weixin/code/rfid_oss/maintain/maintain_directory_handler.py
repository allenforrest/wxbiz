#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: ���ڼ����Ŀ¼ռ�ÿռ��Ƿ񳬹��趨��С������Ԥ�ڴ�С������ɾ������ļ�
Others:��
Key Class&Method List: 
             1. MonitorFileSizeTimeoutHandler�����ڼ����Ŀ¼ռ�ÿռ��Ƿ񳬹��趨��С������Ԥ�ڴ�С������ɾ������ļ�
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:�½��ļ�
"""


import bundleframework as bf

        
class MonitorFileSizeTimeoutHandler(bf.TimeOutHandler):
    """
    Class: DetectLogFileTimeoutHandler
    Description: ���ڼ����Ŀ¼ռ�ÿռ��Ƿ񳬹��趨��С������Ԥ�ڴ�С������ɾ������ļ�
    Base: TimeOutHandler
    Others: ��
    """

    def time_out(self):
        """
        Method: time_out
        Description: ���ڼ����Ŀ¼ռ�ÿռ��Ƿ񳬹��趨��С������Ԥ�ڴ�С������ɾ������ļ�
        Parameter: ��
        Return: ��
        Others: ��
        """

        self.get_worker().get_maintain_directory_manager().monitor_directorysize()
     