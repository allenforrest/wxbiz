#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-13
Description: Portal管理模块 订阅者管理线程
Key Class&Method List: 
             1. SubscriberConfigWorker -- worker类
History:
1. Date: 2013-5-13
   Author: Allen
   Modification: create
"""
import import_paths

import bundleframework as bf
import basic_rep_to_web
import mit

import err_code_mgr

import tracelog
import cmd_code_def

import msg_params_def


class PortalSubscriberInfoQueryHandler(bf.CmdHandler):
    """
    Class: PortalSubscriberInfoQueryHandler
    Description: Portal下发的查询订阅者信息的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理查询订阅者信息的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = msg_params_def.PortalSubscriberInfoQueryRsp()
        result.init_all_attr()
        tracelog.info('subscriber cfg worker recv sub frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            sub_qry = msg_params_def.PortalSubscriberInfoQueryReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_SUBSCRIBER_INFO_QUERY',
                                                            param_name = 'PortalSubscriberInfoQueryReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        num_per_page = None
        current_page = None
        group_id = None
        
        if sub_qry is not None:
            if hasattr(sub_qry, "num_per_page"):
                num_per_page = sub_qry.num_per_page

            if hasattr(sub_qry, "current_page"):
                current_page = sub_qry.current_page

        if sub_qry.group_id is not None and len(sub_qry.group_id) != 0:
            group_id = int(sub_qry.group_id)

        all_records = self.get_worker().get_app().get_mit_manager().lookup_attrs('Subscriber', ['group_ids'])

        multi_sql = mit.MultiSQL()
        multi_sql.set_sqlite_sql('subscribe_seq_no desc')   
        
        records = self.get_worker().get_app().get_mit_manager().lookup_attrs('Subscriber',
                                                                             [
                                                                              'subscriber_open_id',
                                                                              'weixin_id',
                                                                              'nickname',
                                                                              'gender',
                                                                              'city',
                                                                              'group_ids',
                                                                              'assoc_member_id',
                                                                              'admin_flag'                                                                     
                                                                              ],
                                                                             order_by_sql = multi_sql
                                                                             #num_per_page = num_per_page, 
                                                                             #current_page = current_page
                                                                             )
        
        result.subscribers = []
        
        all_subscribers = []
        for sub_rec in records:
            if group_id is not None and group_id not in sub_rec[5].group_ids:
                continue
            
            sub = msg_params_def.Subscriber()
            sub.init_all_attr()
            sub.subscriber_open_id = sub_rec[0]
            sub.weixin_id = sub_rec[1]
            sub.nickname = sub_rec[2]
            sub.gender = sub_rec[3]
            sub.city = sub_rec[4]
            sub.group_ids = [str(gid) for gid in sub_rec[5].group_ids]
            
            members = self.get_worker().get_app().get_mit_manager().rdm_find('Member', 
                                                                             member_id = sub_rec[6])            

            if len(members) == 0:
                sub.member_flag = False
                sub.assoc_member_id = None
                sub.assoc_member_name = None
            else:
                sub.member_flag = True
                sub.assoc_member_id = sub_rec[6]
                sub.assoc_member_name = members[0].name
            
            sub.head_img = '/' + msg_params_def.WX_HEAD_IMG_FILE_SAVE_LOCAL_PATH + sub.subscriber_open_id + '.png'
            
            sub.admin_flag = True if sub_rec[7] == 'True' else False
            
            all_subscribers.append(sub)

        if group_id is None:
            result.count = self.get_worker().get_app().get_mit_manager().count('Subscriber')
        else:
            count = 0
            for sub_rec in all_records:
                if group_id in sub_rec[0].group_ids:
                    count += 1
            
            result.count = count

        if num_per_page is not None and num_per_page > 0 and current_page is not None:
            all_sub_map = {}
            page_num = 0
            count = 0
            for s in all_subscribers:
                if all_sub_map.has_key(page_num) is False:
                    all_sub_map[page_num] = []
                all_sub_map[page_num].append(s)
                count += 1
                page_num = count / num_per_page 
        
            if all_sub_map.has_key(current_page) is True:
                result.subscribers = all_sub_map[current_page]
            else:
                result.return_code = err_code_mgr.ERR_PORTAL_SUBSCRIBER_NOT_EXISTS
                result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_SUBSCRIBER_NOT_EXISTS)
    
                result.prepare_for_ack(sub_qry, result.return_code, result.description)
                self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                return
        else:
            result.subscribers = all_subscribers
            
        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.prepare_for_ack(sub_qry, result.return_code, result.description)
        tracelog.info(result.serialize())
         
        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
        

