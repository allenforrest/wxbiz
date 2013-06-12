#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-27
Description: 本文中实现了MOC的基类和校验规则的基类
Others:      
Key Class&Method List: 
             1. MocBase: MOC的基类
History:     2. MocRule: MOC的校验规则的基类
1. Date:
   Author:
   Modification:
"""

from _mit import const

    
class MocBase:
    """
    Class: MocBase
    Description: MOC的基类
    Base: 
    Others: 本类中的大部分属性和方法，都是需要子类重载的
    """

    # MOC的名称
    __MOC_NAME__ = ""

    # EAU->IMC同步的标识
    __IMC_SYNC_PRIORITY__ = const.IMC_SYNC_NOT_SYNC

    # 普通属性定义
    __ATTR_DEF__ = ()

    # 复合的属性定义
    __COMPLEX_ATTR_DEF__ =()

    # 属性定义的字典
    __ATTR_DEF_MAP__ = {}

    # 索引
    __ATTR_INDEX__ = ()

    # sqlite和Oracle的各种sql语句
    __SQLITE_SELECT_SQL__ = ''
    __ORACLE_SELECT_SQL__ = ''

    __SQLITE_INSERT_SQL__ = ''
    __ORACLE_INSERT_SQL__ = ''

    __SQLITE_UPDATE_SQL__ = ''
    __ORACLE_UPDATE_SQL__ = ''



    # 当对象是json格式存储在主表中的时候，_db_contain是None
    _db_contain = None
    _mit_context = None
    _rule_class = None  # 对应的MocRule类

    
    
    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
        """

        pass

    @classmethod
    def gen_moid(cls, **kw):
        """
        Method:    gen_moid
        Description: 给定关键属性的值，生成moid
        Parameter: 
            **kw: 关键属性的值
        Return: 
        Others: 需子类重载
        """

        return ""
        
    
    def get_moid(self):
        """
        Method:    get_moid
        Description: 获取当前对象的moid
        Parameter: 无
        Return: 
        Others: 
            moid是字符串类型，其形式为: XXXX_yyy_zzz
            其中，XXXX是__MOC_NAME__
                  yyy和zzz是关键属性的值。如果属性值是字符串，则需要使用单引号

            需子类重载
        """

        return ""

    @classmethod
    def get_moc_name(cls):
        """
        Method:    get_moc_name
        Description: 获取MOC的名称
        Parameter: 无
        Return: MOC的名称
        Others: 不需子类重载
        """

        return cls.__MOC_NAME__

    @classmethod
    def is_need_sync_to_ems(cls):
        """
        Method: is_need_sync_to_ems
        Description: 判断当前MOC是否需要数据同步到上层网管，例如IMC
        Parameter: 无
        Return:
        Others: 
        """
        return cls.__IMC_SYNC_PRIORITY__ != const.IMC_SYNC_NOT_SYNC
    
    @classmethod
    def get_attr_def(cls, attr_name):
        """
        Method:    get_attr_def
        Description: 获取属性定义
        Parameter: 
            attr_name: 属性的名称
        Return: 属性定义
        Others: 不需子类重载
        """

        return cls.__ATTR_DEF_MAP__.get(attr_name)
        
    @classmethod
    def get_db_contain(cls, db_sync = False):
        """
        Method:    get_db_contain
        Description: 获取操作当前MOC的数据库访问对象
        Parameter:
            db_sync: 是否要进行DB同步
        Return: 当前MOC的数据库访问对象
        Others: 不需子类重载
        """
        db_contain = cls._db_contain
        db_contain.set_db_sync(db_sync)
        return db_contain

    @classmethod
    def get_mit_context(cls):
        """
        Method:    get_mit_context
        Description: 获取mit的上下文
        Parameter: 无
        Return: mit的上下文
        Others: 不需子类重载
        """

        return cls._mit_context


    @classmethod
    def set_moc_rule(cls, moc_rule):
        """
        Method:    set_moc_rule
        Description: 设置MOC的校验规则类
        Parameter: 
            moc_rule: 校验规则类
        Return: 
        Others: 不需子类重载
        """

        cls._rule = moc_rule

    @classmethod
    def get_moc_rule(cls):
        """
        Method:    get_moc_rule
        Description: 获取MOC校验规则
        Parameter: 无
        Return: 
        Others: 不需子类重载
        """

        return cls._rule

    @classmethod
    def get_attr_names(cls):
        """
        Method:    get_attr_names
        Description: 获取属性的名称列表
        Parameter: 无
        Return: 属性的名称列表
        Others: 返回属性名称列表，分成两个部分，分别是关键字和非关键字属性列表
                需子类重载
        """

        # key, non key
        return (), ()

    #def get_attr_values(cls):
    #    # 与get_attr_names对应，这里返回的是属性的值
    #    return (), ()
        
    def from_db_record(self, record):
        """
        Method:    from_db_record
        Description: 根据一条数据库记录填充属性的值
        Parameter: 
            record: 数据库记录
        Return: 
        Others: 需子类重载
        """

        pass
        
    def to_db_record(self):
        """
        Method:    to_db_record
        Description: 根据属性构造一条可以插入数据库的记录
        Parameter: 无
        Return: 可以插入数据库的记录
        Others: 需子类重载
        """

        pass

    def to_db_record_for_update(self):
        """
        Method:    to_db_record
        Description: 根据属性构造一条可以update到数据库的记录
        Parameter: 无
        Return: 可以update到数据库的记录
        Others: 需子类重载
        """

        pass

    def from_binary(self):
        """
        Method:    from_binary
        Description: 
        Parameter: 无
        Return: 
        Others: 扩展的接口，暂时不使用
        """

        pass

    def to_binary(self):
        """
        Method:    to_binary
        Description: 
        Parameter: 无
        Return: 
        Others: 扩展的接口，暂时不使用
        """

        pass

        
