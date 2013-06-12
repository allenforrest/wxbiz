#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: �����ж�����web����̨app֮����Ϣת���Ľ���
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


import os.path
import sys

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import tracelog

from message_dispath_worker import MessageDispathWorker


class WebGateApp(bf.BasicApp):
    """
    Class:    WebGateApp
    Description: WebGateģ��Ľ�����
    Base: BasicApp    
    Others: ��
    """

    def __init__(self):
        """
        Method: __init__
        Description: ���ʼ��
        Parameter: ��
        Return: 
        Others: 
        """

        bf.BasicApp.__init__(self, "WebGate")
            
    
    def _ready_for_work(self):
        """
        Method:    _ready_for_work
        Description: ��������ʱ�ĳ�ʼ��������ע���̺߳�worker
        Parameter:  ��
        Return: 
                0   -- �ɹ�
                                      ��0 -- ʧ��
        Others: ��
        """
        
        worker = MessageDispathWorker(min_task_id=1, max_task_id=9999)
        
        self.register_worker(worker)
        
        return 0



if __name__ == "__main__":
    WebGateApp().run()




