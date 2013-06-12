#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-11
Description: 微信接口Gate 消息处理worker
Key Class&Method List: 
             1. WXGateApp -- 进程类
History:
1. Date: 2013-5-11
   Author: Allen
   Modification: create
"""
import import_paths

import bundleframework as bf
import tracelog
import cmd_code_def
import msg_params_def
import err_code_mgr

from lxml import etree

class WXTextMsgProc(object):
    def __init__(self, xml_dict):
        self._xml = xml_dict
    
    def gen_msg(self):
        msg = msg_params_def.WXPushTextMessage()
        msg.init_all_attr()
        msg.subscriber_open_id = self._xml['FromUserName']
        msg.public_account_id = self._xml['ToUserName']
        msg.create_time = self._xml['CreateTime']
        msg.msg_type = msg_params_def.WX_MSG_TYPE_TEXT
        msg.content = self._xml['Content']
        msg.msg_id = self._xml['MsgId']
        return (cmd_code_def.CLOUD_WX_PUSH_TEXT_MSG, msg)

class WXImageMsgProc(object):
    def __init__(self, xml_dict):
        self._xml = xml_dict
    
    def gen_msg(self):
        msg = msg_params_def.WXPushImageMessage()
        msg.init_all_attr()
        msg.subscriber_open_id = self._xml['FromUserName']
        msg.public_account_id = self._xml['ToUserName']
        msg.create_time = self._xml['CreateTime']
        msg.msg_type = msg_params_def.WX_MSG_TYPE_IMAGE
        msg.pic_url = self._xml['PicUrl']
        msg.msg_id = self._xml['MsgId']
        return (cmd_code_def.CLOUD_WX_PUSH_IMAGE_MSG, msg)

class WXLocationMsgProc(object):
    def __init__(self, xml_dict):
        self._xml = xml_dict
    
    def gen_msg(self):
        msg = msg_params_def.WXPushLocationMessage()
        msg.init_all_attr()
        msg.subscriber_open_id = self._xml['FromUserName']
        msg.public_account_id = self._xml['ToUserName']
        msg.create_time = self._xml['CreateTime']
        msg.msg_type = msg_params_def.WX_MSG_TYPE_LOCATION
        msg.location_x = self._xml['Location_X']
        msg.location_y = self._xml['Location_Y']
        msg.scale = self._xml['Scale']
        msg.label = self._xml['Label']
        msg.msg_id = self._xml['MsgId']
        return (cmd_code_def.CLOUD_WX_PUSH_LOCATION_MSG, msg)

class WXLinkMsgProc(object):
    def __init__(self, xml_dict):
        self._xml = xml_dict
    
    def gen_msg(self):
        msg = msg_params_def.WXPushLinkMessage()
        msg.init_all_attr()
        msg.subscriber_open_id = self._xml['FromUserName']
        msg.public_account_id = self._xml['ToUserName']
        msg.create_time = self._xml['CreateTime']
        msg.msg_type = msg_params_def.WX_MSG_TYPE_LINK
        msg.title = self._xml['Title']
        msg.description = self._xml['Description']
        msg.url = self._xml['Url']
        msg.msg_id = self._xml['MsgId']
        return (cmd_code_def.CLOUD_WX_PUSH_LINK_MSG, msg)

class WXEventMsgProc(object):
    def __init__(self, xml_dict):
        self._xml = xml_dict
    
    def gen_msg(self):
        msg = msg_params_def.WXPushEventMessage()
        msg.init_all_attr()
        msg.subscriber_open_id = self._xml['FromUserName']
        msg.public_account_id = self._xml['ToUserName']
        msg.create_time = self._xml['CreateTime']
        msg.msg_type = msg_params_def.WX_MSG_TYPE_EVENT
        msg.event = self._xml['Event']
        msg.event_key = self._xml['EventKey']
        return (cmd_code_def.CLOUD_WX_PUSH_EVENT_MSG, msg)
    
class WXRplTextMsgProc(object):
    def __init__(self, msg):
        self._msg = msg_params_def.WXReplyTextMessage.deserialize(msg)
    
    def gen_xml(self):
        text_tpl = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]>
        </Content><FuncFlag>0</FuncFlag>
        </xml>"""
        text_xml = text_tpl % (self._msg.subscriber_open_id,
                               self._msg.public_account_id,
                               self._msg.create_time,
                               self._msg.content
                               )
        return text_xml

