#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-11
Description: ΢�Ź����˺���ƽ̨ �ӿ���Ϣ����
Others:      
Key Class&Method List: 
History: 
1. Date: 2013-05-11
   Author: Allen
   Modification: create
"""

import import_paths

import serializable_obj
import basic_rep_to_web
import type_def

LOCAL_HOST_DOMAIN = 'mshow.wx.viewiot.net'

###############################################################################################
"""
MSG_A_MILK = 'aptamil'
MSG_H_MILK = 'hipp'
MSG_ACK_KNOWN = 'ok'

LL_WX_INFO = ['oXnCzjgRMGKw_kZ5bpClTouSBycQ', '1968919201']
XWN_WX_INFO = ['oXnCzjrdxRpzySXYKFKhuCuTmIXo', '739542740']

ALL_MILK_OPENID = [LL_WX_INFO[0], XWN_WX_INFO[0]]

MILK_MAP = {MSG_A_MILK: [LL_WX_INFO, ],
            MSG_H_MILK: [XWN_WX_INFO, ]}
"""

###############################################################################################
#PORTAL_IMG_FILE_LOCAL_PATH_PREFIX = '/usr/local/apache/htdocs/weixinpublic/'
PORTAL_IMG_FILE_LOCAL_PATH_PREFIX = '/work/weixin_public/web/weixinpublic/'

PORTAL_IMG_FILE_SAVE_LOCAL_PATH = 'js/ueditor/php/upload/'
PORTAL_LOGO_IMG_FILE_LOCAL_PATH = 'js/ueditor/php/upload/logo.jpg'
WX_HEAD_IMG_FILE_SAVE_LOCAL_PATH = 'js/ueditor/php/upload/headimg/'

WX_MEMBER_MENU_CFG_ARTICLE_IMG_URL = 'js/ueditor/php/upload/menu.png'
WX_MEMBER_MBR_ASSOC_ARTICLE_IMG_URL = 'js/ueditor/php/upload/member.png'
WX_MEMBER_MENU_CFG_PORTAL_URL  = 'index.php/weixin/delivery/bookMenu/member_id/'
WX_MEMBER_MBR_ASSOC_PORTAL_URL = 'index.php/weixin/subscriber/userAssoMember/subscriber_open_id/'

PORTAL_CLOUD_IMAGE_UPLOAD_NEW = 'upload'
PORTAL_CLOUD_IMAGE_UPLOAD_MOD = 'modify'
PORTAL_CLOUD_IMAGE_UPLOAD_DEL = 'delete'

###############################################################################################
WX_MSG_TYPE_EVENT    = 'event'
WX_MSG_TYPE_TEXT     = 'text'
WX_MSG_TYPE_IMAGE    = 'image'
WX_MSG_TYPE_LOCATION = 'location'
WX_MSG_TYPE_LINK     = 'link'
WX_MSG_TYPE_NEWS     = 'news'
WX_MSG_TYPE_MUSIC    = 'music'

###############################################################################################
PORTAL_SUBJECT_TYPE_ALL = 'all'
PORTAL_TASK_PUSH_ARTICLE = 'article'
PORTAL_TASK_MEMBER_DAILY = 'member'

###############################################################################################

#WX_TXT_SUBSCRIBE_TIPS = """��ӭ���Ĺ�ע�����ǵ�%dλ�����ߡ�"""

WX_TXT_SUBSCRIBE_TITLE = """��ӭ���Ĺ�ע"""

WX_TXT_SUBSCRIBE_TIPS = """#%d#"""

WX_TXT_SUBJECT_TIPS = """
Ŀǰ��������Ŀ�����ģ�
%s
��������Ŀ�š� 
"""

WX_TXT_ERROR_INPUT = """�Բ������������Ŀ����Ч��"""

WX_TXT_INVALID_MEMBER = """�Բ�����������ũׯ��Ա�����߻�û�а󶨻�Ա�������롸��Ա�����л�Ա΢�Ű󶨡�"""

WX_TXT_NULL_SUBJECT = """����Ŀ���������ڽ����У������ڴ���"""

WX_TXT_WELCOME_SHARE = """��л���ķ����ͷ���"""

"""
ʹ�ð�����
1��ֱ��������Ŀ��Ų�����Ŀ�ڵ��������ݡ�
2��������Ѽ���ũׯ��Ա�������롸��Ա������΢�Ű󶨡�
3����Ա�������Ͳ˵���ѡ�������롸�˵������ɽ��б��ܲ˵���ѡ��
"""

WX_TXT_UNKNOWN_SUBSCRIBER = """�Բ������Ķ��ĳ����쳣��������ȡ����ע�������˺ţ�Ȼ�����¹�ע�����ɻָ����������������ʾǸ�⡣"""

PORTAL_TXT_MSG_SHARE_TXT_TITLE = """%s����%s��"""

PORTAL_TXT_MSG_SHARE_PIC_TITLE = """%s��ͼƬ���� """

PORTAL_TXT_MSG_SHARE_CONTENT = """����%s��%s����
%s
"""

PORTAL_TXT_MSG_SHARE_IMG = """����%s��ͼƬ����%s��"""

PORTAL_TXT_MENU_CFG_NOTIFY_TXT = """�𾴵�%s��Ա�����ţ�%s����
���ܲ�Ʒ�������ڣ�%s
�����롸�˵����������Ͳ˵���ѡ��
��ѡ��ֹ����Ϊ��������ǰ���졣"""

PORTAL_TXT_DELIVERY_EXPIRED_NOTIFY_TXT = """�𾴵�%s��Ա�����ţ�%s����
���Ļ�Ա����Ч���ڣ�%s
��Ʒ���ͷ��񼴽����ڣ���ӭ����ϵũׯ��ǩ��Ա��"""

PORTAL_TXT_DELIVERY_DIY_NOTIFY_TXT = """�𾴵�%s��Ա�����ţ�%s����
���ܲ�Ʒ�������ڣ�%s
��������ѡ�˲�Ʒ���������Ͳ˵����£�
%s
�����ڴ���
"""

