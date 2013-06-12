#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: 调试函数定义
Others:      
Key Class&Method List: 
    1. ....
History: 
1. Date:2013-03-23
   Author:ACP2013
   Modification:新建文件
"""

import tracelog

DEBUG_ENABLED = False

def info(message, *args):
    """
    Method: info
    Description: 输出调试信息
    """
    message = '[DEBUG] %s' % (str(message))
    if DEBUG_ENABLED is True:
        if args is None:
            tracelog.info(message)
        else:
            tracelog.info(message.format(*args))