class WXRplMusicMsgProc(object):
    def __init__(self, msg):
        self._msg = msg_params_def.WXReplyMusicMessage.deserialize(msg)
    
    def gen_xml(self):
        music_tpl = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[music]]></MsgType>
        <Music>
        <Title><![CDATA[%s]]></Title>
        <Description><![CDATA[%s]]></Description>
        <MusicUrl><![CDATA[%s]]></MusicUrl>
        <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
        </Music>
        <FuncFlag>0</FuncFlag>
        </xml>"""
        music_xml = music_tpl % (self._msg.subscriber_open_id,
                               self._msg.public_account_id,
                               self._msg.create_time,
                               self._msg.title,
                               self._msg.description,
                               self._msg.music_url,
                               self._msg.hq_music_url,
                               )
        return music_xml        

class WXRplNewsMsgProc(object):
    def __init__(self, msg):
        self._msg = msg_params_def.WXReplyNewsMessage.deserialize(msg)
    
    def gen_xml(self):
        news_tpl = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>%s</ArticleCount>
        <Articles>
        %s
        </Articles>
        <FuncFlag>1</FuncFlag>
        </xml>"""

        article_tpl = """<item>
        <Title><![CDATA[%s]]></Title>
        <Description><![CDATA[%s]]></Description>
        <PicUrl><![CDATA[%s]]></PicUrl>
        <Url><![CDATA[%s]]></Url>
        </item>"""
        
        articles_xml = ""
        
        for count in xrange(self._msg.article_count):
            article = self._msg.articles[count]
            articles_xml += article_tpl % (article.title,
                                           article.description,
                                           article.pic_url,
                                           article.url
                                           )
        news_xml = news_tpl % (self._msg.subscriber_open_id,
                               self._msg.public_account_id,
                               self._msg.create_time,
                               str(self._msg.article_count),
                               articles_xml
                               )
        return news_xml  


class WXPushMessageHandler(bf.CmdHandler):
    """
    Class: RecvWXMessageHandler
    Description: 接收微信发来的消息，解析XML，转发给业务模块
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理消息，解析XML，转发给业务模块，接收业务模块的响应，构造XML返回给微信
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        self._req_frame = frame
        
        wx_msg_proc_dict = {
                            msg_params_def.WX_MSG_TYPE_TEXT: WXTextMsgProc,
                            msg_params_def.WX_MSG_TYPE_IMAGE: WXImageMsgProc,
                            msg_params_def.WX_MSG_TYPE_LOCATION: WXLocationMsgProc,
                            msg_params_def.WX_MSG_TYPE_LINK: WXLinkMsgProc,
                            msg_params_def.WX_MSG_TYPE_EVENT: WXEventMsgProc
                            }
    
        buf = frame.get_data()
        tracelog.info('recv msg from WX: %s' % buf)

        self._message = msg_params_def.CommonContentReq.deserialize(buf)
        
        root = etree.fromstring(self._message.content)
        msg_dict = {}
        for child in root:
            msg_dict[child.tag] = child.text
        
        wx_msg_proc = wx_msg_proc_dict[msg_dict['MsgType']]
        cmd, msg = wx_msg_proc(msg_dict).gen_msg()
        
        sub_frame = bf.AppFrame()
        sub_frame.set_cmd_code(cmd)
        sub_frame.set_receiver_pid(self.get_worker().get_pid("SubscriberManApp"))
        sub_frame.add_data(msg.serialize())
        self.wait_for_ack(sub_frame, 5)

    def _on_round_timeout(self, round_id, r):
        """
        Method: _on_round_timeout
        Description: 命令Round超时处理
        Parameter: 
            round_id: 
            r: 
        Return: 
        Others: 
        """
        # 微信5秒收不到响应会断开连接，因此无需太复杂的异常处理，记录日志即可
        tracelog.error('send message to SubscriberManApp, ack timeout')        
        
    def _on_round_over(self, round_id, r):        
        """
        Method: _on_round_over
        Description: 接收业务模块的响应，构造XML返回给微信
        Parameter: 
            round_id: 
            r: 
        Return: 
        Others: 
        """
        frame = r.get_response_frame()
        msg_type = frame.get_data()
        msg_buf = frame.get_data(1)

        wx_rpl_msg_proc_dict = {msg_params_def.WX_MSG_TYPE_TEXT: WXRplTextMsgProc,
                                msg_params_def.WX_MSG_TYPE_MUSIC: WXRplMusicMsgProc,
                                msg_params_def.WX_MSG_TYPE_NEWS: WXRplNewsMsgProc,
                                }        
        wx_rpl_msg_proc = wx_rpl_msg_proc_dict[msg_type]
        xml_msg = wx_rpl_msg_proc(msg_buf).gen_xml()
        
        reply = msg_params_def.CommonContentRsp()
        reply.init_all_attr()
        reply.return_code = err_code_mgr.ER_SUCCESS
        reply.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        reply.prepare_for_ack(self._message, reply.return_code, reply.description)          
        reply.content = xml_msg

        tracelog.info('reply msg to WX: %s' % reply.content)
        
        self.get_worker().get_app().send_ack_dispatch(self._req_frame, (reply.serialize(), ))


class ReceiveWXMessageWorker(bf.CmdWorker):
    """
    Class: ReceiveWXMessageWorker
    Description: 处理微信消息的Worker
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

        bf.CmdWorker.__init__(self, "ReceiveWXMessageWorker", min_task_id, max_task_id)
        
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

        self.register_handler(WXPushMessageHandler(), cmd_code_def.WX_ACCESS_HTTP_POST_FORWARD)
        return 0
