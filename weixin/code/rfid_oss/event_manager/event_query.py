#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-01
Description: 事件查询处理类，负责事件查询请求和事件导出请求的处理
Others:      
Key Class&Method List: 
             1. EventQueryAndExportProcessor
History: 
1. Date:2012-11-01
   Author:ACP2013
   Modification:新建文件
"""


import mit
import err_code_mgr
import tracelog

class EventQueryAndExportProcessor():
    """
    Class: EventQueryAndExportProcessor
    Description: 事件查询请求和事件导出请求的处理,考虑到效率问题，需要使用SQL语句进行查询。目前只提供了SQLITE的SQL语句，后续再提供ORACLE的SQL语句
    Base: 
    Others: 
        __mit_manager，用于查询event信息
        __default_language，缺省语言
    """

    __SQLITE_EXPORT_SQL__ = """select tbl_Event.sequence_no, event_id, name, level, time, device_type, device_id, object_type, object_id , description, cause 
    from tbl_Event, tbl_EventDetail %s  Order by tbl_Event.sequence_no DESC """
    __SQLITE_QUERY_SQL__ = __SQLITE_EXPORT_SQL__  + " limit %d,%d"
    __SQLITE_COUNT_SQL__ = "select count(1) as record_count from tbl_Event, tbl_EventDetail %s "
    __SQLITE_WHERE_SQL__ = ' where tbl_Event.sequence_no = tbl_EventDetail.sequence_no '
    
    
    __ORACLE_EXPORT_SQL__ = """select tbl_Event."sequence_no" as "sequence_no", "event_id", 
    "name", "level", "time", "device_type", "device_id", "object_type", "object_id", "description", "cause" 
    from tbl_Event, tbl_EventDetail %s Order by tbl_Event."sequence_no" DESC """
    __ORACLE_QUERY_SQL__ = """select "sequence_no", "event_id", "name", "level", "time", "device_type", 
    "device_id", "object_type", "object_id", "description", "cause" 
    from ( select "sequence_no", "event_id", "name", "level", "time", "device_type", "device_id", "object_type", 
    "object_id", "description", "cause" , rownum as con from  ("""   + __ORACLE_EXPORT_SQL__   + """) where rownum >= %d )  where con <= %d """    
    __ORACLE_COUNT_SQL__ = "select count(1) as record_count from tbl_Event, tbl_EventDetail %s "
    __ORACLE_WHERE_SQL__ = ' where tbl_Event."sequence_no" = tbl_EventDetail."sequence_no" '
    
    def __init__(self, mit_manager, default_language):
        """
        Method: __init__
        Description: 对象初始化函数
        Parameter: 
            mit_manager: mit manager对象
            default_language: 缺省语言
        Return: 无
        Others: 
        """

        self.__mit_manager = mit_manager        
        self.__default_language = default_language    
        
    def query_event_from_db(self, event_query_request):
        """
        Method: query_event_from_db
        Description: 从数据库中查询event,通过注册的raw_select_event_from_db函数来直接通过查询语句查询结果
        Parameter: 
            event_query_request: 查询event的查询条件
        Return: RstCollector对象实例，包含查询后的记录
        Others: 
        """

        
        where_sqlite_sql, where_oracle_sql, params = self.__gen_where_sql(event_query_request.event_filter)
        
#        sql_str =  self.__SQLITE_QUERY_SQL__%(where_sql
#                                             , event_query_request.current_page*event_query_request.num_per_page
#                                             , event_query_request.num_per_page)
#        ret = self.__mit_manager.call_custom_function("raw_select_event_from_db", sql_str, params)
        
        multisql = mit.MultiSQL()
        sqlite_sql_str =  self.__SQLITE_QUERY_SQL__%(where_sqlite_sql
                                             , event_query_request.current_page*event_query_request.num_per_page
                                             , event_query_request.num_per_page)
        oracle_sql_str =  self.__ORACLE_QUERY_SQL__%(where_oracle_sql
                                             , event_query_request.current_page*event_query_request.num_per_page
                                             , event_query_request.num_per_page)
        
        multisql.set_sqlite_sql(sqlite_sql_str)
        multisql.set_oracle_sql(oracle_sql_str)        
        ret = self.__mit_manager.call_custom_function("raw_select_event_from_db", multisql, params)
        
        return ret
    
    def export_event_from_db(self, event_filter):        
        """
        Method: export_event_from_db
        Description: 从数据库中查询导出请求所需要的event，和查询请求的唯一区别是，导出时需要分页参数
        Parameter: 
            event_filter: 导出event的查询条件
        Return: RstCollector对象实例，包含查询后的记录
        Others: 
        """

        where_sqlite_sql, where_oracle_sql, params = self.__gen_where_sql(event_filter)        
#        sql_str =  self.__SQLITE_EXPORT_SQL__%where_sql
#                
#        ret = self.__mit_manager.call_custom_function("raw_select_event_from_db", sql_str, params)

        multisql = mit.MultiSQL()
        sqlite_sql_str =  self.__SQLITE_EXPORT_SQL__%where_sqlite_sql                                             
        oracle_sql_str =  self.__ORACLE_EXPORT_SQL__%where_oracle_sql                                             
        
        multisql.set_sqlite_sql(sqlite_sql_str)
        multisql.set_oracle_sql(oracle_sql_str)        
        ret = self.__mit_manager.call_custom_function("raw_select_event_from_db", multisql, params)
        
        return ret
    
    def count_event_from_db(self, event_filter):        
        """
        Method: count_event_from_db
        Description: 从数据库中查询记录总数，用于查询请求时的分页计算
        Parameter: 
            event_filter: 查询event的查询条件
        Return: RstCollector对象实例，包含记录总数。
        Others: 
        """

        where_sqlite_sql, where_oracle_sql, params = self.__gen_where_sql(event_filter)        
#        sql_str =  self.__SQLITE_COUNT_SQL__%where_sql
#                
#        ret = self.__mit_manager.call_custom_function("raw_select_event_from_db", sql_str, params)

        multisql = mit.MultiSQL()
        sqlite_sql_str =  self.__SQLITE_COUNT_SQL__%where_sqlite_sql                                             
        oracle_sql_str =  self.__ORACLE_COUNT_SQL__%where_oracle_sql                                             
        
        multisql.set_sqlite_sql(sqlite_sql_str)
        multisql.set_oracle_sql(oracle_sql_str)
          
        ret = self.__mit_manager.call_custom_function("raw_select_event_from_db", multisql, params)
        
        return ret
    
    def event_filter_list(self):
        """
        Method: event_filter_list
        Description: 查询出所有的查询过滤条件信息
        Parameter: 无
        Return: 
            event level list
            event device type list
            event object type list
        Others: 
        """

        level_set = set()
        device_type_set = set()
        object_type_set = set()
        records = self.__mit_manager.lookup_attrs('EventType', ['level', 'device_type', 'object_type'])                
        for record in records:            
            level_set.add(record[0])
            device_type_set.add(record[1])
            object_type_set.add(record[2])
        return list(level_set), list(device_type_set), list(object_type_set)
    
    @classmethod
    def raw_query(cls, mit_context, sql_str, params):
        """
        Method: raw_query
        Description: 向mit注册的用于执行SQL语句的函数
        Parameter: 
            mit_context: mit manager的mit_context对象
            sql_str: 需要执行的SQL语句
            params: SQL语句的参数
        Return: RstCollector对象，包含执行结果信息，和查询到的所有记录信息
        Others: 
        """

        rst = mit.RstCollector()
        try:                        
            records = mit_context.raw_select_ex(sql_str, params)
        except Exception, err:
            rst.set_err_code(err_code_mgr.ER_RAW_SELECT_EXCEPTION)
            rst.set_msg(err_code_mgr.get_error_msg(err_code_mgr.ER_RAW_SELECT_EXCEPTION, err=err))
            return rst
            
        rst.set_err_code(err_code_mgr.ER_SUCCESS)        
        rst.set_field('records', records)
        return rst
    
    def __gen_where_sql(self, event_filter):
        """
        Method: __gen_where_sql
        Description: 根据event_filter信息生成SQL语句
        Parameter: 
            event_filter: event查询过滤条件
        Return: SQL语句
        Others: 
        """

        where_sqlite_sql = EventQueryAndExportProcessor.__SQLITE_WHERE_SQL__
        where_oracle_sql = EventQueryAndExportProcessor.__ORACLE_WHERE_SQL__
        params = []
        index = 1
        
        if event_filter.language is None or event_filter.language=='':            
            event_filter.language = self.__default_language
        where_sqlite_sql += 'and tbl_EventDetail.language=?%d '%index
        where_oracle_sql += 'and tbl_EventDetail."language"=:%d '%index
        params.append(event_filter.language)
        index += 1
        
        if event_filter.event_id is not None and event_filter.event_id!='':
            where_sqlite_sql += 'and tbl_Event.event_id=?%d '%index
            where_oracle_sql += 'and tbl_Event."event_id"=:%d '%index
            params.append(event_filter.event_id)
            index += 1
        
        if event_filter.level is not None and event_filter.level!='':
            where_sqlite_sql += 'and tbl_Event.level=?%d '%index
            where_oracle_sql += 'and tbl_Event."level"=:%d '%index
            params.append(event_filter.level)
            index += 1
        
        if event_filter.start_time is not None and event_filter.start_time!=0:
            where_sqlite_sql += 'and tbl_Event.time_inner>=?%d '%index
            where_oracle_sql += 'and tbl_Event."time_inner">=:%d '%index
            params.append(event_filter.start_time)
            index += 1
        
        if event_filter.end_time is not None and event_filter.end_time!=0:
            where_sqlite_sql += 'and tbl_Event.time_inner<=?%d '%index
            where_oracle_sql += 'and tbl_Event."time_inner"<=:%d '%index
            params.append(event_filter.end_time)
            index += 1
        
        if event_filter.device_type is not None and event_filter.device_type!='':
            where_sqlite_sql += 'and tbl_Event.device_type=?%d '%index
            where_oracle_sql += 'and tbl_Event."device_type"=:%d '%index
            params.append(event_filter.device_type)
            index += 1
            
        if event_filter.device_id is not None and event_filter.device_id!='':
            where_sqlite_sql += 'and tbl_Event.device_id=?%d '%index
            where_oracle_sql += 'and tbl_Event."device_id"=:%d '%index
            params.append(event_filter.device_id)
            index += 1
        
        if event_filter.object_type is not None and event_filter.object_type!='':
            where_sqlite_sql += 'and tbl_Event.object_type=?%d '%index
            where_oracle_sql += 'and tbl_Event."object_type"=:%d '%index
            params.append(event_filter.object_type)
            index += 1
            
        if event_filter.object_id is not None and event_filter.object_id!='':
            where_sqlite_sql += 'and tbl_Event.object_id=?%d '%index
            where_oracle_sql += 'and tbl_Event."object_id"=:%d '%index
            params.append(event_filter.object_id)
            index += 1
        
        return where_sqlite_sql, where_oracle_sql, params
    