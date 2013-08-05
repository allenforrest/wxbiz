#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-13
Description: 微信订阅者状态管理模块Worker
Key Class&Method List: 
             1. SubscriberManagerWorker -- 进程类
History:
1. Date: 2013-5-13
   Author: Allen
   Modification: create
"""

import cPickle
import time

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import mit
import tracelog
import basic_rep_to_web

import err_code_mgr
import cmd_code_def
import msg_params_def
import fsm_def
import subscriber_def
import subscriber_state_man

class SubscriberWXTextMsgHandler(bf.CmdHandler):
    """
    Class: SubscriberWXTextMsgHandler
    Description: 微信订阅者文本消息处理handler
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理微信订阅者文本消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        buf = frame.get_data()
        tracelog.info('receive WX text msg :%s' % buf)
        
        text_msg = msg_params_def.WXPushTextMessage.deserialize(buf)
        
        processor = self.get_worker().get_state_manager().get_processor(text_msg.subscriber_open_id)
        if processor is None:
            tracelog.error('receive WX text msg from unknown subscriber(open_id %s)' % text_msg.subscriber_open_id)

            reply_msg_type = msg_params_def.WX_MSG_TYPE_TEXT

            resub_msg = msg_params_def.WXReplyTextMessage()
            resub_msg.init_all_attr()
            resub_msg.subscriber_open_id = text_msg.subscriber_open_id
            resub_msg.public_account_id = text_msg.public_account_id
            resub_msg.create_time = str(int(time.time()))
            resub_msg.msg_type = reply_msg_type
            resub_msg.content = msg_params_def.WX_TXT_UNKNOWN_SUBSCRIBER.decode('gbk').encode('utf-8')
            resub_msg.func_flag = '0'
            
            self.get_worker().get_app().send_ack_dispatch(frame, (reply_msg_type, resub_msg.serialize()))
            return
        else:
            # 订阅者消息发送给状态机
            event = fsm_def.FsmEvent(fsm_def.SUBSCRIBER_MESSAGE_EVENT, text_msg.subscriber_open_id, frame.clone())
            new_frame = bf.AppFrame()
            new_frame.set_cmd_code(cmd_code_def.CLOUD_SUBSCRIBER_STATE_EVENT_MSG)
            new_frame.add_data(cPickle.dumps(event))
            self.get_worker().dispatch_frame_to_worker('SubscriberManagerWorker', new_frame)
            
            # 订阅者消息事件上报
            event_report = msg_params_def.PortalEventEventReportReq()
            event_report.init_all_attr()
            event_report.user_session = '0'
            event_report.event_type = msg_params_def.EVENT_TYPE_MESSAGE
            event = msg_params_def.SubscriberMessageEvent()
            event.init_all_attr()
            event.subscriber_open_id = text_msg.subscriber_open_id
            
            event.weixin_id = processor.get_target().get_spec().weixin_id
            event.nickname = processor.get_target().get_spec().nickname
            if processor.get_target().get_assoc_member() is not None:
                event.member_id = processor.get_target().get_assoc_member().member_id
                event.name = processor.get_target().get_assoc_member().name
            else:
                event.member_id = ''
                event.name = ''
                
            event.text_msg = text_msg.content
            event.pic_url = ''
            event.time = time.strftime('%Y-%m-%d %H:%M:%S')
            
            event_report.content = event.serialize()
            
            evt_frame = bf.AppFrame()
            evt_frame.set_cmd_code(cmd_code_def.PORTAL_EVENT_EVENT_REPORT)
            evt_frame.add_data(event_report.serialize())
            self.get_worker().dispatch_frame_to_process_by_pid(self.get_worker().get_pid('EventCenterApp'), evt_frame)

            