PORTAL_TXT_DELIVERY_DEFAULT_NOTIFY_TXT = """�𾴵�%s��Ա�����ţ�%s����
���ܲ�Ʒ�������ڣ�%s
������û����ѡ��Ʒ��������ũׯ��Ϊ����ѡ�������˵��������ڴ���
"""

PORTAL_TXT_MENU_CFG_TITLE = """�������Ͳ˵���ѡ"""

PORTAL_TXT_MENU_CFG_DESCRIPTION = """�𾴵Ļ�Ա��������̬��Ʒ���ͼƻ���ʼ���������Ķ����ġ��������Ͳ˵���ѡ�� """

PORTAL_TXT_MBR_ASSOC_TITLE = """ũׯ��Ա΢����֤"""

PORTAL_TXT_MBR_ASSOC_DESCRIPTION = """�𾴵�΢���û���������Ѿ������������̬ũׯ�Ļ�Ա���ֲ��������ͨ��΢����֤��Ա�ţ�����ÿ�����Ͳ˵���ѡ�����������Ķ����ġ����л�Ա�󶨡� """

PORTAL_TXT_DEFAULT_MENU = """Ĭ�ϲ˵�"""

###############################################################################################
# �û������ķ����100��ʼ��1-99ΪϵͳԤ��
GROUP_SYS_DEFAULT = 1
GROUP_USERDEFINE_ID_BASE = 100

# �û������������100��ʼ��1-99ΪϵͳԤ��
ARTICLE_SYS_MENU_CFG = 1
ARTICLE_SYS_MEMBER_ASSOC = 2
ARTICLE_USERDEFINE_ID_BASE = 100

SUBJECT_SYS_INNER_DEF = 1 
SUBJECT_USERDEFINE_ID_BASE = 100

class GroupList(serializable_obj.JsonSerializableObj):
    """
    Class: GroupList
    Description: �����߷����б�
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_ids" : [type_def.TYPE_UINT32]
                    }


class CommonQueryReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: CommonQueryReq
    Description: ͨ�ò�ѯ����
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "num_per_page" : type_def.TYPE_INT32, # ��ѡ����
                    "current_page" : type_def.TYPE_INT32, # ��ѡ����
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

# WX_ACCESS_HTTP_POST_FORWARD:
# 1. ������Ϣ�ṹ��CommonContentReq
# 2. ��Ӧ��Ϣ�ṹ��CommonContentRsp
class CommonContentReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: WXAccessHttpPostReq
    Description: PHPת��΢�ŷ��ʺ�̨��POST��Ϣ
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "content": type_def.TYPE_STRING
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    

class CommonContentRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: WXAccessHttpPostReq
    Description: PHPת��΢�ŷ��ʺ�̨��POST��Ϣ
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "content": type_def.TYPE_STRING
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)


# PORTAL_SUBSCRIBER_MEMBER_ASSOCIATE:
# 1. ������Ϣ�ṹ��PortalSubscriberMemberAssociateReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalSubscriberMemberAssociateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberMemberAssociateReq
    Description: �˹����������ߺͻ�Ա
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # ������openID
                    "member_id": type_def.TYPE_STRING,          # ��ԱID
                    "name": type_def.TYPE_STRING,               # ��Ա����
                    "cellphone": type_def.TYPE_STRING           # ��ϵ��ʽ 
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_SUBSCRIBER_ADMIN_ASSOCIATE:
# 1. ������Ϣ�ṹ��PortalSubscriberAdminAssociateReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalSubscriberAdminAssociateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberAdminAssociateReq
    Description: �����߹���Ա�������
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # ������openID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
        

# PORTAL_SUBSCRIBER_INFO_QUERY:
# 1. ������Ϣ�ṹ��PortalSubscriberInfoQueryReq
# 2. ��Ӧ��Ϣ�ṹ��PortalSubscriberInfoQueryRsp
class Subscriber(serializable_obj.JsonSerializableObj):
    """
    Class: Subscriber
    Description: ��������Ϣ
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # ������openID(���治��ʾ)
                    "nickname": type_def.TYPE_STRING,           # �ǳ�
                    "weixin_id": type_def.TYPE_STRING,          # ΢�ź�
                    "gender": type_def.TYPE_STRING,             # �Ա�
                    "city": type_def.TYPE_STRING,               # ����
                    "group_ids": [type_def.TYPE_STRING],        # ����ID�б�
                    "member_flag": type_def.TYPE_BOOL,          # �Ƿ��Ѽ����Ա
                    "head_img": type_def.TYPE_STRING,           # ͷ��ͼƬ�ļ�
                    "admin_flag": type_def.TYPE_BOOL,           # �Ƿ��ǹ���Ա
                    "assoc_member_id": type_def.TYPE_STRING,    # �����Ļ�ԱID
                    "assoc_member_name": type_def.TYPE_STRING   # �����Ļ�Ա����
                   }

class PortalSubscriberInfoQueryReq(CommonQueryReq):
    """
    Class: PortalSubscriberInfoQueryReq
    Description: ��ѯ���ж�������Ϣ����
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_id": type_def.TYPE_STRING  # ����ID��Ϊ�����ѯ���ж����ߣ������շ����ѯ��
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)

    
class PortalSubscriberInfoQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalSubscriberInfoQueryRsp
    Description: ��ѯ���ж�������Ϣ��Ӧ
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # ����������
                    "subscribers": [Subscriber]     # �������б�
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)


# PORTAL_SUBSCRIBER_GROUP_CREATE:
# 1. ������Ϣ�ṹ��PortalSubscriberGroupCreateReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class Group(serializable_obj.JsonSerializableObj):
    """
    Class: Group
    Description: �����߷�����Ϣ
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_id": type_def.TYPE_STRING,       # ����ID(���治��ʾ)
                    "group_name": type_def.TYPE_STRING,     # ������
                    "group_sub_num": type_def.TYPE_UINT32,  # �����ڰ����Ķ���������
                    "description": type_def.TYPE_STRING     # ��������
                   }
    
class PortalSubscriberGroupCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberGroupCreateReq
    Description: ���������߷���
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_name": type_def.TYPE_STRING,  # ������
                    "description": type_def.TYPE_STRING  # ��������
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    

# PORTAL_SUBSCRIBER_GROUP_REMOVE:
# 1. ������Ϣ�ṹ��PortalSubscriberGroupRemoveReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalSubscriberGroupRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberGroupRemoveReq
    Description: ɾ�������߷���
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_id": type_def.TYPE_STRING    # ����ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_SUBSCRIBER_GROUP_MODIFY:
# 1. ������Ϣ�ṹ��PortalSubscriberGroupModifyReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalSubscriberGroupModifyReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberGroupModifyReq
    Description: �޸Ķ����߷���
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_id": type_def.TYPE_STRING,       # ����ID(���治��ʾ)
                    "group_name": type_def.TYPE_STRING,     # ������
                    "description": type_def.TYPE_STRING     # ��������
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_SUBSCRIBER_GROUP_QUERY:
# 1. ������Ϣ�ṹ��CommonQueryReq
# 2. ��Ӧ��Ϣ�ṹ��PortalSubscriberGroupQueryRsp
class PortalSubscriberGroupQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalSubscriberGroupModifyReq
    Description: �޸Ķ����߷���
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # ��������
                    "groups": [Group]               # �����б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)

# PORTAL_SUBSCRIBER_GROUP_ASSOCIATE:
# 1. ������Ϣ�ṹ��PortalSubscriberGroupAssociateReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalSubscriberGroupAssociateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberGroupAssociateReq
    Description: �����߼���Ⱥ��(����ͬʱ������Ⱥ��)
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # ������openID
                    "group_ids": [type_def.TYPE_STRING]         # ����ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_SUBSCRIBER_GROUP_MSG_PUSH:
# 1. ������Ϣ�ṹ��PortalSubscriberGroupMsgPushReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalSubscriberGroupMsgPushReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberGroupMsgPushReq
    Description: ��������ϢȺ��
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_ids": [type_def.TYPE_STRING],   # ����ID�б�
                    "text_msg": type_def.TYPE_STRING       # �ظ����ı���Ϣ
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    

# PORTAL_MEMBER_MEMBER_CREATE:
# 1. ������Ϣ�ṹ��PortalMemberMemberCreateModReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
# PORTAL_MEMBER_MEMBER_MODIFY:
# 1. ������Ϣ�ṹ��PortalMemberMemberCreateModReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class Member(serializable_obj.JsonSerializableObj):
    """
    Class: Member
    Description: ��Ա��Ϣ
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING,          # ��ԱID(���治��ʾ)
                    "name": type_def.TYPE_STRING,               # ����
                    "cellphone": type_def.TYPE_STRING,          # ��ϵ��ʽ
                    "weixin_id": type_def.TYPE_STRING,          # ΢�ź�
                    "delivery_addr": type_def.TYPE_STRING,      # ���͵�ַ
                    "delivery_time": type_def.TYPE_STRING,      # ����ʱ��
                    "delivery_expiry": type_def.TYPE_STRING,    # ���ͽ�ֹ���ڣ���Ч�ڣ�
                    "subscribe_flag": type_def.TYPE_BOOL,       # �Ƿ��Ѷ���
                    "nickname": type_def.TYPE_STRING,           # ΢���ǳ�
                   }
    
class PortalMemberMemberCreateModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMemberCreateModReq
    Description: ������Ա
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING,          # ��ԱID
                    "name": type_def.TYPE_STRING,               # ����
                    "cellphone": type_def.TYPE_STRING,          # ��ϵ��ʽ
                    "delivery_addr": type_def.TYPE_STRING,      # ���͵�ַ
                    "delivery_time": type_def.TYPE_STRING,      # ����ʱ��(1-7�����ڼ�)
                    "delivery_expiry": type_def.TYPE_STRING,    # ���ͽ�ֹ���ڣ���Ч�ڣ�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)



# PORTAL_MEMBER_MEMBER_REMOVE:
# 1. ������Ϣ�ṹ��PortalMemberMemberRemoveReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalMemberMemberRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMemberRemoveReq
    Description: ɾ����Ա
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING      # ��ԱID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

    
# PORTAL_MEMBER_MEMBER_QUERY:
# 1. ������Ϣ�ṹ��PortalMemberMemberQueryReq
# 2. ��Ӧ��Ϣ�ṹ��PortalMemberMemberQueryRsp
class PortalMemberMemberQueryReq(CommonQueryReq):
    """
    Class: PortalSubscriberInfoQueryReq
    Description: ��ѯ��Ա��Ϣ��Ӧ(���������Ϣ��num_per_page/current_pageΪ0�����ѯ���н��)
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING  # ��ԱID
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)


class PortalMemberMemberQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalMemberMemberQueryRsp
    Description: ��ѯ��Ա��Ϣ��Ӧ(���������Ϣ��num_per_page/current_pageΪ0�����ѯ���н��)
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # ��Ա����
                    "members": [Member]             # ��Ա�б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)


# PORTAL_DELIVERY_MEMBER_MENU_CFG:
# 1. ������Ϣ�ṹ��PortalDeliveryMemberMenuCfgReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalDeliveryMemberMenuCfgReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalDeliveryMemberMenuCfgReq
    Description: ���û�Ա�����Ͳ˵�
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING,      # ��ԱID
                    "vegetables": [type_def.TYPE_STRING]    # ��Ʒ�嵥(��ƷID�б�)
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_DELIVERY_VEGETABLE_CREATE:
# 1. ������Ϣ�ṹ��PortalDeliveryVegetableCreateReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb

class VegetableList(serializable_obj.JsonSerializableObj):
    """
    Class: VegetableList
    Description: ��Ʒ�б�
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "vegetables": [type_def.TYPE_STRING]    # ��Ʒ�嵥(��ƷID�б�)
                    }


class Vegetable(serializable_obj.JsonSerializableObj):
    """
    Class: Vegetable
    Description: ��Ʒ��Ϣ
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "v_id": type_def.TYPE_STRING,           # ��ƷID
                    "name": type_def.TYPE_STRING,           # ��Ʒ��
                    "description": type_def.TYPE_STRING     # ��Ʒ����
                   }

class PortalDeliveryVegetableCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalDeliveryVegetableCreateModReq
    Description: ������Ʒ
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "name": type_def.TYPE_STRING,           # ��Ʒ��
                    "description": type_def.TYPE_STRING     # ��Ʒ����
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_DELIVERY_VEGETABLE_MODIFY:
# 1. ������Ϣ�ṹ��PortalDeliveryVegetableModReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalDeliveryVegetableModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalDeliveryVegetableModReq
    Description: �޸Ĳ�Ʒ
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "v_id": type_def.TYPE_STRING,           # ��ƷID
                    "name": type_def.TYPE_STRING,           # ��Ʒ��
                    "description": type_def.TYPE_STRING     # ��Ʒ����
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_DELIVERY_VEGETABLE_REMOVE:
# 1. ������Ϣ�ṹ��PortalDeliveryVegetableRemoveReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalDeliveryVegetableRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalDeliveryVegetableRemoveReq
    Description: ɾ����Ʒ
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "v_id": type_def.TYPE_STRING           # ��ƷID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_DELIVERY_VEGETABLE_QUERY:
# 1. ������Ϣ�ṹ��PortalDeliveryVegetableQueryReq
# 2. ��Ӧ��Ϣ�ṹ��PortalDeliveryVegetableQueryRsp
class PortalDeliveryVegetableQueryReq(CommonQueryReq):
    """
    Class: PortalDeliveryVegetableQueryReq
    Description: ��ѯ��Ʒ��Ϣ����
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "v_id": type_def.TYPE_STRING    # ��ƷID
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)
    
class PortalDeliveryVegetableQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalDeliveryVegetableQueryRsp
    Description: ��ѯ��Ʒ��Ϣ��Ӧ
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # ��Ʒ����
                    "vegetables": [Vegetable]       # ��Ʒ�б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    

# PORTAL_DELIVERY_MENU_CREATE:
# 1. ������Ϣ�ṹ��PortalDeliveryMenuCreateModReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class Menu(serializable_obj.JsonSerializableObj):
    """
    Class: Menu
    Description: �˵���Ϣ
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "menu_id": type_def.TYPE_STRING,        # �˵�ID(���治��ʾ)
                    "name": type_def.TYPE_STRING,           # �˵���
                    "count": type_def.TYPE_INT32,           # �˵������Ĳ�Ʒ����
                    "vegetable": [type_def.TYPE_STRING]     # ��Ʒ�б�
                   }
    
class PortalMemberMenuCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMenuCreateReq
    Description: �����˵�
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "name": type_def.TYPE_STRING,           # �˵���
                    "content": type_def.TYPE_STRING         # �˵�����
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_MEMBER_MENU_MODIFY:
# 1. ������Ϣ�ṹ��PortalMemberMenuModReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb    
class PortalMemberMenuModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMenuModReq
    Description: �޸Ĳ˵�
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "menu_id": type_def.TYPE_STRING,        # �˵�ID(���治��ʾ)
                    "name": type_def.TYPE_STRING,           # �˵���
                    "content": type_def.TYPE_STRING         # �˵�����
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    

# PORTAL_MEMBER_MENU_REMOVE:
# 1. ������Ϣ�ṹ��PortalMemberMenuRemoveReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalMemberMenuRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMenuRemoveReq
    Description: ɾ���˵�
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "menu_id": type_def.TYPE_STRING      # �˵�ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

    
# PORTAL_MEMBER_MENU_QUERY:
# 1. ������Ϣ�ṹ��CommonQueryReq
# 2. ��Ӧ��Ϣ�ṹ��PortalMemberMenuQueryRsp
class PortalMemberMenuQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalMemberMenuQueryRsp
    Description: ��ѯ�˵���Ϣ��Ӧ
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # �˵�����
                    "menus": [Menu]                 # �˵��б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    
# PORTAL_DELIVERY_REPORT_QUERY:
# 1. ������Ϣ�ṹ��PortalDeliveryReportQueryReq
# 2. ��Ӧ��Ϣ�ṹ��PortalDeliveryReportQueryRsp
class DeliveryReport(serializable_obj.JsonSerializableObj):
    """
    Class: DeliveryReport
    Description: ���ͱ�����Ϣ
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING,          # ��ԱID
                    "name": type_def.TYPE_STRING,               # ��ʵ����
                    "cellphone": type_def.TYPE_STRING,          # ��ϵ��ʽ
                    "delivery_addr": type_def.TYPE_STRING,      # ���͵�ַ
                    "delivery_time": type_def.TYPE_STRING,      # ����ʱ��(�������͵�׼ȷ����)
                    "vegetables": [type_def.TYPE_STRING]        # ���Ͳ˵�(��Ʒ�����б�)
                   }
        
class PortalDeliveryReportQueryReq(CommonQueryReq):
    """
    Class: PortalDeliveryReportQueryReq
    Description: ��ѯ���ͱ�������
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING, # ��ԱID��Ϊ�����ѯ���л�Ա�����ͱ��棬�����ջ�Ա��ѯ��
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)
    
class PortalDeliveryReportQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalDeliveryReportQueryRsp
    Description: ��ѯ���ͱ�����Ӧ
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,           # ���ͱ�������
                    "delivery_reports": [DeliveryReport]    # ���ͱ����б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)

    
# PORTAL_CONTENT_HELPTIPS_SET:
# 1. ������Ϣ�ṹ��CommonContentReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
# PORTAL_CONTENT_HELPTIPS_QUERY
# 1. ������Ϣ�ṹ��basic_rep_to_web.BasicReqFromWeb
# 2. ��Ӧ��Ϣ�ṹ��CommonContentRsp


