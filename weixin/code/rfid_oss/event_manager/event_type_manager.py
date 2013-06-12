#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-14
Description: 启动时加载EventType到内存中，便于event存储时的处理
Others:      
Key Class&Method List: 
             1. EventTypeManager
History: 
1. Date:2012-11-14
   Author:ACP2013
   Modification:新建文件
"""


class EventTypeManager():
    """
    Class: EventTypeManager
    Description: Event Type管理类，可以通过event id查询到event type和event type detail信息
    Base: 无
    Others: 
        __event_type_map，event_id到event_type的MAP
        __event_type_detail_map,（event_id，language)到event_type_datail的MAP
        __event_id_languages,event_id 到 [language] 的MAP
    """

    def __init__(self):
        """
        Method: __init__
        Description: 对象初始化函数
        Parameter: 无
        Return: 
        Others: 
        """

        
        #event_id作为key, event_type是value
        self.__event_type_map = {}
        
        #（event_id，language)的字符串作为key, event_type_datail是value
        self.__event_type_detail_map = {}
        
        #event_id作为key, language列表是value
        self.__event_id_languages = {}
    
    def load_event_type(self, mit_manager):
        """
        Method: load_event_type
        Description: 加载系统中所有的event type信息到map中
        Parameter: 
            mit_manager: 用于查询event type的mit manager对象
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
        Description: 通过event_id获取event_type
        Parameter: 
            event_id: event的标识
        Return: event_type对象
        Others: 
        """

        event_type = None
        if self.__event_type_map.has_key(event_id):
            event_type = self.__event_type_map[event_id]
        return event_type
    
    def get_event_id_languages(self, event_id):
        """
        Method: get_event_id_languages
        Description:通过event_id得到其支持的language的列表 
        Parameter: 
            event_id: event的标识
        Return: language的列表 
        Others: 
        """

        value = []
        if self.__event_id_languages.has_key(event_id) is True:
            value = self.__event_id_languages[event_id]
        return value        
    
    def get_event_type_detail_by_id_and_language(self, event_id, language):
        """
        Method: get_event_type_detail_by_id_and_language
        Description: 通过event_id和lanuage得到event_type_detail
        Parameter: 
            event_id: event的标识
            language: 语言
        Return: event_type_detail对象
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
        Description: 通过event_id得到 [event_type_detail]
        Parameter: 
            event_id: event的标识
        Return: [event_type_detail]
        Others: 
        """

        #是否考虑使用固定长度，性能好一点？
        details = []
        event_languages = self.get_event_id_languages(event_id)
        for language in event_languages:
            detail = self.get_event_type_detail_by_id_and_language(event_id, language)
            if detail is not None:
                details.append(detail)
                
        return details

