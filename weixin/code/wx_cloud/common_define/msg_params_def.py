#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-05-11
Description: 微信公共账号云平台 接口消息定义
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

#WX_TXT_SUBSCRIBE_TIPS = """欢迎您的关注，您是第%d位订阅者。"""

WX_TXT_SUBSCRIBE_TITLE = """欢迎您的关注"""

WX_TXT_SUBSCRIBE_TIPS = """#%d#"""

WX_TXT_SUBJECT_TIPS = """
目前有如下栏目供查阅：
%s
请输入栏目号。 
"""

WX_TXT_ERROR_INPUT = """对不起，您输入的栏目号无效。"""

WX_TXT_INVALID_MEMBER = """对不起，您还不是农庄会员，或者还没有绑定会员，请输入「会员」进行会员微信绑定。"""

WX_TXT_NULL_SUBJECT = """该栏目的内容正在建设中，敬请期待。"""

WX_TXT_WELCOME_SHARE = """感谢您的反馈和分享。"""

"""
使用帮助：
1、直接输入栏目编号查阅栏目内的新鲜内容。
2、如果您已加入农庄会员，请输入「会员」进行微信绑定。
3、会员享受配送菜单自选服务，输入「菜单」即可进行本周菜单自选。
"""

WX_TXT_UNKNOWN_SUBSCRIBER = """对不起，您的订阅出现异常，请您先取消关注本公众账号，然后重新关注，即可恢复，给您带来不便表示歉意。"""

PORTAL_TXT_MSG_SHARE_TXT_TITLE = """%s：「%s」"""

PORTAL_TXT_MSG_SHARE_PIC_TITLE = """%s的图片分享 """

PORTAL_TXT_MSG_SHARE_CONTENT = """来自%s（%s）：
%s
"""

PORTAL_TXT_MSG_SHARE_IMG = """来自%s的图片分享（%s）"""

PORTAL_TXT_MENU_CFG_NOTIFY_TXT = """尊敬的%s会员（卡号：%s）：
本周菜品配送日期：%s
请输入「菜单」进行配送菜单自选。
自选截止日期为配送日期前两天。"""

PORTAL_TXT_DELIVERY_EXPIRED_NOTIFY_TXT = """尊敬的%s会员（卡号：%s）：
您的会员卡有效日期：%s
菜品配送服务即将到期，欢迎您联系农庄续签会员。"""

PORTAL_TXT_DELIVERY_DIY_NOTIFY_TXT = """尊敬的%s会员（卡号：%s）：
本周菜品配送日期：%s
本周您自选了菜品，您的配送菜单如下：
%s
敬请期待。
"""

PORTAL_TXT_DELIVERY_DEFAULT_NOTIFY_TXT = """尊敬的%s会员（卡号：%s）：
本周菜品配送日期：%s
本周您没有自选菜品，半日闲农庄将为您精选合理搭配菜单，敬请期待。
"""

PORTAL_TXT_MENU_CFG_TITLE = """本周配送菜单自选"""

PORTAL_TXT_MENU_CFG_DESCRIPTION = """尊敬的会员，本周生态菜品配送计划开始，请点击“阅读正文”进行配送菜单自选。 """

PORTAL_TXT_MBR_ASSOC_TITLE = """农庄会员微信认证"""

PORTAL_TXT_MBR_ASSOC_DESCRIPTION = """尊敬的微信用户，如果您已经加入半日闲生态农庄的会员俱乐部，请务必通过微信认证会员号，享受每周配送菜单自选服务。请点击“阅读正文”进行会员绑定。 """

PORTAL_TXT_DEFAULT_MENU = """默认菜单"""

###############################################################################################
# 用户创建的分组从100起始，1-99为系统预留
GROUP_SYS_DEFAULT = 1
GROUP_USERDEFINE_ID_BASE = 100

# 用户创建的主题从100起始，1-99为系统预留
ARTICLE_SYS_MENU_CFG = 1
ARTICLE_SYS_MEMBER_ASSOC = 2
ARTICLE_USERDEFINE_ID_BASE = 100

SUBJECT_SYS_INNER_DEF = 1 
SUBJECT_USERDEFINE_ID_BASE = 100

