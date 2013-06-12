#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-18
Description: ���ļ���ʵ����MOC���ݿ�����Ĺ�����
Others:      
Key Class&Method List: 
             1. MocDbContain: MOC���ݿ�����Ĺ�����
History: 
1. Date:
   Author:
   Modification:
"""

from db_sync.db_sync_event_manager import DBSyncEventManager
from _mit.moc_attr_def import MocAttrDef, ComplexAttrDef

class MocDbContain:   
    """
    Class: MocDbContain
    Description: MOC���ݿ�����Ĺ�����
    Base: 
    Others: 
    """

    """
    �������ݿ�Ķ������
    ����MocBase����һ�𣬿��Զ�̬���滻���ݿ⣬���ҿ��Է�ֹ��صĽӿڱ���������
    """
    def __init__(self, moc, db_mgr):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            moc: MOC��
            db_mgr: ���ݿ����ӹ�����
        Return: 
        Others: 
        """

        self.__moc = moc
        self.__db_mgr = db_mgr
        self.__db_sync = False

    def set_db_sync(self, db_sync):
        self.__db_sync = db_sync

    def get_db_sync(self):
        return self.__db_sync

    def get_condition_sql(self, **conditions):
        # ע: ��������������ݿ�ؼ��ʳ�ͻ���򷵻ص�sql�����ǲ��Ϸ���
        if len(conditions) == 0:
            return ""
        
        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        if dbms_type == "sqlite":
            tmp = ["[%s] = :%s" % (k, k) for k in conditions.iterkeys()]
        elif dbms_type == "oracle":
            tmp = ["\"%s\" = :%s" % (k, k) for k in conditions.iterkeys()]
                           
        return " and ".join(tmp)
        

        
    def add(self, instance):
        """
        Method:    add
        Description: ����һ��MOC����ʵ�������ݿ���
        Parameter: 
            instance: MOC����ʵ��
        Return: 
        Others: 
        """

        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        if dbms_type == "sqlite":
            sql = self.__moc.__SQLITE_INSERT_SQL__
        elif dbms_type == "oracle":
            sql = self.__moc.__ORACLE_INSERT_SQL__

        record = instance.to_db_record()
        if self.get_db_sync() is True:
            DBSyncEventManager(db_con).add_insert_event(instance)
        db_con.get_query().execute(sql, record)
    
    def mod(self, instance):
        """
        Method:    mod
        Description: �޸�һ������ʵ��
        Parameter: 
            instance: ����ʵ��
        Return: 
        Others: 
        """

        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        if dbms_type == "sqlite":
            sql = self.__moc.__SQLITE_UPDATE_SQL__
        elif dbms_type == "oracle":
            sql = self.__moc.__ORACLE_UPDATE_SQL__

        record = instance.to_db_record_for_update()
       
        if self.get_db_sync() is True:
            DBSyncEventManager(db_con).add_update_event(instance)
        db_con.get_query().execute(sql, record)
    
    def remove(self, moid):
        """
        Method:    remove
        Description: ɾ��һ������ʵ��
        Parameter: 
            moid: �����moid
        Return: 
        Others: 
        """

        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        if dbms_type == "sqlite":
            sql = "delete from tbl_%s where moid = ?" % (self.__moc.__MOC_NAME__)
        elif dbms_type == "oracle":
            sql = 'delete from tbl_%s where "moid" = :1' % (self.__moc.__MOC_NAME__)

        if self.get_db_sync() is True:
            moc = self.lookup(moid)
            DBSyncEventManager(db_con).add_remove_event(moc)
        db_con.get_query().execute(sql, (moid,))

    def remove_all(self):
        """
        Method:    remove_all
        Description: ɾ�����еĶ���ʵ��
        Parameter: 
        Return: 
        Others: 
            ע�⣬�����ʹ�ñ��ӿ�
                  ���ӿ�ֱ��ɾ��MOC�����м�¼���Ҳ���У�����ù���
        """
        
        db_con = self.__db_mgr.get_active_db()
        if self.get_db_sync() is True:
            DBSyncEventManager(db_con).add_remove_all_event(self.__moc)
        db_con.get_query().execute("delete from tbl_%s" % (self.__moc.__MOC_NAME__))
    
    def lookup(self, moid, **key_attr_values):
        """
        Method:    lookup
        Description: ����ִ�еĶ���ʵ��
        Parameter: 
            moid: �����ҵĶ����moid
            key_attr_values:�ؼ����Ե�ֵ
        Return: 
            None: ����ʵ��
            ��None: ָ���Ķ���ʵ��������            
        Others: 
            ���ָ����moid����ô��ֱ��ʹ��moidȥ���ң���ʱkey_attr_values�������κ�����
            ���û��ָ��moid����ô��ʹ��key_attr_values����moid��Ȼ��ȥ����
            ���ͨ��key_attr_values���ң���ôkey_attr_values������ȫ���Ĺؼ����Ե�ֵ
        """

        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        if dbms_type == "sqlite":
            sql = self.__moc.__SQLITE_SELECT_SQL__ + ' where moid = ?'
        elif dbms_type == "oracle":
            sql = self.__moc.__ORACLE_SELECT_SQL__ + ' where "moid" = :1'

        if moid is None:
            moid = self.__moc.gen_moid(**key_attr_values)
        
        rst= db_con.get_query().select(sql, (moid,))
        if len(rst) > 0:     
            instance = self.__moc()
            instance.from_db_record(rst[0])
            return instance
        else:
            return None 

    def __get_query_sql(self, dbms_type, attr_names, where_sql, order_by_sql, num_per_page, current_page):
        """
        Method:    __get_page_sql
        Description: ��ȡ��ҳ��ѯ��SQL���
        Parameter: \
            dbms_type: ���ݿ�ϵͳ������
            attr_names: ����ѯ���ֶ����б�
            where_sql: where�Ӿ�
            order_by_sql: ������������MultiSQLʵ��
            num_per_page:��ѯ�����ҳ��ʾʱ��ÿҳ��ʾ�ļ�¼���� 
            current_page:��ѯ�����ҳ��ʾʱ����ǰҳ�����, 0��ʾ��һҳ
        Return: �����˷�ҳ��ѯ���ܵĲ�ѯ���
        Others:  
            ��ҳ��ѯ����sqlite�У�ʹ��limit N offset M
            
        ������oracle��,�����ӱ���ȡ������ĳ�ֶ�����ǰM��N����¼
            SQL> select ID from
               (
                 select ID , rownum as con from
                 (
                  select ID from TestSort order by ID
                 )
                 where rownum <= 3 /*Nֵ*/
               )
               where con >= 2; /*M ֵ*/
            ID
            ----------
                   2
                   3
        """

        if dbms_type == "sqlite":
            sql = "select %s from tbl_%s" % (",".join(attr_names), self.__moc.__MOC_NAME__)
            if len(where_sql) > 0:
                sql += " where " + where_sql

            if order_by_sql is not None:
                sql += " order by " + order_by_sql.get_sql(dbms_type)

            sql += " limit %d offset %d" % (num_per_page, num_per_page * current_page)
            return sql
            
        elif dbms_type == "oracle":
            select_sql = 'select "%s" ' % ('","'.join(attr_names))
            sql = select_sql + " from tbl_%s" % self.__moc.__MOC_NAME__

            if len(where_sql) > 0:
                sql += " where " + where_sql

            if order_by_sql is not None:
                sql += " order by " + order_by_sql.get_sql(dbms_type)

            max_row = num_per_page * (current_page + 1)
            min_row = (num_per_page * current_page) + 1
            
            # conzzzzz: Ϊ�˱����������ֶ�����
            sql = ("%s from "
                   " ("
                   "   %s, rownum as conzzzzz from "
                   "   ( %s ) "
                   "   where rownum <=%d "
                   " )"
                   " where conzzzzz >= %d") % (
                              select_sql
                            , select_sql
                            , sql
                            , max_row
                            , min_row)

        return sql


    def __get_all_attr_names(self):
        
        attr_names = ["moid"] + [attr.name for attr in self.__moc.__ATTR_DEF__]
        
        return attr_names
            
    
    def find_objs(self, order_by_sql = None, num_per_page=None, current_page=None, **conditions):
        """
        Method:    find_objs
        Description: ����һ�����Ե�ֵ���Ҷ���ʵ��
        Parameter: 
            order_by_sql: ������������MultiSQLʵ��
                      ���磬����name����: order_by = "name"
                      ���磬����name����+id����: order_by = "name desc, id asc"
                      ע��, oracle�У���Ҫ���ֶ���ʹ��˫���Ű�����
            num_per_page:��ѯ�����ҳ��ʾʱ��ÿҳ��ʾ�ļ�¼���� 
            current_page:��ѯ�����ҳ��ʾʱ����ǰҳ�����, 0��ʾ��һҳ
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ���ϲ��������Ķ���ʵ�����б�
        Others: 
            ���MOC�������У�������Ϊ"num_per_page"��"current_page"����ô����ʹ
            �øýӿ�ͨ��conditions��ѯ���ݣ�����ͨ�������»���ǰ׺�ȷ�ʽ�ı�����
            ����
            
        """

        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        where_sql = self.get_condition_sql(**conditions)   
        
        if num_per_page is None or current_page is None:
            if dbms_type == "sqlite":
                sql = self.__moc.__SQLITE_SELECT_SQL__
            elif dbms_type == "oracle":
                sql = self.__moc.__ORACLE_SELECT_SQL__

            if len(where_sql) > 0:
                sql += " where " + where_sql

            if order_by_sql is not None:
                sql += " order by " + order_by_sql.get_sql(dbms_type)
        else:
            attr_names = self.__get_all_attr_names()
            sql = self.__get_query_sql(dbms_type, attr_names, where_sql, order_by_sql, num_per_page, current_page)

        
        if len(where_sql) > 0:
            rst = db_con.get_query().select(sql, conditions)            
        else:
            rst = db_con.get_query().select(sql)
        
        objs = [self.__moc() for i in xrange(len(rst))]

        for i, record in enumerate(rst): 
            objs[i].from_db_record(record)
            
        return objs


    def lookup_attrs(self, attr_names, order_by_sql = None, num_per_page=None, current_page=None, **conditions):
        """
        Method:    lookup_attrs
        Description: ��ѯָ��������
        Parameter: 
            attr_names: ��Ҫ��ѯ����������
            order_by_sql: ��������, ��MultiSQLʵ��
                      ���磬����name����: order_by = "name"
                      ���磬����name����+id����: order_by = "name desc, id asc"
                      ע��, oracle�У���Ҫ���ֶ���ʹ��˫���Ű�����
            num_per_page:��ѯ�����ҳ��ʾʱ��ÿҳ��ʾ�ļ�¼���� 
            current_page:��ѯ�����ҳ��ʾʱ����ǰҳ�����, 0��ʾ��һҳ
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ���������Ķ���ʵ���������б�
        Others: 
        """
        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        where_sql = self.get_condition_sql(**conditions)    
        if num_per_page is None or current_page is None:
            if dbms_type == "sqlite":
                sql = "select %s from tbl_%s" % (",".join(attr_names), self.__moc.__MOC_NAME__)
            elif dbms_type == "oracle":
                sql = 'select "%s" from tbl_%s' % ('","'.join(attr_names), self.__moc.__MOC_NAME__)

            if len(where_sql) > 0:
                sql += " where " + where_sql

            if order_by_sql is not None:
                sql += " order by " + order_by_sql.get_sql(dbms_type)
        else:
            sql = self.__get_query_sql(dbms_type, attr_names, where_sql, order_by_sql, num_per_page, current_page)
          
        
        if len(where_sql) > 0:            
            rst = self.__raw_select(sql, conditions)
        else:            
            rst = self.__raw_select(sql)

        if len(rst) == 0:
            return rst
            
        complex_attrs = []
        for i, attr_name in enumerate(attr_names):
            attr_def = self.__moc.get_attr_def(attr_name)
            if isinstance(attr_def, ComplexAttrDef):
                attr_type = self.__moc.get_mit_context().get_complex_attr_type(attr_def.attr_type)
                if attr_type is None:
                    raise Exception("complex attribute type(%s) is not registed!" % attr_def.attr_type)
                complex_attrs.append((i, attr_type))

        if len(complex_attrs) == 0:
            return rst


        # ���������͵����ݣ�ת��Ϊʵ�ʵĶ���
        for i, record in enumerate(rst):            
            record = list(record) # sqlite�У�ÿ�н������Ԫ��
            rst[i] = record
            
            for j, attr_type in complex_attrs:
                item = record[j]
                # oracle�У��������Զ���Ϊclog������
                # item��cx_Oracle.LOB����
                if item is not None and dbms_type == "oracle":
                    item = record[j].read()
                    
                record[j] = attr_type.deserialize(item) if item is not None else None
                
        return rst
        
    def find_objs_by_sql(self, where_sql):
        """
        Method:    find_objs_by_sql
        Description: ����SQL����ѯ�����б�
        Parameter: 
            where_sql: MultiSQLʵ��, ������SQL����where�Ӿ䣬������where�ؼ���
                       ע��, oracle�У���Ҫ���ֶ���ʹ��˫���Ű�����
        Return: ���������Ķ���ʵ���б�
        Others: 
        """
        
    
        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        if dbms_type == "sqlite":
            sql = self.__moc.__SQLITE_SELECT_SQL__
        elif dbms_type == "oracle":
            sql = self.__moc.__ORACLE_SELECT_SQL__

        rst = db_con.get_query().select("%s where %s" % (sql, where_sql.get_sql(dbms_type)))        
        objs = [self.__moc() for i in xrange(len(rst))]

        for i, record in enumerate(rst):                        
            objs[i].from_db_record(record)
            
        return objs    
    
    def __raw_select(self, sql, *agrs, **kw):    
        """
        Method:    __raw_select
        Description: �����ݿ���ִ��һ��SELECT��䣬���ؽ����
        Parameter: 
            sql: SQL���
            *agrs: �����б�
            **kw: �ֵ�����б�
        Return: ���ݿ�����
        Others: 
        """

        db_con = self.__db_mgr.get_active_db()
        rst = db_con.get_query().select(sql, *agrs, **kw)        

        return rst

