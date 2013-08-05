#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-07-09
Description: 会员状态机管理模块
Key Class&Method List: 
             1. MbrMenuCfgStateHandler
             2. MbrDeliveryStateHandler
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


class MbrMenuCfgStateHandler(fsm_def.BaseStateHandler):
    """
    Class: MbrMenuCfgStateHandler
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

        tracelog.info ('member %s enter %s state' % (self._processor.get_target().get_id(), fsm_def.MEMBER_MENU_CFG_STATE))
        if self._processor.get_target().get_old_state() == fsm_def.MEMBER_MENU_CFG_STATE:
            return

        new_delivery = True
        
        if self._processor.get_target().get_old_state() == None:
            recs = self._processor.get_worker().get_app().get_mit_manager().rdm_find('Delivery', member_id = self._processor.get_target().get_id())
            if len(recs) > 0:
                for rec in recs:
                    delivery_time = time.mktime(time.strptime(rec.delivery_date, '%Y-%m-%d'))
                    now = time.time()
                    if delivery_time > now:
                        new_delivery = False
                        delivery_id = rec.delivery_id
                        new_moc = rec
                        break
        
        if new_delivery is True:
            delivery_moc = self._processor.get_worker().get_app().get_mit_manager().gen_rdm("Delivery")
            delivery_moc.delivery_id = self._processor.get_worker().get_app().get_delivery_no_creator().get_new_no()
            delivery_id = delivery_moc.delivery_id 
            delivery_moc.member_id = self._processor.get_target().get_id()
            delivery_moc.delivery_date = self._processor.get_worker().get_next_delivery_date(self._processor.get_target().get_today(), 
                                                                                             int(self._processor.get_target().get_spec().delivery_time))
            delivery_moc.modify_flag = True
    
            new_moc = delivery_moc
            self._processor.get_worker().get_app().get_mit_manager().rdm_add(delivery_moc)
            tracelog.info('member %s create a new delivery record(id %d), next delivery date %s, modify_flag %s' % (self._processor.get_target().get_id(), delivery_id, new_moc.delivery_date, new_moc.modify_flag))
        else:
            tracelog.info('member %s hold the delivery record(id %d), next delivery date %s, modify_flag %s' % (self._processor.get_target().get_id(), new_moc.delivery_id, new_moc.delivery_date, new_moc.modify_flag))
            
        self._processor.get_target().set_delivery_id(delivery_id)

        # 如果会员与微信订阅者已绑定，通知订阅者自选菜单
        if self._processor.get_target().get_spec().subscriber_open_id is not None and len(self._processor.get_target().get_spec().subscriber_open_id) > 0:
            # 构造推送消息发给SubscriberManApp
            push_msg = msg_params_def.CloudPortalTextPushMessage()
            push_msg.init_all_attr()
            push_msg.subscriber_open_ids = [self._processor.get_target().get_spec().subscriber_open_id]
            raw_txt = msg_params_def.PORTAL_TXT_MENU_CFG_NOTIFY_TXT.decode('gbk').encode('utf-8') % (self._processor.get_target().get_spec().name, 
                                                                                                     self._processor.get_target().get_id(),
                                                                                                     new_moc.delivery_date)
            push_msg.text_msg = raw_txt
            push_frame = bf.AppFrame()
            push_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_TEXT_PUSH_MSG)
            push_frame.add_data(push_msg.serialize())
            self._processor.get_worker().dispatch_frame_to_process_by_pid(self._processor.get_worker().get_pid("SubscriberManApp"), push_frame)

    def exec_state(self):
        """
        Method: exec_state
        Description: 
        Parameter:
        Return: 
        Others: 
        """

        tracelog.info ('member %s exec %s state' % (self._processor.get_target().get_id(), fsm_def.MEMBER_MENU_CFG_STATE))

    def exit_state(self):
        """
        Method: exit_state
        Description: 
        Parameter: 
        Return: 
        Others: 
        """
        tracelog.info ('member %s exit %s state' % (self._processor.get_target().get_id(), fsm_def.MEMBER_MENU_CFG_STATE))


class MbrDeliveryStateHandler(fsm_def.BaseStateHandler):
    """
    Class: MbrDeliveryStateHandler
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

        tracelog.info ('member %s enter %s state' % (self._processor.get_target().get_id(), fsm_def.MEMBER_DELIVERY_STATE))
        if self._processor.get_target().get_old_state() == fsm_def.MEMBER_DELIVERY_STATE:
            return

        # 如果状态机的初始状态就是配送状态，需要先创建一个默认配送菜单记录
        if self._processor.get_target().get_old_state() == None:
            new_delivery = True
            recs = self._processor.get_worker().get_app().get_mit_manager().rdm_find('Delivery', member_id = self._processor.get_target().get_id())
            if len(recs) > 0:
                for rec in recs:
                    delivery_time = time.mktime(time.strptime(rec.delivery_date, '%Y-%m-%d'))
                    now = time.time()
                    if delivery_time > now:
                        new_delivery = False
                        delivery_id = rec.delivery_id
                        break
            
            if new_delivery is True:
                delivery_moc = self._processor.get_worker().get_app().get_mit_manager().gen_rdm("Delivery")
                delivery_moc.delivery_id = self._processor.get_worker().get_app().get_delivery_no_creator().get_new_no()
                delivery_id = delivery_moc.delivery_id 
                delivery_moc.member_id = self._processor.get_target().get_id()
                delivery_moc.delivery_date = self._processor.get_worker().get_next_delivery_date(self._processor.get_target().get_today(), 
                                                                                                 int(self._processor.get_target().get_spec().delivery_time))
                delivery_moc.modify_flag = False
        
                self._processor.get_worker().get_app().get_mit_manager().rdm_add(delivery_moc)
                tracelog.info('member %s create a new delivery record(id %d)' % (self._processor.get_target().get_id(), delivery_id))

            self._processor.get_target().set_delivery_id(delivery_id)

        d_recs = self._processor.get_worker().get_app().get_mit_manager().lookup_attrs('Delivery', ['delivery_id', 'delivery_date', 'vegetables'], delivery_id = self._processor.get_target().get_delivery_id())
        if len(d_recs) > 0:
            delivery_moc = self._processor.get_worker().get_app().get_mit_manager().gen_rdm("Delivery")
            delivery_moc.delivery_id = d_recs[0][0]
            delivery_moc.member_id = self._processor.get_target().get_id()
            delivery_moc.delivery_date = d_recs[0][1]
            delivery_moc.modify_flag = False
            
            self._processor.get_worker().get_app().get_mit_manager().rdm_mod(delivery_moc)

            # 如果会员与微信订阅者已绑定，通知订阅者当期的配送菜单
            if self._processor.get_target().get_spec().subscriber_open_id is not None and len(self._processor.get_target().get_spec().subscriber_open_id) > 0:
                # 构造推送消息发给SubscriberManApp
                push_msg = msg_params_def.CloudPortalTextPushMessage()
                push_msg.init_all_attr()
                push_msg.subscriber_open_ids = [self._processor.get_target().get_spec().subscriber_open_id]
                if d_recs[0][2] is None:
                    raw_txt = msg_params_def.PORTAL_TXT_DELIVERY_DEFAULT_NOTIFY_TXT.decode('gbk').encode('utf-8') % (self._processor.get_target().get_spec().name, 
                                                                                                                     self._processor.get_target().get_id(),
                                                                                                                     d_recs[0][1])
                else:
                    v_list = []
                    all_v_moc = self._processor.get_worker().get_app().get_mit_manager().rdm_find('Vegetable')
                    for v in d_recs[0][2].vegetables:
                        for v_moc in all_v_moc:
                            if v == str(v_moc.v_id):
                                v_list.append(v_moc.name)
                                break
                    
                    split = ', '
                    mbr_menu = split.join(v_list)
                    raw_txt = msg_params_def.PORTAL_TXT_DELIVERY_DIY_NOTIFY_TXT.decode('gbk').encode('utf-8') % (self._processor.get_target().get_spec().name, 
                                                                                                                 self._processor.get_target().get_id(),
                                                                                                                 d_recs[0][1],
                                                                                                                 mbr_menu)
                push_msg.text_msg = raw_txt
                push_frame = bf.AppFrame()
                push_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_TEXT_PUSH_MSG)
                push_frame.add_data(push_msg.serialize())
                self._processor.get_worker().dispatch_frame_to_process_by_pid(self._processor.get_worker().get_pid("SubscriberManApp"), push_frame)

                tracelog.info('member %s modify the delivery record(id %d), next delivery date %s, modify_flag %s' % (delivery_moc.member_id, delivery_moc.delivery_id, delivery_moc.delivery_date, delivery_moc.modify_flag))
        
    def exec_state(self):
        """
        Method: exec_state
        Description: 
        Parameter: 
        Return: 
        Others: 
        """

        tracelog.info ('member %s exec %s state' % (self._processor.get_target().get_id(), fsm_def.MEMBER_DELIVERY_STATE))

    def exit_state(self):
        """
        Method: exit_state
        Description: 
        Parameter:
        Return: 
        Others: 
        """
        tracelog.info ('member %s exit %s state' % (self._processor.get_target().get_id(), fsm_def.MEMBER_DELIVERY_STATE))