class GroupList(serializable_obj.JsonSerializableObj):
    """
    Class: GroupList
    Description: 订阅者分组列表
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_ids" : [type_def.TYPE_UINT32]
                    }


class CommonQueryReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: CommonQueryReq
    Description: 通用查询请求
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "num_per_page" : type_def.TYPE_INT32, # 可选参数
                    "current_page" : type_def.TYPE_INT32, # 可选参数
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

# WX_ACCESS_HTTP_POST_FORWARD:
# 1. 请求消息结构：CommonContentReq
# 2. 响应消息结构：CommonContentRsp
class CommonContentReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: WXAccessHttpPostReq
    Description: PHP转发微信访问后台的POST消息
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
    Description: PHP转发微信访问后台的POST消息
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "content": type_def.TYPE_STRING
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)


# PORTAL_SUBSCRIBER_MEMBER_ASSOCIATE:
# 1. 请求消息结构：PortalSubscriberMemberAssociateReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalSubscriberMemberAssociateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberMemberAssociateReq
    Description: 人工关联订阅者和会员
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # 订阅者openID
                    "member_id": type_def.TYPE_STRING,          # 会员ID
                    "name": type_def.TYPE_STRING,               # 会员姓名
                    "cellphone": type_def.TYPE_STRING           # 联系方式 
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_SUBSCRIBER_ADMIN_ASSOCIATE:
# 1. 请求消息结构：PortalSubscriberAdminAssociateReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalSubscriberAdminAssociateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberAdminAssociateReq
    Description: 订阅者管理员身份设置
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # 订阅者openID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
        

# PORTAL_SUBSCRIBER_INFO_QUERY:
# 1. 请求消息结构：PortalSubscriberInfoQueryReq
# 2. 响应消息结构：PortalSubscriberInfoQueryRsp
class Subscriber(serializable_obj.JsonSerializableObj):
    """
    Class: Subscriber
    Description: 订阅者信息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # 订阅者openID(界面不显示)
                    "nickname": type_def.TYPE_STRING,           # 昵称
                    "weixin_id": type_def.TYPE_STRING,          # 微信号
                    "gender": type_def.TYPE_STRING,             # 性别
                    "city": type_def.TYPE_STRING,               # 城市
                    "group_ids": [type_def.TYPE_STRING],        # 分组ID列表
                    "member_flag": type_def.TYPE_BOOL,          # 是否已加入会员
                    "head_img": type_def.TYPE_STRING,           # 头像图片文件
                    "admin_flag": type_def.TYPE_BOOL,           # 是否是管理员
                    "assoc_member_id": type_def.TYPE_STRING,    # 关联的会员ID
                    "assoc_member_name": type_def.TYPE_STRING   # 关联的会员姓名
                   }

class PortalSubscriberInfoQueryReq(CommonQueryReq):
    """
    Class: PortalSubscriberInfoQueryReq
    Description: 查询所有订阅者信息请求
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_id": type_def.TYPE_STRING  # 分组ID（为空则查询所有订阅者，否则按照分组查询）
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)

    
class PortalSubscriberInfoQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalSubscriberInfoQueryRsp
    Description: 查询所有订阅者信息响应
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # 订阅者数量
                    "subscribers": [Subscriber]     # 订阅者列表
                    }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)


# PORTAL_SUBSCRIBER_GROUP_CREATE:
# 1. 请求消息结构：PortalSubscriberGroupCreateReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class Group(serializable_obj.JsonSerializableObj):
    """
    Class: Group
    Description: 订阅者分组信息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_id": type_def.TYPE_STRING,       # 分组ID(界面不显示)
                    "group_name": type_def.TYPE_STRING,     # 分组名
                    "group_sub_num": type_def.TYPE_UINT32,  # 分组内包含的订阅者数量
                    "description": type_def.TYPE_STRING     # 分组描述
                   }
    
class PortalSubscriberGroupCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberGroupCreateReq
    Description: 创建订阅者分组
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_name": type_def.TYPE_STRING,  # 分组名
                    "description": type_def.TYPE_STRING  # 分组描述
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    

# PORTAL_SUBSCRIBER_GROUP_REMOVE:
# 1. 请求消息结构：PortalSubscriberGroupRemoveReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalSubscriberGroupRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberGroupRemoveReq
    Description: 删除订阅者分组
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_id": type_def.TYPE_STRING    # 分组ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_SUBSCRIBER_GROUP_MODIFY:
# 1. 请求消息结构：PortalSubscriberGroupModifyReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalSubscriberGroupModifyReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberGroupModifyReq
    Description: 修改订阅者分组
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_id": type_def.TYPE_STRING,       # 分组ID(界面不显示)
                    "group_name": type_def.TYPE_STRING,     # 分组名
                    "description": type_def.TYPE_STRING     # 分组描述
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_SUBSCRIBER_GROUP_QUERY:
# 1. 请求消息结构：CommonQueryReq
# 2. 响应消息结构：PortalSubscriberGroupQueryRsp
class PortalSubscriberGroupQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalSubscriberGroupModifyReq
    Description: 修改订阅者分组
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # 分组数量
                    "groups": [Group]               # 分组列表
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)

# PORTAL_SUBSCRIBER_GROUP_ASSOCIATE:
# 1. 请求消息结构：PortalSubscriberGroupAssociateReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalSubscriberGroupAssociateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberGroupAssociateReq
    Description: 订阅者加入群组(允许同时加入多个群组)
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # 订阅者openID
                    "group_ids": [type_def.TYPE_STRING]         # 分组ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_SUBSCRIBER_GROUP_MSG_PUSH:
# 1. 请求消息结构：PortalSubscriberGroupMsgPushReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalSubscriberGroupMsgPushReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalSubscriberGroupMsgPushReq
    Description: 订阅者消息群发
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "group_ids": [type_def.TYPE_STRING],   # 分组ID列表
                    "text_msg": type_def.TYPE_STRING       # 回复的文本消息
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    

