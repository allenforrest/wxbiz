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

from moc_wx import Article, Group, HelpTips, Subject, Member, Group, WXBizInfo, Subscriber, Delivery

if __name__=='__main__':
    
    mit_manager = mit.Mit()
    mit_manager.regist_moc(Article.Article, Article.ArticleRule)
    mit_manager.regist_moc(Group.Group, Group.GroupRule)
    mit_manager.regist_moc(HelpTips.HelpTips, HelpTips.HelpTipsRule)
    mit_manager.regist_moc(Subject.Subject, Subject.SubjectRule)
    mit_manager.regist_moc(Member.Member, Member.MemberRule)
    mit_manager.regist_moc(Group.Group, Group.GroupRule)
    mit_manager.regist_moc(WXBizInfo.WXBizInfo, WXBizInfo.WXBizInfoRule)
    mit_manager.regist_moc(Subscriber.Subscriber, Subscriber.SubscriberRule)
    mit_manager.regist_moc(Delivery.Delivery, Delivery.DeliveryRule)
    
    mit_manager.open_sqlite("../../data/sqlite/wx_cloud.db")
    """
    bizs = mit_manager.rdm_find('WXBizInfo', biz_id = 0)
    if len(bizs) == 0:
        biz_rdm = mit_manager.gen_rdm('WXBizInfo')
        biz_rdm.biz_id = 0
        biz_rdm.access_token = 'liuhaiqing'
        biz_rdm.login_user = 'allenxu@gmail.com'
        biz_rdm.login_pwd = 'Xuweinan812185'
        mit_manager.rdm_add(biz_rdm)
        print('init the WX Biz info succ.')
    
    ungroup_subs = mit_manager.rdm_find('Group', group_id = msg_params_def.SUBSCRIBER_DEFAULT_GROUP)
    if len(ungroup_subs) == 0:
        grp_rdm = mit_manager.gen_rdm('Group')
        grp_rdm.group_id = msg_params_def.SUBSCRIBER_DEFAULT_GROUP
        grp_rdm.group_name = '未分组'.decode('gbk').encode('utf-8')
        grp_rdm.description = '默认'.decode('gbk').encode('utf-8')
        mit_manager.rdm_add(grp_rdm)
        print('init the default group(ungroup) succ.')

    subjects = mit_manager.rdm_find('Subject', subject_id = 0)
    if len(subjects) == 0:
        subject_rdm = mit_manager.gen_rdm('Subject')
        subject_rdm.subject_id = 0
        subject_rdm.name = 'trigger'
        subject_rdm.description = ''
        mit_manager.rdm_add(subject_rdm)
        print('init the trigger subject succ.')

    """
    r = mit_manager.rdm_find('Delivery')
    for rec in r:
        print rec.delivery_id, type(rec.modify_flag)
        #mit_manager.rdm_remove(rec)