class MbrDeliveryExpiredStateHandler(fsm_def.BaseStateHandler):
    """
    Class: MbrDeliveryExpiredStateHandler
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

        tracelog.info ('member %s enter %s state' % (self._processor.get_target().get_id(), fsm_def.MEMBER_DELIVERY_STATE))
        if self._processor.get_target().get_old_state() == fsm_def.MEMBER_DELIVERY_STATE:
            return

        # 如果会员与微信订阅者已绑定，通知订阅者自选菜单
        if self._processor.get_target().get_spec().subscriber_open_id is not None and len(self._processor.get_target().get_spec().subscriber_open_id) > 0:
            # 构造推送消息发给SubscriberManApp
            push_msg = msg_params_def.CloudPortalTextPushMessage()
            push_msg.init_all_attr()
            push_msg.subscriber_open_ids = [self._processor.get_target().get_spec().subscriber_open_id]
            raw_txt = msg_params_def.PORTAL_TXT_DELIVERY_EXPIRED_NOTIFY_TXT.decode('gbk').encode('utf-8') % (self._processor.get_target().get_spec().name, 
                                                                                                     self._processor.get_target().get_id())
            push_msg.text_msg = raw_txt
            push_frame = bf.AppFrame()
            push_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_TEXT_PUSH_MSG)
            push_frame.add_data(push_msg.serialize())
            self._processor.get_worker().dispatch_frame_to_process_by_pid(self._processor.get_worker().get_pid("SubscriberManApp"), push_frame)
        
    def exec_state(self):
        """
        Method: exec_state
        Description: 
        Parameter:
        Return: 
        Others: 
        """

        tracelog.info ('member %s exec %s state' % (self._processor.get_target().get_id(), fsm_def.MEMBER_DELIVERY_STATE))

    def exit_state(self):
        """
        Method: exit_state
        Description: 
        Parameter: 
        Return: 
        Others: 
        """
        tracelog.info ('member %s exit %s state' % (self._processor.get_target().get_id(), fsm_def.MEMBER_DELIVERY_STATE))


class MbrMenuCfgStateMenuCfgEventHandler(fsm_def.FsmHandler):
    """
    Class: MbrMenuCfgStateMenuCfgEventHandler
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
        menucfg_info = event.other_info
        v_list = msg_params_def.VegetableList()
        v_list.init_all_attr()
        v_list.vegetables = menucfg_info.vegetables

        mo_id = processor.get_worker().get_app().get_mit_manager().gen_moid("Delivery", delivery_id = processor.get_target().get_delivery_id())
        processor.get_worker().get_app().get_mit_manager().mod_complex_attr('Delivery', 
                                                                       moid = mo_id, 
                                                                       vegetables = v_list)

        tracelog.info('member %s cfg menu: %s' % (processor.get_target().get_id(), v_list.vegetables))        
        return fsm_def.MEMBER_MENU_CFG_STATE