# PORTAL_MEMBER_MEMBER_CREATE:
# 1. 请求消息结构：PortalMemberMemberCreateModReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
# PORTAL_MEMBER_MEMBER_MODIFY:
# 1. 请求消息结构：PortalMemberMemberCreateModReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class Member(serializable_obj.JsonSerializableObj):
    """
    Class: Member
    Description: 会员信息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING,          # 会员ID(界面不显示)
                    "name": type_def.TYPE_STRING,               # 姓名
                    "cellphone": type_def.TYPE_STRING,          # 联系方式
                    "weixin_id": type_def.TYPE_STRING,          # 微信号
                    "delivery_addr": type_def.TYPE_STRING,      # 配送地址
                    "delivery_time": type_def.TYPE_STRING,      # 配送时间
                    "delivery_expiry": type_def.TYPE_STRING,    # 配送截止日期（有效期）
                    "subscribe_flag": type_def.TYPE_BOOL,       # 是否已订阅
                    "nickname": type_def.TYPE_STRING,           # 微信昵称
                   }
    
class PortalMemberMemberCreateModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMemberCreateModReq
    Description: 创建会员
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING,          # 会员ID
                    "name": type_def.TYPE_STRING,               # 姓名
                    "cellphone": type_def.TYPE_STRING,          # 联系方式
                    "delivery_addr": type_def.TYPE_STRING,      # 配送地址
                    "delivery_time": type_def.TYPE_STRING,      # 配送时间(1-7，星期几)
                    "delivery_expiry": type_def.TYPE_STRING,    # 配送截止日期（有效期）
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)



# PORTAL_MEMBER_MEMBER_REMOVE:
# 1. 请求消息结构：PortalMemberMemberRemoveReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalMemberMemberRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMemberRemoveReq
    Description: 删除会员
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING      # 会员ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

    
# PORTAL_MEMBER_MEMBER_QUERY:
# 1. 请求消息结构：PortalMemberMemberQueryReq
# 2. 响应消息结构：PortalMemberMemberQueryRsp
class PortalMemberMemberQueryReq(CommonQueryReq):
    """
    Class: PortalSubscriberInfoQueryReq
    Description: 查询会员信息响应(如果请求消息中num_per_page/current_page为0，则查询所有结果)
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING  # 会员ID
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)


class PortalMemberMemberQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalMemberMemberQueryRsp
    Description: 查询会员信息响应(如果请求消息中num_per_page/current_page为0，则查询所有结果)
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # 会员数量
                    "members": [Member]             # 会员列表
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)


# PORTAL_DELIVERY_MEMBER_MENU_CFG:
# 1. 请求消息结构：PortalDeliveryMemberMenuCfgReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalDeliveryMemberMenuCfgReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalDeliveryMemberMenuCfgReq
    Description: 配置会员的配送菜单
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING,      # 会员ID
                    "vegetables": [type_def.TYPE_STRING]    # 菜品清单(菜品ID列表)
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_DELIVERY_VEGETABLE_CREATE:
# 1. 请求消息结构：PortalDeliveryVegetableCreateReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb

class VegetableList(serializable_obj.JsonSerializableObj):
    """
    Class: VegetableList
    Description: 菜品列表
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "vegetables": [type_def.TYPE_STRING]    # 菜品清单(菜品ID列表)
                    }


class Vegetable(serializable_obj.JsonSerializableObj):
    """
    Class: Vegetable
    Description: 菜品信息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "v_id": type_def.TYPE_STRING,           # 菜品ID
                    "name": type_def.TYPE_STRING,           # 菜品名
                    "description": type_def.TYPE_STRING     # 菜品描述
                   }

class PortalDeliveryVegetableCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalDeliveryVegetableCreateModReq
    Description: 创建菜品
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "name": type_def.TYPE_STRING,           # 菜品名
                    "description": type_def.TYPE_STRING     # 菜品描述
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_DELIVERY_VEGETABLE_MODIFY:
# 1. 请求消息结构：PortalDeliveryVegetableModReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalDeliveryVegetableModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalDeliveryVegetableModReq
    Description: 修改菜品
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "v_id": type_def.TYPE_STRING,           # 菜品ID
                    "name": type_def.TYPE_STRING,           # 菜品名
                    "description": type_def.TYPE_STRING     # 菜品描述
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_DELIVERY_VEGETABLE_REMOVE:
# 1. 请求消息结构：PortalDeliveryVegetableRemoveReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalDeliveryVegetableRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalDeliveryVegetableRemoveReq
    Description: 删除菜品
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "v_id": type_def.TYPE_STRING           # 菜品ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_DELIVERY_VEGETABLE_QUERY:
# 1. 请求消息结构：PortalDeliveryVegetableQueryReq
# 2. 响应消息结构：PortalDeliveryVegetableQueryRsp
class PortalDeliveryVegetableQueryReq(CommonQueryReq):
    """
    Class: PortalDeliveryVegetableQueryReq
    Description: 查询菜品信息请求
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "v_id": type_def.TYPE_STRING    # 菜品ID
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)
    
class PortalDeliveryVegetableQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalDeliveryVegetableQueryRsp
    Description: 查询菜品信息响应
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # 菜品数量
                    "vegetables": [Vegetable]       # 菜品列表
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    

# PORTAL_DELIVERY_MENU_CREATE:
# 1. 请求消息结构：PortalDeliveryMenuCreateModReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class Menu(serializable_obj.JsonSerializableObj):
    """
    Class: Menu
    Description: 菜单信息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "menu_id": type_def.TYPE_STRING,        # 菜单ID(界面不显示)
                    "name": type_def.TYPE_STRING,           # 菜单名
                    "count": type_def.TYPE_INT32,           # 菜单包含的菜品数量
                    "vegetable": [type_def.TYPE_STRING]     # 菜品列表
                   }
    
class PortalMemberMenuCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMenuCreateReq
    Description: 创建菜单
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "name": type_def.TYPE_STRING,           # 菜单名
                    "content": type_def.TYPE_STRING         # 菜单内容
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_MEMBER_MENU_MODIFY:
# 1. 请求消息结构：PortalMemberMenuModReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb    
class PortalMemberMenuModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMenuModReq
    Description: 修改菜单
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "menu_id": type_def.TYPE_STRING,        # 菜单ID(界面不显示)
                    "name": type_def.TYPE_STRING,           # 菜单名
                    "content": type_def.TYPE_STRING         # 菜单内容
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    

# PORTAL_MEMBER_MENU_REMOVE:
# 1. 请求消息结构：PortalMemberMenuRemoveReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalMemberMenuRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMenuRemoveReq
    Description: 删除菜单
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "menu_id": type_def.TYPE_STRING      # 菜单ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

    
# PORTAL_MEMBER_MENU_QUERY:
# 1. 请求消息结构：CommonQueryReq
# 2. 响应消息结构：PortalMemberMenuQueryRsp
class PortalMemberMenuQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalMemberMenuQueryRsp
    Description: 查询菜单信息响应
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # 菜单数量
                    "menus": [Menu]                 # 菜单列表
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    
# PORTAL_DELIVERY_REPORT_QUERY:
# 1. 请求消息结构：PortalDeliveryReportQueryReq
# 2. 响应消息结构：PortalDeliveryReportQueryRsp
class DeliveryReport(serializable_obj.JsonSerializableObj):
    """
    Class: DeliveryReport
    Description: 配送报表信息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING,          # 会员ID
                    "name": type_def.TYPE_STRING,               # 真实姓名
                    "cellphone": type_def.TYPE_STRING,          # 联系方式
                    "delivery_addr": type_def.TYPE_STRING,      # 配送地址
                    "delivery_time": type_def.TYPE_STRING,      # 配送时间(本次配送的准确日期)
                    "vegetables": [type_def.TYPE_STRING]        # 配送菜单(菜品名称列表)
                   }
        
class PortalDeliveryReportQueryReq(CommonQueryReq):
    """
    Class: PortalDeliveryReportQueryReq
    Description: 查询配送报表请求
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "member_id": type_def.TYPE_STRING, # 会员ID（为空则查询所有会员的配送报告，否则按照会员查询）
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)
    
class PortalDeliveryReportQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalDeliveryReportQueryRsp
    Description: 查询配送报表响应
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,           # 配送报表数量
                    "delivery_reports": [DeliveryReport]    # 配送报表列表
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)

    
# PORTAL_CONTENT_HELPTIPS_SET:
# 1. 请求消息结构：CommonContentReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
# PORTAL_CONTENT_HELPTIPS_QUERY
# 1. 请求消息结构：basic_rep_to_web.BasicReqFromWeb
# 2. 响应消息结构：CommonContentRsp


class Subject(serializable_obj.JsonSerializableObj):
    """
    Class: Subject
    Description: 主题栏目信息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subject_id": type_def.TYPE_STRING,  # 栏目ID
                    "name": type_def.TYPE_STRING,        # 栏目名
                    "article_num": type_def.TYPE_UINT32, # 包含的主题内容数量
                    "description": type_def.TYPE_STRING  # 栏目描述
                   }

class Article(serializable_obj.JsonSerializableObj):
    """
    Class: Article
    Description: 主题内容信息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "article_id": type_def.TYPE_STRING,     # 主题内容ID(查询界面不显示)
                    "title": type_def.TYPE_STRING,          # 标题
                    "subject_id": type_def.TYPE_STRING,     # 归属的栏目ID
                    "description": type_def.TYPE_STRING,    # 概述
                    "pic_url": type_def.TYPE_STRING,        # 缩略图URL
                    "content_url": type_def.TYPE_STRING,    # 正文内容URL
                    "content": type_def.TYPE_STRING,        # 正文内容(HTML)(查询界面不显示)
                    "sub_group_ids": [type_def.TYPE_STRING],# 订阅者分组ID列表
                    "push_timer": type_def.TYPE_STRING,     # 定时推送时间
                    "push_times": type_def.TYPE_UINT16      # 定时推送次数
                   }
    
# PORTAL_CONTENT_SUBJECT_CREATE：
# 1. 请求消息结构：PortalContentSubjectCreateReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb    
class PortalContentSubjectCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalMemberMenuCreateReq
    Description: 创建主题栏目
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "name": type_def.TYPE_STRING,       # 栏目名
                    "description": type_def.TYPE_STRING # 栏目描述
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_CONTENT_SUBJECT_MODIFY
# 1. 请求消息结构：PortalContentSubjectModReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb    
class PortalContentSubjectModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentSubjectModReq
    Description: 修改主题栏目
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "subject_id": type_def.TYPE_STRING,  # 栏目ID
                    "name": type_def.TYPE_STRING,        # 栏目名
                    "description": type_def.TYPE_STRING  # 栏目描述
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_CONTENT_SUBJECT_REMOVE:
# 1. 请求消息结构：PortalContentSubjectRemoveReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalContentSubjectRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentSubjectRemoveReq
    Description: 删除主题栏目
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "subject_id": type_def.TYPE_STRING, # 栏目ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

# PORTAL_CONTENT_SUBJECT_QUERY:
# 1. 请求消息结构：CommonQueryReq
# 2. 响应消息结构：PortalContentSubjectQueryRsp
class PortalContentSubjectQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalContentSubjectQueryRsp
    Description: 查询主题栏目响应
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # 主题栏目数量
                    "subjects": [Subject]           # 主题栏目列表
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)


