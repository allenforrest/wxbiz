#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-25
Description: 
Others:      
Key Class&Method List: 
             1. DataRotatingFileHandler： 日志滚动处理
History: 
1. Date:2012-12-25
   Author:ACP2013
   Modification:新建文件
"""

import time
import logging, logging.handlers
import os

class DataRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """
    Class: DataRotatingFileHandler
    Description: 日志滚动处理
    Base: RotatingFileHandler
    Others: 无
    """

    def __init__(self, filename, mode='a', maxBytes=0,encoding=None, delay=0):
        """
        Method: __init__
        Description: 初始化
        Parameter: 
            filename: 日志文件名
            mode: 文件打开方式
            maxBytes: 日志最大值
            encoding: 日志编码
            delay: 
        Return: 无
        Others: 无
        """

        self.__original_maxbytes = maxBytes
        back_count = 0
        logging.handlers.RotatingFileHandler.__init__(self, filename , mode, maxBytes , back_count , encoding,delay)

    def doRollover(self):
        """
        Method: doRollover
        Description: 日志滚动处理
        Parameter: 无
        Return: 无
        Others: 无
        """

        if self.stream is not None:
            self.stream.close()
            self.stream = None
        current_time = time.strftime("%Y_%m_%d_%H_%M_%S" , time.localtime(time.time()))
        dfn = "%s_%s.log" % (self.baseFilename[:-4],current_time)

        try:
            os.rename(self.baseFilename, dfn)
        except Exception:
            self.maxBytes = int(self.maxBytes * 1.5)
            self.mode = 'a'
            self.stream = self._open()
            return

        if self.maxBytes>self.__original_maxbytes:
            self.maxBytes = self.__original_maxbytes 
        self.mode = 'w'
        self.stream = self._open()

