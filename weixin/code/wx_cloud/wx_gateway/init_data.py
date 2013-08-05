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
   Modification:�½��ļ�
"""

import import_paths
    
import mit

import msg_params_def

from moc_wx import Article, Group, HelpTips, Subject, Member, Group, WXBizInfo

if __name__=='__main__':
    
    mit_manager = mit.Mit()
    mit_manager.regist_moc(Article.Article, Article.ArticleRule)
    mit_manager.regist_moc(Group.Group, Group.GroupRule)
    mit_manager.regist_moc(HelpTips.HelpTips, HelpTips.HelpTipsRule)
    mit_manager.regist_moc(Subject.Subject, Subject.SubjectRule)
    mit_manager.regist_moc(Member.Member, Member.MemberRule)
    mit_manager.regist_moc(Group.Group, Group.GroupRule)
    mit_manager.regist_moc(WXBizInfo.WXBizInfo, WXBizInfo.WXBizInfoRule)
    
    mit_manager.open_sqlite("../../data/sqlite/wx_cloud.db")

    bizs = mit_manager.rdm_find('WXBizInfo', biz_id = 0)
    if len(bizs) == 0:
        biz_rdm = mit_manager.gen_rdm('WXBizInfo')
        biz_rdm.biz_id = 0
        biz_rdm.access_token = 'liuhaiqing'
        biz_rdm.login_user = 'allenxu@gmail.com'
        biz_rdm.login_pwd = 'Xuweinan812185'
        biz_rdm.auto_ip_update = 'True'
        mit_manager.rdm_add(biz_rdm)
        print('init the WX Biz info succ.')
    

