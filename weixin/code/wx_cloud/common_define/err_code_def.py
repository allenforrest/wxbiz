#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-06
Description: RFID��ϵͳ���д����붨��
Others:      
Key Class&Method List: 
        
History: 
1. Date:2012-09-06
   Author:ACP2013
   Modification:�½��ļ�
"""

import err_code_mgr

# ΢�Ź����˺���ƽ̨����������
WX_CLOUD_ERRCODE_BASE      = 0x01000000

# ΢��HTTP�ӿ�(PHP)����ƽ̨(Python)�ӿڴ���������
WX_ITF_ERRCODE_BASE      = WX_CLOUD_ERRCODE_BASE + 0x10000

# ����Portal�ӿ�(PHP)����ƽ̨(Python)�ӿڴ���������
PORTAL_ITF_ERRCODE_BASE  = WX_CLOUD_ERRCODE_BASE + 0x20000

# ��ƽ̨�ڲ�����������
CLOUD_INNER_ERRCODE_BASE = WX_CLOUD_ERRCODE_BASE + 0x30000

wx_gateway_error_defs = {}

wx_man_error_def = {}

portal_man_error_defs = {
                         "ERR_PORTAL_DESERIALIZE_ERROR": (PORTAL_ITF_ERRCODE_BASE + 0,
                                                         "������   %(cmd)s �Ĳ���  %(param_name)s Ϊ�Ƿ��ķ����л��ַ���",
                                                         "invalid string to deserialize from command %(cmd)s parameter  %(param_name)s"),
                               
                         "ERR_PORTAL_ARTICLE_RECORDS_FULL": (PORTAL_ITF_ERRCODE_BASE + 10,
                                                                 "����������Ŀ̫�࣬����ϵͳ���",
                                                                 "The article records are full"),
                         "ERR_PORTAL_ARTICLE_NOT_EXISTS": (PORTAL_ITF_ERRCODE_BASE + 11,
                                                                 "ָ�����������ݲ�����",
                                                                 "The specified article does not exist"),
                         "ERR_PORTAL_ARTICLE_NOT_UPLOADED": (PORTAL_ITF_ERRCODE_BASE + 12,
                                                                 "�����������ں�̨��δ������ɣ���ȴ�������",
                                                                 "The article you want to push has not been created in backgroud, please retry"),
                         "ERR_PORTAL_ARTICLE_PARAMS_INVALID": (PORTAL_ITF_ERRCODE_BASE + 13,
                                                                 "�������ݵı��⡢����ͼ�����Ĳ���Ϊ��",
                                                                 "The title, head picture and content of the article must be exist"),
                         "ERR_PORTAL_SUBJECT_NOT_EXISTS": (PORTAL_ITF_ERRCODE_BASE + 14,
                                                                 "ָ������Ŀ������",
                                                                 "The specified subject does not exist"),
                         
                         "ERR_PORTAL_GROUP_RECORDS_FULL": (PORTAL_ITF_ERRCODE_BASE + 20,
                                                                 "�����߷�����Ŀ̫�࣬����ϵͳ���",
                                                                 "The subscriber group records are full"),
                         "ERR_PORTAL_GROUP_NOT_EXISTS": (PORTAL_ITF_ERRCODE_BASE + 21,
                                                                 "ָ���Ķ����߷��鲻����",
                                                                 "The specified group does not exist"),
                         "ERR_PORTAL_GROUP_ASSOCIATED_BY_SUB": (PORTAL_ITF_ERRCODE_BASE + 22,
                                                                 "�ö����߷����Ѱ����˶����ߣ��޷�ֱ��ɾ��",
                                                                 "The specified group has been associated by subscribers"),
                         "ERR_PORTAL_SUBSCRIBER_NOT_EXISTS": (PORTAL_ITF_ERRCODE_BASE + 23,
                                                                 "ָ���Ķ����߲�����",
                                                                 "The specified subscriber does not exist"),
                         
                         "ERR_PORTAL_EVENT_RECORDS_FULL": (PORTAL_ITF_ERRCODE_BASE + 30,
                                                                 "�¼���Ŀ̫�࣬����ϵͳ���",
                                                                 "The event records are full"),
                         "ERR_PORTAL_EVENT_NOT_EXISTS": (PORTAL_ITF_ERRCODE_BASE + 31,
                                                                 "ָ�����¼�������",
                                                                 "The specified event does not exist"),

                         }


err_code_mgr.regist_errors(wx_gateway_error_defs)
err_code_mgr.regist_errors(wx_man_error_def)
err_code_mgr.regist_errors(portal_man_error_defs)

