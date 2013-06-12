#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-23
Description: 
Others:      
Key Class&Method List: 
    1. ....
History: 
1. Date:2013-03-23
   Author:ACP2013
   Modification:新建文件
"""
import threading
import mit
import debug
import tracelog
import type_def

from db_operator import DBOperator
from db_sync_util import DBSyncUtil
from db_sync_base import DBSyncType, DBSyncOperationType


TABLE_PREFIX = 'tbl_'
EVENT_BATCH_COUNT = 100

class DBSyncEventManager:
    """
    Class: DBSyncEventManager
    Description: 同步对象管理类
    Others:
    """
    __OraSyncEvent = None
    __TABLE_NAME = ""
    __FIELDS = []
    
    @classmethod
    def __get_OraSyncEvent(cls):
        if cls.__OraSyncEvent is None:
            import moc_db_sync.OraSyncEvent
            
            cls.__OraSyncEvent = moc_db_sync.OraSyncEvent.OraSyncEvent            
            cls.__TABLE_NAME = '%s%s' % (TABLE_PREFIX, cls.__OraSyncEvent.get_moc_name())            
            cls.__FIELDS = cls.__OraSyncEvent.__ATTR_DEF__[:]

        return cls.__OraSyncEvent
            
    def __init__(self, connection):
        """
        Method: __init__
        Description: 对象初始化函数
        Parameter:
            connection: 数据库连接
        Return:
        Others:
        """
        self.__connection = connection

        # 触发初始化类
        self.__get_OraSyncEvent()
        

    def create_schema(self):
        """
        Method: create_schema
        Description: 创建表结构
        Parameter: 无
        Return: 
        Others: 
        """
        db_query = self.__connection.get_active_query()
        if DBOperator.check_table_exists(db_query, self.__TABLE_NAME):
            return
        fields = []
        for attr in self.__FIELDS:
            field = DBOperator.get_field_def(attr)
            fields.append(field)
        #创建递增序列
        sql = 'CREATE SEQUENCE user_sync.sync_id_seq START WITH 1 INCREMENT BY 1 MINVALUE 1'
        debug.info(sql)
        db_query.execute(sql)
        
        #创建同步表结构
        sql = 'CREATE TABLE user_sync.%s (%s)' % (self.__TABLE_NAME, ','.join(fields))
        debug.info(sql)
        db_query.execute(sql)

        # 创建主键
        sql = 'ALTER TABLE user_sync.%s ADD CONSTRAINT %s_PK PRIMARY KEY("id")' % (self.__TABLE_NAME, self.__TABLE_NAME)
        debug.info(sql)
        db_query.execute(sql)

        #授权给user_acp
        sql = 'GRANT ALL ON user_sync.%s TO user_acp' % self.__TABLE_NAME
        debug.info(sql)
        db_query.execute(sql)

        sql = 'GRANT ALL ON user_sync.sync_id_seq TO user_acp'
        debug.info(sql)
        db_query.execute(sql)

    def remove_schema(self):
        """
        Method: remove_schema
        Description: 删除表结构
        Parameter: 
        Return: 
        Others: 
        """
        db_query = self.__connection.get_active_query()
        if not DBOperator.check_table_exists(db_query, self.__TABLE_NAME):
            return

        sql = 'DROP SEQUENCE user_sync.sync_id_seq'
        debug.info(sql)
        db_query.execute(sql)

        sql = 'DROP TABLE user_sync.%s' % (self.__TABLE_NAME)
        debug.info(sql)
        db_query.execute(sql)

    def get_events(self):
        """
        Method: get_events
        Description: 取得数据同步Event
        Parameter: 无
        Return: 
        Others: 
        """

        sync_events = []
        db_query = self.__connection.get_active_query()
        with db_query:
            fields = []
            for attr in self.__FIELDS:
                fields.append('"%s"' % attr.name)
            sub_sql = 'SELECT %s FROM user_sync.%s ORDER BY "priority" DESC, "id" ASC' % (','.join(fields), self.__TABLE_NAME)
            sql = 'SELECT rownum, s.* FROM (%s) s WHERE rownum <= %d' % (sub_sql, EVENT_BATCH_COUNT)
            debug.info(sql)
            events_cursor = db_query.select_cursor(sql)
            debug.info('result: %d' % events_cursor.rowcount)
            for event in events_cursor:
                sync_event = self.__get_OraSyncEvent()()
                sync_event.from_db_record(event)
                sync_events.append(sync_event)
        return sync_events

    def get_total_num(self):
        """
        Method: get_total_num
        Description: 取得总记录数
        Parameter: 
        Return:
            总记录数
        Others: 
        """
        db_query = self.__connection.get_active_query()
        sql = 'SELECT COUNT(*) FROM user_sync.%s' % (self.__TABLE_NAME)
        records = db_query.select(sql)
        if (len(records) > 0):
            return records[0][0]
        return 0

    def remove_event(self, event):
        """
        Method: remove_event
        Description: 删除同步通知消息
        Parameter: 
            event: 同步消息
        Return: 
        Others: 
        """

        self.remove_event_by_id(event.id)

    def remove_event_by_id(self, id):
        """
        Method: remove_event_by_id
        Description: 删除同步通知消息
        Parameter: 
            id: 同步消息ID
        Return: 
        Others: 
        """
        db_query = self.__connection.get_active_query()
        sql = 'DELETE FROM user_sync.%s WHERE "id"=%d' % (self.__TABLE_NAME, id)
        debug.info(sql)
        db_query.execute(sql)

    def remove_events(self, ids):
        """
        Method: remove_events
        Description: 删除同步通知消息
        Parameter:
            ids: 同步通知消息ID列表
        Return: 
        Others: 
        """

        db_query = self.__connection.get_active_query()
        for id in ids:
            sql = 'DELETE FROM user_sync.%s WHERE "id"=%d' % (self.__TABLE_NAME, id)
            debug.info(sql)
            db_query.execute(sql)

    def remove_all_events(self):
        """
        Method: remove_all_events
        Description: 删除全部同步通知消息
        Parameter:
        Return: 
        Others: 
        """

        db_query = self.__connection.get_active_query()
        sql = 'DELETE FROM user_sync.%s' % (self.__TABLE_NAME)
        debug.info(sql)
        db_query.execute(sql)

    def _add_event(self, table, sync_type, priority, operation, data, condition = None):
        """
        Method: _add_event
        Description: 追加数据同步Event
        Parameter:
            table: 数据表
            sync_type: 同期类型
            priority: 同步优先级
            operation: 操作类型(INSERT/UPDATE/DELETE)
            data: 同步数据
            condition: 同步条件，INSERT的场合为空
        Return:
        Others:
        """
        tracelog.info('add sync event to database [table=%s]' % table)

        db_query = self.__connection.get_query()

        moc_sync_event = self.__get_OraSyncEvent()()
        moc_sync_event.target = table
        moc_sync_event.priority = priority
        moc_sync_event.type = sync_type
        moc_sync_event.operation = operation
        moc_sync_event.data = data
        moc_sync_event.condition = condition

        fields = []
        field_indexes = []
        i = 1
        for attr in self.__FIELDS:
            fields.append('"%s"' % attr.name)
            if attr.is_key is True:
                field_indexes.append('user_sync.sync_id_seq.nextval')
            else:
                field_indexes.append(':%d' % i)
                i = i + 1
        sql = "INSERT INTO user_sync.%s(%s) VALUES(%s)" % (self.__TABLE_NAME, ','.join(fields), ','.join(field_indexes))
        debug.info(sql)
        records = moc_sync_event.to_db_record_for_update()
        debug.info('records: %s' % records)
        db_query.execute(sql, records[:-1])
        tracelog.info('add sync event completed.')

    def add_full_event(self):
        """
        Method: _add_event
        Description: 追加全同步Event
        Parameter:
        Return:
        Others:
        """
        self._add_event(None, DBSyncType.FULL, 1000, 0, None)

    def add_insert_event(self, moc):
        """
        Method: _add_event
        Description: 追加数据同步Event
        Parameter:
            moc: MOC对象
        Return:
        Others:
        """
        if moc.__IMC_SYNC_PRIORITY__ == mit.IMC_SYNC_NOT_SYNC:
            return

        table = moc.get_moc_name()
        priority = moc.__IMC_SYNC_PRIORITY__
        operation = DBSyncOperationType.INSERT
        data = DBSyncUtil.serialize(moc.to_db_record())
        self._add_event(table, DBSyncType.INCREMENTAL, priority, operation, data, None)

    def add_update_event(self, moc):
        """
        Method: add_update_event
        Description: 更新数据同步Event
        Parameter:
            moc: MOC对象
        Return:
        Others:
        """
        if moc.__IMC_SYNC_PRIORITY__ == mit.IMC_SYNC_NOT_SYNC:
            return

        table = moc.get_moc_name()
        priority = moc.__IMC_SYNC_PRIORITY__
        operation = DBSyncOperationType.UPDATE
        data = DBSyncUtil.serialize(moc.to_db_record())
        condition = ("\"moid\" = '%s'" % moc.get_moid().replace("'", "''"))
        self._add_event(table, DBSyncType.INCREMENTAL, priority, operation, data, condition)

    def add_remove_event(self, moc):
        """
        Method: add_remove_event
        Description: 删除数据同步Event
        Parameter:
            moc: MOC对象
        Return:
        Others:
        """
        if moc.__IMC_SYNC_PRIORITY__ == mit.IMC_SYNC_NOT_SYNC:
            return

        table = moc.get_moc_name()
        priority = moc.__IMC_SYNC_PRIORITY__
        operation = DBSyncOperationType.DELETE
        condition = ("\"moid\" = '%s'" % moc.get_moid().replace("'", "''"))
        self._add_event(table, DBSyncType.INCREMENTAL, priority, operation, None, condition)

    def add_remove_all_event(self, moc):
        """
        Method: add_remove_event
        Description: 删除数据同步Event
        Parameter:
            moc: MOC对象
        Return:
        Others:
        """
        if moc.__IMC_SYNC_PRIORITY__ == mit.IMC_SYNC_NOT_SYNC:
            return

        table = moc.get_moc_name()
        priority = moc.__IMC_SYNC_PRIORITY__
        operation = DBSyncOperationType.DELETE
        self._add_event(table, DBSyncType.INCREMENTAL, priority, operation, None, None)