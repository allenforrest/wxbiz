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

        tracelog.info ('subscriber %s enter %s state' % (self._processor.get_target().get_id(), fsm_def.INIT_STATE))
        if self._processor.get_target().get_old_state() == fsm_def.INIT_STATE:
            return

        last_frame = self._processor.get_target().get_last_frame()
        wx_sub_msg = msg_params_def.WXPushEventMessage.deserialize(last_frame.get_data())
        
        content = msg_params_def.WX_TXT_SUBSCRIBE_TIPS.decode('gbk').encode('utf-8') % self._processor.get_target().get_spec().subscribe_seq_no
        content += "\r\n" + self._processor.get_worker().get_helptips()
        
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

        tracelog.info ('subscriber %s exec %s state' % (self._processor.get_target().get_id(), fsm_def.INIT_STATE))

    def exit_state(self):
        """
        Method: exit_state
        Description: 
        Parameter: 
        Return: 
        Others: 
        """
        tracelog.info ('subscriber %s exit %s state' % (self._processor.get_target().get_id(), fsm_def.INIT_STATE))


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

        tracelog.info ('subscriber %s enter %s state' % (self._processor.get_target().get_id(), fsm_def.SESSION_STATE))

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
                        err_reply = msg_params_def.WX_TXT_ERROR_INPUT.decode('gbk').encode('utf-8') + '\r\n' + self._processor.get_worker().get_helptips()
                    else:
                        err_reply = msg_params_def.WX_TXT_WELCOME_SHARE.decode('gbk').encode('utf-8')
                    reply_msg.content = err_reply
                elif len(article_list) == 0:
                    err_reply = msg_params_def.WX_TXT_NULL_SUBJECT.decode('gbk').encode('utf-8')
                    reply_msg.content = err_reply
                else:
                    del reply_msg
                    reply_msg_type = msg_params_def.WX_MSG_TYPE_NEWS
                    
                    reply_msg = msg_params_def.WXReplyNewsMessage()
                    reply_msg.init_all_attr()
                    reply_msg.subscriber_open_id = wx_msg.subscriber_open_id
                    reply_msg.public_account_id = wx_msg.public_account_id
                    reply_msg.create_time = str(int(time.time()))
                    reply_msg.msg_type = reply_msg_type
                    reply_msg.func_flag = '0'
                    reply_msg.articles = []

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
                        reply_msg.articles.append(wx_article)

                    reply_msg.article_count = len(reply_msg.articles)
            
            self._processor.get_worker().get_app().send_ack_dispatch(last_frame, (reply_msg_type, reply_msg.serialize()))
            self._processor.get_target().free_frame()
        
    def exec_state(self):
        """
        Method: exec_state
        Description: 
        Parameter: 
        Return: 
        Others: 
        """

        tracelog.info ('subscriber %s exec %s state' % (self._processor.get_target().get_id(), fsm_def.SESSION_STATE))

    def exit_state(self):
        """
        Method: exit_state
        Description: 
        Parameter:
        Return: 
        Others: 
        """
        tracelog.info ('subscriber %s exit %s state' % (self._processor.get_target().get_id(), fsm_def.SESSION_STATE))


class SubMenuSelectStateHandler(fsm_def.BaseStateHandler):
    """
    Class: SubMenuSelectStateHandler
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

        tracelog.info ('subscriber %s enter %s state' % (self._processor.get_target().get_id(), fsm_def.MENU_SELECT_STATE))
        if self._processor.get_target().get_old_state() == fsm_def.MENU_SELECT_STATE:
            return
        
    def exec_state(self):
        """
        Method: exec_state
        Description:
        Parameter:
        Return: 
        Others: 
        """

        tracelog.info ('subscriber %s exec %s state' % (self._processor.get_target().get_id(), fsm_def.MENU_SELECT_STATE))

    def exit_state(self):
        """
        Method: exit_state
        Description: 
        Parameter:
        Return: 
        Others: 
        """
        tracelog.info ('subscriber %s exit %s state' % (self._processor.get_target().get_id(), fsm_def.MENU_SELECT_STATE))


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
        return fsm_def.SESSION_STATE


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

        return fsm_def.SESSION_STATE
                

class SubSessionStateMenuSelectEventHandler(fsm_def.FsmHandler):
    """
    Class: SubSessionStateMenuSelectEventHandler
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
        return fsm_def.MENU_SELECT_STATE
    

class SubMenuSelectStateMessageEventHandler(fsm_def.FsmHandler):
    """
    Class: SubMenuSelectStateMessageEventHandler
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
        return fsm_def.MENU_SELECT_STATE
  
  
        