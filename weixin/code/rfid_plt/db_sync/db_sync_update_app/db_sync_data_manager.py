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
import debug
import tracelog
import type_def
import cx_Oracle

from mit import MocAttrDef

from db_operator import DBOperator
from db_sync_util import DBSyncUtil
from db_sync_base import DBSyncType, DBSyncOperationType
from db_sync_base import DBSyncStatus

from dba.error import DBConnectError, DBQueryError

TABLE_PREFIX = 'tbl_'

class DBSyncDataManager:
    """
    Class: DBSyncDataManager
    Description: 同步对象管理类
    Others:
    """
    def __init__(self, app):
        """
        Method: __init__
        Description: 对象初始化函数
        Parameter: 
            app: 
        Return: 
        Others: 
        """

        self.__connection_pool = app.get_conn_pool()
        self.__DBCONN = app.get_connection_name()
        self.__moc_defs = {}

    def create_schemas(self, mocs, sync_object = True):
        """
        Method: create_schemas
        Description: 创建表结构
        Parameter: 
            mocs: MOC对象
            sync_object: 是否是同步对象
        Return: 
        Others: 
        """
        with self.__connection_pool.get_connection(self.__DBCONN) as db_conn:
            db_query = db_conn.get_active_query();
            for moc in mocs:
                self.create_schema(db_query, moc, sync_object)

    def remove_schema(self, db_query, moc):
        """
        Method: create_schema
        Description: 删除表结构
        Parameter:
            db_query: DB查询对象
        """
        moc_name = moc.get_moc_name()
        table_name = self.__moc_defs[moc_name]['TABLE_NAME']
        if not DBOperator.check_table_exists(db_query, table_name):
            return
        if DBOperator.check_table_exists(db_query, table_name):
            sql = 'DROP TABLE user_sync.%s' % (table_name)
            debug.info(sql)
            db_query.execute(sql)

    def create_schema(self, db_query, moc, sync_object):
        """
        Method: create_schema
        Description: 创建表结构
        Parameter:
            db_query: DB查询对象
            moc: MOC对象
            sync_object: 是否是同步对象
        Return: 
        Others: 
        """
        moc_name = moc.get_moc_name()
        if moc_name not in self.__moc_defs.keys():
            self.__moc_defs[moc_name] = {}
            self.__moc_defs[moc_name]['TABLE_NAME'] = '%s%s' % (TABLE_PREFIX, moc.get_moc_name())
            self.__moc_defs[moc_name]['FIELDS'] = []
            self.__moc_defs[moc_name]['FIELDS'].append(MocAttrDef(name = 'moid'
                                                              , is_key = True
                                                              , attr_type = type_def.TYPE_STRING
                                                              , max_len = 128))
            for attr in moc.__ATTR_DEF__:
                self.__moc_defs[moc_name]['FIELDS'].append(attr)

            if (sync_object is True):
                # 追加字段
                self.__moc_defs[moc_name]['FIELDS'].append(MocAttrDef(name = '_SYNC_SOURCE'
                                                              , is_key = False
                                                              , attr_type = type_def.TYPE_INT32
                                                              , max_len = 0))

        table_name = self.__moc_defs[moc_name]['TABLE_NAME']
        #self.remove_schema(db_query, moc)        
        if not DBOperator.check_table_exists(db_query, table_name):
            fields = []
            sql_indexes = []
            index_names = {}
            for attr in self.__moc_defs[moc_name]['FIELDS']:
                field = DBOperator.get_field_def(attr)
                fields.append(field)
                if attr.is_key is True:
                    index_name = 'idx_%s_%s' % (moc.get_moc_name(), attr.name)
                    index_name = index_name[0:20]
                    if index_name in index_names.keys():
                        index_names[index_name] = index_names[index_name] + 1
                    else:
                        index_names[index_name] = 1
                    index_name = '%s_%d' % (index_name, index_names[index_name])
                    sql_indexes.append('CREATE INDEX %s ON user_sync.%s("%s")' % (index_name
                                                                   , table_name
                                                                   , attr.name))
            sql = 'CREATE TABLE user_sync.%s (%s)' % (table_name, ','.join(fields))
            debug.info(sql)
            db_query.execute(sql)

            if sync_object is True:
                # 创建主键
                sql = 'ALTER TABLE user_sync.%s ADD CONSTRAINT %s_PK PRIMARY KEY("moid", "_SYNC_SOURCE")' % (table_name, table_name)
                debug.info(sql)
                db_query.execute(sql)
        
            for sql_index in sql_indexes:
                debug.info(sql_index)
                db_query.execute(sql_index)
            sql = 'GRANT ALL ON user_sync.%s TO user_acp' % table_name
            debug.info(sql)
            db_query.execute(sql)

    def sync_data(self, events, ne_id):
        """
        Method: sync_data
        Description: 同期数据表
        Parameters:
            events: 同步消息列表
            ne_id: 客户端ID
        """
        ret_code = DBSyncStatus.ERROR_SUCCESS
        try:
            ret_code = self._sync_data(events, ne_id)
            tracelog.info('sync data completed')
        except:
            tracelog.exception('sync data failed')
            ret_code = DBSyncStatus.ERROR_FAILED
        return ret_code

    def _sync_data(self, events, ne_id):
        """
        Method: _sync_data
        Description: 同期数据表
        Parameters:
            events: 同步消息列表
            ne_id: 客户端ID
        """
        ret_code = DBSyncStatus.ERROR_SUCCESS
        with self.__connection_pool.get_connection(self.__DBCONN) as db_conn:
            db_query = db_conn.get_active_query()
            for e in events:
                if e.target not in self.__moc_defs:
                    raise NameError('MOC(%s) was not found in specified folder.' % (e.target)) 
                elif e.operation == DBSyncOperationType.INSERT:
                    debug.info('insert data')
                    ret_code = self._add(db_query, e.target, e.data, ne_id)
                elif e.operation == DBSyncOperationType.UPDATE:
                    debug.info('update data')
                    ret_code = self._edit(db_query, e.target, e.data, e.condition, ne_id)
                elif e.operation == DBSyncOperationType.DELETE:
                    debug.info('remove data')
                    ret_code = self._delete(db_query, e.target, e.condition, ne_id)
                if ret_code != DBSyncStatus.ERROR_SUCCESS:
                    return ret_code
        return ret_code

    def _exists(self, db_query, table, data, ne_id):
        """
        Method: _exists
        Description: 检查记录是否存在
        """
        data = DBSyncUtil.deserialize(data)
        i = 1
        moid = None
        for attr in self.__moc_defs[table]['FIELDS']:
            if attr.name == 'moid':
                moid = data[i]
                break
            i = i + 1
        sql = 'SELECT * FROM user_sync.%s WHERE "moid"=:1 AND "_SYNC_SOURCE"=:2' % (self.__moc_defs[table]['TABLE_NAME'])
        debug.info(sql)
        records = db_query.select(sql, [moid, ne_id])
        if len(records) > 0:
            return True
        return False

    def _exists_with_condition(self, db_query, table, condition, ne_id):
        """
        Method: _exists_with_condition
        Description: 检查记录是否存在
        """
        if condition is None:
            return True
        sql = 'SELECT * FROM user_sync.%s WHERE %s AND "_SYNC_SOURCE"=:1' % (self.__moc_defs[table]['TABLE_NAME']
                                                                 , condition)
        debug.info('sql: %s, ne_id: %d' % (sql, ne_id))
        records = db_query.select(sql, [ne_id])
        if len(records) > 0:
            return True
        return False

    def _add(self, db_query, table, data, ne_id):
        """
        Method: _add
        Description: 追加记录
        Parameters:
            db_query: DB查询对象
            table: MOC名
            data: 数据
            ne_id: 客户端ID
        """
        data = DBSyncUtil.deserialize(data)
        fields = []
        field_indexes = []
        i = 1
        for attr in self.__moc_defs[table]['FIELDS']:
            if attr.name == '_SYNC_SOURCE':
                if i <= len(data):
                    data[i-1] = ne_id
                else:
                    data.append(ne_id)
            fields.append('"%s"' % attr.name)
            field_indexes.append(':%d' % i)
            i = i + 1
        sql = 'INSERT INTO user_sync.%s(%s) VALUES(%s)' % (self.__moc_defs[table]['TABLE_NAME']
                                                 ,','.join(fields)
                                                 ,','.join(field_indexes))
        debug.info(sql)
        debug.info(data)
        try:
            db_query.execute(sql, data)
        except DBQueryError, e:
            dberror = e.args[0]
            if issubclass(dberror.__class__, cx_Oracle.DatabaseError):
                error, = dberror.args
                # ORA-0001: unique constraint
                if error.code == 1:
                    tracelog.error('add conflict, full-sync will start')
                    return DBSyncStatus.ERROR_CONFLICT
            tracelog.exception('database error')
            return DBSyncStatus.ERROR_FAILED
        return DBSyncStatus.ERROR_SUCCESS

    def _edit(self, db_query, table, data, condition, ne_id):
        """
        Method: _edit
        Description: 更新记录
        Parameters:
            db_query: DB查询对象
            table: MOC名
            data: 数据
            condition: 更新条件
            ne_id: 客户端ID
        """
        data = DBSyncUtil.deserialize(data)
        fields = []
        i = 1
        for attr in self.__moc_defs[table]['FIELDS']:
            if attr.name == '_SYNC_SOURCE':
                if i <= len(data):
                    data[i-1] = ne_id
                else:
                    data.append(ne_id)
            fields.append('"%s"=:%d' % (attr.name, i))
            i = i + 1
        if condition is None:
            sql = 'UPDATE user_sync.%s SET %s' % (self.__moc_defs[table]['TABLE_NAME']
                                             ,','.join(fields))
        else:
            sql = 'UPDATE user_sync.%s SET %s WHERE %s' % (self.__moc_defs[table]['TABLE_NAME']
                                             ,','.join(fields)
                                             ,condition)
        debug.info(sql)
        debug.info(data)
        cursor = db_query.execute(sql, data)
        if cursor is not None and cursor.rowcount == 0:
            tracelog.error('update conflict, full-sync will start')
            return DBSyncStatus.ERROR_CONFLICT
        return DBSyncStatus.ERROR_SUCCESS

    def _delete(self, db_query, table, condition, ne_id):
        """
        Method: _delete
        Description: 删除记录
        Parameters:
            db_query: DB查询对象
            table: MOC名
            condition: 删除条件
            ne_id: 客户端ID
        """
        if condition is None:
            sql = 'DELETE FROM user_sync.%s' % (self.__moc_defs[table]['TABLE_NAME'])
        else:
            sql = 'DELETE FROM user_sync.%s WHERE %s' % (self.__moc_defs[table]['TABLE_NAME'], condition)
        debug.info(sql)
        cursor = db_query.execute(sql)
        if cursor is not None and cursor.rowcount == 0:
            tracelog.error('remove conflict, full-sync will start')
            return DBSyncStatus.ERROR_CONFLICT
        return DBSyncStatus.ERROR_SUCCESS
