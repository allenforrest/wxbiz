#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-24
Description: 本文件中实现了mit对外提供的接口类
Others:      
Key Class&Method List: 
             1. Mit: mit对外提供的接口类
History: 
1. Date:
   Author:
   Modification:
"""


import threading

from _mit import mit_context
from _mit import rule_exception

import err_code_mgr
import tracelog

# 对mit的操作，都通过Mit类来进行
# 而不是直接对模块进行操作，这样可以比较方便地在同一个进程中启动多个mit实例
# 后续开发中，要避免这些使得同一个进程中mit不能多实例化的做法:
#   1) 不要出现可以修改的类变量，否则同一个类无法再两个mit中同时使用
#   2) 不要出现模块级别的变量(常量可以)，否则两个mit会互相干扰


class NonLock:
    """
    Class: NonLock
    Description: 为了Mit的方法中使用锁的地方代码统一，无论是否加锁都不需要写两种代码
                而开发的假锁(不是真正的锁，不做任何事情)
    Base: 
    Others: 
    """
    def __enter__(self):
        pass
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass


class MitTran:
    """
    Class: MitTran
    Description: 为了使用mit事务提供with语法
    Base: 
    Others: 
    """
    
    def __init__(self, mit):
        """
        Method: 构造函数
        Description: 
        Parameter: 无
        Return: 
        Others: 
        """

        self.__mit = mit
        self.__has_rollback = False

    def __enter__(self):
        """
        Method: __enter__
        Description: 进入with语句
        Parameter: 无
        Return: 当前MitTran对象
        Others: 
        """
        self.__mit.begin_tran()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Method: __exit__
        Description: 退出with语句
        Parameter: 无
        Return: 
        Others: 如果有异常发送了，那么自动回滚事务；否则自动提交事务
        """
        if self.__has_rollback is True:
            return
            
        if exc_type is None:
            self.__mit.commit_tran()
        else:
            self.__mit.rollback_tran()
            
    def rollback(self):
        """
        Method: rollback
        Description: 回滚事务
        Parameter: 无
        Return: 
        Others: 
            如果rollback没有被调用，那么当with语句结束时将自动提交事务
        """
        self.__mit.rollback_tran()
        self.__has_rollback = True
        
        