class SubscriberWXImageMsgHandler(bf.CmdHandler):
    """
    Class: SubscriberWXImageMsgHandler
    Description: 微信订阅者图片消息处理handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理微信订阅者图片消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        buf = frame.get_data()
        tracelog.info('receive WX image msg :%s' % buf)

        img_msg = msg_params_def.WXPushImageMessage.deserialize(buf)
        
        processor = self.get_worker().get_state_manager().get_processor(img_msg.subscriber_open_id)
        if processor is None:
            tracelog.error('receive WX img msg from unknown subscriber(open_id %s)' % img_msg.subscriber_open_id)
            return
        else:
            # 订阅者消息发送给状态机
            event = fsm_def.FsmEvent(fsm_def.SUBSCRIBER_MESSAGE_EVENT, img_msg.subscriber_open_id, frame.clone())
            new_frame = bf.AppFrame()
            new_frame.set_cmd_code(cmd_code_def.CLOUD_SUBSCRIBER_STATE_EVENT_MSG)
            new_frame.add_data(cPickle.dumps(event))
            self.get_worker().dispatch_frame_to_worker('SubscriberManagerWorker', new_frame)
            
            # 订阅者消息事件上报
            event_report = msg_params_def.PortalEventEventReportReq()
            event_report.init_all_attr()
            event_report.user_session = '0'
            event_report.event_type = msg_params_def.EVENT_TYPE_MESSAGE
            event = msg_params_def.SubscriberMessageEvent()
            event.init_all_attr()
            event.subscriber_open_id = img_msg.subscriber_open_id
            
            event.weixin_id = processor.get_target().get_spec().weixin_id
            event.nickname = processor.get_target().get_spec().nickname
            event.member_id = processor.get_target().get_spec().assoc_member_id
            event.name = ''#processor.get_target().get_spec().name
            event.text_msg = ''
            event.pic_url = img_msg.pic_url
            event.time = time.strftime('%Y-%m-%d %H:%M:%S')

            event_report.content = event.serialize()
            
            evt_frame = bf.AppFrame()
            evt_frame.set_cmd_code(cmd_code_def.PORTAL_EVENT_EVENT_REPORT)
            evt_frame.add_data(event_report.serialize())
            self.get_worker().dispatch_frame_to_process_by_pid(self.get_worker().get_pid('EventCenterApp'), evt_frame)


class SubscriberWXLocationMsgHandler(bf.CmdHandler):
    """
    Class: SubscriberWXLocationMsgHandler
    Description: 微信订阅者位置消息处理handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理微信订阅者位置消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        tracelog.info('receive WX location msg :%s' % frame.get_data())


