#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-13
Description: Portal管理模块 内容管理线程
Key Class&Method List: 
             1. ContentManagerWorker -- worker类
History:
1. Date: 2013-5-13
   Author: Allen
   Modification: create
"""
import import_paths

import os

import bundleframework as bf
import basic_rep_to_web

import err_code_mgr

import tracelog
import cmd_code_def

import msg_params_def


class PortalContentArticleCreateHandler(bf.CmdHandler):
    """
    Class: PortalContentArticleCreateHandler
    Description: Portal下发的创建主题文章的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理创建主题文章的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('content man worker recv article frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            article_cfg = msg_params_def.PortalContentArticleCreateReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_ARTICLE_CREATE',
                                                            param_name = 'PortalContentArticleCreateReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        if article_cfg.title is None or len(article_cfg.title) == 0 or article_cfg.pic_url is None or len(article_cfg.pic_url) == 0 or article_cfg.content is None or len(article_cfg.content) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_ARTICLE_PARAMS_INVALID
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_ARTICLE_PARAMS_INVALID)

            result.prepare_for_ack(article_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        article_moc = self.get_worker().get_app().get_mit_manager().gen_rdm("Article")
        article_moc.article_id = self.get_worker().get_app().get_article_no_creator().get_new_no()
        self._article_id = article_moc.article_id
        
        article_moc.title = article_cfg.title
        article_moc.description = article_cfg.description
        article_moc.subject_id = int(article_cfg.subject_id)
        article_moc.pic_url = article_cfg.pic_url
        article_moc.content_url = "%s/%s" % (article_cfg.content_url, article_moc.article_id)
        article_moc.content = article_cfg.content
        article_moc.push_timer = article_cfg.push_timer
        article_moc.push_times = article_cfg.push_times
        article_moc.counter = 0
        
        ret = self.get_worker().get_app().get_mit_manager().rdm_add(article_moc)
        
        if ret.get_err_code() == err_code_mgr.ER_OBJECT_ADD_CONFLICT:
            result.return_code = err_code_mgr.ERR_PORTAL_ARTICLE_RECORDS_FULL
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_ARTICLE_RECORDS_FULL)

            result.prepare_for_ack(article_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        elif ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(article_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        gids = msg_params_def.GroupList()
        gids.group_ids = [int(gid) for gid in article_cfg.sub_group_ids] 
        
        mo_id = self.get_worker().get_app().get_mit_manager().gen_moid("Article", article_id = self._article_id)
        self.get_worker().get_app().get_mit_manager().mod_complex_attr('Article', 
                                                                       moid = mo_id, 
                                                                       group_ids = gids)
                
        if article_moc.push_timer is not None and len(article_moc.push_timer) > 0:
            if article_moc.push_times is None or len(article_moc.push_times) == 0:
                times = 1
            else:
                times = int(article_moc.push_times)
            self.get_worker().get_app().get_push_task_manager().del_task(article_moc.article_id)
            self.get_worker().get_app().get_push_task_manager().add_task(article_moc.push_timer, 
                                                                         times,
                                                                         article_moc.article_id)
        new_frame = bf.AppFrame()
        new_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_CONTENT_UPDATE_MSG)
        self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), new_frame)        
        
        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(article_cfg, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
        
        if article_cfg.pic_url != '' and article_cfg.pic_url.find(msg_params_def.LOCAL_HOST_DOMAIN) >= 0:
            create_frame = bf.AppFrame()
            create_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_ARTICLE_UPLOAD_MSG)
            create_frame.set_receiver_pid(self.get_worker().get_pid('SubscriberManApp'))
            create_frame.add_data(msg_params_def.PORTAL_CLOUD_IMAGE_UPLOAD_NEW)
            create_frame.add_data(str(self._article_id))
            self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), create_frame)        
        

