#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: ���ļ���ʵ���˶������ֵĹ���
Others:      
Key Class&Method List: 
History: 
1. Date:
   Author:
   Modification:
"""

import xml.etree.ElementTree as ET   
import os.path

"""
֧�ֵ����֣�chs, eng
"""

LANG_CHS = "chs"
LANG_ENG = "eng"

g_language = LANG_CHS

# �������ļ��м��ص�ǰ������
def load_from_cfg_file(cfg_file_path):
    """
    Function: load_from_cfg_file
    Description: �������ļ��ж�ȡ��ǰ������
    Parameter: 
        cfg_file_path: �����ļ���·��
    Return: ������
    Others: 
    """

    global g_language
    
    xmldoc = ET.parse(cfg_file_path)
    xmlroot = xmldoc.getroot()
    language = xmlroot.get("lang")
    if language is None:
        return -1
    
    g_language = language
    return 0

def set_language(language):
    """
    Function: set_language
    Description: ���õ�ǰ������
    Parameter: 
        language: ����
    Return: 
    Others: 
    """

    global g_language
    g_language = language

def get_language():
    """
    Function: get_language
    Description: ��ȡ��ǰ������
    Parameter: ��
    Return: ֧�ֵ����֣�chs, eng
    Others: 
    """

    global g_language
    return g_language

def is_chs():
    """
    Function: is_chs
    Description: �ж������Ƿ�������
    Parameter: ��
    Return: �����Ƿ�������
    Others: 
    """

    global g_language
    return g_language == LANG_CHS  

def is_eng():
    """
    Function: is_eng
    Description: �ж������Ƿ���Ӣ��
    Parameter: ��
    Return: �����Ƿ���Ӣ��
    Others: 
    """

    global g_language
    return g_language == LANG_ENG
      