class Subject(serializable_obj.JsonSerializableObj):
    """
    Class: Subject
    Description: ������Ŀ��Ϣ
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subject_id": type_def.TYPE_STRING,  # ��ĿID
                    "name": type_def.TYPE_STRING,        # ��Ŀ��
                    "article_num": type_def.TYPE_UINT32, # ������������������
                    "description": type_def.TYPE_STRING  # ��Ŀ����
                   }

class Article(serializable_obj.JsonSerializableObj):
    """
    Class: Article
    Description: ����������Ϣ
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "article_id": type_def.TYPE_STRING,     # ��������ID(��ѯ���治��ʾ)
                    "title": type_def.TYPE_STRING,          # ����
                    "subject_id": type_def.TYPE_STRING,     # ��������ĿID
                    "description": type_def.TYPE_STRING,    # ����
                    "pic_url": type_def.TYPE_STRING,        # ����ͼURL
                    "content_url": type_def.TYPE_STRING,    # ��������URL
                    "content": type_def.TYPE_STRING,        # ��������(HTML)(��ѯ���治��ʾ)
                    "sub_group_ids": [type_def.TYPE_STRING],# �����߷���ID�б�
                    "push_timer": type_def.TYPE_STRING,     # ��ʱ����ʱ��
                    "push_times": type_def.TYPE_UINT16      # ��ʱ���ʹ���
                   }
    
# PORTAL_CONTENT_SUBJECT_CREATE��
# 1. ������Ϣ�ṹ��PortalContentSubjectCreateReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb    
class PortalContentSubjectCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMenuCreateReq
    Description: ����������Ŀ
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "name": type_def.TYPE_STRING,       # ��Ŀ��
                    "description": type_def.TYPE_STRING # ��Ŀ����
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_CONTENT_SUBJECT_MODIFY
# 1. ������Ϣ�ṹ��PortalContentSubjectModReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb    
class PortalContentSubjectModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentSubjectModReq
    Description: �޸�������Ŀ
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "subject_id": type_def.TYPE_STRING,  # ��ĿID
                    "name": type_def.TYPE_STRING,        # ��Ŀ��
                    "description": type_def.TYPE_STRING  # ��Ŀ����
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_CONTENT_SUBJECT_REMOVE:
# 1. ������Ϣ�ṹ��PortalContentSubjectRemoveReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalContentSubjectRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentSubjectRemoveReq
    Description: ɾ��������Ŀ
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "subject_id": type_def.TYPE_STRING, # ��ĿID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

# PORTAL_CONTENT_SUBJECT_QUERY:
# 1. ������Ϣ�ṹ��CommonQueryReq
# 2. ��Ӧ��Ϣ�ṹ��PortalContentSubjectQueryRsp
class PortalContentSubjectQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalContentSubjectQueryRsp
    Description: ��ѯ������Ŀ��Ӧ
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # ������Ŀ����
                    "subjects": [Subject]           # ������Ŀ�б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)


# PORTAL_CONTENT_ARTICLE_CREATE��
# 1. ������Ϣ�ṹ��PortalContentArticleCreateReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb    
class PortalContentArticleCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentArticleCreateReq
    Description: ������������
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "title": type_def.TYPE_STRING,          # ����
                    "subject_id": type_def.TYPE_STRING,     # ��������ĿID
                    "description": type_def.TYPE_STRING,    # ����
                    "pic_url": type_def.TYPE_STRING,        # ����ͼURL
                    "content_url": type_def.TYPE_STRING,    # ��������URL
                    "content": type_def.TYPE_STRING,        # ��������(HTML)
                    "sub_group_ids": [type_def.TYPE_STRING],# �����߷���ID�б�
                    "push_timer": type_def.TYPE_STRING,     # ��ʱ����ʱ�䣨��ѡ��
                    "push_times": type_def.TYPE_UINT16      # ��ʱ���ʹ�������ѡ��
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_CONTENT_ARTICLE_MODIFY
# 1. ������Ϣ�ṹ��PortalContentArticleModReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb    
class PortalContentArticleModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentArticleModReq
    Description: �޸���������
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "article_id": type_def.TYPE_STRING,     # ��������ID(��ѯ���治��ʾ)
                    "title": type_def.TYPE_STRING,          # ����
                    "subject_id": type_def.TYPE_STRING,     # ��������ĿID
                    "description": type_def.TYPE_STRING,    # ����
                    "pic_url": type_def.TYPE_STRING,        # ����ͼURL
                    "content_url": type_def.TYPE_STRING,    # ��������URL
                    "content": type_def.TYPE_STRING,        # ��������(HTML)(��ѯ���治��ʾ)
                    "sub_group_ids": [type_def.TYPE_STRING],# �����߷���ID�б�
                    "push_timer": type_def.TYPE_STRING,     # ��ʱ����ʱ��
                    "push_times": type_def.TYPE_UINT16      # ��ʱ���ʹ���
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_CONTENT_ARTICLE_REMOVE:
# 1. ������Ϣ�ṹ��PortalContentArticleRemoveReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalContentArticleRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentArticleRemoveReq
    Description: ɾ����������
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "article_id": type_def.TYPE_STRING     # ��������ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

    
# PORTAL_CONTENT_ARTICLE_QUERY:
# 1. ������Ϣ�ṹ��PortalContentArticleQueryReq
# 2. ��Ӧ��Ϣ�ṹ��PortalContentArticleQueryRsp
class PortalContentArticleQueryReq(CommonQueryReq):
    """
    Class: PortalContentArticleQueryReq
    Description: ��ѯ������Ŀ����
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "subject_id": type_def.TYPE_STRING, # ��ĿID��Ϊ�����ѯ�����������ݣ���������Ŀ��ѯ��
                    "article_id": type_def.TYPE_STRING, # ��������ID��Ϊ�����ѯ�����������ݣ������������ѯ��
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)
    
class PortalContentArticleQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalContentSubjectQueryReq
    Description: ��ѯ������Ŀ��Ӧ
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # ������Ŀ����
                    "articles": [Article]           # ������Ŀ�б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)

# PORTAL_CONTENT_ARTICLE_SUBSCRIBER_PUSH:
# 1. ������Ϣ�ṹ��PortalContentArticleSubscriberPush
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalContentArticleSubscriberPush(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentArticleSubscriberPush
    Description: �����������ݸ������߷���
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "article_id": type_def.TYPE_STRING     # ��������ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    


# PORTAL_CONTENT_KEYWORD_RULE_CREATE:
# PORTAL_CONTENT_KEYWORD_RULE_MODIFY: 
# 1. ������Ϣ�ṹ��PortalContentKeywordRuleCreateReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb

KEYWORD_RULE_MATCH_TYPE_TEXT = 'text'
KEYWORD_RULE_MATCH_TYPE_ARTICLE = 'article'

class Keyword(serializable_obj.JsonSerializableObj):
    """
    Class: KeyWord
    Description: �ؼ��ֲ���
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "keyword": type_def.TYPE_STRING,          # �ؼ���
                    "wholeword_match": type_def.TYPE_BOOL     # �Ƿ�ȫ��ƥ��
                   }

