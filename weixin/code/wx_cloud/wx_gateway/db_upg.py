#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-08
Description: 
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:2012-11-08
   Author:ACP2013
   Modification:新建文件
"""

import import_paths
    
import mit

import msg_params_def

from moc_wx import Article as wx_article #
from moc_wx import Event as wx_event #
from moc_wx import Group as wx_group 
from moc_wx import HelpTips as wx_helptips
from moc_wx import Subject as wx_subject #
from moc_wx import Member as wx_member
from moc_wx import Subscriber as wx_subscriber #
from moc_wx import WXBizInfo as wx_bizinfo

from moc_wx_old import Article as wxo_article
from moc_wx_old import Event as wxo_event
from moc_wx_old import Group as wxo_group
from moc_wx_old import HelpTips as wxo_helptips
from moc_wx_old import Subject as wxo_subject
from moc_wx_old import Member as wxo_member
from moc_wx_old import Subscriber as wxo_subscriber
from moc_wx_old import WXBizInfo as wxo_bizinfo

if __name__=='__main__':
    
    old_mit = mit.Mit()
    old_mit.regist_moc(wxo_article.Article, wxo_article.ArticleRule)
    old_mit.regist_moc(wxo_event.Event, wxo_event.EventRule)
    old_mit.regist_moc(wxo_group.Group, wxo_group.GroupRule)
    old_mit.regist_moc(wxo_helptips.HelpTips, wxo_helptips.HelpTipsRule)
    old_mit.regist_moc(wxo_subject.Subject, wxo_subject.SubjectRule)
    old_mit.regist_moc(wxo_member.Member, wxo_member.MemberRule)
    old_mit.regist_moc(wxo_subscriber.Subscriber, wxo_subscriber.SubscriberRule)
    old_mit.regist_moc(wxo_bizinfo.WXBizInfo, wxo_bizinfo.WXBizInfoRule)
    old_mit.regist_complex_attr_type(msg_params_def.GroupList)
    old_mit.regist_complex_attr_type(msg_params_def.VegetableList)
    
    old_mit.open_sqlite("../../data/sqlite/old_wx_cloud.db")

    new_mit = mit.Mit()
    new_mit.regist_moc(wx_article.Article, wx_article.ArticleRule)
    new_mit.regist_moc(wx_group.Group, wx_group.GroupRule)
    new_mit.regist_moc(wx_helptips.HelpTips, wx_helptips.HelpTipsRule)
    new_mit.regist_moc(wx_subject.Subject, wx_subject.SubjectRule)
    new_mit.regist_moc(wx_member.Member, wx_member.MemberRule)
    new_mit.regist_moc(wx_subscriber.Subscriber, wx_subscriber.SubscriberRule)
    new_mit.regist_moc(wx_bizinfo.WXBizInfo, wx_bizinfo.WXBizInfoRule)
    new_mit.regist_complex_attr_type(msg_params_def.GroupList)
    new_mit.regist_complex_attr_type(msg_params_def.VegetableList)

    new_mit.open_sqlite("../../data/sqlite/wx_cloud.db")

    evt_mit = mit.Mit()
    evt_mit.regist_moc(wx_event.Event, wx_event.EventRule)
    evt_mit.open_sqlite("../../data/sqlite/wx_event.db")

    old_arts = old_mit.rdm_find('Article')
    for old_art in old_arts:
        old_id = old_art.article_id
        grps = old_mit.lookup_attrs('Article', ['group_ids'], article_id = old_id)
        old_art.article_id = old_id + msg_params_def.ARTICLE_USERDEFINE_ID_BASE
        old_art.subject_id = old_art.subject_id + msg_params_def.SUBJECT_USERDEFINE_ID_BASE
        url = old_art.content_url
        pos = url.find('articleId/') + len('articleId/')
        new_url = url[:pos] + str(old_art.article_id)
        old_art.content_url = new_url
        r = new_mit.rdm_add(old_art)
        moid = new_mit.gen_moid('Article', article_id = old_art.article_id)
        rr = new_mit.mod_complex_attr('Article', moid = moid, group_ids = grps[0][0])
        
        if rr.get_err_code() == 0 and r.get_err_code() == 0:
            print "Article table upgrade: article_id %d, new id %d success." % (old_id, old_art.article_id)
        else:
            print "Article table upgrade: article_id %d, new id %d failed." % (old_id, old_art.article_id)
        

    evts = old_mit.rdm_find('Event')
    for evt in evts:
        new_evt = evt_mit.gen_rdm("Event")
        new_evt.event_id = evt.event_id
        new_evt.event_type = evt.event_type
        new_evt.content = evt.content
        new_evt.date = '2013-07-21'
        new_evt.read_flag = evt.read_flag
        r = evt_mit.rdm_add(new_evt)
        if r.get_err_code() == 0:
            print "Event table upgrade: event_id %d success." % (evt.event_id)
        else:
            print "Event table upgrade: event_id %d failed." % (evt.event_id)

    grps = old_mit.rdm_find('Group')
    for grp in grps:
        r = new_mit.rdm_add(grp)
        if r.get_err_code() == 0:
            print "Group table upgrade: group_id %d success." % (grp.group_id)
        else:
            print "Group table upgrade: group_id %d failed." % (grp.group_id)

    grps = old_mit.rdm_find('HelpTips')
    for grp in grps:
        r = new_mit.rdm_add(grp)
        if r.get_err_code() == 0:
            print "HelpTips table upgrade: tips_id %d success." % (grp.tips_id)
        else:
            print "HelpTips table upgrade: tips_id %d failed." % (grp.tips_id)    

    grps = old_mit.rdm_find('Subject')
    for grp in grps:
        old_id = grp.subject_id
        grp.subject_id = old_id + msg_params_def.SUBJECT_USERDEFINE_ID_BASE
        r = new_mit.rdm_add(grp)
        if r.get_err_code() == 0:
            print "Subject table upgrade: subject_id %d, new id %d success." % (old_id, grp.subject_id)
        else:
            print "Subject table upgrade: subject_id %d, new id %d failed." % (old_id, grp.subject_id)             

    old_subs = old_mit.rdm_find('Subscriber')
    for old_sub in old_subs:
        grps = old_mit.lookup_attrs('Subscriber', ['group_ids'], subscriber_open_id = old_sub.subscriber_open_id)
        
        new_sub = new_mit.gen_rdm("Subscriber")
        new_sub.subscriber_open_id = old_sub.subscriber_open_id
        new_sub.subscribe_seq_no = old_sub.subscribe_seq_no
        new_sub.fake_id = old_sub.fake_id
        new_sub.weixin_id = old_sub.weixin_id
        new_sub.nickname = old_sub.nickname
        new_sub.gender = old_sub.gender
        new_sub.city = old_sub.city
        new_sub.sub_time = old_sub.sub_time
        new_sub.assoc_member_id = old_sub.assoc_member_id
        new_sub.admin_flag = 'False'
        
        r = new_mit.rdm_add(new_sub)
        moid = new_mit.gen_moid('Subscriber', subscriber_open_id = new_sub.subscriber_open_id)
        rr = new_mit.mod_complex_attr('Subscriber', moid = moid, group_ids = grps[0][0])
        
        if rr.get_err_code() == 0 and r.get_err_code() == 0:
            print "Subscriber table upgrade: subscriber_open_id %s success." % (new_sub.subscriber_open_id)
        else:
            print "Subscriber table upgrade: subscriber_open_id %s failed." % (new_sub.subscriber_open_id)
            

    old_infos = old_mit.rdm_find('WXBizInfo')
    for old_info in old_infos:
        r = new_mit.rdm_add(old_info)
        if r.get_err_code() == 0:
            print "WXBizInfo table upgrade: biz_id %d success." % (old_info.biz_id)
        else:
            print "WXBizInfo table upgrade: biz_id %d failed." % (old_info.biz_id)
    
