#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-13
Description: Portal����ģ��app
Key Class&Method List: 
             1. PortalManApp -- ������
History:
1. Date: 2013-5-13
   Author: Allen
   Modification: create
"""

import time
import collections
import Queue

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import mit
import tracelog
import sequence_no_creator

import err_code_def
import cmd_code_def
import msg_params_def
import content_cfg_worker
import member_cfg_worker
import subscriber_cfg_worker

from moc_wx import Article
from moc_wx import Group
from moc_wx import HelpTips
from moc_wx import Subject
from moc_wx import Member
from moc_wx import Menu
from moc_wx import Subscriber

class PushTimerThread(bf.WatchedThread):
    """
    Class: PushTimerThread
    Description: ���Ͷ�ʱ���߳�
    Base: WatchedThread
    Others: 
    """

    def __init__(self):
        """
        Method: __init__
        Description: ���ʼ��
        Parameter: ��
        Return: 
        Others: 
        """

        bf.WatchedThread.__init__(self)
        self.__app = None
        
        #��abs_timeout������߳�ʱ���������
        self._time_task_map = collections.OrderedDict()
        self.event_queue = Queue.Queue()
        
    def set_app(self, app):
        """
        Method:    set_app
        Description: ����app����
        Parameter: 
            app: app���󣬺�����Ҫ����app�Ľӿ�
        Return: 
        Others: 
        """

        self.__app = app
        
    def run(self):
        """
        Method: run
        Description: �߳�ִ�����
        Parameter: ��
        Return: 
        Others: 
        """

        while True:
            time.sleep(0.5)
            self._timeout()
            while self.event_queue.empty() is not True:
                data = self.event_queue.get(True, 0.1)
                self._insert_task_to_map(data[0], data[1], data[2])
                
            if self.feed_dog():
                break
        
        self.over()
    
    def add_task(self, abs_time, times, article_id):
        """
        Method: add_task
        Description: �����������񵽶�ʱ���б���
        Parameter: 
            abs_time: ��ʱʱ�� YYYY-MM-DD HH:MM:SS
            times: �����ظ�����
            article_id: ������������ID
        Return: 
        Others: 
        """
        self.event_queue.put_nowait((abs_time, times, article_id))
        
    def del_task(self, article_id):
        """
        Method: del_task
        Description: �ڶ�ʱ���б���ɾ����������
        Parameter: 
            article_id: ������������ID
        Return: 
        Others: 
        """

        items = self._time_task_map.items()
        for item in items:
            if item[1][0] == article_id:
                items.remove(item)
    
    def _insert_task_to_map(self, abs_time, times, article_id):
        """
        Method: _insert_task_to_map
        Description: ��������붨ʱ���������
        Parameter: 
            abs_time: ��ʱʱ�� YYYY-MM-DD HH:MM:SS
            times: �����ظ�����
            article_id: ������������ID
        Return: 
        Others: 
        """

        time_stru = time.strptime(abs_time, '%Y-%m-%d %H:%M:%S')
        abs_time_f = time.mktime(time_stru)   
              
        index = 0
        items = self._time_task_map.items()
        for item in items:
            if abs_time < item[0]:
                break
            index += 1
        items.insert(index, (abs_time_f, (article_id, times)))
        self._time_task_map = collections.OrderedDict(items)

    def _timeout(self):
        """
        Method: _timeout
        Description: ��ʱ����
        Parameter: ��
        Return: ��
        Others: 
        """
        abs_now = time.time()
        items = self._time_task_map.items()
        for item in items:
            #��ΪOrderedDict�ǰ�ʱ��˳��ģ���ˣ�ֻҪ���ֵ�ǰ����Ϣ��û�г�ʱ���������Ϣ��û�г�ʱ
            if abs_now < item[0]:
                break
            else:
                article_id, times = item[1]
                msg = msg_params_def.PortalContentArticleSubscriberPush()
                msg.init_all_attr()
                msg.article_id = str(article_id)
               
                frame = bf.AppFrame()
                frame.set_cmd_code(cmd_code_def.PORTAL_CONTENT_ARTICLE_SUBSCRIBER_PUSH)                
                frame.add_data(msg.serialize())
                self.__app.dispatch_frame_to_worker('ContentConfigWorker', frame)
                
                times = times - 1
                del self._time_task_map[item[0]]
                
                if times > 0:
                    next_abs_time = abs_now + 24 * 3600
                    self._insert_task_to_map(next_abs_time, times, article_id)


class PortalManApp(bf.BasicApp):
    """
    Class:    PortalManApp
    Description: PortalManAppģ��Ľ�����
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

        bf.BasicApp.__init__(self, "PortalManApp")
        self._mit_manager = mit.Mit()
        self._article_no_creator = sequence_no_creator.SequenceNoCreator()
        self._subject_no_creator = sequence_no_creator.SequenceNoCreator()
        self._group_no_creator = sequence_no_creator.SequenceNoCreator()
        self._push_task_manager = None
            
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
        
        self._mit_manager.regist_complex_attr_type(msg_params_def.GroupList)
        
        self._mit_manager.open_sqlite("../../data/sqlite/wx_cloud.db")

        worker = content_cfg_worker.ContentConfigWorker(min_task_id = 1, max_task_id = 9999)
        self.register_worker(worker)

        worker = subscriber_cfg_worker.SubscriberConfigWorker(min_task_id = 1, max_task_id = 9999)
        self.register_worker(worker)
        
        #worker = member_cfg_worker.MemberConfigWorker(min_task_id = 1, max_task_id = 9999)
        #self.register_worker(worker)

        self._push_task_manager = PushTimerThread()
        self._push_task_manager.set_app(self)
        self.register_watched_thread(self._push_task_manager)
        
        ##����������
        article_seq_no = self.get_mit_manager().get_attr_max_value('Article', 'article_id')
        if article_seq_no is None:
            article_seq_no =  0
        self._article_no_creator.init_creator(2 ** 16, article_seq_no)

        subject_seq_no = self.get_mit_manager().get_attr_max_value('Subject', 'subject_id')
        if subject_seq_no is None:
            subject_seq_no =  0
        self._subject_no_creator.init_creator(2 ** 8, subject_seq_no)

        group_seq_no = self.get_mit_manager().get_attr_max_value('Group', 'group_id')
        if group_seq_no is None or group_seq_no < msg_params_def.SUBSCRIBER_USERDEFINE_GROUP_BASE:
            group_seq_no =  msg_params_def.SUBSCRIBER_USERDEFINE_GROUP_BASE
        
        self._group_no_creator.init_creator(2 ** 8, group_seq_no)        
        
        return 0

    def get_push_task_manager(self):
        return self._push_task_manager
    
    def get_mit_manager(self):
        """
        Method: get_mit_manager
        Description: ��ȡ���̵�mit������
        Parameter: ��
        Return: mit������
        Others: 
        """

        return self._mit_manager
    
    def get_article_no_creator(self):
        return self._article_no_creator

    def get_subject_no_creator(self):
        return self._subject_no_creator
    
    def get_group_no_creater(self):
        return self._group_no_creator
    
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

        tracelog.info('portal man app send ack frame: %s' % frame_ack)
        tracelog.info('frame buf: %s' % frame_ack.get_data())
        self.dispatch_frame_to_process_by_pid(frame.get_sender_pid(), frame_ack)
            

if __name__ == "__main__":
    PortalManApp().run()