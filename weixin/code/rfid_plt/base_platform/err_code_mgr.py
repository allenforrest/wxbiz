#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-15
Description: ���������ģ��
Others:   
ʹ�ô�����Ϣ:

1�����Լ�ģ���Ŀ¼�£�����һ�������Ĵ����ļ�����Ŵ�����Ϣ
2������������
    ����: ER_TIMEOUT = 101

3����������������Ϣ��������Ӣ��
    ����
        my_errors = {      
                  ER_INNER_ERROR        : ("�ڲ�����", "Inner error")
                , ER_TIMEOUT            : ("��ʱ", "Timeout")
                }

    ע: ������Ϣ�У����Զ��嶯̬�������Ա����ɿɶ��Ը��ѺõĴ�����Ϣ
        ����: ER_ERADER_IS_OFFLINE: ("��д��%(read_id)d������", "The reader %(read_id)d is off line")

        ����ʱϣ�����յĴ�����Ϣ�У���Ҫ�аٷֺţ���ôʹ��%%��ʾ%
        ����: ER_FILE_DOWNLOAD_FAILED: ("�ļ�%(file_name)s����ʧ�ܣ���ǰ����Ϊ%%%(progress)d", "Download the file %(file_name)s failed at progress %%%(progress)d")
        
    
4����ģ������ʱ������err_code.regist_errors(my_errors)ע�������Ϣ

5����ȡ������Ϣʱ: 
    err_code_mgr.get_error_msg(XXXXX) # XXXXX�Ǵ������

    ��ȡ���ж�̬�����Ĵ�����:
     err_code_mgr.get_error_msg(ER_FILE_DOWNLOAD_FAILED, file_name="a.txt", progress=30)




Key Class&Method List: 
History: 
1. Date:
   Author:
   Modification:
"""

import language_cfg


ER_SUCCESS                              = 0  # �ɹ�

ER_INNER_ERROR                          = 100
ER_TIMEOUT                              = 101
ER_NO_MEMORY                            = 102
ER_INVALID_REQUEST                      = 103
ER_INVALID_IP                           = 104
ER_DB_ERROR                             = 105

g_common_errors = {
      "ER_SUCCESS"            : (0, "�����ɹ�", "Success")
      
    , "ER_INNER_ERROR"        : (100, "�ڲ�����", "Inner error")
    , "ER_TIMEOUT"            : (101, "��ʱ", "Timeout")
    , "ER_NO_MEMORY"          : (102, "�ڴ治��", "The memory is not enough")
    , "ER_INVALID_REQUEST"    : (103, "��Ч������", "The requst is invalid")
    , "ER_INVALID_IP"         : (104, "��Ч��IP��ַ", "The IP is invalid")
    , "ER_DB_ERROR"           : (105, "���ݿ����ʧ��", "Database operation failed")
}



g_custom_errors = {}




def get_error_msg(err_code, **kw):
    """
    Function: get_error_msg
    Description: ���ݴ������ȡ������Ϣ
    Parameter: 
        err_code: ������
        **kw: ���������Ϣ����Ҫ�ж�̬�Ĳ�������ô��ͨ�������kw��ָ��
    Return: 
    Others: 
        ���kw�����ַ�����������ô�ַ���������utf-8�����
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
            # ��Unicode�����¸�ʽ���ַ�������������
            # msg = msg.decode("utf-8")
            msg = msg % kw
            #msg = msg.encode("utf-8")

    return msg

def regist_errors(error_defs):
    """
    Function: regist_errors
    Description: ע�������Ϣ
    Parameter: 
        error_defs: ������Ϣ
                    error_defs�Ľṹ: {"ER_MACRO_NAME" : (err_code, "��������", "description in English")}
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


