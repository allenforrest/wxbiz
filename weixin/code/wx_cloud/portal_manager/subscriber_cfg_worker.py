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
        
        records = self.get_worker().get_app().get_mit_manager().lookup_attrs('Subscriber',
                                                                             [
                                                                              'subscriber_open_id',
                                                                              'weixin_id',
                                                                              'nickname',
                                                                              'gender',
                                                                              'city',
                                                                              'group_ids',
                                                                              'assoc_member_id'                                                                             
                                                                              ],
                                                                             num_per_page = num_per_page, 
                                                                             current_page = current_page
                                                                             )
        
        result.subscribers = []
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
            
            result.subscribers.append(sub)

        if group_id is None:
            result.count = self.get_worker().get_app().get_mit_manager().count('Subscriber')
        else:
            count = 0
            for sub_rec in all_records:
                if group_id in sub_rec[0].group_ids:
                    count += 1
            
            result.count = count
            
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

        #self.register_handler(PortalSubscriberMemberAssociateHandler(), cmd_code_def.PORTAL_SUBSCRIBER_MEMBER_ASSOCIATE)
        return 0

