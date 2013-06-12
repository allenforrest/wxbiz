#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-21
Description: 本文件中实现了mit上下文类
Others:      
Key Class&Method List: 
             1. MitContext: mit上下文
History: 
1. Date:
   Author:
   Modification:
"""

import copy
import new
from _mit.mit_db_mgr import MitDbMgr
from _mit.db_contain import MocDbContain

from _mit.rule_engine import RuleEngine
from _mit.raw_data_moi import RawDataMoi
from _mit.reslut_collector import RstCollector



import err_code_mgr


ERR_MSG_MOC_NOT_REG = "MOC(%s) is not registed!"


class MitContext:
    """
    Class: MitContext
    Description: mit上下文
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
            __all_moc: 所有注册的MOC类
            __db_mgr: 数据库连接管理
            __rule_engine: 校验规则引擎
            __rst_collector: 结果收集器
            __complex_attr_type: 注册的复合属性定义
            __custom_functions: 注册的自定义函数
        """
        
        self.__all_moc = {}
        self.__db_mgr = MitDbMgr()
        self.__rule_engine = RuleEngine()
        self.__rst_collector = RstCollector()
        self.__complex_attr_type = {}
        self.__custom_functions = {} 
        self.__db_sync = True

    def set_db_sync(self, db_sync):
        self.__db_sync = db_sync

    def get_db_sync(self, db_sync):
        return self.__db_sync

    def regist_moc(self, moc, rule_class):
        """
        Method:    regist_moc
        Description: 注册MOC
        Parameter: 
            moc: MOC类
            rule_class: 与MOC匹配的规则校验类
        Return: 
        Others: 
        """

        wap_moc = new.classobj("wap_%s" % moc.__name__, (moc, ), {})
        wap_moc._mit_context = self
        wap_moc._rule_class = rule_class
        wap_moc._db_contain = MocDbContain(wap_moc, self.__db_mgr)
        
        self.__all_moc[moc.__name__] = wap_moc

    def regist_complex_attr_type(self, attr_type_class):
        """
        Method:    regist_complex_attr_type
        Description: 注册复合属性
        Parameter: 
            attr_type_class: 复合属性的类
        Return: 
        Others: 
        """

        self.__complex_attr_type[attr_type_class.__name__] = attr_type_class

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

                注: 若是在mit中通过MitContext调用自定义函数，其事务是有mit类来控制的
        """        

        self.__custom_functions[function_name] = (call_obj, is_need_tran)

    def get_custom_function(self, function_name):
        return self.__custom_functions.get(function_name, (None, None))
        
    
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

        call_obj, is_need_tran = self.__custom_functions.get(function_name, (None, None))
        if call_obj is None:
            raise Exception("custom function (%s) is not registed!" % function_name)

        call_obj(self, *args, **kw)
        
        
    def get_all_moc(self):
        """
        Method:    get_all_moc
        Description: 获取所有的MOC类
        Parameter: 无
        Return: 所有的MOC类
        Others: 
        """

        return self.__all_moc.copy()
        
    def get_moc(self, moc_name):
        """
        Method:    get_moc
        Description: 获取指定名称的MOC类
        Parameter: 
            moc_name: MOC名称
        Return: MOC类
        Others: 
        """

        return self.__all_moc.get(moc_name)

    def get_complex_attr_type(self, type_name):
        """
        Method:    get_complex_attr_type
        Description: 获取复合属性定义
        Parameter: 
            type_name: 复合属性定义的名称
        Return: 复合属性定义
        Others: 
        """

        return self.__complex_attr_type.get(type_name)
        

    def get_db_mgr(self):
        """
        Method:    get_db_mgr
        Description: 获取数据库连接管理的对象
        Parameter: 无
        Return: 数据库连接管理的对象
        Others: 
        """

        return self.__db_mgr

    def get_rule_engine(self):
        """
        Method:    get_rule_engine
        Description: 获取规则校验的引擎
        Parameter: 无
        Return: 规则校验的引擎
        Others: 
        """

        return self.__rule_engine

    def get_rst_collector(self):
        """
        Method:    get_rst_collector
        Description: 获取结果收集器
        Parameter: 无
        Return: 结果收集器
        Others: 
        """

        return self.__rst_collector

    def reset_rst_collect(self):
        """
        Method:    reset_rst_collect
        Description: 重置结果收集器
        Parameter: 无
        Return: 结果收集器
        Others: 
        """

           
        self.__rst_collector = RstCollector()

        return self.__rst_collector

    def release_rst_collect(self):
        """
        Method:    release_rst_collect
        Description: 销毁结果收集器
        Parameter: 无
        Return: 被消耗的结果收集器
        Others: 
        """

        tmp =  self.__rst_collector

        self.__rst_collector = None
        return tmp

    def __gen_instance_by_rdm(self, rdm, old_instance = None, olny_fill_keys = False):
        """
        Method:    __gen_instance_by_rdm
        Description: 根据rdm对象生成mit中MOC类的对象实例
        Parameter: 
            rdm: RawDataMoi的实例
            old_instance: 数据库中修改前的对象实例
            olny_fill_keys: 生成的MOC实例是否仅仅填充关键字
        Return: MOC类的对象实例
        Others: 
            当增加对象时，old_instance=None，olny_fill_keys=False
            当修改对象时，old_instance不为None，olny_fill_keys=False
            当删除对象时，old_instance=None，olny_fill_keys=True
        """

        if old_instance is None:
            moc = self.get_moc(rdm.get_moc_name())
            
            if moc is None:
                raise Exception(ERR_MSG_MOC_NOT_REG % rdm.get_moc_name())

            instance = moc()
            
        else:
            instance = copy.deepcopy(old_instance)

        keys, nonkeys = instance.get_attr_names()
        
        # 关键属性
        for attr in keys:
            try:
                setattr(instance, attr, getattr(rdm, attr))
            except:
                pass

        # 非关键属性
        if olny_fill_keys is False:
            for attr in nonkeys:
                try:
                    setattr(instance, attr, getattr(rdm, attr))
                except:
                    pass

        return instance


        
    def rdm_add(self, rdm):
        """
        Method:    rdm_add
        Description: 增加一个对象实例
        Parameter: 
            rdm: RawDataMoi的实例
        Return: 
        Others: 
        """
        
        instance = self.__gen_instance_by_rdm(rdm)
        moid = instance.get_moid()
        moc = self.get_moc(rdm.get_moc_name())

        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % rdm.get_moc_name())

        if moc._rule_class is None:
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_IS_READ_ONLY, mocname = rdm.get_moc_name())
            return
            
        # 判断对象是否已经存在
        if moc.get_db_contain().is_exist(moid):
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_ADD_CONFLICT, moid = moid)

            return 
        
        
        rule_obj = moc._rule_class(moc, self, self.__rule_engine)
        

        rule_obj.pre_add_obj(instance, rdm)
        rule_obj.pre_add_check(instance)

        # 对象写入DB
        moc.get_db_contain(self.__db_sync).add(instance)
        
        rule_obj.object_check(instance)
        rule_obj.class_check()
        rule_obj.asso_check(instance)
        rule_obj.post_add_check(instance)
        
        rule_obj.post_add_obj(instance, rdm)
        

    def rdm_mod(self, rdm):
        """
        Method:    rdm_mod
        Description: 修改一个对象实例
        Parameter: 
            rdm: RawDataMoi的实例
        Return: 
        Others: 
        """

        tmp_instance = self.__gen_instance_by_rdm(rdm, olny_fill_keys = True)
        moid = tmp_instance.get_moid()

        moc = self.get_moc(rdm.get_moc_name())

        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % rdm.get_moc_name())

        if moc._rule_class is None:
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_IS_READ_ONLY, mocname = rdm.get_moc_name())
            return
            
        # 获取数据库中的对象
        old_instance = moc.get_db_contain().lookup(moid)
        
        # 判断对象是否存在        
        if old_instance is None:
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_NOT_EXIST, moid = moid)
            return 

        # 根据rdm中的属性和数据库中的数据，生成一个新的对象
        new_instance = self.__gen_instance_by_rdm(rdm, old_instance)
                
        rule_obj = moc._rule_class(moc, self, self.__rule_engine)
        

        rule_obj.pre_mod_obj(new_instance, old_instance, rdm)
        rule_obj.pre_mod_check(new_instance, old_instance)

        # 对象写入DB
        moc.get_db_contain(self.__db_sync).mod(new_instance)
        
        rule_obj.object_check(new_instance)
        rule_obj.class_check()
        rule_obj.asso_check(new_instance)
        rule_obj.post_mod_check(new_instance, old_instance)
        
        rule_obj.post_mod_obj(new_instance, old_instance, rdm)
        

    def rdm_remove(self, rdm):
        """
        Method:    rdm_remove
        Description: 删除对象实例
        Parameter: 
            rdm: RawDataMoi的实例
        Return: 
        Others: 
        """

        tmp_instance = self.__gen_instance_by_rdm(rdm, olny_fill_keys = True)
        moid = tmp_instance.get_moid()
        moc = self.get_moc(rdm.get_moc_name())

        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % rdm.get_moc_name())

        if moc._rule_class is None:
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_IS_READ_ONLY, mocname = rdm.get_moc_name())
            return
            
        # 获取数据库中的对象
        old_instance = moc.get_db_contain().lookup(moid)
        
        # 判断对象是否已经存在
        if old_instance is None:
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_NOT_EXIST, moid = moid)
            return         
        
        rule_obj = moc._rule_class(moc, self, self.__rule_engine)
        

        rule_obj.pre_rmv_obj(old_instance, rdm)
        rule_obj.pre_rmv_check(old_instance)

        # 先删除子对象
        rule_obj.rmv_sub_objs(old_instance)

        # 对象写入DB
        moc.get_db_contain(self.__db_sync).remove(old_instance.get_moid())
        
        rule_obj.class_check()
        rule_obj.post_rmv_check(old_instance)
        
        rule_obj.post_rmv_obj(old_instance, rdm)

    def rdms_add(self, rdms):
        """
        Method:    rdms_add
        Description: 增加多个对象实例
        Parameter: 
            rdms: RawDataMoi的实例列表
        Return: 
        Others: 
        """
        for rdm in rdms:
            self.rdm_add(rdm)

    def rdms_mod(self, rdms):
        """
        Method:    rdms_mod
        Description: 修改一个对象实例
        Parameter: 
            rdms: RawDataMoi的实例
        Return: 
        Others: 
        """
        for rdm in rdms:
            self.rdm_mod(rdm)
            
    def rdms_remove(self, rdms):
        """
        Method:    rdms_remove
        Description: 删除一系列对象实例
        Parameter: 
            rdms: RawDataMoi的实例列表
        Return: 
        Others: 
        """
        for rdm in rdms:
            self.rdm_remove(rdm)

    def mod_complex_attr(self, moc_name, moid, **complex_attr_value):
        """
        Method:    mod_complex_attr
        Description: 修改复合属性
        Parameter: 
            moc_name: 被修改的MOC类的名称
            moid: 被修改的MOC的moid
            **complex_attr_value: 复合属性名称和属性值
        Return: 
        Others: 
        """

        moc = self.get_moc(moc_name)

        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % rdm.get_moc_name())

        if moc._rule_class is None:
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_IS_READ_ONLY, mocname = moc_name)
            return
            
        rule_obj = moc._rule_class(moc, self, self.__rule_engine)

        # 判断对象是否已经存在
        if not self.is_exist(moc_name, moid):
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_NOT_EXIST, moid = moid)
            return
            
        for attr_name, attr_value in complex_attr_value.iteritems():
            rule_obj.check_complex_attr(moid, attr_name, attr_value) 
            moc.get_db_contain(self.__db_sync).mod_complex_attr(moid, attr_name, attr_value)
            rule_obj.post_mod_complex_attr(moid, attr_name, attr_value) 
        
        
    def lookup(self, moc_name, moid, **key_attr_values):
        """
        Method:    lookup
        Description: 根据moid查找对象实例
        Parameter: 
            moc_name: MOC类的名称
            moid: 指定的moid
            key_attr_values:关键属性的值
        Return: 
            None: 指定的对象实例不存在
            非None: 查找到的对象实例
        Others: 
            如果指定了moid，那么就直接使用moid去查找，此时key_attr_values不再有任何作用
            如果没有指定moid，那么将使用key_attr_values构造moid，然后去查找
            如果通过key_attr_values查找，那么key_attr_values必须是全部的关键属性的值
        """
            
        moc = self.get_moc(moc_name)
        
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)


        instance = moc.get_db_contain().lookup(moid, **key_attr_values)

        return instance


    def find_objs(self, moc_name, order_by_sql = None, num_per_page=None, current_page=None, **conditions):
        """
        Method:    find_objs
        Description: 根据一组条件查找对象
        Parameter: 
            moc_name: 被查找的MOC的名称
            order_by_sql: 排序条件, 是MultiSQL实例
                      例如，按照name升序: order_by = "name"
                      例如，按照name降序+id升序: order_by = "name desc, id asc"
                      注意, oracle中，需要将字段名使用双引号包起来
            num_per_page:查询结果分页显示时，每页显示的记录数量 
            current_page:查询结果分页显示时，当前页的序号, 0表示第一页
            **conditions: 查找条件，形式如: 属性名=属性值
        Return: 符合条件的对象实例的列表
        Others: 
        """

        # 根据moc_name，得到MOC类，通过MOC类的MocDbContain，来查找

        moc = self.get_moc(moc_name)

        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)


        instances = moc.get_db_contain().find_objs(order_by_sql, num_per_page, current_page, **conditions)

        return instances



    def lookup_attrs(self, moc_name, attr_names, order_by_sql = None, num_per_page=None, current_page=None, **conditions):
        """
        Method:    lookup_attrs
        Description: 查询指定的属性
        Parameter: 
            moc_name: 被查找的MOC的名称
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

        # 根据moc_name，得到MOC类，通过MOC类的MocDbContain，来查找

        moc = self.get_moc(moc_name)

        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)

        rst = moc.get_db_contain().lookup_attrs(attr_names, order_by_sql, num_per_page, current_page, **conditions)

        return rst


    def find_objs_by_sql(self, moc_name, where_sql):
        """
        Method:    find_objs_by_sql
        Description: 根据SQL语句查询对象列表
        Parameter: 
            moc_name: 被查找的MOC的名称
            where_sql: MultiSQL实例, 定义了SQL语句的where子句，不包含where关键字
                    注意, oracle中，需要将字段名使用双引号包起来
        Return: 符合条件的对象实例列表
        Others: 
        """

        # 根据moc_name，得到MOC类，通过MOC类的MocDbContain，来查找

        moc = self.get_moc(moc_name)

        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)

        rst = moc.get_db_contain().find_objs_by_sql(where_sql)

        return rst

    
    
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

        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
        
        return  moc.get_db_contain().is_exist(moid, **key_attr_values)

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

        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
      
        return  moc.get_db_contain().count(**conditions)


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
        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
      
        return  moc.get_db_contain(self.__db_sync).remove_all()

        
        
    
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
        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
      
        return  moc.get_db_contain().get_attr_max_value(attr_name, **conditions)


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
        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
      
        return  moc.get_db_contain().get_attr_min_value(attr_name, **conditions)
        
    def raw_select(self, sql, *agrs, **kw):    
        """
        Method:    raw_select
        Description: 在数据库总执行一条SELECT语句，返回结果集
        Parameter: 
            sql: SQL语句
        Return: 数据库结果集
        Others: 不要利用该接口执行非查询的SQL，否则会导致cache、同步等问题
        """

        db_con = self.__db_mgr.get_active_db()
        rst = db_con.get_query().select(sql, *agrs, **kw)        
        return rst

    def raw_select_ex(self, multisql, *agrs, **kw):    
        """
        Method:    raw_select_ex
        Description: 在数据库总执行一条SELECT语句，返回结果集
        Parameter: 
            multi_sql: MultiSQL实例，存放了不同数据库系统的SQL语句
        Return: 数据库结果集
        Others: 不要利用该接口执行非查询的SQL，否则会导致cache、同步等问题
        """

        db_con = self.__db_mgr.get_active_db()

        dbms_type = db_con.get_dbms_type()
        sql = multisql.get_sql(dbms_type)

        rst = db_con.get_query().select(sql, *agrs, **kw)        
        return rst


    def raw_exec(self, moc_name, sql, *agrs, **kw):
        """
        Method:    raw_exec
        Description: 在数据库总执行一条非SELECT的SQL语句，返回结果集
        Parameter: 
            moc_name: 在sql中，将会发生修改的MOC的名字
            sql: SQL语句
        Return: 数据库结果集
        Others: 
            1) 不要利用该接口执行SELECT的语句，否则会导致cache、同步等问题
            2) 请正确指定moc_name，否则会导致cache、同步等问题
        """
        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)

        if moc.is_need_sync_to_ems():
            raise Exception("MOC(%s) is need sync to EMS, can not modify by raw_exec" % moc_name)
        
        db_con = self.__db_mgr.get_active_db()
        rst = db_con.get_query().execute(sql, *agrs, **kw)        
        return rst

        
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
        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
            
        if moc.is_need_sync_to_ems():
            raise Exception("MOC(%s) is need sync to EMS, can not modify by raw_exec" % moc_name)
            
        db_con = self.__db_mgr.get_active_db()

        dbms_type = db_con.get_dbms_type()
        sql = multisql.get_sql(dbms_type)
        
        rst = db_con.get_query().execute(sql, *agrs, **kw)        
        return rst
        

    def gen_rdm_by_instance(self, instance, **attr_values):
        """
        Method:    gen_rdm_by_instance
        Description: 根据MOC实例生成RawDataMoi实例
        Parameter: 
            instance: MOC实例
            **attr_values: 附加的属性值
        Return: RawDataMoi实例 
        Others: 如果指定了attr_values，那么在根据MOC实例生成RawDataMoi实例后，
                继续使用attr_values中的属性值设置到生成的RawDataMoi实例中
        """

        rdm = RawDataMoi(instance.get_moc_name(), **attr_values)

        keys, nonkeys = instance.get_attr_names()
        
        # 关键属性
        for attr in keys:
            if attr not in attr_values:
                setattr(rdm, attr, getattr(instance, attr))

        # 非关键属性
        for attr in nonkeys:
            if attr not in attr_values:
                setattr(rdm, attr, getattr(instance, attr))


        return rdm


    def gen_moid(self, moc_name, **key_attr_values):
        """
        Method:    gen_moid
        Description: 生成moid
        Parameter: 
            moc_name: MOC名称
            **key_attr_values: 关键属性的值
        Return: 
        Others: 
        """

        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)

        return moc.gen_moid(**key_attr_values)
        