class KeywordRule(serializable_obj.JsonSerializableObj):
    """
    Class: KeywordRule
    Description: �ؼ���ƥ�����
    Base: JsonSerializableObj
    Others: 
    """
    
    __ATTR_DEF__ = {
                    "rule_id": type_def.TYPE_STRING,    # ����ID        
                    "rule_name": type_def.TYPE_STRING,  # ������
                    "keywords": [Keyword],              # �ؼ����б�
                    "match_type": type_def.TYPE_STRING, # ƥ�����ͣ��ı���Ϣ���������ݣ�
                    "contents": [type_def.TYPE_STRING]  # ���ݣ��ı���Ϣ���ݡ����������б�
                   }


class PortalContentKeywordRuleCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentKeywordRuleCreateModReq
    Description: �����ؼ���ƥ�����
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "rule_name": type_def.TYPE_STRING,  # ������
                    "keywords": [Keyword],              # �ؼ����б�
                    "match_type": type_def.TYPE_STRING, # ƥ�����ͣ��ı���Ϣ���������ݣ�
                    "contents": [type_def.TYPE_STRING]  # ���ݣ��ı���Ϣ���ݡ����������б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_CONTENT_KEYWORD_RULE_MODIFY: 
# 1. ������Ϣ�ṹ��PortalContentKeywordRuleModReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalContentKeywordRuleModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentKeywordRuleCreateModReq
    Description: �����ؼ���ƥ�����
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "rule_id": type_def.TYPE_STRING,    # ����ID        
                    "rule_name": type_def.TYPE_STRING,  # ������
                    "keywords": [Keyword],              # �ؼ����б�
                    "match_type": type_def.TYPE_STRING, # ƥ�����ͣ��ı���Ϣ���������ݣ�
                    "contents": [type_def.TYPE_STRING]  # ���ݣ��ı���Ϣ���ݡ����������б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_CONTENT_KEYWORD_RULE_REMOVE:
# 1. ������Ϣ�ṹ��PortalContentKeywordRuleRemoveReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
class PortalContentKeywordRuleRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentKeywordRuleRemoveReq
    Description: ɾ���ؼ���ƥ�����
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "rule_id": type_def.TYPE_STRING    # ����ID        
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_CONTENT_KEYWORD_RULE_QUERY:
# 1. ������Ϣ�ṹ��PortalContentKeywordRuleQueryReq
# 2. ��Ӧ��Ϣ�ṹ��PortalContentKeywordRuleQueryRsp
class PortalContentKeywordRuleQueryReq(CommonQueryReq):
    """
    Class: PortalContentKeywordRuleQueryReq
    Description: ��ѯ�ؼ��ֹ�������
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "rule_id": type_def.TYPE_STRING    # ����ID        
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)
    
class PortalContentKeywordRuleQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalContentKeywordRuleQueryRsp
    Description: ��ѯ�ؼ��ֹ�����Ӧ
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # ������
                    "rules": [KeywordRule]          # �����б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    

# PORTAL_EVENT_EVENT_REPORT:
# 1. ������Ϣ�ṹ��PortalEventEventReportReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicRepToWeb
EVENT_TYPE_SUBSCRIBE  = 'subscribe'  # �����¼�
EVENT_TYPE_MESSAGE    = 'message'    # ��������Ϣ�¼� 
EVENT_TYPE_DELIVERY   = 'delivery'   # ��Ա��Ʒ�����¼�
EVENT_TYPE_USERLOGIN  = 'login'      # �����û���¼�¼�
EVENT_TYPE_PORTALOPER = 'operation'  # ��̨��Ҫ�����¼�
EVENT_TYPE_MENUCFG    = 'menucfg'    # ��Ա�˵���ѡ�¼�

EVENT_PORTAL_OPERATION_ADD  = '����'
EVENT_PORTAL_OPERATION_MOD  = '�޸�'
EVENT_PORTAL_OPERATION_DEL  = 'ɾ��'
EVENT_PORTAL_OPERATION_PUSH = '����'

EVENT_PORTAL_OBJECT_SUBJECT   = '��Ŀ'
EVENT_PORTAL_OBJECT_ARTICLE   = '����'
EVENT_PORTAL_OBJECT_HELPTIPS  = '��ӭ��'
EVENT_PORTAL_OBJECT_MEMBER    = '��Ա'
EVENT_PORTAL_OBJECT_VEGETABLE = '��Ʒ'

class PortalEventEventReportReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalEventEventReportReq
    Description: �¼��ϱ���Ϣ
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "event_type": type_def.TYPE_STRING, # �¼�����
                    "content": type_def.TYPE_STRING     # �¼���ϸ��Ϣ����ͬ�¼����͵���ϢJSON����
                    }  
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_EVENT_EVENT_QUERY:
# 1. ������Ϣ�ṹ��PortalEventEventQueryReq
# 2. ��Ӧ��Ϣ�ṹ��PortalEventEventQueryRsp
class Event(serializable_obj.JsonSerializableObj):
    """
    Class: Event
    Description: ���ظ������ߵ�ÿ��Event����Ϣ
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "event_id": type_def.TYPE_STRING,   # �¼�ID 
                    "event_type": type_def.TYPE_STRING, # �¼�����
                    "content": type_def.TYPE_STRING,    # �¼���ϸ��Ϣ����ͬ�¼����͵���ϢJSON����
                    "read_flag": type_def.TYPE_BOOL     # �Ѷ���־
                    }    

