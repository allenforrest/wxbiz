#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-18
Description: 订阅者状态机管理模块
Key Class&Method List: 
             1. SubInitStateHandler
             2. SubSessionStateHandler
             3. SubMenuSelectStateHandler
History:
1. Date: 2013-5-18
   Author: Allen
   Modification: create
"""

import time
import cPickle

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import tracelog

import err_code_mgr
import cmd_code_def
import msg_params_def
import fsm_def
import subscriber_def
import sys


class SubInitStateHandler(fsm_def.BaseStateHandler):
    """
    Class: SubInitStateHandler
    Description: 
    Base: BaseStateHandler
    Others: 
    """

    def enter_state(self):
        """
        Method: enter_state
        Description: 
        Parameter: 
        Return: 
        Others: 
        """

        tracelog.info ('subscriber %s enter %s state' % (self._processor.get_target().get_id(), fsm_def.SUBSCRIBER_INIT_STATE))
        if self._processor.get_target().get_old_state() == fsm_def.SUBSCRIBER_INIT_STATE:
            return

        last_frame = self._processor.get_target().get_last_frame()
        wx_sub_msg = msg_params_def.WXPushEventMessage.deserialize(last_frame.get_data())
        
        content = self._processor.get_worker().get_helptips()
        content += "\r\n" + msg_params_def.WX_TXT_SUBSCRIBE_TIPS.decode('gbk').encode('utf-8') % self._processor.get_target().get_spec().subscribe_seq_no
        
        reply_msg_type = msg_params_def.WX_MSG_TYPE_TEXT
        
        sub_welcome_msg = msg_params_def.WXReplyTextMessage()
        sub_welcome_msg.init_all_attr()
        sub_welcome_msg.subscriber_open_id = wx_sub_msg.subscriber_open_id
        sub_welcome_msg.public_account_id = wx_sub_msg.public_account_id
        sub_welcome_msg.create_time = str(int(time.time()))
        sub_welcome_msg.msg_type = reply_msg_type
        sub_welcome_msg.content = content
        sub_welcome_msg.func_flag = '0'
        
        self._processor.get_worker().get_app().send_ack_dispatch(last_frame, (reply_msg_type, sub_welcome_msg.serialize()))
        self._processor.get_target().free_frame()
        
    def exec_state(self):
        """
        Method: exec_state
        Description: 
        Parameter:
        Return: 
        Others: 
        """

        tracelog.info ('subscriber %s exec %s state' % (self._processor.get_target().get_id(), fsm_def.SUBSCRIBER_INIT_STATE))

    def exit_state(self):
        """
        Method: exit_state
        Description: 
        Parameter: 
        Return: 
        Others: 
        """
        tracelog.info ('subscriber %s exit %s state' % (self._processor.get_target().get_id(), fsm_def.SUBSCRIBER_INIT_STATE))


class SubSessionStateHandler(fsm_def.BaseStateHandler):
    """
    Class: SubSessionStateHandler
    Description: 
    Base: BaseStateHandler
    Others: 
    """

    def enter_state(self):
        """
        Method: enter_state
        Description: 
        Parameter: 
        Return: 
        Others: 
        """

        tracelog.info ('subscriber %s enter %s state' % (self._processor.get_target().get_id(), fsm_def.SUBSCRIBER_SESSION_STATE))

        if self._processor.get_target().get_old_state() is not None:
            last_frame = self._processor.get_target().get_last_frame()
            if last_frame.get_cmd_code() == cmd_code_def.CLOUD_WX_PUSH_TEXT_MSG:
                wx_msg = msg_params_def.WXPushTextMessage.deserialize(last_frame.get_data())
            elif last_frame.get_cmd_code() == cmd_code_def.CLOUD_WX_PUSH_IMAGE_MSG:
                wx_msg = msg_params_def.WXPushImageMessage.deserialize(last_frame.get_data())
    
            reply_msg_type = msg_params_def.WX_MSG_TYPE_TEXT
            
            reply_msg = msg_params_def.WXReplyTextMessage()
            reply_msg.init_all_attr()
            reply_msg.subscriber_open_id = wx_msg.subscriber_open_id
            reply_msg.public_account_id = wx_msg.public_account_id
            reply_msg.create_time = str(int(time.time()))
            reply_msg.msg_type = reply_msg_type
            reply_msg.func_flag = '0'
        
            if last_frame.get_cmd_code() == cmd_code_def.CLOUD_WX_PUSH_IMAGE_MSG:
                reply_msg.content = msg_params_def.WX_TXT_WELCOME_SHARE.decode('gbk').encode('utf-8')
            else:
                
                wx_input = wx_msg.content
                article_list = self._processor.get_worker().get_articles(wx_input)
                if article_list is None:
                    if wx_input.isdigit() is True:
                        reply_msg_type = msg_params_def.WX_MSG_TYPE_NEWS
                
                        description = self._processor.get_worker().get_helptips()
                
                        news_reply_msg = msg_params_def.WXReplyNewsMessage()
                        news_reply_msg.init_all_attr()
                        news_reply_msg.subscriber_open_id = wx_msg.subscriber_open_id
                        news_reply_msg.public_account_id = wx_msg.public_account_id
                        news_reply_msg.create_time = str(int(time.time()))
                        news_reply_msg.msg_type = reply_msg_type
                        news_reply_msg.func_flag = '0'
                        news_reply_msg.articles = []
                
                        wx_article = msg_params_def.WXArticle()
                        wx_article.init_all_attr()
                        wx_article.title = msg_params_def.WX_TXT_ERROR_INPUT.decode('gbk').encode('utf-8')
                        wx_article.description = description
                        wx_article.pic_url = ''
                        wx_article.url = ''
                        
                        news_reply_msg.articles.append(wx_article)
                
                        news_reply_msg.article_count = 1
                        
                        err_reply = None
                        #err_reply = msg_params_def.WX_TXT_ERROR_INPUT.decode('gbk').encode('utf-8') + '\r\n' + self._processor.get_worker().get_helptips()
                    else:
                        """
                        if wx_msg.subscriber_open_id in msg_params_def.ALL_MILK_OPENID:
                            if wx_input.find(msg_params_def.MSG_A_MILK) >= 0:
                                stock = 'out of stock' if self._processor.get_worker().get_app().get_windeln_info()[1] is True else 'in stock'
                                err_reply = '%s: price %s, %s!' % (msg_params_def.MSG_A_MILK, self._processor.get_worker().get_app().get_windeln_info()[0], stock)
                            elif wx_input.find(msg_params_def.MSG_H_MILK) >= 0:
                                err_reply = '%s monitor service not available' % msg_params_def.MSG_H_MILK
                            elif wx_input == msg_params_def.MSG_ACK_KNOWN:
                                err_reply = 'notify done!'
                                self._processor.get_worker().get_app().get_task_worker().set_notify(wx_msg.subscriber_open_id, False)
                        else:
                        """
                        if wx_input.find('会员'.decode('gbk').encode('utf-8')) >= 0:
                            reply_msg_type = msg_params_def.WX_MSG_TYPE_NEWS
                            news_reply_msg = msg_params_def.WXReplyNewsMessage()
                            news_reply_msg.init_all_attr()
                            news_reply_msg.subscriber_open_id = wx_msg.subscriber_open_id
                            news_reply_msg.public_account_id = wx_msg.public_account_id
                            news_reply_msg.create_time = str(int(time.time()))
                            news_reply_msg.msg_type = reply_msg_type
                            news_reply_msg.func_flag = '0'
                            news_reply_msg.articles = []
                    
                            wx_article = msg_params_def.WXArticle()
                            wx_article.init_all_attr()
                            wx_article.title = msg_params_def.PORTAL_TXT_MBR_ASSOC_TITLE.decode('gbk').encode('utf-8')
                            wx_article.description = msg_params_def.PORTAL_TXT_MBR_ASSOC_DESCRIPTION.decode('gbk').encode('utf-8')
                            pic_url = 'http://%s/' % msg_params_def.LOCAL_HOST_DOMAIN + msg_params_def.WX_MEMBER_MBR_ASSOC_ARTICLE_IMG_URL
                            wx_article.pic_url = self._processor.get_worker().update_url(pic_url)
                            url = 'http://%s/' % msg_params_def.LOCAL_HOST_DOMAIN + msg_params_def.WX_MEMBER_MBR_ASSOC_PORTAL_URL + wx_msg.subscriber_open_id
                            wx_article.url = self._processor.get_worker().update_url(url)
                            
                            news_reply_msg.articles.append(wx_article)
                            news_reply_msg.article_count = 1
                            err_reply = None
                        elif wx_input.find('菜单'.decode('gbk').encode('utf-8')) >= 0:
                            if self._processor.get_target().get_assoc_member() is None:
                                err_reply = msg_params_def.WX_TXT_INVALID_MEMBER.decode('gbk').encode('utf-8')
                            else:
                                reply_msg_type = msg_params_def.WX_MSG_TYPE_NEWS
                                news_reply_msg = msg_params_def.WXReplyNewsMessage()
                                news_reply_msg.init_all_attr()
                                news_reply_msg.subscriber_open_id = wx_msg.subscriber_open_id
                                news_reply_msg.public_account_id = wx_msg.public_account_id
                                news_reply_msg.create_time = str(int(time.time()))
                                news_reply_msg.msg_type = reply_msg_type
                                news_reply_msg.func_flag = '0'
                                news_reply_msg.articles = []
                        
                                wx_article = msg_params_def.WXArticle()
                                wx_article.init_all_attr()
                                wx_article.title = msg_params_def.PORTAL_TXT_MENU_CFG_TITLE.decode('gbk').encode('utf-8')
                                wx_article.description = msg_params_def.PORTAL_TXT_MENU_CFG_DESCRIPTION.decode('gbk').encode('utf-8')
                                pic_url = 'http://%s/' % msg_params_def.LOCAL_HOST_DOMAIN + msg_params_def.WX_MEMBER_MENU_CFG_ARTICLE_IMG_URL
                                wx_article.pic_url = self._processor.get_worker().update_url(pic_url)
                                url = 'http://%s/' % msg_params_def.LOCAL_HOST_DOMAIN + msg_params_def.WX_MEMBER_MENU_CFG_PORTAL_URL + self._processor.get_target().get_spec().assoc_member_id
                                wx_article.url = self._processor.get_worker().update_url(url)
                                
                                news_reply_msg.articles.append(wx_article)
                                news_reply_msg.article_count = 1
                                err_reply = None
                        else:
                            #err_reply = msg_params_def.WX_TXT_WELCOME_SHARE.decode('gbk').encode('utf-8')
                            reply_msg_type = msg_params_def.WX_MSG_TYPE_NEWS
                    
                            description = self._processor.get_worker().get_helptips()
                    
                            news_reply_msg = msg_params_def.WXReplyNewsMessage()
                            news_reply_msg.init_all_attr()
                            news_reply_msg.subscriber_open_id = wx_msg.subscriber_open_id
                            news_reply_msg.public_account_id = wx_msg.public_account_id
                            news_reply_msg.create_time = str(int(time.time()))
                            news_reply_msg.msg_type = reply_msg_type
                            news_reply_msg.func_flag = '0'
                            news_reply_msg.articles = []
                    
                            wx_article = msg_params_def.WXArticle()
                            wx_article.init_all_attr()
                            wx_article.title = msg_params_def.WX_TXT_WELCOME_SHARE.decode('gbk').encode('utf-8')
                            wx_article.description = description
                            wx_article.pic_url = ''
                            wx_article.url = ''
                            
                            news_reply_msg.articles.append(wx_article)
                    
                            news_reply_msg.article_count = 1
                            
                            err_reply = None
                            
                    reply_msg.content = err_reply
                elif len(article_list) == 0:
                    err_reply = msg_params_def.WX_TXT_NULL_SUBJECT.decode('gbk').encode('utf-8')
                    reply_msg.content = err_reply
                else:
                    reply_msg_type = msg_params_def.WX_MSG_TYPE_NEWS
                    
                    news_reply_msg = msg_params_def.WXReplyNewsMessage()
                    news_reply_msg.init_all_attr()
                    news_reply_msg.subscriber_open_id = wx_msg.subscriber_open_id
                    news_reply_msg.public_account_id = wx_msg.public_account_id
                    news_reply_msg.create_time = str(int(time.time()))
                    news_reply_msg.msg_type = reply_msg_type
                    news_reply_msg.func_flag = '0'
                    news_reply_msg.articles = []

                    sub_grps = self._processor.get_target().get_group_ids().group_ids
                    
                    for article in article_list:
                        art_grps = article[5].group_ids
                        
                        flag = False
                        for sub_grp in sub_grps:
                            if sub_grp in art_grps:
                                flag = True
                                break
                        
                        if flag is False:
                            continue
                        
                        wx_article = msg_params_def.WXArticle()
                        wx_article.init_all_attr()
                        wx_article.title = article[1]
                        wx_article.description = article[2]
                        wx_article.pic_url = article[3]
                        wx_article.url = article[4]
                        news_reply_msg.articles.append(wx_article)

                    news_reply_msg.article_count = len(news_reply_msg.articles)
                    if news_reply_msg.article_count == 0:
                        reply_msg_type = msg_params_def.WX_MSG_TYPE_TEXT
                        err_reply = msg_params_def.WX_TXT_NULL_SUBJECT.decode('gbk').encode('utf-8')
                        reply_msg.content = err_reply

            msg = reply_msg if reply_msg.content is not None else news_reply_msg
            self._processor.get_worker().get_app().send_ack_dispatch(last_frame, (reply_msg_type, msg.serialize()))
            self._processor.get_target().free_frame()
        
    def exec_state(self):
        """
        Method: exec_state
        Description: 
        Parameter: 
        Return: 
        Others: 
        """

        tracelog.info ('subscriber %s exec %s state' % (self._processor.get_target().get_id(), fsm_def.SUBSCRIBER_SESSION_STATE))

    def exit_state(self):
        """
        Method: exit_state
        Description: 
        Parameter:
        Return: 
        Others: 
        """
        tracelog.info ('subscriber %s exit %s state' % (self._processor.get_target().get_id(), fsm_def.SUBSCRIBER_SESSION_STATE))


class SubInitStateMessageEventHandler(fsm_def.FsmHandler):
    """
    Class: SubInitStateMessageEventHandler
    Description: 
    Base: FsmHandler
    Others: 
    """

    def handle(self, processor, event):
        """
        Method: handle
        Description: 
        Parameter: 
            processor: 
            event: 
        Return: 
        Others: 
        """

        tracelog.info(self)
        processor.get_target().save_frame(event.other_info)
        return fsm_def.SUBSCRIBER_SESSION_STATE


class SubSessionStateMessageEventHandler(fsm_def.FsmHandler):
    """
    Class: SubSessionStateMessageEventHandler
    Description: 
    Base: FsmHandler
    Others: 
    """

    def handle(self, processor, event):
        """
        Method: handle
        Description: 
        Parameter: 
            processor: 
            event: 
        Return: 
        Others: 
        """
        tracelog.info(self)
        processor.get_target().save_frame(event.other_info)

        return fsm_def.SUBSCRIBER_SESSION_STATE
                