class SubscriberWXLinkMsgHandler(bf.CmdHandler):
    """
    Class: SubscriberWXLinkMsgHandler
    Description: 微信订阅者链接消息处理handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理微信订阅者链接消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)       
        tracelog.info('receive WX link msg :%s' % frame.get_data())


class SubscriberWXEventMsgHandler(bf.CmdHandler):
    """
    Class: SubscriberWXEventMsgHandler
    Description: 微信订阅者事件消息处理handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理微信订阅者事件消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)        
        buf = frame.get_data()
        tracelog.info('receive WX event msg :%s' % buf)
        
        event_msg = msg_params_def.WXPushEventMessage.deserialize(buf)
     
        processor = self.get_worker().get_state_manager().get_processor(event_msg.subscriber_open_id)
        if processor is None:
            if event_msg.event == msg_params_def.WX_EVENT_TYPE_SUBSCRIBE:
                sub_moc = self.get_worker().get_app().get_mit_manager().gen_rdm("Subscriber")
                sub_moc.subscribe_seq_no = self.get_worker().get_app().get_sub_no_creator().get_new_no()
                sub_moc.subscriber_open_id = event_msg.subscriber_open_id
                sub_moc.sub_time = time.strftime('%Y-%m-%d %H:%M:%S')
                sub_moc.admin_flag = 'False'
                gids = msg_params_def.GroupList()
                gids.group_ids = [msg_params_def.GROUP_SYS_DEFAULT] # 初次订阅默认为未分组

                tracelog.info('new subscriber: openid %s, seqno %d' % (sub_moc.subscriber_open_id, sub_moc.subscribe_seq_no))

                sub = subscriber_def.Subscriber(sub_moc, gids, fsm_def.SUBSCRIBER_INIT_STATE)
                sub.save_frame(frame.clone())
                processor = fsm_def.StateProcessor(sub, self.get_worker())
                processor.register_state_handler(fsm_def.SUBSCRIBER_INIT_STATE, subscriber_state_man.SubInitStateHandler(processor))
                processor.register_state_handler(fsm_def.SUBSCRIBER_SESSION_STATE, subscriber_state_man.SubSessionStateHandler(processor))
                
                self.get_worker().get_state_manager().add_processor(processor)

                ret = self.get_worker().get_app().get_mit_manager().rdm_add(sub_moc)
                if ret.get_err_code() == err_code_mgr.ER_OBJECT_ADD_CONFLICT:
                    tracelog.warning('receive duplicate WX subscribe event from subscriber(sub id %d)' % event_msg.subscriber_open_id)

                moid = self.get_worker().get_app().get_mit_manager().gen_moid('Subscriber', subscriber_open_id = sub_moc.subscriber_open_id)
                self.get_worker().get_app().get_mit_manager().mod_complex_attr('Subscriber', moid = moid, group_ids = gids)
            else:
                tracelog.error('receive WX event(%s) msg from unknown subscriber(open_id %s)' % (event_msg.event, event_msg.subscriber_open_id))
            return
        else:
            if event_msg.event == msg_params_def.WX_EVENT_TYPE_UNSUBSCRIBE:
                tracelog.info('subscriber unsub openid %s' % event_msg.subscriber_open_id)
                
                subs = self.get_worker().get_app().get_mit_manager().rdm_find("Subscriber", subscriber_open_id = event_msg.subscriber_open_id)
                if len(subs) == 0:
                    tracelog.warning('receive unsubscribe event from open id %s, but the subscriber info does not exist in DB' % event_msg.subscriber_open_id)
                else:
                    self.get_worker().get_app().get_mit_manager().rdm_remove(subs[0])
                
                # 订阅事件上报
                event_report = msg_params_def.PortalEventEventReportReq()
                event_report.init_all_attr()
                event_report.user_session = '0'
                event_report.event_type = msg_params_def.EVENT_TYPE_SUBSCRIBE
                event = msg_params_def.SubscribeEvent()
                event.init_all_attr()
                event.subscriber_open_id = event_msg.subscriber_open_id
                event.weixin_id = processor.get_target().get_spec().weixin_id
                event.nickname = processor.get_target().get_spec().nickname
                event.action = '取消订阅'.decode('gbk').encode('utf-8')
                event.time = time.strftime('%Y-%m-%d %H:%M:%S')
    
                event_report.content = event.serialize()
                
                evt_frame = bf.AppFrame()
                evt_frame.set_cmd_code(cmd_code_def.PORTAL_EVENT_EVENT_REPORT)
                evt_frame.add_data(event_report.serialize())
                self.get_worker().dispatch_frame_to_process_by_pid(self.get_worker().get_pid('EventCenterApp'), evt_frame)

                self.get_worker().get_state_manager().remove_processor(processor)
                del processor

                return
        
        tracelog.warning('receive WX unsupported event(%s) notification msg' % event_msg.event)


class SubscriberStateEventMsgHandler(bf.CmdHandler):
    """
    Class: SubscriberStateEventMsgHandler
    Description: 订阅者状态机事件消息处理handler
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者状态机事件消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)       

        buf = frame.get_data()
        event = cPickle.loads(buf)
        self.get_worker().get_state_manager().process_event(event)
        

class SubscriberManInitHandler(bf.CmdHandler):
    """
    Class: SubscriberManInitHandler
    Description: 订阅者管理模块初始化消息处理handler 
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者管理模块初始化消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        subs = self.get_worker().get_app().get_mit_manager().rdm_find("Subscriber")
        for sub_moc in subs:
            grps = self.get_worker().get_app().get_mit_manager().lookup_attrs("Subscriber", ['group_ids'], subscriber_open_id = sub_moc.subscriber_open_id)
            sub = subscriber_def.Subscriber(sub_moc, grps[0][0], fsm_def.SUBSCRIBER_SESSION_STATE)

            if sub_moc.assoc_member_id is not None and len(sub_moc.assoc_member_id) > 0:
                mbrs = self.get_worker().get_app().get_mit_manager().rdm_find("Member", member_id = sub_moc.assoc_member_id)
                if len(mbrs) > 0:
                    sub.set_assoc_member(mbrs[0])
            
            processor = fsm_def.StateProcessor(sub, self.get_worker())
            processor.register_state_handler(fsm_def.SUBSCRIBER_INIT_STATE, subscriber_state_man.SubInitStateHandler(processor))
            processor.register_state_handler(fsm_def.SUBSCRIBER_SESSION_STATE, subscriber_state_man.SubSessionStateHandler(processor))
            
            self.get_worker().get_state_manager().add_processor(processor)          


