#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-15
Description: 错误码管理模块
Others:   
使用错误信息:

1、在自己模块的目录下，建立一个单独的代码文件，存放错误信息
2、定义错误码宏
    例如: ER_TIMEOUT = 101

3、定义错误的描述信息，包括中英文
    例如
        my_errors = {      
                  ER_INNER_ERROR        : ("内部错误", "Inner error")
                , ER_TIMEOUT            : ("超时", "Timeout")
                }

    注: 错误信息中，可以定义动态参数，以便生成可读性更友好的错误信息
        例如: ER_ERADER_IS_OFFLINE: ("读写器%(read_id)d不在线", "The reader %(read_id)d is off line")

        若此时希望最终的错误信息中，需要有百分号，那么使用%%表示%
        例如: ER_FILE_DOWNLOAD_FAILED: ("文件%(file_name)s下载失败，当前进度为%%%(progress)d", "Download the file %(file_name)s failed at progress %%%(progress)d")
        
    
4、在模块启动时，调用err_code.regist_errors(my_errors)注册错误信息

5、获取错误信息时: 
    err_code_mgr.get_error_msg(XXXXX) # XXXXX是错误码宏

    获取带有动态参数的错误码:
     err_code_mgr.get_error_msg(ER_FILE_DOWNLOAD_FAILED, file_name="a.txt", progress=30)




Key Class&Method List: 
History: 
1. Date:
   Author:
   Modification:
"""

import language_cfg


ER_SUCCESS                              = 0  # 成功

ER_INNER_ERROR                          = 100
ER_TIMEOUT                              = 101
ER_NO_MEMORY                            = 102
ER_INVALID_REQUEST                      = 103
ER_INVALID_IP                           = 104
ER_DB_ERROR                             = 105

g_common_errors = {
      "ER_SUCCESS"            : (0, "操作成功", "Success")
      
    , "ER_INNER_ERROR"        : (100, "内部错误", "Inner error")
    , "ER_TIMEOUT"            : (101, "超时", "Timeout")
    , "ER_NO_MEMORY"          : (102, "内存不足", "The memory is not enough")
    , "ER_INVALID_REQUEST"    : (103, "无效的请求", "The requst is invalid")
    , "ER_INVALID_IP"         : (104, "无效的IP地址", "The IP is invalid")
    , "ER_DB_ERROR"           : (105, "数据库操作失败", "Database operation failed")
}



g_custom_errors = {}




def get_error_msg(err_code, **kw):
    """
    Function: get_error_msg
    Description: 根据错误码获取错误信息
    Parameter: 
        err_code: 错误码
        **kw: 如果错误信息中需要有动态的参数，那么就通过这里的kw来指定
    Return: 
    Others: 
        如果kw中有字符串参数，那么字符串必须是utf-8编码的
    """

    global g_custom_errors
   
    msg = g_custom_errors.get(err_code)
    if msg is None:
        return "unknown error(%d)" % err_code

    
    if language_cfg.is_eng():
        msg = msg[1]
        if len(kw) > 0:
            msg = msg % kw
    else:
        msg = msg[0]
        if len(kw) > 0:
            # 在Unicode对象下格式化字符串，避免乱码
            # msg = msg.decode("utf-8")
            msg = msg % kw
            #msg = msg.encode("utf-8")

    return msg

def regist_errors(error_defs):
    """
    Function: regist_errors
    Description: 注册错误信息
    Parameter: 
        error_defs: 错误信息
                    error_defs的结构: {"ER_MACRO_NAME" : (err_code, "中文描述", "description in English")}
    Return: 
    Others: 
        
    """
    global g_custom_errors

    global_vars = globals() 

    for macro_name, info in error_defs.iteritems():
        err_code, des_chs, des_eng = info        
        global_vars[macro_name] = err_code

        
        g_custom_errors[err_code] = (des_chs.decode("gbk").encode("utf-8"), des_eng)
        
        
regist_errors(g_common_errors)


