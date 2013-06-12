#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-06
Description: RFID子系统所有错误码定义
Others:      
Key Class&Method List: 
        
History: 
1. Date:2012-09-06
   Author:ACP2013
   Modification:新建文件
"""

import err_code_mgr

# 微信公共账号云平台命令码区段
WX_CLOUD_ERRCODE_BASE      = 0x01000000

# 微信HTTP接口(PHP)与云平台(Python)接口错误码区段
WX_ITF_ERRCODE_BASE      = WX_CLOUD_ERRCODE_BASE + 0x10000

# 管理Portal接口(PHP)与云平台(Python)接口错误码区段
PORTAL_ITF_ERRCODE_BASE  = WX_CLOUD_ERRCODE_BASE + 0x20000

# 云平台内部错误码区段
CLOUD_INNER_ERRCODE_BASE = WX_CLOUD_ERRCODE_BASE + 0x30000

wx_gateway_error_defs = {}

wx_man_error_def = {}

portal_man_error_defs = {
                         "ERR_PORTAL_DESERIALIZE_ERROR": (PORTAL_ITF_ERRCODE_BASE + 0,
                                                         "从命令   %(cmd)s 的参数  %(param_name)s 为非法的反序列化字符串",
                                                         "invalid string to deserialize from command %(cmd)s parameter  %(param_name)s"),
                               
                         "ERR_PORTAL_ARTICLE_RECORDS_FULL": (PORTAL_ITF_ERRCODE_BASE + 10,
                                                                 "主题内容数目太多，超出系统规格",
                                                                 "The article records are full"),
                         "ERR_PORTAL_ARTICLE_NOT_EXISTS": (PORTAL_ITF_ERRCODE_BASE + 11,
                                                                 "指定的主题内容不存在",
                                                                 "The specified article does not exist"),
                         "ERR_PORTAL_ARTICLE_NOT_UPLOADED": (PORTAL_ITF_ERRCODE_BASE + 12,
                                                                 "该主题内容在后台还未创建完成，请等待后重试",
                                                                 "The article you want to push has not been created in backgroud, please retry"),
                         "ERR_PORTAL_ARTICLE_PARAMS_INVALID": (PORTAL_ITF_ERRCODE_BASE + 13,
                                                                 "主题内容的标题、缩略图、正文不能为空",
                                                                 "The title, head picture and content of the article must be exist"),
                         "ERR_PORTAL_SUBJECT_NOT_EXISTS": (PORTAL_ITF_ERRCODE_BASE + 14,
                                                                 "指定的栏目不存在",
                                                                 "The specified subject does not exist"),
                         
                         "ERR_PORTAL_GROUP_RECORDS_FULL": (PORTAL_ITF_ERRCODE_BASE + 20,
                                                                 "订阅者分组数目太多，超出系统规格",
                                                                 "The subscriber group records are full"),
                         "ERR_PORTAL_GROUP_NOT_EXISTS": (PORTAL_ITF_ERRCODE_BASE + 21,
                                                                 "指定的订阅者分组不存在",
                                                                 "The specified group does not exist"),
                         "ERR_PORTAL_GROUP_ASSOCIATED_BY_SUB": (PORTAL_ITF_ERRCODE_BASE + 22,
                                                                 "该订阅者分组已包含了订阅者，无法直接删除",
                                                                 "The specified group has been associated by subscribers"),
                         "ERR_PORTAL_SUBSCRIBER_NOT_EXISTS": (PORTAL_ITF_ERRCODE_BASE + 23,
                                                                 "指定的订阅者不存在",
                                                                 "The specified subscriber does not exist"),
                         
                         "ERR_PORTAL_EVENT_RECORDS_FULL": (PORTAL_ITF_ERRCODE_BASE + 30,
                                                                 "事件数目太多，超出系统规格",
                                                                 "The event records are full"),
                         "ERR_PORTAL_EVENT_NOT_EXISTS": (PORTAL_ITF_ERRCODE_BASE + 31,
                                                                 "指定的事件不存在",
                                                                 "The specified event does not exist"),

                         }


err_code_mgr.regist_errors(wx_gateway_error_defs)
err_code_mgr.regist_errors(wx_man_error_def)
err_code_mgr.regist_errors(portal_man_error_defs)