class SubscriberContentUpdateMsgHandler(bf.CmdHandler):
    """
    Class: SubscriberContentUpdateMsgHandler
    Description: 内容更新通知消息处理handler
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理内容更新通知消息 
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        helptips = ''
        articles = {}
        
        helps = self.get_worker().get_app().get_mit_manager().rdm_find("HelpTips")
        subjects = self.get_worker().get_app().get_mit_manager().rdm_find("Subject")
        if len(helps) == 0 or len(subjects) == 0:
            tracelog.info('content update, but helptips or subject info does not exist in DB')
        else:
            sub_info = ''
            index = 1
            for sub in subjects:
                sub_info += '%s. %s\n' % (index, sub.name)
                articles[str(index)] = []

                multi_sql = mit.MultiSQL()
                multi_sql.set_sqlite_sql('article_id desc')                
                arts = self.get_worker().get_app().get_mit_manager().lookup_attrs("Article",
                                                                                 [
                                                                                  'article_id',
                                                                                  'title',
                                                                                  'description',
                                                                                  'pic_url',
                                                                                  'content_url',
                                                                                  'group_ids'
                                                                                  ],
                                                                                  order_by_sql = multi_sql,
                                                                                  subject_id = sub.subject_id)
                if len(arts) > 10:
                    for loop in xrange(10):
                        articles[str(index)].append(arts[loop])
                elif len(arts) > 0:
                    articles[str(index)] = arts
                    
                index += 1
                    
            helptips = helps[0].content + '\r\n' + msg_params_def.WX_TXT_SUBJECT_TIPS.decode('gbk').encode('utf-8') % sub_info
            
            self.get_worker().set_helptips(helptips)
            self.get_worker().set_articles(articles)
            

class SubscriberGroupAssocMsgHandler(bf.CmdHandler):
    """
    Class: SubscriberGroupAssocMsgHandler
    Description: 订阅者分组更新通知消息处理handler
    Base: CmdHandler
    Others: 
    """
    
    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者分组更新通知消息 
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()

        buf = frame.get_data()
        
        assoc_req = msg_params_def.PortalSubscriberGroupAssociateReq.deserialize(buf)
        
        gids = msg_params_def.GroupList()
        gids.group_ids = [int(gid) for gid in assoc_req.group_ids] 
        
        mo_id = self.get_worker().get_app().get_mit_manager().gen_moid("Subscriber", subscriber_open_id = assoc_req.subscriber_open_id)
        ret = self.get_worker().get_app().get_mit_manager().mod_complex_attr('Subscriber', 
                                                                             moid = mo_id, 
                                                                             group_ids = gids)
        if ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(assoc_req, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        processor = self.get_worker().get_state_manager().get_processor(assoc_req.subscriber_open_id)
        if processor is None:
            tracelog.error('subscriber(openid %s) from mit does not setup the sm processor!' % assoc_req.subscriber_open_id)
        else:
            processor.get_target().set_groups(gids)
            
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(assoc_req, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class SubscriberMemberAssocMsgHandler(bf.CmdHandler):
    """
    Class: SubscriberMemberAssocMsgHandler
    Description: 订阅者会员绑定通知消息处理handler
    Base: CmdHandler
    Others: 
    """
    
    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者会员绑定通知消息 
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()

        buf = frame.get_data()
        
        assoc_req = msg_params_def.PortalSubscriberMemberAssociateReq.deserialize(buf)

        subs = self.get_worker().get_app().get_mit_manager().rdm_find('Subscriber', subscriber_open_id = assoc_req.subscriber_open_id)        
        if len(subs) > 0:
            tracelog.info('subscriber %s assoc member %s succ' % (assoc_req.subscriber_open_id, assoc_req.member_id))
            subs[0].assoc_member_id = assoc_req.member_id
            ret = self.get_worker().get_app().get_mit_manager().rdm_mod(subs[0])
            if ret.get_err_code() != 0:
                result.return_code = ret.get_err_code()
                result.description = ret.get_msg()
                
                result.prepare_for_ack(assoc_req, result.return_code, result.description)
                self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                return
        
        processor = self.get_worker().get_state_manager().get_processor(assoc_req.subscriber_open_id)
        if processor is None:
            tracelog.error('subscriber(openid %s) from mit does not setup the sm processor!' % assoc_req.subscriber_open_id)
        else:
            mbrs = self.get_worker().get_app().get_mit_manager().rdm_find('Member', member_id = assoc_req.member_id)
            if len(mbrs) > 0:
                processor.get_target().set_assoc_member(mbrs[0])
            
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(assoc_req, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class SubscriberAdminAssocMsgHandler(bf.CmdHandler):
    """
    Class: SubscriberAdminAssocMsgHandler
    Description: 订阅者管理员绑定通知消息处理handler
    Base: CmdHandler
    Others: 
    """
    
    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者管理员绑定通知消息 
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()

        buf = frame.get_data()
        
        assoc_req = msg_params_def.PortalSubscriberAdminAssociateReq.deserialize(buf)
        
        old_subs = self.get_worker().get_app().get_mit_manager().rdm_find('Subscriber', admin_flag = 'True')
        if len(old_subs) > 0:
            old_sub_open_id = old_subs[0].subscriber_open_id
            old_subs[0].admin_flag = 'False'
            self.get_worker().get_app().get_mit_manager().rdm_mod(old_subs[0])

            old_processor = self.get_worker().get_state_manager().get_processor(old_sub_open_id)
            if old_processor is not None:
                old_processor.get_target().set_admin_flag('False')

        subs = self.get_worker().get_app().get_mit_manager().rdm_find('Subscriber', subscriber_open_id = assoc_req.subscriber_open_id)        
        if len(subs) > 0:
            subs[0].admin_flag = 'True'
            ret = self.get_worker().get_app().get_mit_manager().rdm_mod(subs[0])
            if ret.get_err_code() != 0:
                result.return_code = ret.get_err_code()
                result.description = ret.get_msg()
                
                result.prepare_for_ack(assoc_req, result.return_code, result.description)
                self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                return
        
        processor = self.get_worker().get_state_manager().get_processor(assoc_req.subscriber_open_id)
        if processor is None:
            tracelog.error('subscriber(openid %s) from mit does not setup the sm processor!' % assoc_req.subscriber_open_id)
        else:
            processor.get_target().set_admin_flag('True')
            
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(assoc_req, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class SubscriberTextMsgPushHandler(bf.CmdHandler):
    """
    Class: SubscriberTextMsgPushHandler
    Description: 文本消息主动发送给订阅者处理handler
    Base: CmdHandler
    Others: 
    """
    
    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理文本消息主动发送给订阅者命令 
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        buf = frame.get_data()
        push_msg = msg_params_def.CloudPortalTextPushMessage.deserialize(buf)
        
        for open_id in push_msg.subscriber_open_ids:
            processor = self.get_worker().get_state_manager().get_processor(open_id)
            if processor is None:
                tracelog.warning('portal text msg reply push to the unknown subscriber(openid %s)' % open_id)
            else:
                fakeid = processor.get_target().get_spec().fake_id

                tracelog.info('send text msg to fake_id %s' % fakeid)
                self.get_worker().get_app().get_task_worker().push_text(fakeid, push_msg.text_msg)


class SubscriberArticlePushHandler(bf.CmdHandler):
    """
    Class: SubscriberGroupAssocMsgHandler
    Description: 主题内容主动推送给订阅者处理handler
    Base: CmdHandler
    Others: 
    """
    
    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理主题内容主动推送给订阅者命令
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        buf = frame.get_data()
        push_msg = msg_params_def.CloudPortalArticlePushMessage.deserialize(buf)
        for sub_open_id in push_msg.sub_open_ids:
            processor = self.get_worker().get_state_manager().get_processor(sub_open_id)
            if len(processor.get_target().get_spec().fake_id) > 0:
                tracelog.info('push article id %d to fake_id %s, news_id %s' % (push_msg.article_id,
                                                                                processor.get_target().get_spec().fake_id,
                                                                                push_msg.wx_news_id))
                self.get_worker().get_app().get_task_worker().push_article(processor.get_target().get_spec().fake_id,
                                                                           push_msg.wx_news_id,
                                                                           push_msg.article_id)        


class SubscriberArticleUploadHandler(bf.CmdHandler):
    """
    Class: SubscriberArticleUploadHandler
    Description: 主题内容上传到微信后台处理handler
    Base: CmdHandler
    Others: 
    """
    
    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理主题内容上传到微信后台命令
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        op = frame.get_data()
        article_id = int(frame.get_data(1))
        
        if op == msg_params_def.PORTAL_CLOUD_IMAGE_UPLOAD_DEL:
            wx_news_id = frame.get_data(2)
            tracelog.info('del article on WX portal(id %d)' % article_id)
            if len(wx_news_id) == 0:
                tracelog.warning('the deleted article(id %d) has not created the news!' % article_id)
                return

            self.get_worker().get_app().get_task_worker().del_article(wx_news_id)
            return
        
        arts = self.get_worker().get_app().get_mit_manager().rdm_find('Article', article_id = article_id)
        if len(arts) == 0:
            tracelog.warning('portal want to %s the unknown article (id %d) on wx portal' % (op, article_id))
            self.get_worker().get_app().send_ack_dispatch(frame, ('', ))
            return
        
        if op == msg_params_def.PORTAL_CLOUD_IMAGE_UPLOAD_NEW:
            tracelog.info('create new article on WX portal(id %d)' % article_id)
            pic_url = arts[0].pic_url.strip('http://')
            pic_path = msg_params_def.PORTAL_IMG_FILE_LOCAL_PATH_PREFIX + pic_url[pic_url.find('/'):].lstrip('/')
            self.get_worker().get_app().get_task_worker().upload_article(article_id, pic_path, arts[0].title, arts[0].description, arts[0].content, 0)
                           
        elif op == msg_params_def.PORTAL_CLOUD_IMAGE_UPLOAD_MOD:
            tracelog.info('mod article on WX portal(id %d)' % article_id)
            if len(arts[0].wx_news_id) > 0:
                self.get_worker().get_app().get_task_worker().del_article(arts[0].wx_news_id)               

            pic_url = arts[0].pic_url.strip('http://')
            pic_path = msg_params_def.PORTAL_IMG_FILE_LOCAL_PATH_PREFIX + pic_url[pic_url.find('/'):].lstrip('/')
            self.get_worker().get_app().get_task_worker().upload_article(article_id, pic_path, arts[0].title, arts[0].description, arts[0].content, 0)               
        else:
            tracelog.warning('article upload msg has the unknown operation code %s' % op)               
        

class SubscriberManagerWorker(bf.CmdWorker):
    """
    Class: SubscriberManagerWorker
    Description: 订阅者状态管理模块
    Base: CmdWorker
    Others: 
    """

    def __init__(self, min_task_id, max_task_id):
        """
        Method: __init__
        Description: 类初始化
        Parameter: 无
        Return: 
        Others: 
        """

        bf.CmdWorker.__init__(self, "SubscriberManagerWorker", min_task_id, max_task_id)
        
        self._state_manager = fsm_def.FsmManager()
        self._state_manager.register_event_handler(fsm_def.SUBSCRIBER_INIT_STATE, fsm_def.SUBSCRIBER_MESSAGE_EVENT, subscriber_state_man.SubInitStateMessageEventHandler())
        self._state_manager.register_event_handler(fsm_def.SUBSCRIBER_SESSION_STATE, fsm_def.SUBSCRIBER_MESSAGE_EVENT, subscriber_state_man.SubSessionStateMessageEventHandler())
        
        # 欢迎词与帮助语的缓存
        self._helptips_cache = ''
        # 主题内容的缓存, key: subject_id, value: article列表
        self._articles_cache = {}
        self.__wan_ip = None
        self.__outer_nc_ip = None 

    def set_helptips(self, helptips):
        self._helptips_cache = helptips

    def set_articles(self, articles):
        self._articles_cache = articles
            
    def get_helptips(self):
        return self._helptips_cache
    
    def get_articles(self, subject_id):
        if self._articles_cache.has_key(subject_id):
            return self._articles_cache[subject_id]
        else:
            return None

    def get_state_manager(self):
        """
        Method: get_state_manager
        Description: 获取订阅者状态管理器
        Parameter: 无
        Return: 读写器状态管理器
        Others: 
        """
        return self._state_manager

    def ready_for_work(self):
        """
        Method: ready_for_work
        Description: 注册命令处理handler
        Parameter: 无
        Return: 
        Others: 
        """

        self.register_handler(SubscriberWXTextMsgHandler(),     cmd_code_def.CLOUD_WX_PUSH_TEXT_MSG)
        self.register_handler(SubscriberWXImageMsgHandler(),    cmd_code_def.CLOUD_WX_PUSH_IMAGE_MSG)
        self.register_handler(SubscriberWXLocationMsgHandler(), cmd_code_def.CLOUD_WX_PUSH_LOCATION_MSG)
        self.register_handler(SubscriberWXLinkMsgHandler(),     cmd_code_def.CLOUD_WX_PUSH_LINK_MSG)
        self.register_handler(SubscriberWXEventMsgHandler(),    cmd_code_def.CLOUD_WX_PUSH_EVENT_MSG)
        self.register_handler(SubscriberStateEventMsgHandler(), cmd_code_def.CLOUD_SUBSCRIBER_STATE_EVENT_MSG)

        self.register_handler(SubscriberContentUpdateMsgHandler(), cmd_code_def.CLOUD_PORTAL_CONTENT_UPDATE_MSG)
        self.register_handler(SubscriberGroupAssocMsgHandler(),    cmd_code_def.CLOUD_PORTAL_SUB_GROUP_ASSOC_MSG)
        self.register_handler(SubscriberMemberAssocMsgHandler(),   cmd_code_def.CLOUD_PORTAL_SUB_MEMBER_ASSOC_MSG)
        self.register_handler(SubscriberAdminAssocMsgHandler(),    cmd_code_def.CLOUD_PORTAL_SUB_ADMIN_ASSOC_MSG)
        self.register_handler(SubscriberTextMsgPushHandler(),      cmd_code_def.CLOUD_PORTAL_TEXT_PUSH_MSG)
        self.register_handler(SubscriberArticlePushHandler(),      cmd_code_def.CLOUD_PORTAL_ARTICLE_PUSH_MSG)
        self.register_handler(SubscriberArticleUploadHandler(),    cmd_code_def.CLOUD_PORTAL_ARTICLE_UPLOAD_MSG)
        
        self.register_handler(SubscriberManInitHandler(), cmd_code_def.CLOUD_SUBSCRIBER_MANAGER_INIT_MSG)
        
        frame = bf.AppFrame()
        frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_CONTENT_UPDATE_MSG)
        self.dispatch_frame_to_worker('SubscriberManagerWorker', frame)

        frame = bf.AppFrame()
        frame.set_cmd_code(cmd_code_def.CLOUD_SUBSCRIBER_MANAGER_INIT_MSG)
        self.dispatch_frame_to_worker('SubscriberManagerWorker', frame)
        
        self.__outer_nc_ip = msg_params_def.LOCAL_HOST_DOMAIN #self.get_app().get_device_cfg_info().get_device_external_ip()
                
        return 0

    def update_wan_ip(self, ip):
        self.__wan_ip = ip
        
    def update_url(self, url):
        if self.__wan_ip is None:
            u = url.strip('http://')
            new_url = 'http://' + self.__outer_nc_ip + u[u.find('/'):]
            return new_url
        else:
            u = url.strip('http://')
            new_url = 'http://' + self.__wan_ip + u[u.find('/'):]
            return new_url

