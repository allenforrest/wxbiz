#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-18
Description: 本文件中实现了MOC数据库操作的功能类
Others:      
Key Class&Method List: 
             1. MocDbContain: MOC数据库操作的功能类
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
    Description: MOC数据库操作的功能类
    Base: 
    Others: 
    """

    """
    负责数据库的对象操作
    不与MocBase合在一起，可以动态地替换数据库，并且可以防止相关的接口被随意重载
    """
    def __init__(self, moc, db_mgr):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            moc: MOC类
            db_mgr: 数据库连接管理类
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
        # 注: 如果属性名与数据库关键词冲突，则返回的sql可能是不合法的
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
        Description: 增加一个MOC对象实例到数据库中
        Parameter: 
            instance: MOC对象实例
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
        Description: 修改一个对象实例
        Parameter: 
            instance: 对象实例
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
        Description: 删除一个对象实例
        Parameter: 
            moid: 对象的moid
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
        Description: 删除所有的对象实例
        Parameter: 
        Return: 
        Others: 
            注意，请谨慎使用本接口
                  本接口直接删除MOC的所有记录，且不会校验配置规则
        """
        
        db_con = self.__db_mgr.get_active_db()
        if self.get_db_sync() is True:
            DBSyncEventManager(db_con).add_remove_all_event(self.__moc)
        db_con.get_query().execute("delete from tbl_%s" % (self.__moc.__MOC_NAME__))
    
    def lookup(self, moid, **key_attr_values):
        """
        Method:    lookup
        Description: 查找执行的对象实例
        Parameter: 
            moid: 待查找的对象的moid
            key_attr_values:关键属性的值
        Return: 
            None: 对象实例
            非None: 指定的对象实例不存在            
        Others: 
            如果指定了moid，那么就直接使用moid去查找，此时key_attr_values不再有任何作用
            如果没有指定moid，那么将使用key_attr_values构造moid，然后去查找
            如果通过key_attr_values查找，那么key_attr_values必须是全部的关键属性的值
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
        Description: 获取分页查询的SQL语句
        Parameter: \
            dbms_type: 数据库系统的类型
            attr_names: 待查询的字段名列表
            where_sql: where子句
            order_by_sql: 排序条件，是MultiSQL实例
            num_per_page:查询结果分页显示时，每页显示的记录数量 
            current_page:查询结果分页显示时，当前页的序号, 0表示第一页
        Return: 增加了分页查询功能的查询语句
        Others:  
            分页查询，在sqlite中，使用limit N offset M
            
        　　在oracle中,如果想从表中取出按照某字段排序前M到N条记录
            SQL> select ID from
               (
                 select ID , rownum as con from
                 (
                  select ID from TestSort order by ID
                 )
                 where rownum <= 3 /*N值*/
               )
               where con >= 2; /*M 值*/
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
            
            # conzzzzz: 为了避免与其他字段重名
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
        Description: 根据一组属性的值查找对象实例
        Parameter: 
            order_by_sql: 排序条件，是MultiSQL实例
                      例如，按照name升序: order_by = "name"
                      例如，按照name降序+id升序: order_by = "name desc, id asc"
                      注意, oracle中，需要将字段名使用双引号包起来
            num_per_page:查询结果分页显示时，每页显示的记录数量 
            current_page:查询结果分页显示时，当前页的序号, 0表示第一页
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 符合查找条件的对象实例的列表
        Others: 
            如果MOC的属性中，有名称为"num_per_page"或"current_page"，那么不能使
            用该接口通过conditions查询数据，可以通过增加下划线前缀等方式改变属性
            名称
            
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
        Description: 查询指定的属性
        Parameter: 
            attr_names: 需要查询的属性名称
            order_by_sql: 排序条件, 是MultiSQL实例
                      例如，按照name升序: order_by = "name"
                      例如，按照name降序+id升序: order_by = "name desc, id asc"
                      注意, oracle中，需要将字段名使用双引号包起来
            num_per_page:查询结果分页显示时，每页显示的记录数量 
            current_page:查询结果分页显示时，当前页的序号, 0表示第一页
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 符合条件的对象实例的属性列表
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


        # 将复合类型的数据，转换为实际的对象
        for i, record in enumerate(rst):            
            record = list(record) # sqlite中，每行结果都是元组
            rst[i] = record
            
            for j, attr_type in complex_attrs:
                item = record[j]
                # oracle中，复合属性定义为clog类型了
                # item是cx_Oracle.LOB类型
                if item is not None and dbms_type == "oracle":
                    item = record[j].read()
                    
                record[j] = attr_type.deserialize(item) if item is not None else None
                
        return rst
        
    def find_objs_by_sql(self, where_sql):
        """
        Method:    find_objs_by_sql
        Description: 根据SQL语句查询对象列表
        Parameter: 
            where_sql: MultiSQL实例, 定义了SQL语句的where子句，不包含where关键字
                       注意, oracle中，需要将字段名使用双引号包起来
        Return: 符合条件的对象实例列表
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
        Description: 在数据库总执行一条SELECT语句，返回结果集
        Parameter: 
            sql: SQL语句
            *agrs: 参数列表
            **kw: 字典参数列表
        Return: 数据库结果集
        Others: 
        """

        db_con = self.__db_mgr.get_active_db()
        rst = db_con.get_query().select(sql, *agrs, **kw)        

        return rst

#    def raw_select_ex(self, sqls_map, *agrs, **kw):    
#        """
#        Method:    raw_select_ex
#        Description: 在数据库总执行一条SELECT语句，返回结果集
#        Parameter: 
#            sql: SQL语句的一个字典，key是数据库类型, 例如,oracle sqlite
#        Return: 数据库结果集
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
        Description: 判断对象实例是否存在
        Parameter: 
            moid: 对象实例的moid
            key_attr_values:关键属性的值
        Return: 对象实例是否存在
        Others: 
            如果指定了moid，那么就直接使用moid去查找，此时key_attr_values不再有任何作用
            如果没有指定moid，那么将使用key_attr_values构造moid，然后去查找
            如果通过key_attr_values查找，那么key_attr_values必须是全部的关键属性的值
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
        Description: 统计符合条件的对象的个数
        Parameter: 
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 符合条件的对象的个数
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
        Description: 获取属性最大值
        Parameter: 
            attr_name: 属性的名称
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 符合条件的对象的属性的最大值，如果没有符合条件的对象，则返回None
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
        Description: 获取属性最小值
        Parameter: 
            attr_name: 属性的名称
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 符合条件的对象的属性的最小值，如果没有符合条件的对象，则返回None
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
        Description: 修改复合属性
        Parameter: 
            moid: 对象实例的moid
            attr_name: 被修改的属性名
            attr_value: 属性值
        Return: 
        Others: 
        """

        """
        保存复合属性的值
        """

        attr_value_map = {"moid" : moid
                     , attr_name : attr_value.serialize() if attr_value is not None else None}
        
        # 根据MOC定义中的复合类型的属性，将数据转换为json格式，并且写入数据库
               
        
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
