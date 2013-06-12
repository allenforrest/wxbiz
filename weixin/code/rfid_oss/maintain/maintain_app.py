#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: log的定时维护，log按日期打包，log打包任务情况查询
Others:无
Key Class&Method List: 
             1. MaintainApp：APP类，负责worker的注册
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:新建文件
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
    Description: log的定时维护，log按日期打包，log打包任务情况查询，
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

        bf.BasicApp.__init__(self, "MaintainApp")

    
    def _ready_for_work(self):
        """
        Method: _ready_for_work
        Description: 注册MaintainLogWorker,和MaintainDirectoryWorker
        Parameter: 无
        Return: 0
        Others: 无
        """
        event_sender.set_local_app(self)

        bf.BasicApp._ready_for_work(self)
        # 注册directory worker和log worker
        worker = maintain_log_worker.MaintainLogWorker()     
        self.register_worker(worker)

        worker = maintain_directory_worker.MaintainDirectoryWorker()
        self.register_worker(worker)
        
        return 0
   
    def send_ack(self, frame, datas):
        """
        Method: send_ack
        Description: 向发出请求的进程发送处理结果的错误码
        Parameter: 
            frame: 收到的要处理的消息
            datas: 发送处理结果的消息 
        Return: 无
        Others: 无
        """

        frame_ack = bf.AppFrame()
        frame_ack.prepare_for_ack(frame)        
        for data in datas:
            frame_ack.add_data(data)
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)
        
        
    def get_sequence_no_creator(self):
        """
        Method: get_sequence_no_creator
        Description: 获许序列创建规则
        Parameter: 无
        Return: 序列创建规则
        Others: 无
        """

        return self.__no_creator
    

        
MaintainApp().run()