class PortalContentArticleModifyHandler(bf.CmdHandler):
    """
    Class: PortalContentArticleModifyHandler
    Description: Portal下发的修改主题文章的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理修改主题文章的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('content man worker recv article frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            article_mod = msg_params_def.PortalContentArticleModReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_ARTICLE_MODIFY',
                                                            param_name = 'PortalContentArticleModReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        if article_mod.title is None or len(article_mod.title) == 0 or article_mod.pic_url is None or len(article_mod.pic_url) == 0 or article_mod.content is None or len(article_mod.content) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_ARTICLE_PARAMS_INVALID
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_ARTICLE_PARAMS_INVALID)

            result.prepare_for_ack(article_mod, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        self._article_id = int(article_mod.article_id)
        article_moc = self.get_worker().get_app().get_mit_manager().rdm_find("Article", article_id = self._article_id)
        if len(article_moc) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_ARTICLE_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_ARTICLE_NOT_EXISTS)

            result.prepare_for_ack(article_mod, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        article_moc[0].title = article_mod.title
        article_moc[0].description = article_mod.description
        article_moc[0].subject_id = int(article_mod.subject_id)
        article_moc[0].pic_url = article_mod.pic_url
        article_moc[0].content = article_mod.content
        article_moc[0].push_timer = article_mod.push_timer
        article_moc[0].push_times = article_mod.push_times
        
        ret = self.get_worker().get_app().get_mit_manager().rdm_mod(article_moc[0])
        
        if ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(article_mod, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        gids = msg_params_def.GroupList()
        gids.group_ids = [int(gid) for gid in article_mod.sub_group_ids] 
        
        mo_id = self.get_worker().get_app().get_mit_manager().gen_moid("Article", article_id = self._article_id)
        self.get_worker().get_app().get_mit_manager().mod_complex_attr('Article', 
                                                                       moid = mo_id, 
                                                                       group_ids = gids)

        if article_moc[0].push_timer is not None and len(article_moc[0].push_timer) > 0:
            if article_moc[0].push_times is None or len(article_moc[0].push_times) == 0:
                times = 1
            else:
                times = int(article_moc[0].push_times)
            self.get_worker().get_app().get_push_task_manager().del_task(article_moc[0].article_id)
            self.get_worker().get_app().get_push_task_manager().add_task(article_moc[0].push_timer, 
                                                                         times,
                                                                         article_moc[0].article_id)

        new_frame = bf.AppFrame()
        new_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_CONTENT_UPDATE_MSG)
        self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), new_frame)        
                
        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(article_mod, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))

        if article_mod.pic_url != '' and article_mod.pic_url.find(msg_params_def.LOCAL_HOST_DOMAIN) >= 0:
            mod_frame = bf.AppFrame()
            mod_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_ARTICLE_UPLOAD_MSG)
            mod_frame.set_receiver_pid(self.get_worker().get_pid('SubscriberManApp'))
            mod_frame.add_data(msg_params_def.PORTAL_CLOUD_IMAGE_UPLOAD_MOD)
            mod_frame.add_data(str(self._article_id))
            self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), mod_frame)        
            

class PortalContentArticleRemoveHandler(bf.CmdHandler):
    """
    Class: PortalContentArticleRemoveHandler
    Description: Portal下发的删除主题文章的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理删除主题文章的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('content man worker recv article frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            article_rmv = msg_params_def.PortalContentArticleRemoveReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_ARTICLE_REMOVE',
                                                            param_name = 'PortalContentArticleRemoveReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        articles = self.get_worker().get_app().get_mit_manager().rdm_find(moc_name = "Article", article_id = int(article_rmv.article_id))
        if len(articles) == 1:
            wx_news_id = articles[0].wx_news_id                     
            # 删除本地图片文件
            if articles[0].pic_url.find('upload/memory.png') < 0:
                try:
                    pic_url = articles[0].pic_url.strip('http://')
                    pic_path = msg_params_def.PORTAL_IMG_FILE_LOCAL_PATH_PREFIX + pic_url[pic_url.find('/'):]
                    os.remove(pic_path)
                except Exception, e:
                    tracelog.error('del img file(%s) in local path failed(%s)' % (pic_path, e))
            
            self.get_worker().get_app().get_mit_manager().rdm_remove(articles[0])

        self.get_worker().get_app().get_push_task_manager().del_task(article_rmv.article_id)

        new_frame = bf.AppFrame()
        new_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_CONTENT_UPDATE_MSG)
        self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), new_frame)        

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(article_rmv, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))

        del_frame = bf.AppFrame()
        del_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_ARTICLE_UPLOAD_MSG)
        del_frame.set_receiver_pid(self.get_worker().get_pid('SubscriberManApp'))
        del_frame.add_data(msg_params_def.PORTAL_CLOUD_IMAGE_UPLOAD_DEL)
        del_frame.add_data(str(article_rmv.article_id))
        del_frame.add_data(wx_news_id)
        
        self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), del_frame)        