class PortalSubscriberGroupAssociateHandler(bf.CmdHandler):
    """
    Class: PortalSubscriberGroupAssociateHandler
    Description: Portal下发的订阅者加入分组的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者加入分组的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
                
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('subscriber cfg worker recv group frame: %s' % frame)
        
        self._req_frame = frame
        buf = frame.get_data()
        
        try:
            assoc_req = msg_params_def.PortalSubscriberGroupAssociateReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_SUBSCRIBER_GROUP_ASSOCIATE',
                                                            param_name = 'PortalSubscriberGroupAssociateReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        self._message = assoc_req
        # 检查订阅者是否存在
        subs = self.get_worker().get_app().get_mit_manager().rdm_find('Subscriber',
                                                                      subscriber_open_id = assoc_req.subscriber_open_id)   

        if len(subs) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_SUBSCRIBER_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_SUBSCRIBER_NOT_EXISTS)

            result.prepare_for_ack(assoc_req, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        else:
            # 检查订阅者关联的分组是否都存在
            group_ids = assoc_req.group_ids
            for gid in group_ids:
                grps = self.get_worker().get_app().get_mit_manager().rdm_find('Group',
                                                                              group_id = int(gid))
                if len(grps) == 0:
                    result.return_code = err_code_mgr.ERR_PORTAL_GROUP_NOT_EXISTS
                    result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_GROUP_NOT_EXISTS)
        
                    result.prepare_for_ack(assoc_req, result.return_code, result.description)
                    self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                    return
            
            sub_frame = bf.AppFrame()
            sub_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_SUB_GROUP_ASSOC_MSG)
            sub_frame.set_receiver_pid(self.get_worker().get_pid("SubscriberManApp"))
            sub_frame.add_data(buf)
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
        tracelog.error('send message to SubscriberManApp, ack timeout')        
        
    def _on_round_over(self, round_id, r):        
        """
        Method: _on_round_over
        Description: 接收订阅者管理模块的响应，构造响应返回给WEB
        Parameter: 
            round_id: 
            r: 
        Return: 
        Others: 
        """
        frame = r.get_response_frame()
        buf = frame.get_data()
        self.get_worker().get_app().send_ack_dispatch(self._req_frame, (buf, ))
                

class PortalSubscriberGroupCreateHandler(bf.CmdHandler):
    """
    Class: PortalSubscriberGroupCreateHandler
    Description: Portal下发的创建订阅者分组的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理创建订阅者分组的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('subscriber cfg worker recv group frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            grp_cfg = msg_params_def.PortalSubscriberGroupCreateReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_SUBSCRIBER_GROUP_CREATE',
                                                            param_name = 'PortalSubscriberGroupCreateReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        grp_moc = self.get_worker().get_app().get_mit_manager().gen_rdm("Group")
        grp_moc.group_id = self.get_worker().get_app().get_group_no_creater().get_new_no()
        grp_moc.group_name = grp_cfg.group_name
        grp_moc.description = grp_cfg.description
        ret = self.get_worker().get_app().get_mit_manager().rdm_add(grp_moc)
        
        if ret.get_err_code() == err_code_mgr.ER_OBJECT_ADD_CONFLICT:
            result.return_code = err_code_mgr.ERR_PORTAL_GROUP_RECORDS_FULL
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_GROUP_RECORDS_FULL)

            result.prepare_for_ack(grp_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        elif ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(grp_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(grp_cfg, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalSubscriberGroupModifyHandler(bf.CmdHandler):
    """
    Class: PortalSubscriberGroupModifyHandler
    Description: Portal下发的修改分组的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理修改分组的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
                
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('subscriber cfg worker recv group frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            grp_mod = msg_params_def.PortalSubscriberGroupModifyReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_SUBSCRIBER_GROUP_MODIFY',
                                                            param_name = 'PortalSubscriberGroupModifyReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        grp_moc = self.get_worker().get_app().get_mit_manager().gen_rdm("Group")
        grp_moc.group_id = int(grp_mod.group_id)
        grp_moc.group_name = grp_mod.group_name
        grp_moc.description = grp_mod.description

        ret = self.get_worker().get_app().get_mit_manager().rdm_mod(grp_moc)
        
        if ret.get_err_code() == err_code_mgr.ER_OBJECT_NOT_EXIST:
            result.return_code = err_code_mgr.ERR_PORTAL_GROUP_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_GROUP_NOT_EXISTS)

            result.prepare_for_ack(grp_mod, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        elif ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(grp_mod, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(grp_mod, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalSubscriberGroupRemoveHandler(bf.CmdHandler):
    """
    Class: PortalSubscriberGroupRemoveHandler
    Description: Portal下发的删除分组的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理删除分组的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('subscriber cfg worker recv group frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            grp_rmv = msg_params_def.PortalSubscriberGroupRemoveReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_SUBSCRIBER_GROUP_REMOVE',
                                                            param_name = 'PortalSubscriberGroupRemoveReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        group_id = int(grp_rmv.group_id)
        grps = self.get_worker().get_app().get_mit_manager().rdm_find(moc_name = "Group", group_id = group_id)
        if len(grps) == 1:
            subs = self.get_worker().get_app().get_mit_manager().lookup_attrs('Subscriber', ['group_ids'])
            for sub in subs:
                if group_id in sub[0]:
                    result.return_code = err_code_mgr.ERR_PORTAL_GROUP_ASSOCIATED_BY_SUB
                    result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_GROUP_ASSOCIATED_BY_SUB)
        
                    result.prepare_for_ack(grp_rmv, result.return_code, result.description)
                    self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                    return
                            
            self.get_worker().get_app().get_mit_manager().rdm_remove(grps[0])

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(grp_rmv, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalSubscriberGroupQueryHandler(bf.CmdHandler):
    """
    Class: PortalSubscriberGroupQueryHandler
    Description: Portal下发的查询分组的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理查询分组的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = msg_params_def.PortalSubscriberGroupQueryRsp()
        result.init_all_attr()
        tracelog.info('subscriber cfg worker recv group frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            grp_qry = msg_params_def.CommonQueryReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_SUBSCRIBER_GROUP_QUERY',
                                                            param_name = 'CommonQueryReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        records = self.get_worker().get_app().get_mit_manager().rdm_find('Group')
        sub_records = self.get_worker().get_app().get_mit_manager().lookup_attrs('Subscriber', ['group_ids'])
        
        result.groups = []
        for grp_rec in records:
            grp = msg_params_def.Group()
            grp.init_all_attr()
            grp.group_id = str(grp_rec.group_id)
            grp.group_name = grp_rec.group_name
            grp.description = grp_rec.description

            count = 0
            for sub_rec in sub_records:
                if grp_rec.group_id in sub_rec[0].group_ids:
                    count += 1            
            grp.group_sub_num = count

            result.groups.append(grp)

        # 给WEB回成功响应
        result.count = len(result.groups)
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.prepare_for_ack(grp_qry, result.return_code, result.description)
        tracelog.info(result.serialize())
         
        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalSubscriberGroupMsgPushHandler(bf.CmdHandler):
    """
    Class: PortalSubscriberGroupMsgPushHandler
    Description: Portal下发的订阅者分组消息群发的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者分组消息群发的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('subscriber cfg worker recv group msg push frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            push_info = msg_params_def.PortalSubscriberGroupMsgPushReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_SUBSCRIBER_GROUP_MSG_PUSH',
                                                            param_name = 'PortalSubscriberGroupMsgPushReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        grp_list_valid = True
        
        grps = self.get_worker().get_app().get_mit_manager().rdm_find('Group')
        if len(grps) > 0:
            gids = [grp.group_id for grp in grps]
            for gid in push_info.group_ids:
                if int(gid) not in gids:
                    grp_list_valid = False
                    break
        else:
            grp_list_valid = False

        if grp_list_valid is False:
            result.return_code = err_code_mgr.ERR_PORTAL_GROUP_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_GROUP_NOT_EXISTS)

            result.prepare_for_ack(push_info, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        

        records = self.get_worker().get_app().get_mit_manager().lookup_attrs('Subscriber',
                                                                             [
                                                                              'subscriber_open_id',
                                                                              'group_ids',
                                                                              ])
        push_subs = {}
        
        for gid in push_info.group_ids:
            for rec in records:
                if int(gid) in rec[1].group_ids:
                    push_subs[rec[0]] = None
        
        push_sub_list = push_subs.keys()
        
        # 构造推送消息发给SubscriberManApp
        push_msg = msg_params_def.CloudPortalTextPushMessage()
        push_msg.init_all_attr()
        push_msg.subscriber_open_ids = push_sub_list
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


class PortalSubscriberMemberAssociateHandler(bf.CmdHandler):
    """
    Class: PortalSubscriberMemberAssociateHandler
    Description: Portal下发的订阅者绑定会员的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者绑定会员的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
                
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('subscriber cfg worker recv member frame: %s' % frame)
        
        self._req_frame = frame
        buf = frame.get_data()
        
        try:
            assoc_req = msg_params_def.PortalSubscriberMemberAssociateReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_SUBSCRIBER_MEMBER_ASSOCIATE',
                                                            param_name = 'PortalSubscriberMemberAssociateReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        self._message = assoc_req
        # 检查订阅者是否存在
        subs = self.get_worker().get_app().get_mit_manager().rdm_find('Subscriber',
                                                                      subscriber_open_id = assoc_req.subscriber_open_id)   

        if len(subs) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_SUBSCRIBER_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_SUBSCRIBER_NOT_EXISTS)

            result.prepare_for_ack(assoc_req, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        else:
            old_member_id = subs[0].assoc_member_id
            
            # 检查订阅者关联的会员是否都存在
            if len(assoc_req.member_id) > 0: 
                members = self.get_worker().get_app().get_mit_manager().rdm_find('Member', member_id = assoc_req.member_id)
                if len(members) == 0:
                    result.return_code = err_code_mgr.ERR_PORTAL_MEMBER_NOT_EXISTS
                    result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_MEMBER_NOT_EXISTS)
        
                    result.prepare_for_ack(assoc_req, result.return_code, result.description)
                    self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                    return
                else:
                    # 如果后台下发了会员名和联系方式，表示是微信用户自行关联，需要检查会员信息是否合法
                    if (len(assoc_req.name) > 0 and assoc_req.name != members[0].name) or (len(assoc_req.cellphone) > 0 and assoc_req.cellphone != members[0].cellphone):
                        result.return_code = err_code_mgr.ERR_PORTAL_MEMBER_INFO_INVALID
                        result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_MEMBER_INFO_INVALID)
            
                        result.prepare_for_ack(assoc_req, result.return_code, result.description)
                        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
                        return
                    
                    tracelog.info('member %s assoc subscriber %s succ' % (assoc_req.member_id, assoc_req.subscriber_open_id))

                    # 解除老的绑定关系
                    if old_member_id is not None and len(old_member_id) > 0:
                        old_members = self.get_worker().get_app().get_mit_manager().rdm_find('Member', member_id = old_member_id)
                        if len(old_members) > 0:
                            old_members[0].subscriber_open_id = ''
                            self.get_worker().get_app().get_mit_manager().rdm_mod(old_members[0])
        
                    members[0].subscriber_open_id = assoc_req.subscriber_open_id
                    self.get_worker().get_app().get_mit_manager().rdm_mod(members[0])
                    
                    mbr_pro = self.get_worker().get_app().get_member_man_worker().get_state_manager().get_processor(assoc_req.member_id)
                    if mbr_pro is not None:
                        mbr_pro.get_target().set_assoc_subscriber(subs[0])
                    
            sub_frame = bf.AppFrame()
            sub_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_SUB_MEMBER_ASSOC_MSG)
            sub_frame.set_receiver_pid(self.get_worker().get_pid("SubscriberManApp"))
            sub_frame.add_data(buf)
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
        tracelog.error('send message to SubscriberManApp, ack timeout')        
        
    def _on_round_over(self, round_id, r):        
        """
        Method: _on_round_over
        Description: 接收订阅者管理模块的响应，构造响应返回给WEB
        Parameter: 
            round_id: 
            r: 
        Return: 
        Others: 
        """
        frame = r.get_response_frame()
        buf = frame.get_data()
        self.get_worker().get_app().send_ack_dispatch(self._req_frame, (buf, ))


class PortalSubscriberAdminAssociateHandler(bf.CmdHandler):
    """
    Class: PortalSubscriberAdminAssociateHandler
    Description: Portal下发的订阅者绑定管理员的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理订阅者绑定管理员的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
                
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('subscriber cfg worker recv admin frame: %s' % frame)
        
        self._req_frame = frame
        buf = frame.get_data()
        
        try:
            assoc_req = msg_params_def.PortalSubscriberAdminAssociateReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_SUBSCRIBER_ADMIN_ASSOCIATE',
                                                            param_name = 'PortalSubscriberAdminAssociateReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        self._message = assoc_req
        # 检查订阅者是否存在
        subs = self.get_worker().get_app().get_mit_manager().rdm_find('Subscriber',
                                                                      subscriber_open_id = assoc_req.subscriber_open_id)   

        if len(subs) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_SUBSCRIBER_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_SUBSCRIBER_NOT_EXISTS)

            result.prepare_for_ack(assoc_req, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        else:
            sub_frame = bf.AppFrame()
            sub_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_SUB_ADMIN_ASSOC_MSG)
            sub_frame.set_receiver_pid(self.get_worker().get_pid("SubscriberManApp"))
            sub_frame.add_data(buf)
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
        tracelog.error('send message to SubscriberManApp, ack timeout')        
        
    def _on_round_over(self, round_id, r):        
        """
        Method: _on_round_over
        Description: 接收订阅者管理模块的响应，构造响应返回给WEB
        Parameter: 
            round_id: 
            r: 
        Return: 
        Others: 
        """
        frame = r.get_response_frame()
        buf = frame.get_data()
        self.get_worker().get_app().send_ack_dispatch(self._req_frame, (buf, ))

            
class SubscriberConfigWorker(bf.CmdWorker):
    """
    Class: SubscriberConfigWorker
    Description: 订阅者管理线程worker类
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

        bf.CmdWorker.__init__(self, "SubscriberConfigWorker", min_task_id, max_task_id)
        
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

        self.register_handler(PortalSubscriberGroupCreateHandler(), cmd_code_def.PORTAL_SUBSCRIBER_GROUP_CREATE)
        self.register_handler(PortalSubscriberGroupModifyHandler(), cmd_code_def.PORTAL_SUBSCRIBER_GROUP_MODIFY)
        self.register_handler(PortalSubscriberGroupRemoveHandler(), cmd_code_def.PORTAL_SUBSCRIBER_GROUP_REMOVE)
        self.register_handler(PortalSubscriberGroupQueryHandler(),  cmd_code_def.PORTAL_SUBSCRIBER_GROUP_QUERY)

        self.register_handler(PortalSubscriberInfoQueryHandler(), cmd_code_def.PORTAL_SUBSCRIBER_INFO_QUERY)
        self.register_handler(PortalSubscriberGroupAssociateHandler(), cmd_code_def.PORTAL_SUBSCRIBER_GROUP_ASSOCIATE)
        self.register_handler(PortalSubscriberGroupMsgPushHandler(), cmd_code_def.PORTAL_SUBSCRIBER_GROUP_MSG_PUSH)

        self.register_handler(PortalSubscriberMemberAssociateHandler(), cmd_code_def.PORTAL_SUBSCRIBER_MEMBER_ASSOCIATE)
        self.register_handler(PortalSubscriberAdminAssociateHandler(), cmd_code_def.PORTAL_SUBSCRIBER_ADMIN_ASSOCIATE)
        return 0

