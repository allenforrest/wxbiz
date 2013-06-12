#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-17
Description: 事件中心 事件管理模块
Key Class&Method List: 
             1. EventManWorker -- worker类
History:
1. Date: 2013-5-17
   Author: Allen
   Modification: create
"""
import import_paths
import time
import urllib

import bundleframework as bf
import basic_rep_to_web
import mit

import err_code_mgr

import tracelog
import cmd_code_def

import msg_params_def


class EventCenterEventReportHandler(bf.CmdHandler):
    """
    Class: EventCenterEventReportHandler
    Description: 事件通知命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理创建栏目的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('event man worker recv event frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            report = msg_params_def.PortalEventEventReportReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_EVENT_EVENT_REPORT',
                                                            param_name = 'PortalEventEventReportReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        evt_moc = self.get_worker().get_app().get_mit_manager().gen_rdm("Event")
        evt_moc.event_id = self.get_worker().get_app().get_event_seq_no_creater().get_new_no()
        evt_moc.event_type = report.event_type
        evt_moc.content = report.content
        evt_moc.read_flag = False
        ret = self.get_worker().get_app().get_mit_manager().rdm_add(evt_moc)
        
        if ret.get_err_code() == err_code_mgr.ER_OBJECT_ADD_CONFLICT:
            result.return_code = err_code_mgr.ERR_PORTAL_EVENT_RECORDS_FULL
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_EVENT_RECORDS_FULL)

            result.prepare_for_ack(report, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        elif ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(report, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        if frame.get_sender_pid() == self.get_worker().get_pid('WebGate'):
            # 给WEB回成功响应
            result.return_code = err_code_mgr.ER_SUCCESS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
            result.prepare_for_ack(report, result.return_code, result.description)
    
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))



