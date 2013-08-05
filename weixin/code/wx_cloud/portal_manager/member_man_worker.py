#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-13
Description: Portal����ģ�� ��Ա�����߳�
Key Class&Method List: 
             1. MemberManagerWorker -- worker��
History:
1. Date: 2013-7-7
   Author: Allen
   Modification: create
"""
import import_paths

import os
import time
import cPickle

import bundleframework as bf
import basic_rep_to_web
import mit

import err_code_mgr

import tracelog
import cmd_code_def
import fsm_def
import msg_params_def
import member_def

import member_state_man

class PortalMemberCfgMemberHandler(bf.CmdHandler):
    """
    Class: PortalMemberCreateMemberHandler
    Description: Portal�·��Ĵ�����Ա������handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: ��������Ա��������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('member cfg worker recv cfg member frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            member_cfg = msg_params_def.PortalMemberMemberCreateModReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_MEMBER_MEMBER_CREATE',
                                                            param_name = 'PortalMemberMemberCreateModReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        records = self.get_worker().get_app().get_mit_manager().rdm_find("Member", member_id = member_cfg.member_id)
        if len(records) == 0:
            member_moc = self.get_worker().get_app().get_mit_manager().gen_rdm("Member")
            member_moc.member_id = member_cfg.member_id
            member_moc.name = member_cfg.name
            member_moc.cellphone = member_cfg.cellphone
            member_moc.delivery_addr = member_cfg.delivery_addr
            member_moc.delivery_time = member_cfg.delivery_time
            member_moc.delivery_expiry = member_cfg.delivery_expiry

            ret = self.get_worker().get_app().get_mit_manager().rdm_add(member_moc)
            member_spec = member_moc
            
        else:
            records[0].name = member_cfg.name
            records[0].cellphone = member_cfg.cellphone
            records[0].delivery_addr = member_cfg.delivery_addr
            records[0].delivery_time = member_cfg.delivery_time
            records[0].delivery_expiry = member_cfg.delivery_expiry
        
            ret = self.get_worker().get_app().get_mit_manager().rdm_mod(records[0])
            
            processor = self.get_worker().get_state_manager().get_processor(member_cfg.member_id)
            if processor is not None:
                tracelog.info('member(%s) info modify, remove the old processor' % member_cfg.member_id)
                self.get_worker().get_state_manager().remove_processor(processor)
                del processor
                
            member_spec = records[0]
        
        if ret.get_err_code() == err_code_mgr.ER_OBJECT_ADD_CONFLICT:
            result.return_code = err_code_mgr.ERR_PORTAL_MEMBER_RECORDS_FULL
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_MEMBER_RECORDS_FULL)

            result.prepare_for_ack(member_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        elif ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(member_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        # ������Ա״̬��
        now_date = time.localtime() #time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')
        weekday = now_date.tm_wday + 1
        
        # ���ݻ�Ա���������ں͵�ǰ���ڣ��жϻ�Ա״̬���ĳ�ʼ״̬
        menucfg_period, delivery_period = self.get_worker().get_delivery_period(int(member_cfg.delivery_time))
        if weekday in menucfg_period:
            init_state = fsm_def.MEMBER_MENU_CFG_STATE
        elif weekday in delivery_period:
            if weekday == int(member_cfg.delivery_time):
                init_state = fsm_def.MEMBER_MENU_CFG_STATE
            else:
                init_state = fsm_def.MEMBER_DELIVERY_STATE
        else:
            init_state = fsm_def.MEMBER_MENU_CFG_STATE
        
        mbr = member_def.Member(member_spec, init_state)

        if member_spec.subscriber_open_id is not None and len(member_spec.subscriber_open_id) > 0:
            subs = self.get_worker().get_app().get_mit_manager().rdm_find("Subscriber", subscriber_open_id = member_spec.subscriber_open_id)
            if len(subs) > 0:
                mbr.set_assoc_subscriber(subs[0])
        
        processor = fsm_def.StateProcessor(mbr, self.get_worker())
        processor.register_state_handler(fsm_def.MEMBER_MENU_CFG_STATE, member_state_man.MbrMenuCfgStateHandler(processor))
        processor.register_state_handler(fsm_def.MEMBER_DELIVERY_STATE, member_state_man.MbrDeliveryStateHandler(processor))
        processor.register_state_handler(fsm_def.MEMBER_EXPIRED_STATE, member_state_man.MbrDeliveryExpiredStateHandler(processor))
        
        self.get_worker().get_state_manager().add_processor(processor)

        # ��WEB�سɹ���Ӧ
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(member_cfg, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
        
        # ���͹ؼ������¼�֪ͨ
        if frame.get_cmd_code() == cmd_code_def.PORTAL_MEMBER_MEMBER_CREATE:
            oper_type = msg_params_def.EVENT_PORTAL_OPERATION_ADD + msg_params_def.EVENT_PORTAL_OBJECT_MEMBER
        else:
            oper_type = msg_params_def.EVENT_PORTAL_OPERATION_MOD + msg_params_def.EVENT_PORTAL_OBJECT_MEMBER
            
        self.get_worker().get_app().send_portal_operation_event(member_cfg.user_session, oper_type.decode('gbk').encode('utf-8'), member_cfg.name)


class PortalMemberRemoveMemberHandler(bf.CmdHandler):
    """
    Class: PortalMemberRemoveMemberHandler
    Description: Portal�·���ɾ����Ա������handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: ����ɾ����Ա��������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('member cfg worker recv rmv member frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            member_rmv = msg_params_def.PortalMemberMemberRemoveReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_MEMBER_MEMBER_REMOVE',
                                                            param_name = 'PortalMemberMemberRemoveReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        records = self.get_worker().get_app().get_mit_manager().rdm_find(moc_name = "Member", member_id = member_rmv.member_id)
        if len(records) == 1:
            member_name = records[0].name
            
            # ���΢�Ŷ���������û�Ա�󶨣���Ҫ֪ͨ������ɾ���󶨹�ϵ
            if records[0].subscriber_open_id is not None and len(records[0].subscriber_open_id) > 0:
                deassoc = msg_params_def.PortalSubscriberMemberAssociateReq()
                deassoc.init_all_attr()
                deassoc.user_session = member_rmv.user_session
                deassoc.subscriber_open_id = records[0].subscriber_open_id
                deassoc.member_id = ''
                deassoc.name = ''
                deassoc.cellphone = ''
                
                deassoc_frame = bf.AppFrame()
                deassoc_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_SUB_MEMBER_ASSOC_MSG)
                deassoc_frame.add_data(deassoc.serialize())
                self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), deassoc_frame)        
            
            self.get_worker().get_app().get_mit_manager().rdm_remove(records[0])

            processor = self.get_worker().get_state_manager().get_processor(member_rmv.member_id)
            if processor is not None:
                tracelog.info('member(%s) remove, remove the processor' % member_rmv.member_id)
                self.get_worker().get_state_manager().remove_processor(processor)
                del processor

        recs = self.get_worker().get_app().get_mit_manager().rdm_find(moc_name = "Delivery", member_id = member_rmv.member_id)
        if len(recs) > 0:
            for rec in recs:
                self.get_worker().get_app().get_mit_manager().rdm_remove(rec)
                
        # ��WEB�سɹ���Ӧ
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(member_rmv, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))

        # ���͹ؼ������¼�֪ͨ
        oper_type = msg_params_def.EVENT_PORTAL_OPERATION_DEL + msg_params_def.EVENT_PORTAL_OBJECT_MEMBER
        self.get_worker().get_app().send_portal_operation_event(member_rmv.user_session, oper_type.decode('gbk').encode('utf-8'), member_name)


class PortalMemberQueryMemberHandler(bf.CmdHandler):
    """
    Class: PortalMemberQueryMemberHandler
    Description: Portal�·��Ĳ�ѯ��Ա������handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: �����ѯ��Ա��������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = msg_params_def.PortalMemberMemberQueryRsp()
        result.init_all_attr()
        tracelog.info('member cfg worker recv query member frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            member_qry = msg_params_def.PortalMemberMemberQueryReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_MEMBER_MEMBER_QUERY',
                                                            param_name = 'PortalMemberMemberQueryReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        num_per_page = None
        current_page = None
        
        if member_qry is not None:
            if hasattr(member_qry, "num_per_page"):
                num_per_page = member_qry.num_per_page

            if hasattr(member_qry, "current_page"):
                current_page = member_qry.current_page

        # num_per_page = 0 ��ʾ��ѯ���У�����ҳ       
        if num_per_page == 0:
            num_per_page = None
            current_page = None
            
        if member_qry.member_id is None or len(member_qry.member_id) == 0:
            records = self.get_worker().get_app().get_mit_manager().rdm_find('Member', 
                                                                             num_per_page = num_per_page,
                                                                             current_page = current_page)
            
            result.count = self.get_worker().get_app().get_mit_manager().count('Member')
        else:
            records = self.get_worker().get_app().get_mit_manager().rdm_find('Member', 
                                                                             num_per_page = num_per_page,
                                                                             current_page = current_page,
                                                                             member_id = member_qry.member_id)
            
            result.count = self.get_worker().get_app().get_mit_manager().count('Member', member_id = member_qry.member_id)
            
        result.members = []
        for rec in records:
            
            member = msg_params_def.Member()
            member.init_all_attr()
            member.member_id = rec.member_id
            member.name = rec.name
            member.cellphone = rec.cellphone
            member.delivery_addr = rec.delivery_addr
            member.delivery_time = rec.delivery_time
            member.delivery_expiry = rec.delivery_expiry
            member.subscribe_flag = False
            
            if rec.subscriber_open_id is not None and len(rec.subscriber_open_id) > 0:
                subs = self.get_worker().get_app().get_mit_manager().rdm_find('Subscriber', subscriber_open_id = rec.subscriber_open_id)
                if len(subs) > 0:
                    member.subscribe_flag = True
                    member.weixin_id = subs[0].weixin_id
                    member.nickname = subs[0].nickname

            result.members.append(member)

        # ��WEB�سɹ���Ӧ
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.prepare_for_ack(member_qry, result.return_code, result.description)
        tracelog.info(result.serialize())
         
        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
        

class PortalDeliveryCreateVegetableHandler(bf.CmdHandler):
    """
    Class: PortalDeliveryCreateVegetableHandler
    Description: Portal�·��Ĵ�����Ʒ������handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: ��������Ʒ��������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('member cfg worker recv create vegetable frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            v_cfg = msg_params_def.PortalDeliveryVegetableCreateReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_DELIVERY_VEGETABLE_CREATE',
                                                            param_name = 'PortalDeliveryVegetableCreateReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        v_recs = self.get_worker().get_app().get_mit_manager().rdm_find('Vegetable', name = v_cfg.name)
        if len(v_recs) > 0:
            result.return_code = err_code_mgr.ERR_PORTAL_VEGETABLE_NAME_CONFLICT
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_VEGETABLE_NAME_CONFLICT)

            result.prepare_for_ack(v_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        v_moc = self.get_worker().get_app().get_mit_manager().gen_rdm("Vegetable")
        v_moc.v_id = self.get_worker().get_app().get_vegetable_no_creator().get_new_no()
        v_moc.name = v_cfg.name
        v_moc.description = v_cfg.description
        v_moc.counter = 0
        
        ret = self.get_worker().get_app().get_mit_manager().rdm_add(v_moc)
        
        if ret.get_err_code() == err_code_mgr.ER_OBJECT_ADD_CONFLICT:
            result.return_code = err_code_mgr.ERR_PORTAL_VEGETABLE_RECORDS_FULL
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_VEGETABLE_RECORDS_FULL)

            result.prepare_for_ack(v_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        elif ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(v_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        # ��WEB�سɹ���Ӧ
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(v_cfg, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))

        # ���͹ؼ������¼�֪ͨ
        oper_type = msg_params_def.EVENT_PORTAL_OPERATION_ADD + msg_params_def.EVENT_PORTAL_OBJECT_VEGETABLE
        self.get_worker().get_app().send_portal_operation_event(v_cfg.user_session, oper_type.decode('gbk').encode('utf-8'), v_moc.name)


class PortalDeliveryModifyVegetableHandler(bf.CmdHandler):
    """
    Class: PortalDeliveryModifyVegetableHandler
    Description: Portal�·����޸Ĳ�Ʒ������handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: �����޸Ĳ�Ʒ��������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
                
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('member cfg worker recv mod vegetable frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            v_mod = msg_params_def.PortalDeliveryVegetableModReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_DELIVERY_VEGETABLE_MODIFY',
                                                            param_name = 'PortalDeliveryVegetableModReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        v_moc = self.get_worker().get_app().get_mit_manager().rdm_find("Vegetable", v_id = int(v_mod.v_id))
        if len(v_moc) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_VEGETABLE_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_VEGETABLE_NOT_EXISTS)

            result.prepare_for_ack(v_mod, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        v_recs = self.get_worker().get_app().get_mit_manager().rdm_find('Vegetable', name = v_mod.name)
        if len(v_recs) > 0:
            if v_moc[0].v_id is not v_recs[0].v_id:
                result.return_code = err_code_mgr.ERR_PORTAL_VEGETABLE_NAME_CONFLICT
                result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_VEGETABLE_NAME_CONFLICT)
    
                result.prepare_for_ack(v_mod, result.return_code, result.description)
                self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                return
        
        v_moc[0].name = v_mod.name
        v_moc[0].description = v_mod.description

        ret = self.get_worker().get_app().get_mit_manager().rdm_mod(v_moc[0])
        if ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(v_mod, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        # ��WEB�سɹ���Ӧ
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(v_mod, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))

        # ���͹ؼ������¼�֪ͨ
        oper_type = msg_params_def.EVENT_PORTAL_OPERATION_MOD + msg_params_def.EVENT_PORTAL_OBJECT_VEGETABLE
        self.get_worker().get_app().send_portal_operation_event(v_mod.user_session, oper_type.decode('gbk').encode('utf-8'), v_mod.name)


class PortalDeliveryRemoveVegetableHandler(bf.CmdHandler):
    """
    Class: PortalDeliveryRemoveVegetableHandler
    Description: Portal�·���ɾ����Ʒ������handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: ����ɾ����Ʒ��������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('member cfg worker recv rmv vegetable frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            v_rmv = msg_params_def.PortalDeliveryVegetableRemoveReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_DELIVERY_VEGETABLE_REMOVE',
                                                            param_name = 'PortalDeliveryVegetableRemoveReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        v_moc = self.get_worker().get_app().get_mit_manager().rdm_find(moc_name = "Vegetable", v_id = int(v_rmv.v_id))
        if len(v_moc) == 1:
            name = v_moc[0].name
            self.get_worker().get_app().get_mit_manager().rdm_remove(v_moc[0])
            
        # ��WEB�سɹ���Ӧ
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(v_rmv, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))

        # ���͹ؼ������¼�֪ͨ
        oper_type = msg_params_def.EVENT_PORTAL_OPERATION_DEL + msg_params_def.EVENT_PORTAL_OBJECT_VEGETABLE
        self.get_worker().get_app().send_portal_operation_event(v_rmv.user_session, oper_type.decode('gbk').encode('utf-8'), name)


class PortalDeliveryQueryVegetableHandler(bf.CmdHandler):
    """
    Class: PortalDeliveryQueryVegetableHandler
    Description: Portal�·��Ĳ�ѯ��Ʒ������handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: �����ѯ��Ʒ��������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = msg_params_def.PortalDeliveryVegetableQueryRsp()
        result.init_all_attr()
        tracelog.info('content man worker recv subject frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            v_qry = msg_params_def.PortalDeliveryVegetableQueryReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_DELIVERY_VEGETABLE_QUERY',
                                                            param_name = 'PortalDeliveryVegetableQueryReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        num_per_page = None
        current_page = None
        
        if v_qry is not None:
            if hasattr(v_qry, "num_per_page"):
                num_per_page = v_qry.num_per_page

            if hasattr(v_qry, "current_page"):
                current_page = v_qry.current_page

        # num_per_page = 0 ��ʾ��ѯ���У�����ҳ       
        if num_per_page == 0:
            num_per_page = None
            current_page = None
            
        if v_qry.v_id is not None and len(v_qry.v_id) > 0:
            records = self.get_worker().get_app().get_mit_manager().rdm_find('Vegetable',
                                                                             num_per_page = num_per_page,
                                                                             current_page = current_page, 
                                                                             v_id = int(v_qry.v_id))
            result.count = self.get_worker().get_app().get_mit_manager().count('Vegetable', v_id = int(v_qry.v_id))
        else:
            records = self.get_worker().get_app().get_mit_manager().rdm_find('Vegetable',
                                                                             num_per_page = num_per_page,
                                                                             current_page = current_page 
                                                                             )
            result.count = self.get_worker().get_app().get_mit_manager().count('Vegetable')
        
        result.vegetables = []
        for rec in records:
            v = msg_params_def.Vegetable()
            v.init_all_attr()
            v.v_id = str(rec.v_id)
            v.name = rec.name
            v.description = rec.description
            result.vegetables.append(v)

        # ��WEB�سɹ���Ӧ
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.prepare_for_ack(v_qry, result.return_code, result.description)
        tracelog.info(result.serialize())
         
        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalDeliveryMemberNenuCfgHandler(bf.CmdHandler):
    """
    Class: PortalDeliveryMemberNenuCfgHandler
    Description: Portal�·��Ļ�Ա���Ͳ˵����Ƶ�����handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: �����Ա���Ͳ˵����Ƶ�������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('member cfg worker recv menu cfg frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            menu_cfg_info = msg_params_def.PortalDeliveryMemberMenuCfgReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_DELIVERY_MEMBER_MENU_CFG',
                                                            param_name = 'PortalDeliveryMemberMenuCfgReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        
        m_moc = self.get_worker().get_app().get_mit_manager().rdm_find(moc_name = "Member", member_id = menu_cfg_info.member_id)
        if len(m_moc) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_MEMBER_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_MEMBER_NOT_EXISTS)

            result.prepare_for_ack(menu_cfg_info, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        processor = self.get_worker().get_state_manager().get_processor(menu_cfg_info.member_id)
        if processor is not None:
            if processor.get_target().get_state() == fsm_def.MEMBER_DELIVERY_STATE:
                result.return_code = err_code_mgr.ERR_PORTAL_MEMBER_MENUCFG_EXPIRY
                result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_MEMBER_MENUCFG_EXPIRY)
    
                result.prepare_for_ack(menu_cfg_info, result.return_code, result.description)
                self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                return
        else:
            result.return_code = err_code_mgr.ERR_PORTAL_MEMBER_DELIVERY_EXPIRY
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_MEMBER_DELIVERY_EXPIRY)

            result.prepare_for_ack(menu_cfg_info, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return            
            
        # ��WEB�سɹ���Ӧ
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(menu_cfg_info, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))

        # �˵������¼����͸�״̬��
        event = fsm_def.FsmEvent(fsm_def.MEMBER_MENU_CFG_EVENT, menu_cfg_info.member_id, menu_cfg_info)
        new_frame = bf.AppFrame()
        new_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_MEMBER_STATE_EVENT_MSG)
        new_frame.add_data(cPickle.dumps(event))
        self.get_worker().dispatch_frame_to_worker('MemberManagerWorker', new_frame)
        
        # �˵������¼��ϱ�
        event_report = msg_params_def.PortalEventEventReportReq()
        event_report.init_all_attr()
        event_report.user_session = menu_cfg_info.user_session
        event_report.event_type = msg_params_def.EVENT_TYPE_MENUCFG
        event = msg_params_def.MemberConfigMenuEvent()
        event.init_all_attr()
        
        event.member_id = menu_cfg_info.member_id
        event.subscriber_open_id = m_moc[0].subscriber_open_id
        event.weixin_id = processor.get_target().get_assoc_subscriber().weixin_id
        event.name = m_moc[0].name
        event.nickname = processor.get_target().get_assoc_subscriber().nickname

        event.time = time.strftime('%Y-%m-%d %H:%M:%S')

        v_list = []
        all_v_moc = self.get_worker().get_app().get_mit_manager().rdm_find('Vegetable')
        for v in menu_cfg_info.vegetables:
            for v_moc in all_v_moc:
                if v == str(v_moc.v_id):
                    v_list.append(v_moc.name)
                    break
            
        split = ', '
        event.menu = split.join(v_list)
        
        event_report.content = event.serialize()
        
        evt_frame = bf.AppFrame()
        evt_frame.set_cmd_code(cmd_code_def.PORTAL_EVENT_EVENT_REPORT)
        evt_frame.add_data(event_report.serialize())
        self.get_worker().dispatch_frame_to_process_by_pid(self.get_worker().get_pid('EventCenterApp'), evt_frame)


class PortalDeliveryReportQueryHandler(bf.CmdHandler):
    """
    Class: PortalDeliveryReportQueryHandler
    Description: Portal�·��Ĳ�ѯ���ͱ��������handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: �����ѯ���ͱ����������Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = msg_params_def.PortalDeliveryReportQueryRsp()
        result.init_all_attr()
        tracelog.info('member cfg worker recv query delivery report frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            member_qry = msg_params_def.PortalDeliveryReportQueryReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_DELIVERY_REPORT_QUERY',
                                                            param_name = 'PortalDeliveryReportQueryReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        num_per_page = None
        current_page = None
        
        if member_qry is not None:
            if hasattr(member_qry, "num_per_page"):
                num_per_page = member_qry.num_per_page

            if hasattr(member_qry, "current_page"):
                current_page = member_qry.current_page

        # num_per_page = 0 ��ʾ��ѯ���У�����ҳ       
        if num_per_page == 0:
            num_per_page = None
            current_page = None

        multi_sql = mit.MultiSQL()
        multi_sql.set_sqlite_sql('delivery_id desc')   
                
        if member_qry.member_id is not None and len(member_qry.member_id):
            records = self.get_worker().get_app().get_mit_manager().lookup_attrs('Delivery',
                                                                                 ['member_id', 'delivery_date', 'modify_flag', 'vegetables'],
                                                                                 order_by_sql = multi_sql,                                                                                 
                                                                                 num_per_page = num_per_page,
                                                                                 current_page = current_page,
                                                                                 member_id = member_qry.member_id)
            result.count = self.get_worker().get_app().get_mit_manager().count('Delivery', member_id = member_qry.member_id)
        else:
            records = self.get_worker().get_app().get_mit_manager().lookup_attrs('Delivery',
                                                                                 ['member_id', 'delivery_date', 'modify_flag', 'vegetables'],
                                                                                 order_by_sql = multi_sql,                                                                                 
                                                                                 num_per_page = num_per_page,
                                                                                 current_page = current_page)
            result.count = self.get_worker().get_app().get_mit_manager().count('Delivery')
        
        result.delivery_reports = []
        for rec in records:
            if rec[2] == 1: # TYPE_BOOL��sqlite���д�Ϊint���ͣ�1-True��0-False
                continue
            
            mbrs = self.get_worker().get_app().get_mit_manager().rdm_find('Member', member_id = rec[0])
            if len(mbrs) == 0:
                tracelog.error('member(%s) in delivery records, but not in member table' % rec[0])
                continue

            report = msg_params_def.DeliveryReport()
            report.init_all_attr()
            report.member_id = rec[0]
            report.name = mbrs[0].name
            report.cellphone = mbrs[0].cellphone
            report.delivery_addr = mbrs[0].delivery_addr
            report.delivery_time = rec[1]
            if rec[3] is not None:
                v_list = []
                all_v_moc = self.get_worker().get_app().get_mit_manager().rdm_find('Vegetable')
                for v in rec[3].vegetables:
                    for v_moc in all_v_moc:
                        if v == str(v_moc.v_id):
                            v_list.append(v_moc.name)
                            break
                
                report.vegetables = v_list
            else:
                report.vegetables = [msg_params_def.PORTAL_TXT_DEFAULT_MENU.decode('gbk').encode('utf-8')]
            
            result.delivery_reports.append(report)

        # ��WEB�سɹ���Ӧ
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.prepare_for_ack(member_qry, result.return_code, result.description)
        tracelog.info(result.serialize())
         
        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalMemberManInitHandler(bf.CmdHandler):
    """
    Class: PortalMemberManInitHandler
    Description: ��Ա����ģ���ʼ����Ϣ����handler 
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: �����Ա����ģ���ʼ����Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)

        # ÿ��ʮ�˵�
        now_date = time.localtime()
        weekday = now_date.tm_wday + 1
        date_tuple = (now_date.tm_year, now_date.tm_mon, now_date.tm_mday, 0, 0, 1, now_date.tm_wday, now_date.tm_yday, now_date.tm_isdst)
        
        self.get_worker().get_app().get_push_task_manager().del_task(msg_params_def.PORTAL_TASK_MEMBER_DAILY, 0) # object_idĬ��Ϊ0
        self.get_worker().get_app().get_push_task_manager().add_task(msg_params_def.PORTAL_TASK_MEMBER_DAILY,
                                                                     time.mktime(date_tuple), 
                                                                     65535,
                                                                     0)

        mbrs = self.get_worker().get_app().get_mit_manager().rdm_find("Member")
        for mbr_moc in mbrs:
            # ������Ա״̬��
            # ���ݻ�Ա���������ں͵�ǰ���ڣ��жϻ�Ա״̬���ĳ�ʼ״̬
            menucfg_period, delivery_period = self.get_worker().get_delivery_period(int(mbr_moc.delivery_time))
            if weekday in menucfg_period:
                init_state = fsm_def.MEMBER_MENU_CFG_STATE
            elif weekday in delivery_period:
                if weekday == int(mbr_moc.delivery_time):
                    init_state = fsm_def.MEMBER_MENU_CFG_STATE
                else:
                    init_state = fsm_def.MEMBER_DELIVERY_STATE
            else:
                init_state = fsm_def.MEMBER_MENU_CFG_STATE
            
            mbr = member_def.Member(mbr_moc, init_state)
            
            if mbr_moc.subscriber_open_id is not None and len(mbr_moc.subscriber_open_id) > 0:
                subs = self.get_worker().get_app().get_mit_manager().rdm_find("Subscriber", subscriber_open_id = mbr_moc.subscriber_open_id)
                if len(subs) > 0:
                    mbr.set_assoc_subscriber(subs[0])
                    
            processor = fsm_def.StateProcessor(mbr, self.get_worker())
            processor.register_state_handler(fsm_def.MEMBER_MENU_CFG_STATE, member_state_man.MbrMenuCfgStateHandler(processor))
            processor.register_state_handler(fsm_def.MEMBER_DELIVERY_STATE, member_state_man.MbrDeliveryStateHandler(processor))
            processor.register_state_handler(fsm_def.MEMBER_EXPIRED_STATE, member_state_man.MbrDeliveryExpiredStateHandler(processor))
            
            self.get_worker().get_state_manager().add_processor(processor)


class PortalMemberStateEventMsgHandler(bf.CmdHandler):
    """
    Class: PortalMemberStateEventMsgHandler
    Description: ��Ա״̬���¼���Ϣ����handler
    Base: CmdHandler
    Others: 
    """

    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: �����Ա״̬���¼���Ϣ
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)       

        buf = frame.get_data()
        event = cPickle.loads(buf)
        self.get_worker().get_state_manager().process_event(event)

        processor = self.get_worker().get_state_manager().get_processor(event.target_id)
        if processor is not None:
            if processor.get_target().get_state() == fsm_def.MEMBER_EXPIRED_STATE:
                tracelog.info('member(%s) expired, remove the processor' % event.target_id)
                self.get_worker().get_state_manager().remove_processor(processor)
                del processor
                

class MemberManagerWorker(bf.CmdWorker):
    """
    Class: MemberManagerWorker
    Description: ��Ա�����߳�worker��
    Base: CmdWorker
    Others: 
    """

    
    def __init__(self, min_task_id, max_task_id):
        """
        Method: __init__
        Description: ���ʼ��
        Parameter: 
            min_task_id: ��С����ID
            max_task_id: �������ID
        Return: 
        Others: 
        """

        bf.CmdWorker.__init__(self, "MemberManagerWorker", min_task_id, max_task_id)

        self._state_manager = fsm_def.FsmManager()
        self._state_manager.register_event_handler(fsm_def.MEMBER_MENU_CFG_STATE, fsm_def.MEMBER_DAILY_EVENT, member_state_man.MbrAnyStateDailyEventHandler())
        self._state_manager.register_event_handler(fsm_def.MEMBER_MENU_CFG_STATE, fsm_def.MEMBER_MENU_CFG_EVENT, member_state_man.MbrMenuCfgStateMenuCfgEventHandler())
        self._state_manager.register_event_handler(fsm_def.MEMBER_DELIVERY_STATE, fsm_def.MEMBER_DAILY_EVENT, member_state_man.MbrAnyStateDailyEventHandler())

    def get_state_manager(self):
        """
        Method: get_state_manager
        Description: ��ȡ������״̬������
        Parameter: ��
        Return: ��д��״̬������
        Others: 
        """
        return self._state_manager
        
        
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

        self.register_handler(PortalMemberCfgMemberHandler(), cmd_code_def.PORTAL_MEMBER_MEMBER_CREATE)
        self.register_handler(PortalMemberCfgMemberHandler(), cmd_code_def.PORTAL_MEMBER_MEMBER_MODIFY)
        self.register_handler(PortalMemberRemoveMemberHandler(), cmd_code_def.PORTAL_MEMBER_MEMBER_REMOVE)
        self.register_handler(PortalMemberQueryMemberHandler(), cmd_code_def.PORTAL_MEMBER_MEMBER_QUERY)

        self.register_handler(PortalDeliveryCreateVegetableHandler(), cmd_code_def.PORTAL_DELIVERY_VEGETABLE_CREATE)
        self.register_handler(PortalDeliveryModifyVegetableHandler(), cmd_code_def.PORTAL_DELIVERY_VEGETABLE_MODIFY)
        self.register_handler(PortalDeliveryRemoveVegetableHandler(), cmd_code_def.PORTAL_DELIVERY_VEGETABLE_REMOVE)
        self.register_handler(PortalDeliveryQueryVegetableHandler(), cmd_code_def.PORTAL_DELIVERY_VEGETABLE_QUERY)

        self.register_handler(PortalDeliveryMemberNenuCfgHandler(), cmd_code_def.PORTAL_DELIVERY_MEMBER_MENU_CFG)
        self.register_handler(PortalDeliveryReportQueryHandler(), cmd_code_def.PORTAL_DELIVERY_REPORT_QUERY)
        
        self.register_handler(PortalMemberManInitHandler(), cmd_code_def.CLOUD_PORTAL_MEMBER_MGR_INIT_MSG)
        self.register_handler(PortalMemberStateEventMsgHandler(), cmd_code_def.CLOUD_PORTAL_MEMBER_STATE_EVENT_MSG)

        frame = bf.AppFrame()
        frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_MEMBER_MGR_INIT_MSG)
        self.dispatch_frame_to_worker('MemberManagerWorker', frame)
                
        return 0
    
    def get_delivery_period(self, delivery_weekday):
        delivery_period = []
        menucfg_period = []
        for day in range(1, 8):
            dgap = day - delivery_weekday
            if dgap < 0:
                dgap = dgap + 7
            if dgap >= 1 and dgap <= 4:
                menucfg_period.append(day)
    
            mgap = delivery_weekday - day
            if mgap < 0:
                mgap = mgap + 7
            if mgap >=0 and mgap <= 2:
                delivery_period.append(day)
                
        return (menucfg_period, delivery_period)    

    def get_next_delivery_date(self, time_in_sec, delivery_weekday):
        now_date = time.localtime(time_in_sec)
        weekday = now_date.tm_wday + 1
        
        gap = delivery_weekday - weekday
        if gap <= 0:
            gap += 7
        
        next_sec = time_in_sec + 24 * 3600 * gap
        next_date = time.strftime('%Y-%m-%d', time.localtime(next_sec))
        return next_date