class MocRule:
    """
    Class: MocRule
    Description: MOC校验规则的基类
    Base: 
    Others: 将MOC的定义和规则分开，可以实现统一MOC在不同的mit中的规则不一样
    """
    
    def __init__(self, moc, mit_context, rule_engine):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            moc: 绑定的MOC类
            mit_context: mit上下文
            rule_engine: 校验规则引擎
        Return: 
        Others: 
        """

        self._moc = moc
        self._mit_context = mit_context
        self._rule_engine = rule_engine


    ######################### 规则校验接口 begin #########################
    def get_moc(self, moc_name):
        """
        Method:    get_moc
        Description: 根据MOC的名称获取MOC类
        Parameter: 
            moc_name: MOC的名称
        Return: MOC类
        Others: 
            mit中，如果需要获取MOC类，不要通过import的方式来导入MOC类，
            而是通过get_moc()的方式来获取MOC类
        """

        return self._mit_context.get_moc(moc_name)


    def get_mit_context(self):
        """
        Method:    get_mit_context
        Description: 获取mit上下文
        Parameter: 无
        Return: mit上下文
        Others: 
        """

        return self._mit_context

    def check(self, is_True, err_code, **msg_paras):
        """
        Method:    check
        Description: 校验一个规则
        Parameter: 
            is_True: 规则条件是否满足，可以是一个bool值或者表达式
            err_code: 当is_True为False时，触发错误，err_code为错误码
            **msg_paras: 如果错误码中有动态参数，那么通过msg_paras来指定
        Return: 
        Others: 
        """

        self._rule_engine.check(is_True, err_code, **msg_paras)


    
    def class_check(self):
        """
        Method:    class_check
        Description: MOC类级别的校验规则
        Parameter: 无
        Return: 
        Others: 
        """

        pass

    def object_check(self, new_instance):
        """
        Method:    object_check
        Description: 当增加、修改对象时，针对对象本身进行规则检查
        Parameter: 
            new_instance: 增加或修改后的对象实例
        Return: 
        Others: 
        """
        self.check_attr_value(new_instance)
        

    def asso_check(self, new_instance):
        """
        Method:    asso_check
        Description: 当增加、修改对象时，针对对象关联关系进行规则检查
        Parameter: 
            new_instance: 增加或修改后的对象实例
        Return: 
        Others: 
        """

        pass


    
    def pre_add_check(self, new_instance):
        """
        Method:    pre_add_check
        Description: 增加对象前的校验规则
        Parameter: 
            new_instance: 增加的对象实例
        Return: 
        Others: 
        """

        pass
    
    def post_add_check(self, new_instance):
        """
        Method:    post_add_check
        Description: 增加对象后的校验规则
        Parameter: 
            new_instance: 增加的对象实例
        Return: 
        Others: 
        """

        pass
    
    def pre_mod_check(self, new_instance, old_instance):
        """
        Method:    pre_mod_check
        Description: 修改对象前的校验规则
        Parameter: 
            new_instance: 修改后的对象实例
            old_instance: 修改前的对象实例
        Return: 
        Others: 
        """

        pass

    def post_mod_check(self, new_instance, old_instance):
        """
        Method:    post_mod_check
        Description: 修改对象后的校验规则
        Parameter: 
            new_instance: 修改后的对象实例
            old_instance: 修改前的对象实例 
        Return: 
        Others: 
        """

        pass
    
    def pre_rmv_check(self, old_instance):
        """
        Method:    pre_rmv_check
        Description: 删除对象前的校验规则
        Parameter: 
            old_instance: 删除前的对象实例 
        Return: 
        Others: 
        """

        pass
    
    def post_rmv_check(self, old_instance):
        """
        Method:    post_rmv_check
        Description: 删除对象后的校验规则
        Parameter: 
            old_instance: 删除前的对象实例 
        Return: 
        Others: 
        """

        pass


    def check_attr_value(self, new_instance):
        """
        Method:    check_attr_value
        Description: 增加、修改对象前，校验对象的普通属性
        Parameter: 
            new_instance: 增加或修改后的对象实例
        Return: 
        Others: 
        """

        pass


    def check_complex_attr(self, moid, attr_name, attr_value):
        """
        Method:    check_complex_attr
        Description: 修改复合属性前，校验复合属性
        Parameter: 
            moid: 被修改的对象实例的moid
            attr_name: 被修改的属性的名称
            attr_value: 修改后的属性值
        Return: 
        Others: 
        """

        pass

    
    ######################### 规则校验接口 end #########################
    

    ####################### 联动修改接口 begin #########################
    

    #def alloc_resource(self, new_instance):
    #    """
    #    增加对象时，分配资源
    #    """
    #    pass
    #
    #def mod_resource(self, new_instance, old_instance):
    #    pass
    #
    #
    #def release_resource(self, old_instance):
    #    pass

    
    def pre_add_obj(self, new_instance, rdm):
        """
        Method:    pre_add_obj
        Description: 增加对象前，如果需要联动修改其他对象、分配资源等，则在这里处理
        Parameter: 
            new_instance: 增加的对象实例
            rdm: RawDataMoi实例
        Return: 
        Others: 
        """


        pass
        
    def post_add_obj(self, new_instance, rdm):
        """
        Method:    post_add_obj
        Description: 增加对象后，如果需要联动修改其他对象，则在这里处理
        Parameter: 
            new_instance: 增加的对象实例
            rdm: RawDataMoi实例
        Return: 
        Others: 
        """

        pass

        
    def pre_mod_obj(self, new_instance, old_instance, rdm):
        """
        Method:    pre_mod_obj
        Description: 修改对象前，如果需要联动修改其他对象，则在这里处理
        Parameter: 
            new_instance: 修改后的对象实例
            old_instance: 修改前的对象实例
            rdm: RawDataMoi实例
        Return: 
        Others: 
        """

        pass
        
    def post_mod_obj(self, new_instance, old_instance, rdm):
        """
        Method:    post_mod_obj
        Description: 修改对象后，如果需要联动修改其他对象，则在这里处理
        Parameter: 
            new_instance: 修改后的对象实例
            old_instance: 修改前的对象实例
            rdm: RawDataMoi实例
        Return: 
        Others: 
        """

        pass

        
    def pre_rmv_obj(self, old_instance, rdm):
        """
        Method:    pre_rmv_obj
        Description: 删除对象前，如果需要联动修改其他对象，则在这里处理
        Parameter: 
            old_instance: 删除前的对象实例
            rdm: RawDataMoi实例
        Return: 
        Others: 
        """

        pass    

    def post_rmv_obj(self, old_instance, rdm):
        """
        Method:    post_rmv_obj
        Description: 删除对象后，如果需要联动修改其他对象、释放资源等，则在这里处理
        Parameter: 
            old_instance: 删除前的对象实例
            rdm: RawDataMoi实例
        Return: 
        Others: 
        """

        pass


    def rmv_sub_objs(self, old_instance):
        """
        Method:    rmv_sub_objs
        Description: 删除子对象
        Parameter: 
            old_instance: 删除前的对象实例
        Return: 
        Others: 
        """

        pass



    def post_mod_complex_attr(self, moid, attr_name, attr_value):
        """
        Method:    post_mod_complex_attr
        Description: 修改完复合属性后，联动修改数据
        Parameter: 
            moid: 被修改的对象实例的moid
            attr_name: 被修改的属性的名称
            attr_value: 修改后的属性值
        Return: 
        Others: 
        """
    
        pass
    
    ####################### 联动修改接口 end #########################



    

    