class MbrAnyStateDailyEventHandler(fsm_def.FsmHandler):
    """
    Class: MbrAnyStateDailyEventHandler
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
        date = time.localtime(event.other_info)
        today = date.tm_wday + 1
        processor.get_target().set_today(event.other_info)
        
        menucfg_period, delivery_period = processor.get_worker().get_delivery_period(int(processor.get_target().get_spec().delivery_time))
        if today in menucfg_period:
            new_state = fsm_def.MEMBER_MENU_CFG_STATE
        elif today in delivery_period:
            if today == int(processor.get_target().get_spec().delivery_time):
                new_state = fsm_def.MEMBER_MENU_CFG_STATE
            else:
                new_state = fsm_def.MEMBER_DELIVERY_STATE

        expiry_date = processor.get_target().get_spec().delivery_expiry
        expiry_time = time.mktime(time.strptime(expiry_date, '%Y-%m-%d'))
        
        if event.other_info > expiry_time:
            tracelog.info ('member %s delivery expired on %s' % (processor.get_target().get_id(), expiry_date))
            new_state = fsm_def.MEMBER_EXPIRED_STATE
                
        tracelog.info('today is %s(%d), member %s delivery weekday %s, next state %s' % (time.strftime('%Y-%m-%d %H:%M:%S', date),
                                                                                         today, 
                                                                                         processor.get_target().get_id(), 
                                                                                         processor.get_target().get_spec().delivery_time, 
                                                                                         new_state))        
        return new_state