class PortalContentArticleQueryHandler(bf.CmdHandler):
    """
    Class: PortalContentArticleQueryHandler
    Description: Portal下发的查询主题文章的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理查询主题文章的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = msg_params_def.PortalContentArticleQueryRsp()
        result.init_all_attr()
        tracelog.info('content man worker recv article frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            article_qry = msg_params_def.PortalContentArticleQueryReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_ARTICLE_QUERY',
                                                            param_name = 'PortalContentArticleQueryReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        num_per_page = None
        current_page = None
        batch_query = True
        pfm_count = False
        
        if article_qry is not None:
            if hasattr(article_qry, "num_per_page"):
                num_per_page = article_qry.num_per_page

            if hasattr(article_qry, "current_page"):
                current_page = article_qry.current_page
       
        if article_qry.subject_id is not None and len(article_qry.subject_id) != 0 and article_qry.subject_id != 'FFFF':
            subject_id = int(article_qry.subject_id)
            records = self.get_worker().get_app().get_mit_manager().lookup_attrs('Article',
                                                                                 [
                                                                                  'article_id',
                                                                                  'title',
                                                                                  'subject_id',
                                                                                  'description',
                                                                                  'pic_url',
                                                                                  'content_url',
                                                                                  'content',
                                                                                  'group_ids',
                                                                                  'push_timer',
                                                                                  'push_times'                                                                                                                                               
                                                                                  ],
                                                                                 num_per_page = num_per_page,
                                                                                 current_page = current_page,
                                                                                 subject_id = subject_id)
            
            result.count = self.get_worker().get_app().get_mit_manager().count('Article', subject_id = subject_id)
        elif article_qry.article_id is not None and len(article_qry.article_id) != 0:
            batch_query = False
            article_id = int(article_qry.article_id)
            records = self.get_worker().get_app().get_mit_manager().lookup_attrs('Article',
                                                                                 [
                                                                                  'article_id',
                                                                                  'title',
                                                                                  'subject_id',
                                                                                  'description',
                                                                                  'pic_url',
                                                                                  'content_url',
                                                                                  'content',
                                                                                  'group_ids',
                                                                                  'push_timer',
                                                                                  'push_times'                                                                                                                                               
                                                                                  ],
                                                                                 num_per_page = num_per_page, 
                                                                                 current_page = current_page,
                                                                                 article_id = article_id)
            result.count = self.get_worker().get_app().get_mit_manager().count('Article', article_id = article_id)
            if article_qry.subject_id != 'FFFF':
                pfm_count = True
        else:
            records = self.get_worker().get_app().get_mit_manager().lookup_attrs('Article',
                                                                                 [
                                                                                  'article_id',
                                                                                  'title',
                                                                                  'subject_id',
                                                                                  'description',
                                                                                  'pic_url',
                                                                                  'content_url',
                                                                                  'content',
                                                                                  'group_ids',
                                                                                  'push_timer',
                                                                                  'push_times'                                                                                                                                               
                                                                                  ],
                                                                                 num_per_page = num_per_page, 
                                                                                 current_page = current_page)
            result.count = self.get_worker().get_app().get_mit_manager().count('Article') 
        
        result.articles = []
        for article_rec in records:
            
            article = msg_params_def.Article()
            article.init_all_attr()
            article.article_id = str(article_rec[0])
            article.title = article_rec[1]
            article.subject_id = str(article_rec[2])
            article.description = article_rec[3]
            article.pic_url = article_rec[4]
            article.content_url = article_rec[5]
            if batch_query is True:
                article.content = ''
            else:
                article.content = article_rec[6]
                
            article.sub_group_ids = [str(gid) for gid in article_rec[7].group_ids]
                
            article.push_timer = article_rec[8]
            article.push_times = article_rec[9]
            
            if pfm_count is True:
                arts = self.get_worker().get_app().get_mit_manager().rdm_find('Article', article_id = article_rec[0])
                arts[0].counter += 1
                self.get_worker().get_app().get_mit_manager().rdm_mod(arts[0])
            
            result.articles.append(article)

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.prepare_for_ack(article_qry, result.return_code, result.description)
        tracelog.info(result.serialize())
         
        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
        

class PortalContentSubjectCreateHandler(bf.CmdHandler):
    """
    Class: PortalContentSubjectCreateHandler
    Description: Portal下发的创建栏目的命令handler
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
        tracelog.info('content man worker recv subject frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            sub_cfg = msg_params_def.PortalContentSubjectCreateReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_SUBJECT_CREATE',
                                                            param_name = 'PortalContentSubjectCreateReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        sub_moc = self.get_worker().get_app().get_mit_manager().gen_rdm("Subject")
        sub_moc.subject_id = self.get_worker().get_app().get_subject_no_creator().get_new_no()
        sub_moc.name = sub_cfg.name
        sub_moc.description = sub_cfg.description
        sub_moc.counter = 0
        ret = self.get_worker().get_app().get_mit_manager().rdm_add(sub_moc)
        
        if ret.get_err_code() == err_code_mgr.ER_OBJECT_ADD_CONFLICT:
            result.return_code = err_code_mgr.ERR_PORTAL_ARTICLE_RECORDS_FULL
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_ARTICLE_RECORDS_FULL)

            result.prepare_for_ack(sub_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        elif ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(sub_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        new_frame = bf.AppFrame()
        new_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_CONTENT_UPDATE_MSG)
        self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), new_frame)        

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(sub_cfg, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalContentSubjectModifyHandler(bf.CmdHandler):
    """
    Class: PortalContentSubjectModifyHandler
    Description: Portal下发的修改栏目的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理修改栏目的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
                
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('content man worker recv subject frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            sub_mod = msg_params_def.PortalContentSubjectModReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_SUBJECT_MODIFY',
                                                            param_name = 'PortalContentSubjectModReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        sub_moc = self.get_worker().get_app().get_mit_manager().rdm_find("Subject", subject_id = int(sub_mod.subject_id))
        if len(sub_moc) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_SUBJECT_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_SUBJECT_NOT_EXISTS)

            result.prepare_for_ack(sub_mod, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        sub_moc[0].name = sub_mod.name
        sub_moc[0].description = sub_mod.description

        ret = self.get_worker().get_app().get_mit_manager().rdm_mod(sub_moc[0])
        if ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(sub_mod, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        new_frame = bf.AppFrame()
        new_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_CONTENT_UPDATE_MSG)
        self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), new_frame)        

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(sub_mod, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalContentSubjectRemoveHandler(bf.CmdHandler):
    """
    Class: PortalContentSubjectRemoveHandler
    Description: Portal下发的删除栏目的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理删除栏目的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('content man worker recv subject frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            sub_rmv = msg_params_def.PortalContentSubjectRemoveReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_SUBJECT_REMOVE',
                                                            param_name = 'PortalContentSubjectRemoveReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        subs = self.get_worker().get_app().get_mit_manager().rdm_find(moc_name = "Subject", subject_id = int(sub_rmv.subject_id))
        if len(subs) == 1:                                    
            self.get_worker().get_app().get_mit_manager().rdm_remove(subs[0])
            
        arts = self.get_worker().get_app().get_mit_manager().rdm_find(moc_name = "Article", subject_id = int(sub_rmv.subject_id))
        for art in arts:
            self.get_worker().get_app().get_mit_manager().rdm_remove(art)

        new_frame = bf.AppFrame()
        new_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_CONTENT_UPDATE_MSG)
        self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), new_frame)        

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(sub_rmv, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalContentSubjectQueryHandler(bf.CmdHandler):
    """
    Class: PortalContentSubjectQueryHandler
    Description: Portal下发的查询栏目的命令handler
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
        
        result = msg_params_def.PortalContentSubjectQueryRsp()
        result.init_all_attr()
        tracelog.info('content man worker recv subject frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            sub_qry = msg_params_def.CommonQueryReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_SUBJECT_QUERY',
                                                            param_name = 'CommonQueryReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        records = self.get_worker().get_app().get_mit_manager().rdm_find('Subject')
        
        result.subjects = []
        for sub_rec in records:
            sub = msg_params_def.Subject()
            sub.init_all_attr()
            sub.subject_id = str(sub_rec.subject_id)
            sub.name = sub_rec.name
            sub.description = sub_rec.description
            sub.article_num = self.get_worker().get_app().get_mit_manager().count('Article', subject_id = sub_rec.subject_id)
            result.subjects.append(sub)

        # 给WEB回成功响应
        result.count = len(result.subjects) 
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.prepare_for_ack(sub_qry, result.return_code, result.description)
        tracelog.info(result.serialize())
         
        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))


class PortalContentHelpTipsSetHandler(bf.CmdHandler):
    """
    Class: PortalContentHelpTipsSetHandler
    Description: Portal下发的设置欢迎词与帮助的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理设置欢迎词与帮助的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('content man worker recv helptips frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            help_cfg = msg_params_def.CommonContentReq.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_HELPTIPS_SET',
                                                            param_name = 'CommonContentReq')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        helps = self.get_worker().get_app().get_mit_manager().rdm_find("HelpTips")
        if len(helps) == 1:                                    
            self.get_worker().get_app().get_mit_manager().rdm_remove(helps[0])
                    
        help_moc = self.get_worker().get_app().get_mit_manager().gen_rdm("HelpTips")
        help_moc.tips_id = 0
        help_moc.content = help_cfg.content

        ret = self.get_worker().get_app().get_mit_manager().rdm_add(help_moc)
        
        if ret.get_err_code() != 0:
            result.return_code = ret.get_err_code()
            result.description = ret.get_msg()
            
            result.prepare_for_ack(help_cfg, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        new_frame = bf.AppFrame()
        new_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_CONTENT_UPDATE_MSG)
        self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), new_frame)        

        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(help_cfg, result.return_code, result.description)

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