#    def raw_select_ex(self, sqls_map, *agrs, **kw):    
#        """
#        Method:    raw_select_ex
#        Description: �����ݿ���ִ��һ��SELECT��䣬���ؽ����
#        Parameter: 
#            sql: SQL����һ���ֵ䣬key�����ݿ�����, ����,oracle sqlite
#        Return: ���ݿ�����
#        Others: 
#        """
#
#        db_con = self.__db_mgr.get_active_db()
#
#        dbms_type = db_con.get_dbms_type()
#        sql = sqls_map.get(dbms_type)
#
#        if sql is None:
#            raise Exception("raw_select_ex(): %s not in sqls_map" % dbms_type)
#            
#        rst = db_con.select(sql, *agrs, **kw)        
#        return rst

    
    

    def is_exist(self, moid = None, **key_attr_values):
        """
        Method:    is_exist
        Description: �ж϶���ʵ���Ƿ����
        Parameter: 
            moid: ����ʵ����moid
            key_attr_values:�ؼ����Ե�ֵ
        Return: ����ʵ���Ƿ����
        Others: 
            ���ָ����moid����ô��ֱ��ʹ��moidȥ���ң���ʱkey_attr_values�������κ�����
            ���û��ָ��moid����ô��ʹ��key_attr_values����moid��Ȼ��ȥ����
            ���ͨ��key_attr_values���ң���ôkey_attr_values������ȫ���Ĺؼ����Ե�ֵ
        """
        if moid is None:
            moid = self.__moc.gen_moid(**key_attr_values)

        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        if dbms_type == "sqlite":
            sql = "select 1 from tbl_%s where moid = ?" % (self.__moc.__MOC_NAME__)
        elif dbms_type == "oracle":
            sql = "select 1 from tbl_%s where \"moid\" = :1" % (self.__moc.__MOC_NAME__)

        rst = db_con.get_query().select(sql, (moid,))        
        
        return len(rst) > 0

    def count(self, **conditions):
        """
        Method:    count
        Description: ͳ�Ʒ��������Ķ���ĸ���
        Parameter: 
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ���������Ķ���ĸ���
        Others: 
        """

        where_sql = self.get_condition_sql(**conditions)   
        
        if len(where_sql) > 0:
            sql = "select count(1) from tbl_%s where %s" % (self.__moc.__MOC_NAME__, where_sql)
            rst = self.__raw_select(sql, conditions)
        else:
            sql = "select count(1) from tbl_%s" % (self.__moc.__MOC_NAME__)
            rst = self.__raw_select(sql)
       
        return rst[0][0]
    


    def get_attr_max_value(self, attr_name, **conditions):
        """
        Method:    get_attr_max_value
        Description: ��ȡ�������ֵ
        Parameter: 
            attr_name: ���Ե�����
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ���������Ķ�������Ե����ֵ�����û�з��������Ķ����򷵻�None
        Others: 
        """
        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        if dbms_type == "sqlite":
            sql = "select max(%s) from tbl_%s"
                            
        elif dbms_type == "oracle":
            sql = 'select max("%s") from tbl_%s'
                            
        where_sql = self.get_condition_sql(**conditions)   
            
        if len(where_sql) > 0:
            sql += " where %s"
            sql = sql % ( attr_name
                        , self.__moc.__MOC_NAME__
                        , where_sql)                            
            rst = self.__raw_select(sql, conditions)
        else:
            sql = sql % (attr_name, self.__moc.__MOC_NAME__)
            rst = self.__raw_select(sql)
       
        return rst[0][0]

    def get_attr_min_value(self, attr_name, **conditions):
        """
        Method:    get_attr_min_value
        Description: ��ȡ������Сֵ
        Parameter: 
            attr_name: ���Ե�����
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ���������Ķ�������Ե���Сֵ�����û�з��������Ķ����򷵻�None
        Others: 
        """
        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        if dbms_type == "sqlite":
            sql = "select min(%s) from tbl_%s"
                            
        elif dbms_type == "oracle":
            sql = 'select min("%s") from tbl_%s'

            
        where_sql = self.get_condition_sql(**conditions)   
        
        if len(where_sql) > 0:
            sql += " where %s"
            sql = sql % (attr_name
                        , self.__moc.__MOC_NAME__
                        , where_sql)
                            
            rst = self.__raw_select(sql, conditions)
        else:
            sql = sql % (attr_name, self.__moc.__MOC_NAME__)
            rst = self.__raw_select(sql)
       
        return rst[0][0]

     
    def mod_complex_attr(self, moid, attr_name, attr_value):
        """
        Method:    mod_complex_attr
        Description: �޸ĸ�������
        Parameter: 
            moid: ����ʵ����moid
            attr_name: ���޸ĵ�������
            attr_value: ����ֵ
        Return: 
        Others: 
        """

        """
        ���渴�����Ե�ֵ
        """

        attr_value_map = {"moid" : moid
                     , attr_name : attr_value.serialize() if attr_value is not None else None}
        
        # ����MOC�����еĸ������͵����ԣ�������ת��Ϊjson��ʽ������д�����ݿ�
               
        
        db_con = self.__db_mgr.get_active_db()
        dbms_type = db_con.get_dbms_type()
        
        if dbms_type == "sqlite":
            sql = "update tbl_%s set %s=:%s  where moid=:moid" % (self.__moc.__MOC_NAME__, attr_name, attr_name)
        elif dbms_type == "oracle":
            sql = "update tbl_%s set \"%s\"=:%s  where \"moid\"=:moid" % (self.__moc.__MOC_NAME__, attr_name, attr_name)

        if self.get_db_sync() is True:
            moc = self.lookup(moid)
            DBSyncEventManager(db_con).add_update_event(moc)
        db_con.get_query().execute(sql, attr_value_map)
