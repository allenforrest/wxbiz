#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-14
Description: ����ʱ����EventType���ڴ��У�����event�洢ʱ�Ĵ���
Others:      
Key Class&Method List: 
             1. EventTypeManager
History: 
1. Date:2012-11-14
   Author:ACP2013
   Modification:�½��ļ�
"""


class EventTypeManager():
    """
    Class: EventTypeManager
    Description: Event Type�����࣬����ͨ��event id��ѯ��event type��event type detail��Ϣ
    Base: ��
    Others: 
        __event_type_map��event_id��event_type��MAP
        __event_type_detail_map,��event_id��language)��event_type_datail��MAP
        __event_id_languages,event_id �� [language] ��MAP
    """

    def __init__(self):
        """
        Method: __init__
        Description: �����ʼ������
        Parameter: ��
        Return: 
        Others: 
        """

        
        #event_id��Ϊkey, event_type��value
        self.__event_type_map = {}
        
        #��event_id��language)���ַ�����Ϊkey, event_type_datail��value
        self.__event_type_detail_map = {}
        
        #event_id��Ϊkey, language�б���value
        self.__event_id_languages = {}
    
    def load_event_type(self, mit_manager):
        """
        Method: load_event_type
        Description: ����ϵͳ�����е�event type��Ϣ��map��
        Parameter: 
            mit_manager: ���ڲ�ѯevent type��mit manager����
        Return: 
        Others: 
        """

        rdms = mit_manager.rdm_find('EventType')
        for rdm in rdms:
            self.__event_type_map[rdm.event_id] = rdm
        
        rdms = mit_manager.rdm_find('EventTypeDetail')
        for rdm in rdms:
            key = repr((rdm.event_id, rdm.language))
            self.__event_type_map[key] = rdm
            
            if self.__event_id_languages.has_key(rdm.event_id) is not True:
                self.__event_id_languages[rdm.event_id] = []
            self.__event_id_languages[rdm.event_id].append(rdm.language)
    
    def get_event_type_by_id(self, event_id):
        """
        Method: get_event_type_by_id
        Description: ͨ��event_id��ȡevent_type
        Parameter: 
            event_id: event�ı�ʶ
        Return: event_type����
        Others: 
        """

        event_type = None
        if self.__event_type_map.has_key(event_id):
            event_type = self.__event_type_map[event_id]
        return event_type
    
    def get_event_id_languages(self, event_id):
        """
        Method: get_event_id_languages
        Description:ͨ��event_id�õ���֧�ֵ�language���б� 
        Parameter: 
            event_id: event�ı�ʶ
        Return: language���б� 
        Others: 
        """

        value = []
        if self.__event_id_languages.has_key(event_id) is True:
            value = self.__event_id_languages[event_id]
        return value        
    
    def get_event_type_detail_by_id_and_language(self, event_id, language):
        """
        Method: get_event_type_detail_by_id_and_language
        Description: ͨ��event_id��lanuage�õ�event_type_detail
        Parameter: 
            event_id: event�ı�ʶ
            language: ����
        Return: event_type_detail����
        Others: 
        """

        event_type_detail = None
        key = repr((event_id, language))
        if self.__event_type_map.has_key(key):
            event_type_detail = self.__event_type_map[key]
        return event_type_detail
    
    def get_event_type_details_by_id(self, event_id):
        """
        Method: get_event_type_details_by_id
        Description: ͨ��event_id�õ� [event_type_detail]
        Parameter: 
            event_id: event�ı�ʶ
        Return: [event_type_detail]
        Others: 
        """

        #�Ƿ���ʹ�ù̶����ȣ����ܺ�һ�㣿
        details = []
        event_languages = self.get_event_id_languages(event_id)
        for language in event_languages:
            detail = self.get_event_type_detail_by_id_and_language(event_id, language)
            if detail is not None:
                details.append(detail)
                
        return details

