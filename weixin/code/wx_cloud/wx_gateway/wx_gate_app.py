#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-11
Description: ΢�Žӿ�gate app
Key Class&Method List: 
             1. WXGateApp -- ������
History:
1. Date: 2013-5-11
   Author: Allen
   Modification: create
"""

import os.path
import sys

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import tracelog

from wx_msg_worker import *

class WXGateApp(bf.BasicApp):
    """
    Class:    WXGateApp
    Description: WXGateģ��Ľ�����
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

        bf.BasicApp.__init__(self, "WXGateApp")
            
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

        worker = ReceiveWXMessageWorker(min_task_id = 1, max_task_id = 9999)
        self.register_worker(worker)

        return 0

    def send_ack_dispatch(self, frame, datas):
        """
        Method: send_ack_dispatch
        Description: �������Ӧ��Ϣ
        Parameter: 
            frame: ��Ϣ֡
            datas: ��������
        Return: 
        Others: 
        """


        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(frame)        
        for data in datas:
            frame_ack.add_data(data)

        tracelog.info('wx gate app send ack frame: %s' % frame_ack)
        tracelog.info('frame buf: %s' % frame_ack.get_data())
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)
        

if __name__ == "__main__":
    WXGateApp().run()