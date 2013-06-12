#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中定义了负责消息转发的worker
Others:      
Key Class&Method List: 
             1. MessageDispathWorker：负责消息转发的worker
History: 
1. Date:
   Author:
   Modification:
"""

import bundleframework as bf
import tracelog

import web_callacp_server
class MessageDispathWorker(bf.CmdWorker):
    """
    Class: MessageDispathWorker
    Description: 负责消息转发的worker
    Base: CmdWorker
    Others: 
    """

    def __init__(self, min_task_id, max_task_id):
        """
        Method: __init__
        Description: 构造函数
        Parameter: 
            min_task_id, max_task_id: 任务号范围
        Return: 
        Others: 
        """

        bf.CmdWorker.__init__(self, "MessageDispathWorker", min_task_id, max_task_id)

        # 通过callacp方式发送ALE报告的客户端
        self._callacp_srv = None

    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker初始化函数
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """
        self._callacp_srv = web_callacp_server.WebCallAcpServer(self.get_app())        
        ret = self._callacp_srv.start_listen()
        if ret != 0:
            tracelog.error("start callacp server for web failed. ret:%d" % ret)
            return ret
        
        return 0

    def is_my_duty(self, frame):
        """
        Method:    is_my_duty
        Description: 判断给定的命令，是否属于当前worker处理
        Parameter: 
            frame: 命令，appframe对象
        Return: 给定的命令，是否属于当前worker处理
        Others: 
            只要命令码是应答消息，那么就认为是MessageDispathWorker要转发给web的
        """
        return frame.is_ack_frame()

    def work(self, frame, total_ready_frames):
        """
        Method:    work
        Description: 执行一个命令
        Parameter: 
            frame: AppFrame
            total_ready_frames: 总共等待执行的命令
        Return: 
        Others: 
            MessageDispathWorker将应答消息转发给web
        """
        
        self._callacp_srv.send_appframe(frame)
        

        
