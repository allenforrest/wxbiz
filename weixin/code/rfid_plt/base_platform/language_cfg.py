#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文件中实现了定义语种的功能
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
支持的语种：chs, eng
"""

LANG_CHS = "chs"
LANG_ENG = "eng"

g_language = LANG_CHS

# 从配置文件中加载当前的语种
def load_from_cfg_file(cfg_file_path):
    """
    Function: load_from_cfg_file
    Description: 从配置文件中读取当前的语种
    Parameter: 
        cfg_file_path: 配置文件的路径
    Return: 错误码
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
    Description: 设置当前的语种
    Parameter: 
        language: 语种
    Return: 
    Others: 
    """

    global g_language
    g_language = language

def get_language():
    """
    Function: get_language
    Description: 获取当前的语种
    Parameter: 无
    Return: 支持的语种：chs, eng
    Others: 
    """

    global g_language
    return g_language

def is_chs():
    """
    Function: is_chs
    Description: 判断语种是否是中文
    Parameter: 无
    Return: 语种是否是中文
    Others: 
    """

    global g_language
    return g_language == LANG_CHS  

def is_eng():
    """
    Function: is_eng
    Description: 判断语种是否是英文
    Parameter: 无
    Return: 语种是否是英文
    Others: 
    """

    global g_language
    return g_language == LANG_ENG
      

