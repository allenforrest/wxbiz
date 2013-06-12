#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: log�Ķ�ʱά����log�����ڴ����log������������ѯ
Others:��
Key Class&Method List: 
             1. MaintainApp��APP�࣬����worker��ע��
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:�½��ļ�
"""


if __name__ == "__main__":
   import import_paths




import bundleframework as bf
import tracelog
import sequence_no_creator

import maintain_log_worker
import maintain_directory_worker
import event_sender

class MaintainApp(bf.BasicApp):  
    """
    Class: MaintainApp
    Description: log�Ķ�ʱά����log�����ڴ����log������������ѯ��
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

        bf.BasicApp.__init__(self, "MaintainApp")

    
    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: ע��MaintainLogWorker,��MaintainDirectoryWorker
        Parameter: ��
        Return: 0
        Others: ��
        """
        event_sender.set_local_app(self)

        bf.BasicApp._ready_for_work(self)
        # ע��directory worker��log worker
        worker = maintain_log_worker.MaintainLogWorker()     
        self.register_worker(worker)

        worker = maintain_directory_worker.MaintainDirectoryWorker()
        self.register_worker(worker)
        
        return 0
   
    def send_ack(self, frame, datas):
        """
        Method: send_ack
        Description: �򷢳�����Ľ��̷��ʹ������Ĵ�����
        Parameter: 
            frame: �յ���Ҫ�������Ϣ
            datas: ���ʹ���������Ϣ 
        Return: ��
        Others: ��
        """

        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(frame)        
        for data in datas:
            frame_ack.add_data(data)
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)
        
        
    def get_sequence_no_creator(self):
        """
        Method: get_sequence_no_creator
        Description: �������д�������
        Parameter: ��
        Return: ���д�������
        Others: ��
        """

        return self.__no_creator
    

        
MaintainApp().run()