#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: ���ļ��ж�����һЩʵ�õĽӿ�
Others:      
Key Class&Method List: 
    1. ....
History: 
1. Date:2013-03-23
   Author:ACP2013
   Modification:�½��ļ�
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
    Description: ͨ����
    Others:
    """
    @classmethod
    def serialize(cls, data):
        """
        Method: serialize
        Description: ���л�MOC����
        Parameters:
            data: ����
        Return:
            cPickle��ʽ�ַ���
        Others:
        """
        if data is None:
            return None
        return cPickle.dumps(data)

    @classmethod
    def deserialize(cls, data):
        """
        Method: deserialize
        Description: �����л��ɶ���
        Parameters:
            data: cPickle�����ַ���
        Return:
            ����ʵ��
        Others:
        """
        if data is None:
            return None
        return cPickle.loads(data)

    @classmethod
    def load_mocs(cls, curdir, moc_instances):
        """
        Method: load_mocs
        Description: ע��MOC����
        Parameter:
            curdir: ��ǰ����MOC��������Ŀ¼
        Return:
            MOC����ʵ���б�
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
        Description: ע��MOC����
        Parameter:
            mit_manager: MIT
            moc_name: MOC������
            register: �Ƿ��½��MIT
        Return:
            MOC����ʵ��
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
        Description: ע��MOC����
        Parameter:
            mit_manager: MIT
            moc_name: MOC������
        Return:
        Others:
        """
        m = importlib.import_module(moc_name)
        moc_class = getattr(m, moc_name)
        mit_manager.regist_moc(moc_class, None)