class Mit:
    """
    Class: Mit
    Description: mit对外提供的接口类
    Base: 
    Others: 
    """


    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
            __context:mit的上下文
            __lock:对mit接口调用时加锁。如果同一个mit对象需要在多个线程中调用
                   那么需要通过init_mit_lock来初始化锁之后，才能保证线程安全
        Others: 
        """

        self.__context = mit_context.MitContext()
        self.__lock = NonLock()

        # 是否已经打开了事务
        self.__is_in_tran = False

    def set_db_sync(self, db_sync):
        self.__context.set_db_sync(db_sync)

    def get_db_sync(self, db_sync):
        return self.__context.get_db_sync()

    def close(self):
        """
        Method:    close
        Description: 关闭mit
        Parameter: 无
        Return: 
        Others: 
        """

        self.__context.get_db_mgr().close_all()


    def init_mit_lock(self):
        """
        Method:    init_mit_lock
        Description: 初始化锁
        Parameter: 无
        Return: 
        Others: 如果同一个mit对象需要在多个线程中调用
                那么需要通过init_mit_lock来初始化锁之后，才能保证线程安全
        """

        self.__lock = threading.RLock()

    def get_lock(self):
        """
        Method: get_lock
        Description: 获取mit的锁，用于一个mit对象被多个线程访问时使用
        Parameter: 无
        Return:
        Others: 
        """
        return self.__lock
        
    def regist_moc(self, moc, rule_class):
        """
        Method:    regist_moc
        Description: 注册MOC类
        Parameter: 
            moc: MOC类
            rule_class: 与MOC类匹配的规则校验类
        Return: 
        Others: 
            如果当前moc是只读的，那么rule_class可以为None
        """

        # 或者再开发一个model类，通过model可以是自动生成的，包含了所有的moc和asso
        # 这样可以一次性初始化mit中的模型
        with self.__lock:
            self.__context.regist_moc(moc, rule_class)

    def regist_complex_attr_type(self, attr_type_class):
        """
        Method:    regist_complex_attr_type
        Description: 注册复合类型的属性
        Parameter: 
            attr_type_class: 复合类型的属性定义
        Return: 
        Others: 
        """

        with self.__lock:
            self.__context.regist_complex_attr_type(attr_type_class)

        
    def regist_asso(self, asso):    
        """
        Method:    regist_asso
        Description: 注册关联关系
        Parameter: 
            asso: 关系定义
        Return: 
        Others: 
        """

        # TODO
        pass
        
        #self.__context.regist_asso(asso)
    

    def regist_custom_function(self, function_name, call_obj, is_need_tran):
        """
        Method:    regist_custom_function
        Description: 注册自定义的函数
        Parameter: 
            function_name: 函数名称
            call_obj: 函数对象，或者其他可以调用的对象
            is_need_tran: 当通过mit的call_custom_function调用该函数时，是否需要mit为
                         这个函数提供事务支持
        Return: 
        Others: 当is_need_tran为True时，mit会自动在调用函数的前后增加事务，
                如果函数没有抛出异常，则自动提交事务
                
                当is_need_tran为True时，mit不会自动在调用函数的前后增加事务，
                通常用于查询数据，或那些需要手动控制事务的场景

                注: 
                1)若是在mit中通过MitContext调用自定义函数，其事务是有mit类来控制的
                2)通过call_custom_function调用自定义函数时，内部传递给自定义参数的第一个参数，始终是MitContext对象
                
        """
        
        self.__context.regist_custom_function(function_name, call_obj, is_need_tran)
        
    def call_custom_function(self, function_name, *args, **kw):
        """
        Method:    regist_custom_function
        Description: 调用自定义的函数
        Parameter: 
            function_name: 
            *args, **kw: 传递给自定义函数的参数
        Return: 返回自定义函数的返回值
        Others: 如果自定义方法不存在，则会抛出异常
                如果自定义方法抛出了异常，那么异常会抛给调用者
        """
        
        with self.__lock:
            ret = None
            
            call_obj, is_need_tran = self.__context.get_custom_function(function_name)
            if call_obj is None:
                raise Exception("custom function (%s) is not registed!" % function_name)

            try:
                if is_need_tran is True:

                    # 如果mit不在事务中，那么就自动创建事务和提交事务
                    need_tran = not self.is_in_tran()
                    
                    if need_tran is True:
                        self.begin_tran()
                    else:
                        # 为了在规则校验失败的情况下，可以回滚掉已近修改的数据
                        # 自动创建savepoint
                        self.__create_savepoint("mit_innner_savepoint__")
                    
                ret = call_obj(self.__context, *args, **kw)            
                
            except:
                if is_need_tran is True:
                    if need_tran:
                        self.rollback_tran()
                    else:
                        self.__rollback_savepoint("mit_innner_savepoint__")
                        
                raise
                
            if is_need_tran is True:
                if need_tran:            
                    self.commit_tran()
                else:
                    self.__release_savepoint("mit_innner_savepoint__")
             
            return ret

    
    def gen_rdm(self, moc_name, **attr_values): 
        """
        Method:    gen_rdm
        Description: 根据属性的值，生成RawDataMoi实例
        Parameter: 
            moc_name: MOC的名称
            **attr_values: 属性的值
        Return: 
        Others: 
        """

        # rdm --- RawDataMoi的缩写
        moc = self.__context.get_moc(moc_name)

        if moc is None:
            return None
            
        
        instance = moc()
        rdm = self.__context.gen_rdm_by_instance(instance, **attr_values)

        return rdm

    def gen_moid(self, moc_name, **key_attr_values):
        """
        Method:    gen_moid
        Description: 根据关键属性的值生成moid
        Parameter: 
            moc_name: MOC的名称
            **key_attr_values: 关键属性的值
        Return: 
        Others: 
        """

        return  self.__context.gen_moid(moc_name, **key_attr_values)

        
    def __call_mod_data_method(self, method_name, *args, **kw):
        """
        Method:    __call_mod_data_method
        Description: 调用MitContext的增、删、改的方法
        Parameter: 
            method_name: 方法名称
            *args: 不定参
            **kw: 字典形式的不定参
        Return: 结果收集器
        Others: 
        """

        with self.__lock:
            rst_collect = self.__context.reset_rst_collect()
            
            try:

                # 如果mit不在事务中，那么就自动创建事务和提交事务
                need_tran = not self.is_in_tran()
                
                if need_tran is True:
                    self.begin_tran()
                else:
                    # 为了在规则校验失败的情况下，可以回滚掉已近修改的数据
                    # 自动创建savepoint
                    self.__create_savepoint("mit_innner_savepoint__")
                    
                getattr(self.__context, method_name)(*args, **kw)
            
            except rule_exception.RuleException, e:
                tracelog.exception("mit.%s(): rule check failed, err_code:%d, err_msg:%s, args:%s, kw:%s" % (
                                  method_name
                                , e.get_err_code()
                                , e.get_msg()
                                , str(args)
                                , str(kw)
                                ))
                rst_collect.set_err_code(e.get_err_code())
                rst_collect.set_msg(e.get_msg())
                
            except:
                tracelog.exception("mit.%s(): unknown exception" % method_name)
                rst_collect.set_err_code(err_code_mgr.ER_MIT_UNKNOWN_ERROR)
                rst_collect.set_msg("mit.%s(): unknown exception" % method_name)
            else:
                rst_collect.set_msg(err_code_mgr.get_error_msg(rst_collect.get_err_code()))


            self.__context.release_rst_collect()


            if need_tran:            
                if rst_collect.get_err_code() == 0:
                    self.commit_tran()
                else:
                    self.rollback_tran()
            else:
                if rst_collect.get_err_code() == 0:
                    self.__release_savepoint("mit_innner_savepoint__")
                else:
                    self.__rollback_savepoint("mit_innner_savepoint__")
             
            return rst_collect


    def rdm_add(self, rdm):
        """
        Method:    rdm_add
        Description: 增加一个对象实例
        Parameter: 
            rdm: RawDataMoi的实例
        Return: 
        Others: 
        """
        
        return self.__call_mod_data_method("rdm_add", rdm)

    def rdms_add(self, rdms):
        """
        Method:    rdm_add
        Description: 增加多个对象实例
        Parameter: 
            rdms: RawDataMoi的实例列表
        Return: 
        Others: 
        """
        
        return self.__call_mod_data_method("rdms_add", rdms)


    def rdm_mod(self, rdm):
        """
        Method:    rdm_mod
        Description: 修改一个对象实例
        Parameter: 
            rdm: RawDataMoi的实例
        Return: 
        Others: 
        """


        return self.__call_mod_data_method("rdm_mod", rdm)

    def rdms_mod(self, rdms):
        """
        Method:    rdms_mod
        Description: 修改一个对象实例
        Parameter: 
            rdms: RawDataMoi的实例
        Return: 
        Others: 
        """

        return self.__call_mod_data_method("rdms_mod", rdms)



    def rdm_remove(self, rdm):
        """
        Method:    rdm_remove
        Description: 删除一个对象实例
        Parameter: 
            rdm: RawDataMoi的实例
        Return: 
        Others: 
        """
        return self.__call_mod_data_method("rdm_remove", rdm)

    def rdms_remove(self, rdms):
        """
        Method:    rdm_remove
        Description: 删除多个对象实例
        Parameter: 
            rdms: RawDataMoi的实例列表
        Return: 
        Others: 
        """
        return self.__call_mod_data_method("rdms_remove", rdms)
        
    def remove_all(self, moc_name):
        """
        Method:    remove_all
        Description: 删除指定的对象的所有记录
        Parameter: 
            moc_name: MOC的名称
        Return: 
        Others: 
            注意，请谨慎使用本接口
                  本接口直接删除MOC的所有记录，且不会校验配置规则                  
        """
        return self.__call_mod_data_method("remove_all", moc_name)
        
    def rdm_lookup(self, moc_name, moid = None, **key_attr_values):
        """
        Method:    rdm_lookup
        Description: 根据moid查找对象实例
        Parameter: 
            moc_name: MOC的名称
            moid: 被查找的实例的moid
            key_attr_values:关键属性的值
        Return: RawDataMoi的实例
        Others: 
            如果指定了moid，那么就直接使用moid去查找，此时key_attr_values不再有任何作用
            如果没有指定moid，那么将使用key_attr_values构造moid，然后去查找
            如果通过key_attr_values查找，那么key_attr_values必须是全部的关键属性的值
        """

        with self.__lock:            
            obj = self.__context.lookup(moc_name, moid, **key_attr_values)

            if obj is None:
                return None

            return self.__context.gen_rdm_by_instance(obj)


    def rdm_find(self, moc_name, order_by_sql = None, num_per_page=None, current_page=None, **conditions):
        """
        Method:    rdm_find
        Description: 根据一组条件查找对象
        Parameter: 
            moc_name: MOC的名称
            order_by_sql: 排序条件, 是MultiSQL实例
                      例如，按照name升序: order_by = "name"
                      例如，按照name降序+id升序: order_by = "name desc, id asc"
                      注意, oracle中，需要将字段名使用双引号包起来
            num_per_page:查询结果分页显示时，每页显示的记录数量 
            current_page:查询结果分页显示时，当前页的序号, 0表示第一页
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 复合条件的RawDataMoi对象实例
        Others: 
        """

        with self.__lock: 
            objs = self.__context.find_objs(moc_name, order_by_sql, num_per_page, current_page, **conditions)

            rdms = [self.__context.gen_rdm_by_instance(obj) for obj in objs]

            return  rdms


    def lookup_attrs(self, moc_name, attr_names, order_by_sql = None, num_per_page=None, current_page=None, **conditions):
        """
        Method:    lookup_attrs
        Description: 查询符合条件的对象属性
        Parameter: 
            moc_name: MOC的名称
            attr_names: 期望查询的属性列表
            order_by_sql: 排序条件, 是MultiSQL实例
                      例如，按照name升序: order_by = "name"
                      例如，按照name降序+id升序: order_by = "name desc, id asc"
                      注意, oracle中，需要将字段名使用双引号包起来
            num_per_page:查询结果分页显示时，每页显示的记录数量 
            current_page:查询结果分页显示时，当前页的序号, 0表示第一页
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 符合条件的对象的属性值
        Others: 
        """

        with self.__lock:         
            return self.__context.lookup_attrs( moc_name, attr_names, order_by_sql, num_per_page, current_page, **conditions)

    def find_objs_by_sql(self, moc_name, where_sql):
        """
        Method:    find_objs_by_sql
        Description: 根据SQL语句查询对象实例
        Parameter: 
            moc_name: MOC的名称
            where_sql: 是MultiSQL实例, 定义了SQL语句的where子句，不包含where关键字
                       注意, oracle中，需要将字段名使用双引号包起来
        Return: 符合条件的RawDataMoi对象实例列表
        Others: 
        """

        with self.__lock:         
            return self.__context.find_objs_by_sql(moc_name, where_sql)

    def count(self, moc_name, **conditions):
        """
        Method:    count
        Description: 统计符合条件的对象的个数
        Parameter: 
            moc_name: MOC的名称
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 符合条件的对象的个数
        Others: 
        """

        with self.__lock:         
            return self.__context.count(moc_name, **conditions)

    def is_exist(self, moc_name, moid = None, **key_attr_values):
        """
        Method:    is_exist
        Description: 判断对象实例是否存在
        Parameter: 
            moc_name: MOC的名称
            moid: 对象实例的moid
            key_attr_values:关键属性的值
        Return: 对象实例是否存在
        Others: 
            如果指定了moid，那么就直接使用moid去查找，此时key_attr_values不再有任何作用
            如果没有指定moid，那么将使用key_attr_values构造moid，然后去查找
            如果通过key_attr_values查找，那么key_attr_values必须是全部的关键属性的值
        """

        with self.__lock:  
            return self.__context.is_exist(moc_name, moid, **key_attr_values)

    def get_attr_max_value(self, moc_name, attr_name, **conditions):
        """
        Method:    get_attr_max_value
        Description: 获取属性最大值
        Parameter: 
            moc_name: MOC的名称
            attr_name: 属性的名称
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 符合条件的对象的属性的最大值，如果没有符合条件的对象，则返回None
        Others: 
        """
        with self.__lock:  
            return self.__context.get_attr_max_value(moc_name, attr_name, **conditions)
            
    def get_attr_min_value(self, moc_name, attr_name, **conditions):
        """
        Method:    get_attr_min_value
        Description: 获取属性最小值
        Parameter: 
            moc_name: MOC的名称
            attr_name: 属性的名称
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 符合条件的对象的属性的最小值，如果没有符合条件的对象，则返回None
        Others: 
        """
        with self.__lock:  
            return self.__context.get_attr_min_value(moc_name, attr_name, **conditions)


    def raw_select_ex(self, multisql, *agrs, **kw):    
        """
        Method:    raw_select_ex
        Description: 在数据库总执行一条SELECT语句，返回结果集
        Parameter: 
            multi_sql: MultiSQL实例，存放了不同数据库系统的SQL语句
        Return: 数据库结果集
        Others: 不要利用该接口执行非查询的SQL，否则会导致cache、同步等问题
        """
        with self.__lock:  
            return self.__context.raw_select_ex(multisql, *agrs, **kw)

    def raw_exec_ex(self, moc_name, multisql, *agrs, **kw):
        """
        Method:    raw_exec_ex
        Description: 在数据库总执行一条非SELECT的SQL语句，返回结果集
        Parameter: 
            moc_name: 在sql中，将会发生修改的MOC的名字
            multisql: MultiSQL实例，存放了不同数据库系统的SQL语句
        Return: 数据库结果集
        Others: 
            1) 不要利用该接口执行SELECT的语句，否则会导致cache、同步等问题
            2) 请正确指定moc_name，否则会导致cache、同步等问题
        """
        
        return self.__call_mod_data_method("raw_exec_ex", moc_name, multisql, *agrs, **kw)


    def mod_complex_attr(self, moc_name, moid, **complex_attr_value):
        """
        Method:    mod_complex_attr
        Description: 修改复合类型属性
        Parameter: 
            moc_name: 被修改的MOC的名称
            moid: 被修改的对象实例的moid
            **complex_attr_value: 复合属性的值，形式如: 属性名=属性值，
                            其中属性值应该是SerializableObj派生类的对象实例
        Return: 
        Others: 
        """

        return self.__call_mod_data_method("mod_complex_attr", moc_name, moid, **complex_attr_value)


    def open_sqlite(self, db_file):
        """
        Method:    open_sqlite
        Description:  打开sqlite数据库
        Parameter: 
            db_file: sqlite数据库文件路径(可以是 :memory:)
        Return: 
        Others: 如果db_file是内存db，那么open后，数据库是空的，
                需要调用init_sqlite_db来创建对象表
        """

        with self.__lock:
            try:
                db_mgr = self.__context.get_db_mgr()
                db_mgr.open_sqlite("sqlite", db_file)

                self.init_sqlite_db()
            except:
                tracelog.exception("mit.open_sqlite failed. db_file:%s" % db_file)
                raise
      
    def init_sqlite_db(self):
        """
        Method:    init_sqlite_db
        Description: 初始化sqlite数据库
        Parameter: 无
        Return: 
        Others: 
        """

        db_mgr = self.__context.get_db_mgr()
        db_con = db_mgr.get_db_con("sqlite")
        if db_con is None:
            return 

        db_query = db_con.get_query()

        mocs = self.__context.get_all_moc()

        for moc in mocs.itervalues():
  
            keys, nonkeys = moc.get_attr_names()
            fields = ["moid"]
            fields += list(keys + nonkeys)

            # 创建表时，需要包含复合类型的属性
            fields += [attr.name for attr in moc.__COMPLEX_ATTR_DEF__]

            table_name = "tbl_" + moc.get_moc_name()
            
            sql = "create table if not exists %s (%s)" % (table_name, ",".join(fields))
                        
            db_query.execute(sql)
            db_query.execute("create index if not exists idx_%s_moid on %s(moid)" % (
                              table_name
                            , table_name))

            

            # 在关键字上创建索引
            if len(keys) > 0:
                db_query.execute("create index if not exists idx_%s_%s on %s(%s)" % (
                                  table_name
                                  , "_".join(keys)
                                , table_name
                                , ",".join(keys)))

            # 创建自定义的索引
            for attr_index in moc.__ATTR_INDEX__:
                db_query.execute("create index if not exists idx_%s_%s on %s(%s)" % (
                                  table_name
                                , "_".join(attr_index)
                                , table_name
                                , ",".join(attr_index)))
            
        
    def open_oracle(self, host="localhost"
                                , port=1521
                                , username="user_acp"
                                , password=""
                                , db="orcl"
                                , sysdba=False):
        """
        Method:    open_oracle
        Description: 打开Oracle数据库连接
        Parameter: 无
        Return: 
        Others: 
        """

        with self.__lock:
            try:
                db_mgr = self.__context.get_db_mgr()
                db_mgr.open_oracle("oracle", host, port, username, password, db, sysdba)
            except:
                tracelog.exception("mit.open_oracle failed. host:%s, port:%d, "
                                    "user:%s, db:%s, sysdba:%s" % (
                                      host
                                    , port
                                    , username
                                    , db
                                    , sysdba
                                    ))
                raise



    def is_in_tran(self):
        """
        Method:    is_in_tran
        Description: 判断mit是否启动了事务
        Parameter: 无
        Return: 
        Others: 
        """

        with self.__lock:
            return self.__is_in_tran
        
    def begin_tran(self):
        """
        Method:    begin_tran
        Description: 启动数据库事务
        Parameter: 无
        Return: 
        Others: 
        """

        with self.__lock:
            if self.__is_in_tran is True:
                raise Exception("Can not start new transaction when the mit is already in transaction")

                            
            db_con = self.__context.get_db_mgr().get_active_db()
            db_con.begin()

            self.__is_in_tran = True
        

    def rollback_tran(self):
        """
        Method:    rollback_tran
        Description: 回滚数据库事务
        Parameter: 无
        Return: 
        Others: 
        """

        with self.__lock:
            if self.__is_in_tran is False:
                raise Exception("Can not rollback transaction when the mit is not in transaction")

                            
            db_con = self.__context.get_db_mgr().get_active_db()
            db_con.rollback()

            self.__is_in_tran = False


    def commit_tran(self):
        """
        Method:    commit_tran
        Description: 提交数据库事务
        Parameter: 无
        Return: 
        Others: 
        """

        with self.__lock:
            if self.__is_in_tran is False:
                raise Exception("Can not commit transaction when the mit is not in transaction")

                            
            db_con = self.__context.get_db_mgr().get_active_db()
            db_con.commit()

            self.__is_in_tran = False
            
    def __create_savepoint(self, savepoint_name):
        """
        Method:    __create_savepoint
        Description: 创建保存点
        Parameter: 
            savepoint_name: 保存点名称
        Return: 
        Others: 
        """

        with self.__lock:
            db_con = self.__context.get_db_mgr().get_active_db()
            db_con.begin(savepoint_name)

    def __rollback_savepoint(self, savepoint_name):
        """
        Method:    __rollback_savepoint
        Description: 回滚保存点
        Parameter: 
            savepoint_name: 保存点名称
        Return: 
        Others: 
        """

        with self.__lock:
            db_con = self.__context.get_db_mgr().get_active_db()
            db_con.rollback(savepoint_name)

    def __release_savepoint(self, savepoint_name):
        """
        Method:    __release_savepoint
        Description: 释放保存点
        Parameter: 
            savepoint_name: 保存点名称
        Return: 
        Others: 
        """

        with self.__lock:
            db_con = self.__context.get_db_mgr().get_active_db()
            db_con.commit(savepoint_name)