class SubscribeEvent(serializable_obj.JsonSerializableObj):
    """
    Class: SubscribeEvent
    Description: �����¼�
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # ������openID(���治��ʾ)
                    "weixin_id": type_def.TYPE_STRING,          # ΢�ź�
                    "nickname": type_def.TYPE_STRING,           # �ǳ�
                    "action": type_def.TYPE_STRING,             # ���������ġ�ȡ�����ģ�
                    "time": type_def.TYPE_STRING                # ����
                    }

class SubscriberMessageEvent(serializable_obj.JsonSerializableObj):
    """
    Class: SubscriberMessageEvent
    Description: ��������Ϣ�¼�
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # ������openID(���治��ʾ)
                    "weixin_id": type_def.TYPE_STRING,          # ΢�ź�
                    "nickname": type_def.TYPE_STRING,           # �ǳ�
                    "member_id": type_def.TYPE_STRING,          # ��ԱID
                    "name": type_def.TYPE_STRING,               # ����
                    "text_msg": type_def.TYPE_STRING,           # �ı���Ϣ
                    "pic_url": type_def.TYPE_STRING,            # ͼƬ��ϢURL
                    "time": type_def.TYPE_STRING                # ����
                    }

class DeliveryNotificationEvent(serializable_obj.JsonSerializableObj):
    """
    Class: DeliveryNotificationEvent
    Description: ����֪ͨ�¼�
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # ������openID(���治��ʾ)
                    "weixin_id": type_def.TYPE_STRING,          # ΢�ź�
                    "nickname": type_def.TYPE_STRING,           # �ǳ�
                    "member_id": type_def.TYPE_STRING,          # ��ԱID
                    "name": type_def.TYPE_STRING,               # ����
                    "delivery_menu": type_def.TYPE_STRING,      # ���Ͳ˵���
                    "delivery_time": type_def.TYPE_STRING       # ����ʱ��
                    }

class UserLoginEvent(serializable_obj.JsonSerializableObj):
    """
    Class: UserLoginEvent
    Description: �û���¼�¼�
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "user_id": type_def.TYPE_STRING,    # �û���
                    "login_time": type_def.TYPE_STRING  # ��¼ʱ��
                    }
    

class PortalOperEvent(serializable_obj.JsonSerializableObj):
    """
    Class: PortalOperEvent
    Description: Portal��Ҫ�����¼�
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "user_id": type_def.TYPE_STRING,    # �û���
                    "oper_time": type_def.TYPE_STRING,  # ����ʱ��
                    "oper_type": type_def.TYPE_STRING,  # �������
                    "content": type_def.TYPE_STRING     # ��������
                    } 


class MemberConfigMenuEvent(serializable_obj.JsonSerializableObj):
    """
    Class: MemberConfigMenuEvent
    Description: ��Ա��ѡ�˵��¼�
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # ������openID(���治��ʾ)
                    "weixin_id": type_def.TYPE_STRING,          # ΢�ź�
                    "nickname": type_def.TYPE_STRING,           # �ǳ�
                    "member_id": type_def.TYPE_STRING,          # ��ԱID
                    "name": type_def.TYPE_STRING,               # ����
                    "menu": type_def.TYPE_STRING,               # ��ѡ�˵�(�ı�)
                    "time": type_def.TYPE_STRING                # ����(�ı�)
                    }       

class PortalEventEventQueryReq(CommonQueryReq):
    """
    Class: PortalEventEventQueryReq
    Description: ��ѯ�¼�����
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "event_type": type_def.TYPE_STRING  # �¼����ͣ�Ϊ�����ѯ�����¼����������¼����Ͳ�ѯ��
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)

        
class PortalEventEventQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalEventEventQueryRsp
    Description: ��ѯ�¼���Ӧ
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # �¼�����
                    "events": [Event]               # �¼��б�
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)

# PORTAL_EVENT_UNREAD_QUERY:
# 1. ������Ϣ�ṹ��basic_rep_to_web.BasicReqFromWeb
# 2. ��Ӧ��Ϣ�ṹ��PortalEventUnreadQueryRsp

class EventNum(serializable_obj.JsonSerializableObj):
    __ATTR_DEF__ = {
                    "event_type": type_def.TYPE_STRING,  # �¼�����
                    "num": type_def.TYPE_INT32           # �¼�����
                   }    

class PortalEventUnreadQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalEventUnreadQueryRsp
    Description: ��ѯδ���¼�������Ӧ
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,          # �¼�������(ĿǰΪ5��
                    'event_unread_nums': [EventNum]
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)


# PORTAL_EVENT_READ_NOTIFY:
# 1. ������Ϣ�ṹ��PortalEventReadNotifyReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicReqToWeb
class PortalEventReadNotifyReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalEventReadNotifyReq
    Description: �¼��Ѷ�֪ͨ
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "event_id": type_def.TYPE_STRING   # �¼�ID 
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_EVENT_MESSAGE_REPLY:
# 1. ������Ϣ�ṹ��PortalEventMessageReplyReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicReqToWeb
class PortalEventMessageReplyReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalEventMessageReplyReq
    Description: ��������Ϣֱ�ӻظ�
    Base: BasicReqFromWeb
    Others: 
    """
    __ATTR_DEF__ = {
                    "event_id": type_def.TYPE_STRING,   # �¼�ID 
                    "text_msg": type_def.TYPE_STRING    # �ظ����ı���Ϣ
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)    