# PORTAL_CONTENT_ARTICLE_CREATE：
# 1. 请求消息结构：PortalContentArticleCreateReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb    
class PortalContentArticleCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentArticleCreateReq
    Description: 创建主题内容
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "title": type_def.TYPE_STRING,          # 标题
                    "subject_id": type_def.TYPE_STRING,     # 归属的栏目ID
                    "description": type_def.TYPE_STRING,    # 概述
                    "pic_url": type_def.TYPE_STRING,        # 缩略图URL
                    "content_url": type_def.TYPE_STRING,    # 正文内容URL
                    "content": type_def.TYPE_STRING,        # 正文内容(HTML)
                    "sub_group_ids": [type_def.TYPE_STRING],# 订阅者分组ID列表
                    "push_timer": type_def.TYPE_STRING,     # 定时推送时间（可选）
                    "push_times": type_def.TYPE_UINT16      # 定时推送次数（可选）
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_CONTENT_ARTICLE_MODIFY
# 1. 请求消息结构：PortalContentArticleModReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb    
class PortalContentArticleModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentArticleModReq
    Description: 修改主题内容
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "article_id": type_def.TYPE_STRING,     # 主题内容ID(查询界面不显示)
                    "title": type_def.TYPE_STRING,          # 标题
                    "subject_id": type_def.TYPE_STRING,     # 归属的栏目ID
                    "description": type_def.TYPE_STRING,    # 概述
                    "pic_url": type_def.TYPE_STRING,        # 缩略图URL
                    "content_url": type_def.TYPE_STRING,    # 正文内容URL
                    "content": type_def.TYPE_STRING,        # 正文内容(HTML)(查询界面不显示)
                    "sub_group_ids": [type_def.TYPE_STRING],# 订阅者分组ID列表
                    "push_timer": type_def.TYPE_STRING,     # 定时推送时间
                    "push_times": type_def.TYPE_UINT16      # 定时推送次数
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    
# PORTAL_CONTENT_ARTICLE_REMOVE:
# 1. 请求消息结构：PortalContentArticleRemoveReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalContentArticleRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentArticleRemoveReq
    Description: 删除主题内容
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "article_id": type_def.TYPE_STRING     # 主题内容ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)

    
# PORTAL_CONTENT_ARTICLE_QUERY:
# 1. 请求消息结构：PortalContentArticleQueryReq
# 2. 响应消息结构：PortalContentArticleQueryRsp
class PortalContentArticleQueryReq(CommonQueryReq):
    """
    Class: PortalContentArticleQueryReq
    Description: 查询主题栏目请求
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "subject_id": type_def.TYPE_STRING, # 栏目ID（为空则查询所有主题内容，否则按照栏目查询）
                    "article_id": type_def.TYPE_STRING, # 主题内容ID（为空则查询所有主题内容，否则按照主题查询）
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)
    
class PortalContentArticleQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalContentSubjectQueryReq
    Description: 查询主题栏目响应
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # 主题栏目数量
                    "articles": [Article]           # 主题栏目列表
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)

# PORTAL_CONTENT_ARTICLE_SUBSCRIBER_PUSH:
# 1. 请求消息结构：PortalContentArticleSubscriberPush
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalContentArticleSubscriberPush(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentArticleSubscriberPush
    Description: 推送主题内容给订阅者分组
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "article_id": type_def.TYPE_STRING     # 主题内容ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)
    


# PORTAL_CONTENT_KEYWORD_RULE_CREATE:
# PORTAL_CONTENT_KEYWORD_RULE_MODIFY: 
# 1. 请求消息结构：PortalContentKeywordRuleCreateReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb

KEYWORD_RULE_MATCH_TYPE_TEXT = 'text'
KEYWORD_RULE_MATCH_TYPE_ARTICLE = 'article'

class Keyword(serializable_obj.JsonSerializableObj):
    """
    Class: KeyWord
    Description: 关键字参数
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "keyword": type_def.TYPE_STRING,          # 关键字
                    "wholeword_match": type_def.TYPE_BOOL     # 是否全词匹配
                   }

class KeywordRule(serializable_obj.JsonSerializableObj):
    """
    Class: KeywordRule
    Description: 关键字匹配规则
    Base: JsonSerializableObj
    Others: 
    """
    
    __ATTR_DEF__ = {
                    "rule_id": type_def.TYPE_STRING,    # 规则ID        
                    "rule_name": type_def.TYPE_STRING,  # 规则名
                    "keywords": [Keyword],              # 关键字列表
                    "match_type": type_def.TYPE_STRING, # 匹配类型（文本消息、主题内容）
                    "contents": [type_def.TYPE_STRING]  # 内容（文本消息内容、主题内容列表）
                   }


class PortalContentKeywordRuleCreateReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentKeywordRuleCreateModReq
    Description: 创建关键字匹配规则
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "rule_name": type_def.TYPE_STRING,  # 规则名
                    "keywords": [Keyword],              # 关键字列表
                    "match_type": type_def.TYPE_STRING, # 匹配类型（文本消息、主题内容）
                    "contents": [type_def.TYPE_STRING]  # 内容（文本消息内容、主题内容列表）
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_CONTENT_KEYWORD_RULE_MODIFY: 
# 1. 请求消息结构：PortalContentKeywordRuleModReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalContentKeywordRuleModReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentKeywordRuleCreateModReq
    Description: 创建关键字匹配规则
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "rule_id": type_def.TYPE_STRING,    # 规则ID        
                    "rule_name": type_def.TYPE_STRING,  # 规则名
                    "keywords": [Keyword],              # 关键字列表
                    "match_type": type_def.TYPE_STRING, # 匹配类型（文本消息、主题内容）
                    "contents": [type_def.TYPE_STRING]  # 内容（文本消息内容、主题内容列表）
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_CONTENT_KEYWORD_RULE_REMOVE:
# 1. 请求消息结构：PortalContentKeywordRuleRemoveReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
class PortalContentKeywordRuleRemoveReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalContentKeywordRuleRemoveReq
    Description: 删除关键字匹配规则
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "rule_id": type_def.TYPE_STRING    # 规则ID        
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_CONTENT_KEYWORD_RULE_QUERY:
# 1. 请求消息结构：PortalContentKeywordRuleQueryReq
# 2. 响应消息结构：PortalContentKeywordRuleQueryRsp
class PortalContentKeywordRuleQueryReq(CommonQueryReq):
    """
    Class: PortalContentKeywordRuleQueryReq
    Description: 查询关键字规则请求
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "rule_id": type_def.TYPE_STRING    # 规则ID        
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)
    
class PortalContentKeywordRuleQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalContentKeywordRuleQueryRsp
    Description: 查询关键字规则响应
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # 规则数
                    "rules": [KeywordRule]          # 规则列表
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    

# PORTAL_EVENT_EVENT_REPORT:
# 1. 请求消息结构：PortalEventEventReportReq
# 2. 响应消息结构：basic_rep_to_web.BasicRepToWeb
EVENT_TYPE_SUBSCRIBE  = 'subscribe'  # 订阅事件
EVENT_TYPE_MESSAGE    = 'message'    # 订阅者消息事件 
EVENT_TYPE_DELIVERY   = 'delivery'   # 会员菜品配送事件
EVENT_TYPE_USERLOGIN  = 'login'      # 管理用户登录事件
EVENT_TYPE_PORTALOPER = 'operation'  # 后台重要操作事件
EVENT_TYPE_MENUCFG    = 'menucfg'    # 会员菜单自选事件

EVENT_PORTAL_OPERATION_ADD  = '创建'
EVENT_PORTAL_OPERATION_MOD  = '修改'
EVENT_PORTAL_OPERATION_DEL  = '删除'
EVENT_PORTAL_OPERATION_PUSH = '推送'

EVENT_PORTAL_OBJECT_SUBJECT   = '栏目'
EVENT_PORTAL_OBJECT_ARTICLE   = '主题'
EVENT_PORTAL_OBJECT_HELPTIPS  = '欢迎词'
EVENT_PORTAL_OBJECT_MEMBER    = '会员'
EVENT_PORTAL_OBJECT_VEGETABLE = '菜品'

class PortalEventEventReportReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalEventEventReportReq
    Description: 事件上报消息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "event_type": type_def.TYPE_STRING, # 事件类型
                    "content": type_def.TYPE_STRING     # 事件详细信息（不同事件类型的信息JSON串）
                    }  
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_EVENT_EVENT_QUERY:
# 1. 请求消息结构：PortalEventEventQueryReq
# 2. 响应消息结构：PortalEventEventQueryRsp
class Event(serializable_obj.JsonSerializableObj):
    """
    Class: Event
    Description: 返回给请求者的每条Event的信息
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "event_id": type_def.TYPE_STRING,   # 事件ID 
                    "event_type": type_def.TYPE_STRING, # 事件类型
                    "content": type_def.TYPE_STRING,    # 事件详细信息（不同事件类型的信息JSON串）
                    "read_flag": type_def.TYPE_BOOL     # 已读标志
                    }    

class SubscribeEvent(serializable_obj.JsonSerializableObj):
    """
    Class: SubscribeEvent
    Description: 订阅事件
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # 订阅者openID(界面不显示)
                    "weixin_id": type_def.TYPE_STRING,          # 微信号
                    "nickname": type_def.TYPE_STRING,           # 昵称
                    "action": type_def.TYPE_STRING,             # 动作（订阅、取消订阅）
                    "time": type_def.TYPE_STRING                # 日期
                    }

class SubscriberMessageEvent(serializable_obj.JsonSerializableObj):
    """
    Class: SubscriberMessageEvent
    Description: 订阅者消息事件
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # 订阅者openID(界面不显示)
                    "weixin_id": type_def.TYPE_STRING,          # 微信号
                    "nickname": type_def.TYPE_STRING,           # 昵称
                    "member_id": type_def.TYPE_STRING,          # 会员ID
                    "name": type_def.TYPE_STRING,               # 姓名
                    "text_msg": type_def.TYPE_STRING,           # 文本消息
                    "pic_url": type_def.TYPE_STRING,            # 图片消息URL
                    "time": type_def.TYPE_STRING                # 日期
                    }

