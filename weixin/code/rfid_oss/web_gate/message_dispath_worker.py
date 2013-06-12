#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ��ж����˸�����Ϣת����worker
Others:      
Key Class&Method List: 
             1. MessageDispathWorker��������Ϣת����worker
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
    Description: ������Ϣת����worker
    Base: CmdWorker
    Others: 
    """

    def __init__(self, min_task_id, max_task_id):
        """
        Method: __init__
        Description: ���캯��
        Parameter: 
            min_task_id, max_task_id: ����ŷ�Χ
        Return: 
        Others: 
        """

        bf.CmdWorker.__init__(self, "MessageDispathWorker", min_task_id, max_task_id)

        # ͨ��callacp��ʽ����ALE����Ŀͻ���
        self._callacp_srv = None

    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker��ʼ������
        Parameter: ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
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
        Description: �жϸ���������Ƿ����ڵ�ǰworker����
        Parameter: 
            frame: ���appframe����
        Return: ����������Ƿ����ڵ�ǰworker����
        Others: 
            ֻҪ��������Ӧ����Ϣ����ô����Ϊ��MessageDispathWorkerҪת����web��
        """
        return frame.is_ack_frame()

    def work(self, frame, total_ready_frames):
        """
        Method:    work
        Description: ִ��һ������
        Parameter: 
            frame: AppFrame
            total_ready_frames: �ܹ��ȴ�ִ�е�����
        Return: 
        Others: 
            MessageDispathWorker��Ӧ����Ϣת����web
        """
        
        self._callacp_srv.send_appframe(frame)
        

        
