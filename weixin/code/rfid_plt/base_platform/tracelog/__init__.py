#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-26
Description: ��־��¼�Ľӿ�
Others: 
        Ĭ������£���־�������stdout
        ͨ��open����־�ļ�����ô��־�ͻ�������ļ���
Key Class&Method List: 
             1. ctrace_logger: �ļ���־�ļ�¼��
History: 
1. Date:
   Author:
   Modification:
"""


import logging, logging.handlers
import traceback
import os.path
import sys
import threading

import date_rotatingfilehandler

"""
ʹ��˵��
import tracelog


tracelog.open(logname, file_path)



tracelog.info("aaa")
tracelog.info("aaa")


tracelog.close()

"""
   

class ctrace_logger(logging.Logger):
    """
    Class: ctrace_logger
    Description: ����logging.Logger, ��ҪĿ����ȷ����־��¼�ӿڲ��׳��쳣
    Base: logging.Logger
    Others: 
    """

    def __init__(self, name):
        logging.Logger.__init__(self, name)
        
        self.setLevel(logging.DEBUG)

        self.handler = None

        #self.console_handler = None
        
        
        self.file_path = ''
        #self.name = ''



    def _log(self, level, msg, args, exc_info=None, extra=None):
        """
        Method:    _log
        Description: ���ػ����_log�����������쳣��ȷ���쳣����������쳣�������������ʧ��
        Parameter: 
            level: ��־�ļ���
            msg: ��־�ı���Ϣ
            args: ����
            exc_info: ��ǰ��ջ��Ϣ
            extra: ������Ϣ
        Return: 
        Others: 
        """

        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        # ȷ��д��־ʱ�������쳣��ͬʱ��������Ļ�ϴ�ӡ��msg
        try:
            if logging._srcfile:
                #IronPython doesn't track Python frames, so findCaller throws an
                #exception on some versions of IronPython. We trap it here so that
                #IronPython can use logging.
                try:
                    fn, lno, func = self.findCaller()
                except ValueError:
                    fn, lno, func = "(unknown file)", 0, "(unknown function)"
            else:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
            if exc_info:
                if not isinstance(exc_info, tuple):
                    exc_info = sys.exc_info()
            record = self.makeRecord(self.name, level, fn, lno, msg, args, exc_info, func, extra)
            self.handle(record)
            
        except:
            print "LOG EXCEPTION", msg
            traceback.print_exc(file=sys.stdout)
            
    def open(self, file_path):   
        """
        Method:    open
        Description: ����־�ļ�
        Parameter: 
            file_path: ��־�ļ�·��
        Return: 
        Others: ÿ���ļ���ŵ���־Ϊ2M������ͨ��max_file_count���Ƶ�ǰ��־���ܴ�С
        """

        self.close()

        self.file_path = file_path
        #self.name = name
        
        #self.logger = logging.getLogger(name)
#        self.handler = logging.handlers.RotatingFileHandler(
#                 file_path
#                , maxBytes=1024*1024*2
#                , backupCount=max_file_count)

        self.handler = date_rotatingfilehandler.DataRotatingFileHandler(
                 file_path
                , maxBytes=1024*1024*2)

        fmt = '\n%(asctime)s  %(levelname)s %(message)s [File:%(filename)s Function:%(funcName)s Line:%(lineno)d]'
        #fmt = '%(asctime)s  %(levelname)s %(message)s'
        formatter = logging.Formatter(fmt)
        self.handler.setFormatter(formatter)
        self.addHandler(self.handler)

        
    def close(self):
        """
        Method:    close
        Description: �ر���־�ļ�
        Parameter: ��
        Return: 
        Others:
        """

        if self.handler is None:
            return
            
        self.handler.flush()     
        self.handler.close()
        self.removeHandler(self.handler)
        
        self.handler = None
        #self.logger = None
        
logging.setLoggerClass(ctrace_logger)
#logging.basicConfig(level=logging.NOTSET)  #Ĭ�ϵ���WARNING



g_logger = None
g_print_lock = None

def _print_log(level, msg, *args, **kwargs):
    """
    Function: _print_log
    Description: ��stdout�����־
    Parameter: 
        msg: ��־�ı�
        *args: ��չ����(��δʹ��)
        **kwargs: ��չ����(��δʹ��)
    Return: 
    Others: 
    """
    global g_print_lock
    if g_print_lock is None:
        g_print_lock = threading.RLock()
        
    with g_print_lock:
        try:
            msg = msg.decode("utf-8")
        except:
            pass
            
        try:
            print level, msg
        except:
            pass
            
def _print_debug(msg, *args, **kwargs):

    _print_log("debug:", msg, *args, **kwargs)

def _print_info(msg, *args, **kwargs):
    _print_log("info:", msg, *args, **kwargs)

def _print_warning(msg, *args, **kwargs):
    _print_log("warning:", msg, *args, **kwargs)
    
def _print_error(msg, *args, **kwargs):
    _print_log("error:", msg, *args, **kwargs)
       
def _exception(msg, *args, **kwargs):    
    """
    Function: _exception
    Description: �������쳣ʱ��ͨ������������쳣��־��stdout
    Parameter: 
        msg: ��־�ı�
        *args: ��չ����(��δʹ��)
        **kwargs: ��չ����(��δʹ��)
    Return: 
    Others: 
    """

    global g_print_lock
    if g_print_lock is None:
        g_print_lock = threading.RLock()
        
    with g_print_lock:
        try:
            msg = msg.decode("utf-8")
        except:
            pass
            
        try:
            print msg
            print(traceback.format_exc())
        except:
            pass
    
debug       = _print_debug
info        = _print_info
warning     = _print_warning
error       = _print_error
exception   = _exception

def open(logname, file_path):
    """
    Function: open
    Description: ����־�ļ�
    Parameter: 
        logname: ��־�ļ�������
        file_path: �ļ���ŵ�Ŀ¼
    Return: 
    Others: 
    """

    global g_logger, debug, info, warning, error, exception

    close()

    g_logger = logging.getLogger(logname)   
    
    g_logger.open(file_path = file_path,)

    debug       = g_logger.debug
    info        = g_logger.info
    warning     = g_logger.warning
    error       = g_logger.error
    exception   = g_logger.exception

def get_logger():
    global g_logger
 
    return g_logger

def close():
    """
    Function: close
    Description: �ر���־�ļ�
    Parameter: 
    Return: 
    Others: �ر���־�ļ��󣬺�����־���������stdout
    """

    global g_logger, debug, info, warning, error, exception

    if g_logger is not None:
        g_logger.close()
        
        g_logger = None


    debug       = _print_debug
    info        = _print_info
    warning     = _print_warning
    error       = _print_error
    exception   = _exception


    

