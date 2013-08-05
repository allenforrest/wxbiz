#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-13
Description: 微信订阅者详细信息更新模块
Key Class&Method List: 
             1. SubscriberManApp -- 进程类
History:
1. Date: 2013-5-13
   Author: Allen
   Modification: create
"""

if __name__ == "__main__":
    import import_paths

import json
import Queue
import time
import md5

import bundleframework as bf
import tracelog

import msg_params_def
import cmd_code_def

GET_SUBSCRIBER_INFO_TIMER_LEN       = 30
SUBSCRIBER_INFO_UPDATE_TIMER_LEN    = 60 * 60 * 24
AUTO_WAN_IP_CHECK_TIMER_LEN         = 3 * 60

#WINDELN_CHECK_TIMER_LEN             = 5 * 60

class GetSubscriberInfoTimeoutHandler(bf.TimeOutHandler):
    """
    Class: GetSubscriberInfoTimeoutHandler
    Description: 获取刚订阅的微信账户详细信息
    Base: TimeOutHandler
    Others: 
    """

    def time_out(self):
        ungroup_sub_buf = self.get_worker().get_app().get_wx_service_api().get_subscribers_by_group(0)
        if ungroup_sub_buf is not None and len(ungroup_sub_buf) > 0:
            ungroup_subs = json.loads(ungroup_sub_buf)
        else:
            return
        #tracelog.info('all subscriber info %s' % ungroup_sub_buf)

        processors = self.get_worker().get_app().get_sub_man_worker().get_state_manager().get_processors()
        for pro in processors:
            if len(pro.get_target().get_spec().fake_id) == 0:
                tracelog.info('new subscriber(openid %s), get the detail info' % pro.get_target().get_id())
                
                subscribe_seq_no_info = msg_params_def.WX_TXT_SUBSCRIBE_TIPS % pro.get_target().get_spec().subscribe_seq_no
                for ungroup_sub in ungroup_subs:
                    fake_id = ungroup_sub['fakeId']
                    last_msgs_buf = self.get_worker().get_app().get_wx_service_api().get_subscriber_last_msgs(fake_id)
                    last_msgs = json.loads(last_msgs_buf)
                    for msg in last_msgs:
                        if msg['content'].encode('utf-8').find(subscribe_seq_no_info.decode('gbk').encode('utf-8')) >= 0:
                            sub_info_buf = self.get_worker().get_app().get_wx_service_api().get_subscriber_info(fake_id)
                            sub_info = json.loads(sub_info_buf)
                            
                            # 更新processor和mit
                            pro.get_target().set_fakeid(fake_id)
                            if sub_info['Sex'] == '1':
                                gender = '男'.decode('gbk').encode('utf-8')
                            elif sub_info['Sex'] == '0':
                                gender = '女'.decode('gbk').encode('utf-8')
                            else:
                                gender = ''
                            
                            pro.get_target().set_detail_info(sub_info['Username'],
                                                             sub_info['NickName'],
                                                             gender,
                                                             sub_info['City'])
                            
                            subs = self.get_worker().get_app().get_mit_manager().rdm_find('Subscriber', subscriber_open_id = pro.get_target().get_id())
                            if len(subs) == 0:
                                tracelog.error('subscriber(openid %s) in processor does not exist in mit!' % pro.get_target().get_id())
                            else:
                                subs[0].fake_id = fake_id
                                subs[0].weixin_id = sub_info['Username']
                                subs[0].nickname = sub_info['NickName']
                                subs[0].gender = gender
                                subs[0].city = sub_info['City']
                                self.get_worker().get_app().get_mit_manager().rdm_mod(subs[0])
                                
                                head_img_file = msg_params_def.PORTAL_IMG_FILE_LOCAL_PATH_PREFIX + msg_params_def.WX_HEAD_IMG_FILE_SAVE_LOCAL_PATH + subs[0].subscriber_open_id + '.png'
                                self.get_worker().get_app().get_wx_service_api().save_head_img(fake_id, head_img_file)
                                
                                tracelog.info('subscriber(fakeid %s, name %s):' % (fake_id, sub_info['NickName']))
                                
                                # 订阅事件上报
                                event_report = msg_params_def.PortalEventEventReportReq()
                                event_report.init_all_attr()
                                event_report.user_session = '0'
                                event_report.event_type = msg_params_def.EVENT_TYPE_SUBSCRIBE
                                event = msg_params_def.SubscribeEvent()
                                event.init_all_attr()
                                event.subscriber_open_id = pro.get_target().get_id()
                                event.weixin_id = subs[0].weixin_id
                                event.nickname = subs[0].nickname
                                event.action = '订阅'.decode('gbk').encode('utf-8')
                                event.time = time.strftime('%Y-%m-%d %H:%M:%S')
                    
                                event_report.content = event.serialize()
                                
                                evt_frame = bf.AppFrame()
                                evt_frame.set_cmd_code(cmd_code_def.PORTAL_EVENT_EVENT_REPORT)
                                evt_frame.add_data(event_report.serialize())
                                self.get_worker().dispatch_frame_to_process_by_pid(self.get_worker().get_pid('EventCenterApp'), evt_frame)
                        
                        
class SubscriberInfoUpdateTimeoutHandler(bf.TimeOutHandler):
    """
    Class: SubscriberInfoUpdateTimeoutHandler
    Description: 定时更新订阅者的详细信息
    Base: TimeOutHandler
    Others: 
    """

    def time_out(self):
        processors = self.get_worker().get_app().get_sub_man_worker().get_state_manager().get_processors()

        for pro in processors:
            if len(pro.get_target().get_spec().fake_id) > 0:
                tracelog.info('subscriber(openid %s, fakeid %s), update the detail info' % (pro.get_target().get_spec().subscriber_open_id, pro.get_target().get_spec().fake_id))
                sub_info_buf = self.get_worker().get_app().get_wx_service_api().get_subscriber_info(pro.get_target().get_spec().fake_id)
                sub_info = json.loads(sub_info_buf)

                # 更新processor和mit
                if sub_info['Sex'] == '1':
                    gender = '男'.decode('gbk').encode('utf-8')
                else:
                    gender = '女'.decode('gbk').encode('utf-8')
                pro.get_target().set_detail_info(sub_info['Username'],
                                                 sub_info['NickName'],
                                                 gender,
                                                 sub_info['City'])
                
                subs = self.get_worker().get_app().get_mit_manager().rdm_find('Subscriber', subscriber_open_id = pro.get_target().get_spec().subscriber_open_id)
                if len(subs) == 0:
                    tracelog.error('subscriber(openid %s) in processor does not exist in mit!' % pro.get_target().get_spec().subscriber_open_id)
                else:
                    subs[0].weixin_id = sub_info['Username']
                    subs[0].nickname = sub_info['NickName']
                    subs[0].gender = gender
                    subs[0].city = sub_info['City']
                    self.get_worker().get_app().get_mit_manager().rdm_mod(subs[0])

                    head_img_file = msg_params_def.PORTAL_IMG_FILE_LOCAL_PATH_PREFIX + msg_params_def.WX_HEAD_IMG_FILE_SAVE_LOCAL_PATH + subs[0].subscriber_open_id + '.png'
                    self.get_worker().get_app().get_wx_service_api().save_head_img(subs[0].fake_id, head_img_file)
            
            time.sleep(5)
                                


class AutoWanIpCheckTimeoutHandler(bf.TimeOutHandler):
    """
    Class: AutoWanIpCheckTimeoutHandler
    Description: 
    Base: TimeOutHandler
    Others: 
    """

    def time_out(self):
        bizs = self.get_worker().get_app().get_mit_manager().rdm_find('WXBizInfo')
        auto_ip_update = bizs[0].auto_ip_update
        if auto_ip_update == 'False':
            return
        
        wan_ip = self.get_worker().get_app().get_wx_service_api().get_wan_ip()
        url = self.get_worker().get_app().get_wx_service_api().get_itf_cfg_info()
        tracelog.info('wan ip has changed to %s, wx url %s ' % (wan_ip, url))
        self.get_worker().send_wan_ip_update_msg(str(wan_ip))
        
        self.get_worker().get_app().get_sub_man_worker().update_wan_ip(wan_ip)
        
        if url is not None and url.find(wan_ip) < 0:
            u = url.strip('http://')
            new_url = 'http://' + wan_ip + u[u.find('/'):]
            ret = self.get_worker().get_app().get_wx_service_api().mod_itf_cfg_info(new_url, bizs[0].access_token)
            tracelog.info('update wx url to %s %s' % (new_url, ret))
        


class WindelnCheckTimeoutHandler(bf.TimeOutHandler):
    """
    Class: WindelnCheckTimeoutHandler
    Description: 
    Base: TimeOutHandler
    Others: 
    """

    def time_out(self):
        """
        price, out_of_stock = self.get_worker().get_app().get_wx_windeln_api().get_aptamil_stock()
        self.get_worker().get_app().update_windeln_info(price, out_of_stock)
        
        if out_of_stock is False:
            tracelog.info('get price %s, stock %s' % (price, out_of_stock))
            for sub in msg_params_def.MILK_MAP[msg_params_def.MSG_A_MILK]:
                if self.get_worker().get_notify(sub[0]) is not False:
                    self.get_worker().get_app().get_wx_service_api().send_text(sub[1], '%s is in stock!' % msg_params_def.MSG_A_MILK)
        else:
            for sub in msg_params_def.MILK_MAP[msg_params_def.MSG_A_MILK]:
                self.get_worker().set_notify(sub[0], True)
        """

class SubscriberTaskWorker(bf.Worker):
    
    TASK_TYPE_SEND_TEXT_MSG  = 'send'
    TASK_TYPE_PUSH_ARTICLE   = 'push'
    TASK_TYPE_UPLOAD_ARTICLE = 'upload'
    TASK_TYPE_DELETE_ARTICLE = 'delete'
    
    def __init__(self):
        """
        Method: __init__
        Description: 类初始化
        Parameter: 无
        Return: 
        Others: 
        """

        bf.Worker.__init__(self, 'SubscriberTaskWorker')
        self._msg_queue = Queue.Queue()
        self._article_news = {}
        self._notify_map = {}
    
    def ready_for_work(self):
        """
        Method:    ready_for_work
        Description: worker初始化工作, 注册该worker关联的handler
        Parameter: 无
        Return: 
        Others: 
        """

        handler = GetSubscriberInfoTimeoutHandler()
        handler.start_timer(GET_SUBSCRIBER_INFO_TIMER_LEN, False)
        self.register_time_out_handler(handler)

        handler = SubscriberInfoUpdateTimeoutHandler()
        handler.start_timer(SUBSCRIBER_INFO_UPDATE_TIMER_LEN, False)
        self.register_time_out_handler(handler)

        handler = AutoWanIpCheckTimeoutHandler()
        handler.start_timer(AUTO_WAN_IP_CHECK_TIMER_LEN, False)
        self.register_time_out_handler(handler)        

        """
        handler = WindelnCheckTimeoutHandler()
        handler.start_timer(WINDELN_CHECK_TIMER_LEN, False)
        self.register_time_out_handler(handler)           
        """
        
        return 0
    
    def idle(self, total_ready_frames):
        if self._msg_queue.empty() is not True:
            msg = self._msg_queue.get(True, 0.1)
            
            if msg[0] is self.TASK_TYPE_SEND_TEXT_MSG:
                send_ret = self.get_app().get_wx_service_api().send_text(msg[1], msg[2])
                tracelog.info('send text to %s, ret %s.' % (msg[1], send_ret))
                
            elif msg[0] is self.TASK_TYPE_PUSH_ARTICLE:
                # 先修改主题后立刻推送，可能修改完主题news_id发生了变化，推送给用户的主题是无效的，需要刷新一下news_id
                if self._article_news.has_key(msg[3]) and msg[2] != self._article_news[msg[3]]:
                    tracelog.info('push news id %s, but the article news id updated to %s' % (msg[2], self._article_news[msg[3]]))
                    newsid = self._article_news[msg[3]]
                else:
                    newsid = msg[2]                          
                resp = self.get_app().get_wx_service_api().send_news(msg[1], newsid)
                tracelog.info('push news %s to sub %s, ret %s' % (newsid, msg[1], resp))
                
            elif msg[0] is self.TASK_TYPE_DELETE_ARTICLE: 
                del_ret = self.get_app().get_wx_service_api().del_news(msg[1])
                tracelog.info('del news(%s) %s!' % (msg[1], del_ret))
                
            elif msg[0] is self.TASK_TYPE_UPLOAD_ARTICLE:
                back_pic = msg_params_def.PORTAL_IMG_FILE_LOCAL_PATH_PREFIX + msg_params_def.PORTAL_LOGO_IMG_FILE_LOCAL_PATH
                file_no = self.get_app().get_wx_service_api().create_news(msg[2], back_pic, msg[3], msg[4], msg[5])
                news_id = file_no if file_no is not None else ''
                tracelog.info('create news ret %s!' % news_id)
                if news_id != '':
                    self._article_news[msg[1]] = news_id
                    self.send_news_id_update_msg(msg[1], news_id)
                else:
                    if msg[6] < 10:
                        tracelog.error('re-upload the article(%d)' % msg[1])
                        loop = msg[6] + 1
                        self.upload_article(msg[1], msg[2], msg[3], msg[4], msg[5], loop)
                    else:
                        tracelog.error('re-upload the article(%d) 10 times, stop!' % msg[1])
                
            else:
                pass
    
            time.sleep(3)
    
    def push_text(self, fake_id, text_msg):
        self._msg_queue.put_nowait((self.TASK_TYPE_SEND_TEXT_MSG, fake_id, text_msg))
       
    def push_article(self, fake_id, news_id, article_id):
        self._msg_queue.put_nowait((self.TASK_TYPE_PUSH_ARTICLE, fake_id, news_id, article_id))

    def upload_article(self, article_id, pic_file, title, desc, content, loop):
        self._msg_queue.put_nowait((self.TASK_TYPE_UPLOAD_ARTICLE, article_id, pic_file, title, desc, content, loop))     

    def del_article(self, news_id):
        self._msg_queue.put_nowait((self.TASK_TYPE_DELETE_ARTICLE, news_id))
        
    def send_news_id_update_msg(self, article_id, news_id):
        frame = bf.AppFrame()
        frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_NEWS_ID_UPDATE_MSG)
        frame.add_data(str(article_id))
        frame.add_data(news_id)
        self.dispatch_frame_to_process_by_pid(self.get_pid("PortalManApp"), frame)        
        
    def send_wan_ip_update_msg(self, wan_ip):
        frame = bf.AppFrame()
        frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_WAN_IP_UPDATE_MSG)
        frame.add_data(wan_ip)
        self.dispatch_frame_to_process_by_pid(self.get_pid("PortalManApp"), frame)           

    """
    def set_notify(self, openid, flag):
        self._notify_map[openid] = flag
    
    def get_notify(self, openid):
        if self._notify_map.has_key(openid):
            return self._notify_map[openid]
        else:
            return True
    """
    