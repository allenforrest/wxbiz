#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-13
Description: ΢�Ŷ����߹���ģ��app
Key Class&Method List: 
             1. SubscriberManApp -- ������
History:
1. Date: 2013-5-13
   Author: Allen
   Modification: create
"""

if __name__ == "__main__":
    import import_paths

import time

import bundleframework as bf
import mit
import tracelog
import sequence_no_creator

import err_code_def
import msg_params_def
import subscriber_man_worker
import subscriber_task_worker
import wx_svc_api
#import wx_windeln_api

from moc_wx import Subscriber, Group, Article, Subject, HelpTips, Member, WXBizInfo


class SubscriberManApp(bf.BasicApp):
    """
    Class:    SubscriberManApp
    Description: SubscriberManAppģ��Ľ�����
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

        bf.BasicApp.__init__(self, "SubscriberManApp")
        self._mit_manager = mit.Mit()
        self._sub_no_creator = sequence_no_creator.SequenceNoCreator()
        self._wx_service_api = None
        self._sub_man_worker = None
           
        self._task_worker = None
        
        self._price = None
        self._stock = False
           
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
        bf.BasicApp._ready_for_work(self)        
        
        self._mit_manager.init_mit_lock()

        self._mit_manager.regist_moc(Article.Article, Article.ArticleRule)
        self._mit_manager.regist_moc(Group.Group, Group.GroupRule)
        self._mit_manager.regist_moc(HelpTips.HelpTips, HelpTips.HelpTipsRule)
        self._mit_manager.regist_moc(Subject.Subject, Subject.SubjectRule)
        self._mit_manager.regist_moc(Member.Member, Member.MemberRule)
        self._mit_manager.regist_moc(Group.Group, Group.GroupRule)
        self._mit_manager.regist_moc(Subscriber.Subscriber, Subscriber.SubscriberRule)
        self._mit_manager.regist_moc(WXBizInfo.WXBizInfo, WXBizInfo.WXBizInfoRule)
        self._mit_manager.regist_complex_attr_type(msg_params_def.GroupList)
        
        self._mit_manager.open_sqlite("../../data/sqlite/wx_cloud.db")

        self._sub_man_worker = subscriber_man_worker.SubscriberManagerWorker(min_task_id = 1, max_task_id = 9999)
        self.register_worker(self._sub_man_worker)

        sub_seq_no = self.get_mit_manager().get_attr_max_value('Subscriber', 'subscribe_seq_no')
        if sub_seq_no is None:
            sub_seq_no =  0
        self._sub_no_creator.init_creator(2 ** 32, sub_seq_no)

        bizs = self._mit_manager.rdm_find('WXBizInfo')
        self._wx_service_api = wx_svc_api.WXServiceAPI(bizs[0].login_user, bizs[0].login_pwd)
        self._wx_service_api.get_biz_fakeid()
        
        #self._wx_windeln_api = wx_windeln_api.WXWindelnAPI('allenxu@gmail.com', 'Xuweinan812185')

        self._task_worker = subscriber_task_worker.SubscriberTaskWorker()
        self.register_worker(self._task_worker)
                
        return 0

    def get_sub_no_creator(self):
        return self._sub_no_creator
    
    def get_wx_service_api(self):
        return self._wx_service_api
    
    def get_wx_windeln_api(self):
        return self._wx_windeln_api
    
    def get_task_worker(self):
        return self._task_worker
        
    def get_sub_man_worker(self):
        return self._sub_man_worker
    
    def get_mit_manager(self):
        """
        Method: get_mit_manager
        Description: ��ȡ���̵�mit������
        Parameter: ��
        Return: mit������
        Others: 
        """

        return self._mit_manager
    
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

        tracelog.info('subscriber man app send ack frame: %s' % frame_ack)
        tracelog.info('frame buf[0]: %s' % frame_ack.get_data())
        if frame_ack.get_data_num() > 1:
            tracelog.info('frame buf[1]: %s' % frame_ack.get_data(1))
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)
            

    """
    def update_windeln_info(self, price, stock):
        self._price = price
        self._stock = stock
    
    def get_windeln_info(self):
        return (self._price, self._stock)
    """
    
if __name__ == "__main__":
    SubscriberManApp().run()
    