# PORTAL_EVENT_MESSAGE_SHARE:
# 1. ������Ϣ�ṹ��PortalEventMessageShareReq
# 2. ��Ӧ��Ϣ�ṹ��basic_rep_to_web.BasicReqToWeb
class PortalEventMessageShareReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalEventMessageShareReq
    Description: ��������Ϣ����ָ����Ŀ
    Base: BasicReqFromWeb
    Others: 
    """
    __ATTR_DEF__ = {
                    "event_id": type_def.TYPE_STRING,           # ��������¼�ID 
                    'subject_id': type_def.TYPE_STRING          # ��������ĿID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)  
    

# PORTAL_EVENT_DAILY_STATS:
# 1. ������Ϣ�ṹ��basic_rep_to_web.BasicReqFromWeb
# 2. ��Ӧ��Ϣ�ṹ��PortalEventDailyStatsRsp
class PortalEventDailyStatsRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalEventMessageShareReq
    Description: ��������Ϣ����ָ����Ŀ
    Base: BasicReqFromWeb
    Others: 
    """
    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,          # �¼�������(ĿǰΪ5��
                    'event_daily_nums': [EventNum]
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    

##############################################################################
    
class WXMessage(serializable_obj.JsonSerializableObj):
    """
    Class: WXMessage
    Description: ΢����Ϣ����
    Base: BsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # ������openID
                    "public_account_id": type_def.TYPE_STRING,  # �����˺�ID
                    "create_time": type_def.TYPE_STRING,        # ��Ϣ����ʱ��
                    "msg_type": type_def.TYPE_STRING            # ��Ϣ����
                    }

class WXPushTextMessage(WXMessage):
    """
    Class: WXPushTextMessage
    Description: ΢���ı���Ϣ
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "content": type_def.TYPE_STRING,    # ��Ϣ����
                    "msg_id": type_def.TYPE_STRING      # ��ϢID
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)
    
          
class WXPushImageMessage(WXMessage):
    """
    Class: WXPushImageMessage
    Description: ΢��ͼƬ��Ϣ
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "pic_url": type_def.TYPE_STRING,    # ͼƬURL
                    "msg_id": type_def.TYPE_STRING      # ��ϢID
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)
    

class WXPushLocationMessage(WXMessage):
    """
    Class: WXPushLocationMessage
    Description: ΢�ŵ���λ����Ϣ
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "location_x": type_def.TYPE_STRING, # ����λ��γ��
                    "location_y": type_def.TYPE_STRING, # ����λ�þ���
                    "scale": type_def.TYPE_STRING,      # ��ͼ���Ŵ�С
                    "label": type_def.TYPE_STRING,      # ����λ����Ϣ
                    "msg_id": type_def.TYPE_STRING      # ��ϢID
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)

class WXPushLinkMessage(WXMessage):
    """
    Class: WXPushLinkMessage
    Description: ΢��������Ϣ
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "title": type_def.TYPE_STRING,      # ��Ϣ����
                    "description": type_def.TYPE_STRING,# ��Ϣ����
                    "url": type_def.TYPE_STRING,        # ��Ϣ����
                    "msg_id": type_def.TYPE_STRING      # ��ϢID
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)


WX_EVENT_TYPE_SUBSCRIBE = 'subscribe'
WX_EVENT_TYPE_UNSUBSCRIBE = 'unsubscribe'
WX_EVENT_TYPE_CLICK = 'CLICK'

class WXPushEventMessage(WXMessage):
    """
    Class: WXPushEventMessage
    Description: ΢��֪ͨ�¼�
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "event": type_def.TYPE_STRING,      # �¼�����
                    "event_key": type_def.TYPE_STRING   # �¼�KEYֵ
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)

class WXReplyTextMessage(WXMessage):
    """
    Class: WXReplyTextMessage
    Description: ΢���ı���Ϣ��Ӧ
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "content": type_def.TYPE_STRING,    # ��Ϣ����
                    "func_flag": type_def.TYPE_STRING   # �Ǳ��־
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)

class WXReplyMusicMessage(WXMessage):
    """
    Class: WXReplyMusicMessage
    Description: ΢��������Ϣ��Ӧ
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "title": type_def.TYPE_STRING,          # ������Ϣ����
                    "description": type_def.TYPE_STRING,    # ������Ϣ����
                    "music_url": type_def.TYPE_STRING,      # ��������
                    "hq_music_url": type_def.TYPE_STRING,   # ��������������
                    "func_flag": type_def.TYPE_STRING       # �Ǳ��־
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)

class WXArticle(serializable_obj.JsonSerializableObj):
    """
    Class: WXArticle
    Description: ΢��ͼ����Ϣ����
    Base: BsonSerializableObj
    Others: 
    """
    __ATTR_DEF__ = {
                    "title": type_def.TYPE_STRING,      # ͼ����Ϣ����
                    "description": type_def.TYPE_STRING,# ͼ����Ϣ����
                    "pic_url": type_def.TYPE_STRING,    # ͼƬ����
                    "url": type_def.TYPE_STRING         # ���ͼ����Ϣ��ת����
                    }
        
class WXReplyNewsMessage(WXMessage):
    """
    Class: WXReplyNewsMessage
    Description: ΢��ͼ����Ϣ��Ӧ
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "article_count": type_def.TYPE_UINT32,       # ͼ����Ϣ����
                    "articles": [WXArticle],                # ͼ����Ϣ�б�
                    "func_flag": type_def.TYPE_STRING       # �Ǳ��־
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)
    

# CLOUD_PORTAL_ARTICLE_PUSH_MSG��
class CloudPortalArticlePushMessage(serializable_obj.JsonSerializableObj):
    """
    Class: CloudPortalArticlePushMessage
    Description: ��������������Ϣ
    Base: BsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "article_id": type_def.TYPE_UINT32,     # ����ID
                    "wx_news_id": type_def.TYPE_STRING,     # ΢��ͼ����ϢID
                    "sub_open_ids": [type_def.TYPE_STRING]  # ���Ͷ������б�
                   }
    
# CLOUD_PORTAL_TEXT_PUSH_MSG
class CloudPortalTextPushMessage(serializable_obj.JsonSerializableObj):
    """
    Class: CloudPortalTextPushMessage
    Description: �ı���Ϣ������Ϣ(֧������)
    Base: BsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_ids": [type_def.TYPE_STRING], # ������openID�б�
                    "text_msg": type_def.TYPE_STRING               # �ظ����ı���Ϣ
                   }