class DeliveryNotificationEvent(serializable_obj.JsonSerializableObj):
    """
    Class: DeliveryNotificationEvent
    Description: 配送通知事件
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # 订阅者openID(界面不显示)
                    "weixin_id": type_def.TYPE_STRING,          # 微信号
                    "nickname": type_def.TYPE_STRING,           # 昵称
                    "member_id": type_def.TYPE_STRING,          # 会员ID
                    "name": type_def.TYPE_STRING,               # 姓名
                    "delivery_menu": type_def.TYPE_STRING,      # 配送菜单名
                    "delivery_time": type_def.TYPE_STRING       # 配送时间
                    }

class UserLoginEvent(serializable_obj.JsonSerializableObj):
    """
    Class: UserLoginEvent
    Description: 用户登录事件
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "user_id": type_def.TYPE_STRING,    # 用户名
                    "login_time": type_def.TYPE_STRING  # 登录时间
                    }
    

class PortalOperEvent(serializable_obj.JsonSerializableObj):
    """
    Class: PortalOperEvent
    Description: Portal重要操作事件
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "user_id": type_def.TYPE_STRING,    # 用户名
                    "oper_time": type_def.TYPE_STRING,  # 操作时间
                    "oper_type": type_def.TYPE_STRING,  # 操作类别
                    "content": type_def.TYPE_STRING     # 操作内容
                    } 


class MemberConfigMenuEvent(serializable_obj.JsonSerializableObj):
    """
    Class: MemberConfigMenuEvent
    Description: 会员自选菜单事件
    Base: JsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # 订阅者openID(界面不显示)
                    "weixin_id": type_def.TYPE_STRING,          # 微信号
                    "nickname": type_def.TYPE_STRING,           # 昵称
                    "member_id": type_def.TYPE_STRING,          # 会员ID
                    "name": type_def.TYPE_STRING,               # 姓名
                    "menu": type_def.TYPE_STRING,               # 自选菜单(文本)
                    "time": type_def.TYPE_STRING                # 日期(文本)
                    }       

class PortalEventEventQueryReq(CommonQueryReq):
    """
    Class: PortalEventEventQueryReq
    Description: 查询事件请求
    Base: CommonQueryReq
    Others: 
    """

    __ATTR_DEF__ = {
                    "event_type": type_def.TYPE_STRING  # 事件类型（为空则查询所有事件，否则按照事件类型查询）
                    }
    __ATTR_DEF__.update(CommonQueryReq.__ATTR_DEF__)

        
class PortalEventEventQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalEventEventQueryRsp
    Description: 查询事件响应
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,   # 事件数量
                    "events": [Event]               # 事件列表
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)

# PORTAL_EVENT_UNREAD_QUERY:
# 1. 请求消息结构：basic_rep_to_web.BasicReqFromWeb
# 2. 响应消息结构：PortalEventUnreadQueryRsp

class EventNum(serializable_obj.JsonSerializableObj):
    __ATTR_DEF__ = {
                    "event_type": type_def.TYPE_STRING,  # 事件类型
                    "num": type_def.TYPE_INT32           # 事件数量
                   }    

class PortalEventUnreadQueryRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalEventUnreadQueryRsp
    Description: 查询未读事件数量响应
    Base: BasicRepToWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,          # 事件类型数(目前为5）
                    'event_unread_nums': [EventNum]
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)


# PORTAL_EVENT_READ_NOTIFY:
# 1. 请求消息结构：PortalEventReadNotifyReq
# 2. 响应消息结构：basic_rep_to_web.BasicReqToWeb
class PortalEventReadNotifyReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalEventReadNotifyReq
    Description: 事件已读通知
    Base: BasicReqFromWeb
    Others: 
    """

    __ATTR_DEF__ = {
                    "event_id": type_def.TYPE_STRING   # 事件ID 
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)


# PORTAL_EVENT_MESSAGE_REPLY:
# 1. 请求消息结构：PortalEventMessageReplyReq
# 2. 响应消息结构：basic_rep_to_web.BasicReqToWeb
class PortalEventMessageReplyReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalEventMessageReplyReq
    Description: 订阅者消息直接回复
    Base: BasicReqFromWeb
    Others: 
    """
    __ATTR_DEF__ = {
                    "event_id": type_def.TYPE_STRING,   # 事件ID 
                    "text_msg": type_def.TYPE_STRING    # 回复的文本消息
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)    


# PORTAL_EVENT_MESSAGE_SHARE:
# 1. 请求消息结构：PortalEventMessageShareReq
# 2. 响应消息结构：basic_rep_to_web.BasicReqToWeb
class PortalEventMessageShareReq(basic_rep_to_web.BasicReqFromWeb):
    """
    Class: PortalEventMessageShareReq
    Description: 订阅者消息分享到指定栏目
    Base: BasicReqFromWeb
    Others: 
    """
    __ATTR_DEF__ = {
                    "event_id": type_def.TYPE_STRING,           # 欲分享的事件ID 
                    'subject_id': type_def.TYPE_STRING          # 分享到的栏目ID
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicReqFromWeb.__ATTR_DEF__)  
    

# PORTAL_EVENT_DAILY_STATS:
# 1. 请求消息结构：basic_rep_to_web.BasicReqFromWeb
# 2. 响应消息结构：PortalEventDailyStatsRsp
class PortalEventDailyStatsRsp(basic_rep_to_web.BasicRepToWeb):
    """
    Class: PortalEventMessageShareReq
    Description: 订阅者消息分享到指定栏目
    Base: BasicReqFromWeb
    Others: 
    """
    __ATTR_DEF__ = {
                    "count": type_def.TYPE_INT32,          # 事件类型数(目前为5）
                    'event_daily_nums': [EventNum]
                   }
    __ATTR_DEF__.update(basic_rep_to_web.BasicRepToWeb.__ATTR_DEF__)
    

