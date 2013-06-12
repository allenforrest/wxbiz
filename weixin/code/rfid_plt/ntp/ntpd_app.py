#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: NTPD NTP�������õ�APP����APP��������NTPD�������ã��򿪹ر�NTP���񣬻�ȡNTPD�������õ���Ϣ
Others: ��     
Key Class&Method List: 
             1. NtpdApp��APP�࣬����worker��ע��  
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:�½��ļ�
"""

if __name__ == "__main__":
    import import_paths
    
import bundleframework as bf
import tracelog

import ntpd_worker

class NtpdApp(bf.BasicApp):  
    """
    Class: NtpdApp
    Description: NTPD NTP�������õ�APP����APP��������NTPD�������ã��򿪹ر�NTP���񣬻�ȡNTPD�������õ���Ϣ
    Base: BasicApp
    Others: ��
    """

    def __init__(self):
        """
        Method: __init__
        Description: ��ʼ��
        Parameter: ��
        Return: ��
        Others: ��
        """

        bf.BasicApp.__init__(self, "NtpdApp")
    
    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: ע��NtpdWorker
        Parameter: ��
        Return: 0
        Others: ��
        """

        bf.BasicApp._ready_for_work(self)        
        worker = ntpd_worker.NtpdWorker()        
        self.register_worker(worker)     
        return 0
        
NtpdApp().run()
