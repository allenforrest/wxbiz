#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: 本文件中定义了一些实用的接口
Others:      
Key Class&Method List: 
    1. ....
History: 
1. Date:2013-03-23
   Author:ACP2013
   Modification:新建文件
"""

import cPickle
import importlib
import os
import sys

import tracelog
import mit

class DBSyncUtil():
    """
    Class: DBSyncUtil
    Description: 通用类
    Others:
    """
    @classmethod
    def serialize(cls, data):
        """
        Method: serialize
        Description: 序列化MOC对象
        Parameters:
            data: 数据
        Return:
            cPickle格式字符串
        Others:
        """
        if data is None:
            return None
        return cPickle.dumps(data)

    @classmethod
    def deserialize(cls, data):
        """
        Method: deserialize
        Description: 反序列化成对象
        Parameters:
            data: cPickle编码字符串
        Return:
            对象实例
        Others:
        """
        if data is None:
            return None
        return cPickle.loads(data)

    @classmethod
    def load_mocs(cls, curdir, moc_instances):
        """
        Method: load_mocs
        Description: 注册MOC对象
        Parameter:
            curdir: 当前加载MOC对象所在目录
        Return:
            MOC对象实例列表
        Others:
        """
        sys.path.append(curdir)
        
        mocdir = os.path.join(curdir)
        for file_name in os.listdir(mocdir):
            pyfile = os.path.join(mocdir, file_name)
            if file_name[-3:].lower() == '.py' and os.path.isfile(pyfile) and file_name[0:2] != '__':
                moc_name = file_name.split('.')[0]                
                moc_class = cls.__load_moc(moc_name)
                if moc_class is not None:
                    moc_instances[moc_name] = moc_class                
                    tracelog.info('load moc object: %s' % moc_name)
                    
            elif os.path.isdir(pyfile):                
                cls.load_mocs(pyfile, moc_instances)
        

    @classmethod
    def __load_moc(cls, moc_name):
        """
        Method: load_moc
        Description: 注册MOC对象
        Parameter:
            mit_manager: MIT
            moc_name: MOC对象名
            register: 是否登陆到MIT
        Return:
            MOC对象实例
        Others:
        """
        try:
            m = importlib.import_module(moc_name)
            moc_class = getattr(m, moc_name, None)
            if moc_class is None:
                return None
            
            if moc_class.__IMC_SYNC_PRIORITY__ != mit.IMC_SYNC_NOT_SYNC:                
                return moc_class
                
        except Exception, e:
            tracelog.error('load moc(%s) failed.%s' % (moc_name, str(e)))

        return None

    @classmethod
    def register_moc(cls, mit_manager, moc_name):
        """
        Method: register_moc
        Description: 注册MOC对象
        Parameter:
            mit_manager: MIT
            moc_name: MOC对象名
        Return:
        Others:
        """
        m = importlib.import_module(moc_name)
        moc_class = getattr(m, moc_name)
        mit_manager.regist_moc(moc_class, None)