##############################################################################
    
class WXMessage(serializable_obj.JsonSerializableObj):
    """
    Class: WXMessage
    Description: 微信消息基类
    Base: BsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_id": type_def.TYPE_STRING, # 订阅者openID
                    "public_account_id": type_def.TYPE_STRING,  # 公共账号ID
                    "create_time": type_def.TYPE_STRING,        # 消息创建时间
                    "msg_type": type_def.TYPE_STRING            # 消息类型
                    }

class WXPushTextMessage(WXMessage):
    """
    Class: WXPushTextMessage
    Description: 微信文本消息
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "content": type_def.TYPE_STRING,    # 消息正文
                    "msg_id": type_def.TYPE_STRING      # 消息ID
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)
    
          
class WXPushImageMessage(WXMessage):
    """
    Class: WXPushImageMessage
    Description: 微信图片消息
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "pic_url": type_def.TYPE_STRING,    # 图片URL
                    "msg_id": type_def.TYPE_STRING      # 消息ID
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)
    

class WXPushLocationMessage(WXMessage):
    """
    Class: WXPushLocationMessage
    Description: 微信地理位置消息
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "location_x": type_def.TYPE_STRING, # 地理位置纬度
                    "location_y": type_def.TYPE_STRING, # 地理位置经度
                    "scale": type_def.TYPE_STRING,      # 地图缩放大小
                    "label": type_def.TYPE_STRING,      # 地理位置信息
                    "msg_id": type_def.TYPE_STRING      # 消息ID
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)

class WXPushLinkMessage(WXMessage):
    """
    Class: WXPushLinkMessage
    Description: 微信链接消息
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "title": type_def.TYPE_STRING,      # 消息标题
                    "description": type_def.TYPE_STRING,# 消息描述
                    "url": type_def.TYPE_STRING,        # 消息链接
                    "msg_id": type_def.TYPE_STRING      # 消息ID
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)


WX_EVENT_TYPE_SUBSCRIBE = 'subscribe'
WX_EVENT_TYPE_UNSUBSCRIBE = 'unsubscribe'
WX_EVENT_TYPE_CLICK = 'CLICK'

class WXPushEventMessage(WXMessage):
    """
    Class: WXPushEventMessage
    Description: 微信通知事件
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "event": type_def.TYPE_STRING,      # 事件类型
                    "event_key": type_def.TYPE_STRING   # 事件KEY值
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)

class WXReplyTextMessage(WXMessage):
    """
    Class: WXReplyTextMessage
    Description: 微信文本消息响应
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "content": type_def.TYPE_STRING,    # 消息正文
                    "func_flag": type_def.TYPE_STRING   # 星标标志
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)

class WXReplyMusicMessage(WXMessage):
    """
    Class: WXReplyMusicMessage
    Description: 微信音乐消息响应
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "title": type_def.TYPE_STRING,          # 音乐消息标题
                    "description": type_def.TYPE_STRING,    # 音乐消息描述
                    "music_url": type_def.TYPE_STRING,      # 音乐链接
                    "hq_music_url": type_def.TYPE_STRING,   # 高质量音乐链接
                    "func_flag": type_def.TYPE_STRING       # 星标标志
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)

class WXArticle(serializable_obj.JsonSerializableObj):
    """
    Class: WXArticle
    Description: 微信图文消息内容
    Base: BsonSerializableObj
    Others: 
    """
    __ATTR_DEF__ = {
                    "title": type_def.TYPE_STRING,      # 图文消息标题
                    "description": type_def.TYPE_STRING,# 图文消息描述
                    "pic_url": type_def.TYPE_STRING,    # 图片链接
                    "url": type_def.TYPE_STRING         # 点击图文消息跳转链接
                    }
        
class WXReplyNewsMessage(WXMessage):
    """
    Class: WXReplyNewsMessage
    Description: 微信图文消息响应
    Base: WXMessage
    Others: 
    """
    __ATTR_DEF__ = {
                    "article_count": type_def.TYPE_UINT32,       # 图文消息个数
                    "articles": [WXArticle],                # 图文消息列表
                    "func_flag": type_def.TYPE_STRING       # 星标标志
                    }
    __ATTR_DEF__.update(WXMessage.__ATTR_DEF__)
    

# CLOUD_PORTAL_ARTICLE_PUSH_MSG：
class CloudPortalArticlePushMessage(serializable_obj.JsonSerializableObj):
    """
    Class: CloudPortalArticlePushMessage
    Description: 主题内容推送消息
    Base: BsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "article_id": type_def.TYPE_UINT32,     # 主题ID
                    "wx_news_id": type_def.TYPE_STRING,     # 微信图文消息ID
                    "sub_open_ids": [type_def.TYPE_STRING]  # 推送订阅者列表
                   }
    
# CLOUD_PORTAL_TEXT_PUSH_MSG
class CloudPortalTextPushMessage(serializable_obj.JsonSerializableObj):
    """
    Class: CloudPortalTextPushMessage
    Description: 文本消息推送消息(支持批量)
    Base: BsonSerializableObj
    Others: 
    """

    __ATTR_DEF__ = {
                    "subscriber_open_ids": [type_def.TYPE_STRING], # 订阅者openID列表
                    "text_msg": type_def.TYPE_STRING               # 回复的文本消息
                   }