class EventCenterEventQueryHandler(bf.CmdHandler):
    """
    Class: EventCenterEventQueryHandler
    Description: Portal下发的查询事件命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理查询栏目的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = msg_params_def.PortalEventEventQueryRsp()
        result.init_all_attr()
        tracelog.info('event man worker recv event frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            evt_qry = msg_params_def.PortalEventEventQueryReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_EVENT_EVENT_QUERY',
                                                            param_name = 'PortalEventEventQueryReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        num_per_page = None
        current_page = None
        
        if evt_qry is not None:
            if hasattr(evt_qry, "num_per_page"):
                num_per_page = evt_qry.num_per_page

            if hasattr(evt_qry, "current_page"):
                current_page = evt_qry.current_page

        event_type = evt_qry.event_type

        multi_sql = mit.MultiSQL()
        multi_sql.set_sqlite_sql('event_id desc')                

        if event_type is not None and len(event_type) != 0:
            records = self.get_worker().get_app().get_mit_manager().rdm_find(moc_name = 'Event',
                                                                             order_by_sql = multi_sql,
                                                                             num_per_page = num_per_page, 
                                                                             current_page = current_page,
                                                                             event_type = event_type)
            result.count = self.get_worker().get_app().get_mit_manager().count('Event', event_type = event_type)
        else:
            records = self.get_worker().get_app().get_mit_manager().rdm_find(moc_name = 'Event', 
                                                                             order_by_sql = multi_sql,
                                                                             num_per_page = num_per_page, 
                                                                             current_page = current_page)
            result.count = self.get_worker().get_app().get_mit_manager().count('Event')
        
        result.events = []
        for evt_rec in records:
            evt = msg_params_def.Event()
            evt.init_all_attr()
            evt.event_id = str(evt_rec.event_id)
            evt.event_type = evt_rec.event_type
            evt.content = evt_rec.content
            evt.read_flag = evt_rec.read_flag 
            result.events.append(evt)

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.prepare_for_ack(evt_qry, result.return_code, result.description)
        tracelog.info(result.serialize())
         
        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class EventCenterReadEventNotifyHandler(bf.CmdHandler):
    """
    Class: EventCenterReadEventNotifyHandler
    Description: Portal下发的事件已读通知的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理事件已读通知的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('event man worker recv event frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            read_notify = msg_params_def.PortalEventReadNotifyReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_EVENT_READ_NOTIFY',
                                                            param_name = 'PortalEventReadNotifyReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        evts = self.get_worker().get_app().get_mit_manager().rdm_find("Event", event_id = int(read_notify.event_id))
        if len(evts) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_EVENT_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_EVENT_NOT_EXISTS)

            result.prepare_for_ack(read_notify, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
            
        else:
            evts[0].read_flag = True                                    
            ret = self.get_worker().get_app().get_mit_manager().rdm_mod(evts[0])
                    
            if ret.get_err_code() != 0:
                result.return_code = ret.get_err_code()
                result.description = ret.get_msg()
                
                result.prepare_for_ack(read_notify, result.return_code, result.description)
                self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                return

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(read_notify, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalContentHelpTipsQueryHandler(bf.CmdHandler):
    """
    Class: PortalContentHelpTipsQueryHandler
    Description: Portal下发的查询欢迎词与帮助的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理查询欢迎词与帮助的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = msg_params_def.CommonContentRsp()
        result.init_all_attr()
        tracelog.info('content man worker recv helptips frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            help_qry = basic_rep_to_web.BasicReqFromWeb.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_HELPTIPS_QUERY',
                                                            param_name = 'BasicReqFromWeb')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        helps = self.get_worker().get_app().get_mit_manager().rdm_find("HelpTips")
        
        if len(helps) == 1:
            result.content = helps[0].content
        else:
            result.content = ''

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.prepare_for_ack(help_qry, result.return_code, result.description)
        tracelog.info(result.serialize())
         
        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                                


class EventCenterUnreadEventQueryHandler(bf.CmdHandler):
    """
    Class: EventCenterUnreadEventQueryHandler
    Description: Portal下发的未读事件数目查询的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理未读事件数目查询的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = msg_params_def.PortalEventUnreadQueryRsp()
        result.init_all_attr()
        tracelog.info('content man worker recv article push frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            req = basic_rep_to_web.BasicReqFromWeb.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_EVENT_UNREAD_QUERY',
                                                            param_name = 'BasicReqFromWeb')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        subscribe_event_count = self.get_worker().get_app().get_mit_manager().count("Event", 
                                                                                    event_type = msg_params_def.EVENT_TYPE_SUBSCRIBE,
                                                                                    read_flag = False)
        message_event_count = self.get_worker().get_app().get_mit_manager().count("Event", 
                                                                                    event_type = msg_params_def.EVENT_TYPE_MESSAGE,
                                                                                    read_flag = False)
        delivery_event_count = self.get_worker().get_app().get_mit_manager().count("Event", 
                                                                                    event_type = msg_params_def.EVENT_TYPE_DELIVERY,
                                                                                    read_flag = False)
        login_event_count = self.get_worker().get_app().get_mit_manager().count("Event", 
                                                                                    event_type = msg_params_def.EVENT_TYPE_USERLOGIN,
                                                                                    read_flag = False)
        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        
        result.count = 4
        result.event_unread_nums = []
        
        unread_num = msg_params_def.EventUnreadNum()
        unread_num.event_type = msg_params_def.EVENT_TYPE_DELIVERY
        unread_num.unread_num = delivery_event_count
        result.event_unread_nums.append(unread_num)
        
        unread_num = msg_params_def.EventUnreadNum()
        unread_num.event_type = msg_params_def.EVENT_TYPE_MESSAGE
        unread_num.unread_num = message_event_count
        result.event_unread_nums.append(unread_num)

        unread_num = msg_params_def.EventUnreadNum()
        unread_num.event_type = msg_params_def.EVENT_TYPE_SUBSCRIBE
        unread_num.unread_num = subscribe_event_count
        result.event_unread_nums.append(unread_num)

        unread_num = msg_params_def.EventUnreadNum()
        unread_num.event_type = msg_params_def.EVENT_TYPE_USERLOGIN
        unread_num.unread_num = login_event_count
        result.event_unread_nums.append(unread_num)

        result.prepare_for_ack(req, result.return_code, result.description)
        tracelog.info(result.serialize())
         
        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class EventCenterMessageReplyHandler(bf.CmdHandler):
    """
    Class: EventCenterMessageReplyHandler
    Description: Portal下发的订阅者消息事件直接文本回复的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者消息事件直接文本回复的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('event center worker recv text reply frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            push_info = msg_params_def.PortalEventMessageReplyReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_EVENT_MESSAGE_REPLY',
                                                            param_name = 'PortalEventMessageReplyReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        events = self.get_worker().get_app().get_mit_manager().rdm_find('Event', event_id = int(push_info.event_id))
        if len(events) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_EVENT_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_EVENT_NOT_EXISTS)

            result.prepare_for_ack(push_info, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        message_event = msg_params_def.SubscriberMessageEvent.deserialize(events[0].content)

        # 构造推送消息发给SubscriberManApp
        push_msg = msg_params_def.CloudPortalTextPushMessage()
        push_msg.init_all_attr()
        push_msg.subscriber_open_id = message_event.subscriber_open_id
        push_msg.text_msg = push_info.text_msg
        
        push_frame = bf.AppFrame()
        push_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_TEXT_PUSH_MSG)
        push_frame.add_data(push_msg.serialize())
        self.get_worker().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), push_frame)
        
        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(push_info, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class EventCenterMessageShareHandler(bf.CmdHandler):
    """
    Class: EventCenterMessageShareHandler
    Description: Portal下发的订阅者消息分享的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者消息分享的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('content man worker recv message share frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            msg_share = msg_params_def.PortalEventMessageShareReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_EVENT_MESSAGE_SHARE',
                                                            param_name = 'PortalEventMessageShareReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        subs = self.get_worker().get_app().get_mit_manager().rdm_find("Subject", subject_id = int(msg_share.subject_id))
        if len(subs) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_SUBJECT_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_SUBJECT_NOT_EXISTS)
            
            result.prepare_for_ack(msg_share, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        events = self.get_worker().get_app().get_mit_manager().rdm_find("Event", event_id = int(msg_share.event_id))
        if len(events) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_EVENT_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_EVENT_NOT_EXISTS)
            
            result.prepare_for_ack(msg_share, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        msg_event = msg_params_def.SubscriberMessageEvent.deserialize(events[0].content)
        
        add_article = msg_params_def.PortalContentArticleCreateReq()
        add_article.init_all_attr()
        add_article.user_session = ''
        add_article.title = msg_params_def.PORTAL_TXT_MSG_SHARE_TITLE.decode('gbk').encode('utf-8') % msg_event.nickname
        add_article.subject_id = msg_share.subject_id
        if msg_event.pic_url == '':
            add_article.pic_url = 'http://' + msg_params_def.LOCAL_HOST_DOMAIN + msg_params_def.PORTAL_IMG_FILE_USER_SHARE_MSG
            add_article.description = msg_params_def.PORTAL_TXT_MSG_SHARE_CONTENT.decode('gbk').encode('utf-8') % (msg_event.nickname, time.strftime('%Y-%m-%d %H:%M:%S'), msg_event.text_msg)

        else:
            pic_file_name = '%s.jpg' % str(int(time.time() * 1000))
            img_save_path = msg_params_def.PORTAL_IMG_FILE_SAVE_LOCAL_PATH % (msg_params_def.PORTAL_IMG_FILE_LOCAL_PATH_PREFIX, pic_file_name)
            urllib.urlretrieve(msg_event.pic_url, img_save_path)
            pic_url = msg_params_def.PORTAL_IMG_FILE_SAVE_LOCAL_PATH % ('http://' + msg_params_def.LOCAL_HOST_DOMAIN, pic_file_name)  
            add_article.pic_url = pic_url
            tracelog.info('share user message, source img path %s, download to local path %s, new img url %s' % (msg_event.pic_url, img_save_path, pic_url))
            add_article.description = msg_params_def.PORTAL_TXT_MSG_SHARE_IMG.decode('gbk').encode('utf-8') % (msg_event.nickname, time.strftime('%Y-%m-%d %H:%M:%S'))
        
        content_url = 'http://%s/index.php/weixin/content/showArticle/articleId' % msg_params_def.LOCAL_HOST_DOMAIN
        add_article.content_url = content_url
        add_article.content = add_article.description
        add_article.push_timer = ''
        add_article.push_times = ''

        grps = self.get_worker().get_app().get_mit_manager().rdm_find('Group')
        add_article.sub_group_ids = [str(grp.group_id) for grp in grps]
        
        new_frame = bf.AppFrame()
        new_frame.set_cmd_code(cmd_code_def.PORTAL_CONTENT_ARTICLE_CREATE)
        new_frame.add_data(add_article.serialize())
        self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("PortalManApp"), new_frame)        
        
        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(msg_share, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))

        
class EventManWorker(bf.CmdWorker):
    """
    Class: EventManWorker
    Description: 事件管理线程worker类
    Base: CmdWorker
    Others: 
    """

    
    def __init__(self, min_task_id, max_task_id):
        """
        Method: __init__
        Description: 类初始化
        Parameter: 
            min_task_id: 最小任务ID
            max_task_id: 最大任务ID
        Return: 
        Others: 
        """

        bf.CmdWorker.__init__(self, "EventManWorker", min_task_id, max_task_id)
        
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

        self.register_handler(EventCenterEventReportHandler(), cmd_code_def.PORTAL_EVENT_EVENT_REPORT)
        self.register_handler(EventCenterEventQueryHandler(), cmd_code_def.PORTAL_EVENT_EVENT_QUERY)
        self.register_handler(EventCenterReadEventNotifyHandler(), cmd_code_def.PORTAL_EVENT_READ_NOTIFY)
        self.register_handler(EventCenterUnreadEventQueryHandler(), cmd_code_def.PORTAL_EVENT_UNREAD_QUERY)
        self.register_handler(EventCenterMessageReplyHandler(),  cmd_code_def.PORTAL_EVENT_MESSAGE_REPLY)
        self.register_handler(EventCenterMessageShareHandler(),  cmd_code_def.PORTAL_EVENT_MESSAGE_SHARE)

        return 0