class PortalContentNewsIdUpdateHandler(bf.CmdHandler):
    """
    Class: PortalContentNewsIdUpdateHandler
    Description: 
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        article_id = int(frame.get_data())
        wx_news_id = frame.get_data(1)
        
        arts = self.get_worker().get_app().get_mit_manager().rdm_find("Article", article_id = article_id)
        if len(arts) == 0:
            tracelog.info('update article(%d) news id(%s), but the article does not exist in mit!' % (article_id, wx_news_id))
            return
        
        arts[0].wx_news_id = wx_news_id
        self.get_worker().get_app().get_mit_manager().rdm_mod(arts[0])

        tracelog.info('update article(id %d) to wx portal (news id %s) success!' % (article_id, wx_news_id))
        

class PortalContentArticlePushHandler(bf.CmdHandler):
    """
    Class: PortalContentArticlePushHandler
    Description: Portal下发的主题内容人工推送的命令handler
    Base: CmdHandler
    Others: 
    """


    def handle_cmd(self, frame):
        """
        Method:    handle_cmd
        Description: 处理主题内容人工推送的命令消息
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """
        tracelog.info(self)
        
        result = basic_rep_to_web.BasicRepToWeb()
        result.init_all_attr()
        tracelog.info('content man worker recv article push frame: %s' % frame)
        buf = frame.get_data()
        
        try:
            push_info = msg_params_def.PortalContentArticleSubscriberPush.deserialize(buf)
        except:
            result.return_code = err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_DESERIALIZE_ERROR,
                                                            cmd = 'PORTAL_CONTENT_ARTICLE_SUBSCRIBER_PUSH',
                                                            param_name = 'PortalContentArticleSubscriberPush')
            result.user_session = ''
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return

        articles = self.get_worker().get_app().get_mit_manager().lookup_attrs("Article",
                                                                              [
                                                                               'article_id',
                                                                               'wx_news_id',
                                                                               'group_ids'
                                                                               ],
                                                                              article_id = int(push_info.article_id))
        if len(articles) == 0:                                    
            result.return_code = err_code_mgr.ERR_PORTAL_ARTICLE_NOT_EXISTS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_ARTICLE_NOT_EXISTS)
            
            result.prepare_for_ack(push_info, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
        
        if len(articles[0][1]) == 0:
            result.return_code = err_code_mgr.ERR_PORTAL_ARTICLE_NOT_UPLOADED
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ERR_PORTAL_ARTICLE_NOT_UPLOADED)
            
            result.prepare_for_ack(push_info, result.return_code, result.description)
            self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))
            return
            
        # 构造推送消息发给SubscriberManApp，由它分发给各个订阅者
        push_msg = msg_params_def.CloudPortalArticlePushMessage()
        push_msg.init_all_attr()
        push_msg.article_id = articles[0][0]
        push_msg.wx_news_id = articles[0][1]
        
        subs = self.get_worker().get_app().get_mit_manager().lookup_attrs("Subscriber",
                                                                          [
                                                                           'subscriber_open_id',
                                                                           'group_ids'
                                                                           ])
        sub_map = {}
        for gid in articles[0][2].group_ids:
            for sub in subs:
                if gid in sub[1].group_ids:
                    sub_map[sub[0]] = True
        
        push_msg.sub_open_ids = sub_map.keys()            
        
        push_frame = bf.AppFrame()
        push_frame.set_cmd_code(cmd_code_def.CLOUD_PORTAL_ARTICLE_PUSH_MSG)
        push_frame.add_data(push_msg.serialize())
        self.get_worker().get_app().dispatch_frame_to_process_by_pid(self.get_worker().get_pid("SubscriberManApp"), push_frame)
        
        # 给WEB回成功响应
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)       
        result.prepare_for_ack(push_info, result.return_code, result.description)

        self.get_worker().get_app().send_ack_dispatch(frame, (result.serialize(), ))

        
class ContentConfigWorker(bf.CmdWorker):
    """
    Class: ContentConfigWorker
    Description: 内容管理线程worker类
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

        bf.CmdWorker.__init__(self, "ContentConfigWorker", min_task_id, max_task_id)
        
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

        self.register_handler(PortalContentArticleCreateHandler(), cmd_code_def.PORTAL_CONTENT_ARTICLE_CREATE)
        self.register_handler(PortalContentArticleModifyHandler(), cmd_code_def.PORTAL_CONTENT_ARTICLE_MODIFY)
        self.register_handler(PortalContentArticleRemoveHandler(), cmd_code_def.PORTAL_CONTENT_ARTICLE_REMOVE)
        self.register_handler(PortalContentArticleQueryHandler(),  cmd_code_def.PORTAL_CONTENT_ARTICLE_QUERY)

        self.register_handler(PortalContentSubjectCreateHandler(), cmd_code_def.PORTAL_CONTENT_SUBJECT_CREATE)
        self.register_handler(PortalContentSubjectModifyHandler(), cmd_code_def.PORTAL_CONTENT_SUBJECT_MODIFY)
        self.register_handler(PortalContentSubjectRemoveHandler(), cmd_code_def.PORTAL_CONTENT_SUBJECT_REMOVE)
        self.register_handler(PortalContentSubjectQueryHandler(),  cmd_code_def.PORTAL_CONTENT_SUBJECT_QUERY)

        self.register_handler(PortalContentHelpTipsSetHandler(),   cmd_code_def.PORTAL_CONTENT_HELPTIPS_SET)
        self.register_handler(PortalContentHelpTipsQueryHandler(), cmd_code_def.PORTAL_CONTENT_HELPTIPS_QUERY)
        
        self.register_handler(PortalContentArticlePushHandler(),   cmd_code_def.PORTAL_CONTENT_ARTICLE_SUBSCRIBER_PUSH)
        self.register_handler(PortalContentNewsIdUpdateHandler(),    cmd_code_def.CLOUD_PORTAL_NEWS_ID_UPDATE_MSG)
        return 0

