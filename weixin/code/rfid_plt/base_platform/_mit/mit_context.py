#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-21
Description: ���ļ���ʵ����mit��������
Others:      
Key Class&Method List: 
             1. MitContext: mit������
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
    Description: mit������
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
            __all_moc: ����ע���MOC��
            __db_mgr: ���ݿ����ӹ���
            __rule_engine: У���������
            __rst_collector: ����ռ���
            __complex_attr_type: ע��ĸ������Զ���
            __custom_functions: ע����Զ��庯��
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
        Description: ע��MOC
        Parameter: 
            moc: MOC��
            rule_class: ��MOCƥ��Ĺ���У����
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
        Description: ע�Ḵ������
        Parameter: 
            attr_type_class: �������Ե���
        Return: 
        Others: 
        """

        self.__complex_attr_type[attr_type_class.__name__] = attr_type_class

    def regist_custom_function(self, function_name, call_obj, is_need_tran):
        """
        Method:    regist_custom_function
        Description: ע���Զ���ĺ���
        Parameter: 
            function_name: ��������
            call_obj: �������󣬻����������Ե��õĶ���
            is_need_tran: ��ͨ��mit��call_custom_function���øú���ʱ���Ƿ���ҪmitΪ
                         ��������ṩ����֧��
        Return: 
        Others: ��is_need_tranΪTrueʱ��mit���Զ��ڵ��ú�����ǰ����������
                �������û���׳��쳣�����Զ��ύ����
                
                ��is_need_tranΪTrueʱ��mit�����Զ��ڵ��ú�����ǰ����������
                ͨ�����ڲ�ѯ���ݣ�����Щ��Ҫ�ֶ���������ĳ���

                ע: ������mit��ͨ��MitContext�����Զ��庯��������������mit�������Ƶ�
        """        

        self.__custom_functions[function_name] = (call_obj, is_need_tran)

    def get_custom_function(self, function_name):
        return self.__custom_functions.get(function_name, (None, None))
        
    
    def call_custom_function(self, function_name, *args, **kw):
        """
        Method:    regist_custom_function
        Description: �����Զ���ĺ���
        Parameter: 
            function_name: 
            *args, **kw: ���ݸ��Զ��庯���Ĳ���
        Return: �����Զ��庯���ķ���ֵ
        Others: ����Զ��巽�������ڣ�����׳��쳣
                ����Զ��巽���׳����쳣����ô�쳣���׸�������
        """

        call_obj, is_need_tran = self.__custom_functions.get(function_name, (None, None))
        if call_obj is None:
            raise Exception("custom function (%s) is not registed!" % function_name)

        call_obj(self, *args, **kw)
        
        
    def get_all_moc(self):
        """
        Method:    get_all_moc
        Description: ��ȡ���е�MOC��
        Parameter: ��
        Return: ���е�MOC��
        Others: 
        """

        return self.__all_moc.copy()
        
    def get_moc(self, moc_name):
        """
        Method:    get_moc
        Description: ��ȡָ�����Ƶ�MOC��
        Parameter: 
            moc_name: MOC����
        Return: MOC��
        Others: 
        """

        return self.__all_moc.get(moc_name)

    def get_complex_attr_type(self, type_name):
        """
        Method:    get_complex_attr_type
        Description: ��ȡ�������Զ���
        Parameter: 
            type_name: �������Զ��������
        Return: �������Զ���
        Others: 
        """

        return self.__complex_attr_type.get(type_name)
        

    def get_db_mgr(self):
        """
        Method:    get_db_mgr
        Description: ��ȡ���ݿ����ӹ���Ķ���
        Parameter: ��
        Return: ���ݿ����ӹ���Ķ���
        Others: 
        """

        return self.__db_mgr

    def get_rule_engine(self):
        """
        Method:    get_rule_engine
        Description: ��ȡ����У�������
        Parameter: ��
        Return: ����У�������
        Others: 
        """

        return self.__rule_engine

    def get_rst_collector(self):
        """
        Method:    get_rst_collector
        Description: ��ȡ����ռ���
        Parameter: ��
        Return: ����ռ���
        Others: 
        """

        return self.__rst_collector

    def reset_rst_collect(self):
        """
        Method:    reset_rst_collect
        Description: ���ý���ռ���
        Parameter: ��
        Return: ����ռ���
        Others: 
        """

           
        self.__rst_collector = RstCollector()

        return self.__rst_collector

    def release_rst_collect(self):
        """
        Method:    release_rst_collect
        Description: ���ٽ���ռ���
        Parameter: ��
        Return: �����ĵĽ���ռ���
        Others: 
        """

        tmp =  self.__rst_collector

        self.__rst_collector = None
        return tmp

    def __gen_instance_by_rdm(self, rdm, old_instance = None, olny_fill_keys = False):
        """
        Method:    __gen_instance_by_rdm
        Description: ����rdm��������mit��MOC��Ķ���ʵ��
        Parameter: 
            rdm: RawDataMoi��ʵ��
            old_instance: ���ݿ����޸�ǰ�Ķ���ʵ��
            olny_fill_keys: ���ɵ�MOCʵ���Ƿ�������ؼ���
        Return: MOC��Ķ���ʵ��
        Others: 
            �����Ӷ���ʱ��old_instance=None��olny_fill_keys=False
            ���޸Ķ���ʱ��old_instance��ΪNone��olny_fill_keys=False
            ��ɾ������ʱ��old_instance=None��olny_fill_keys=True
        """

        if old_instance is None:
            moc = self.get_moc(rdm.get_moc_name())
            
            if moc is None:
                raise Exception(ERR_MSG_MOC_NOT_REG % rdm.get_moc_name())

            instance = moc()
            
        else:
            instance = copy.deepcopy(old_instance)

        keys, nonkeys = instance.get_attr_names()
        
        # �ؼ�����
        for attr in keys:
            try:
                setattr(instance, attr, getattr(rdm, attr))
            except:
                pass

        # �ǹؼ�����
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
        Description: ����һ������ʵ��
        Parameter: 
            rdm: RawDataMoi��ʵ��
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
            
        # �ж϶����Ƿ��Ѿ�����
        if moc.get_db_contain().is_exist(moid):
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_ADD_CONFLICT, moid = moid)

            return 
        
        
        rule_obj = moc._rule_class(moc, self, self.__rule_engine)
        

        rule_obj.pre_add_obj(instance, rdm)
        rule_obj.pre_add_check(instance)

        # ����д��DB
        moc.get_db_contain(self.__db_sync).add(instance)
        
        rule_obj.object_check(instance)
        rule_obj.class_check()
        rule_obj.asso_check(instance)
        rule_obj.post_add_check(instance)
        
        rule_obj.post_add_obj(instance, rdm)
        

    def rdm_mod(self, rdm):
        """
        Method:    rdm_mod
        Description: �޸�һ������ʵ��
        Parameter: 
            rdm: RawDataMoi��ʵ��
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
            
        # ��ȡ���ݿ��еĶ���
        old_instance = moc.get_db_contain().lookup(moid)
        
        # �ж϶����Ƿ����        
        if old_instance is None:
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_NOT_EXIST, moid = moid)
            return 

        # ����rdm�е����Ժ����ݿ��е����ݣ�����һ���µĶ���
        new_instance = self.__gen_instance_by_rdm(rdm, old_instance)
                
        rule_obj = moc._rule_class(moc, self, self.__rule_engine)
        

        rule_obj.pre_mod_obj(new_instance, old_instance, rdm)
        rule_obj.pre_mod_check(new_instance, old_instance)

        # ����д��DB
        moc.get_db_contain(self.__db_sync).mod(new_instance)
        
        rule_obj.object_check(new_instance)
        rule_obj.class_check()
        rule_obj.asso_check(new_instance)
        rule_obj.post_mod_check(new_instance, old_instance)
        
        rule_obj.post_mod_obj(new_instance, old_instance, rdm)
        

    def rdm_remove(self, rdm):
        """
        Method:    rdm_remove
        Description: ɾ������ʵ��
        Parameter: 
            rdm: RawDataMoi��ʵ��
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
            
        # ��ȡ���ݿ��еĶ���
        old_instance = moc.get_db_contain().lookup(moid)
        
        # �ж϶����Ƿ��Ѿ�����
        if old_instance is None:
            self.__rule_engine.check(False, err_code_mgr.ER_OBJECT_NOT_EXIST, moid = moid)
            return         
        
        rule_obj = moc._rule_class(moc, self, self.__rule_engine)
        

        rule_obj.pre_rmv_obj(old_instance, rdm)
        rule_obj.pre_rmv_check(old_instance)

        # ��ɾ���Ӷ���
        rule_obj.rmv_sub_objs(old_instance)

        # ����д��DB
        moc.get_db_contain(self.__db_sync).remove(old_instance.get_moid())
        
        rule_obj.class_check()
        rule_obj.post_rmv_check(old_instance)
        
        rule_obj.post_rmv_obj(old_instance, rdm)

    def rdms_add(self, rdms):
        """
        Method:    rdms_add
        Description: ���Ӷ������ʵ��
        Parameter: 
            rdms: RawDataMoi��ʵ���б�
        Return: 
        Others: 
        """
        for rdm in rdms:
            self.rdm_add(rdm)

    def rdms_mod(self, rdms):
        """
        Method:    rdms_mod
        Description: �޸�һ������ʵ��
        Parameter: 
            rdms: RawDataMoi��ʵ��
        Return: 
        Others: 
        """
        for rdm in rdms:
            self.rdm_mod(rdm)
            
    def rdms_remove(self, rdms):
        """
        Method:    rdms_remove
        Description: ɾ��һϵ�ж���ʵ��
        Parameter: 
            rdms: RawDataMoi��ʵ���б�
        Return: 
        Others: 
        """
        for rdm in rdms:
            self.rdm_remove(rdm)

    def mod_complex_attr(self, moc_name, moid, **complex_attr_value):
        """
        Method:    mod_complex_attr
        Description: �޸ĸ�������
        Parameter: 
            moc_name: ���޸ĵ�MOC�������
            moid: ���޸ĵ�MOC��moid
            **complex_attr_value: �����������ƺ�����ֵ
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

        # �ж϶����Ƿ��Ѿ�����
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
        Description: ����moid���Ҷ���ʵ��
        Parameter: 
            moc_name: MOC�������
            moid: ָ����moid
            key_attr_values:�ؼ����Ե�ֵ
        Return: 
            None: ָ���Ķ���ʵ��������
            ��None: ���ҵ��Ķ���ʵ��
        Others: 
            ���ָ����moid����ô��ֱ��ʹ��moidȥ���ң���ʱkey_attr_values�������κ�����
            ���û��ָ��moid����ô��ʹ��key_attr_values����moid��Ȼ��ȥ����
            ���ͨ��key_attr_values���ң���ôkey_attr_values������ȫ���Ĺؼ����Ե�ֵ
        """
            
        moc = self.get_moc(moc_name)
        
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)


        instance = moc.get_db_contain().lookup(moid, **key_attr_values)

        return instance


    def find_objs(self, moc_name, order_by_sql = None, num_per_page=None, current_page=None, **conditions):
        """
        Method:    find_objs
        Description: ����һ���������Ҷ���
        Parameter: 
            moc_name: �����ҵ�MOC������
            order_by_sql: ��������, ��MultiSQLʵ��
                      ���磬����name����: order_by = "name"
                      ���磬����name����+id����: order_by = "name desc, id asc"
                      ע��, oracle�У���Ҫ���ֶ���ʹ��˫���Ű�����
            num_per_page:��ѯ�����ҳ��ʾʱ��ÿҳ��ʾ�ļ�¼���� 
            current_page:��ѯ�����ҳ��ʾʱ����ǰҳ�����, 0��ʾ��һҳ
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ���������Ķ���ʵ�����б�
        Others: 
        """

        # ����moc_name���õ�MOC�࣬ͨ��MOC���MocDbContain��������

        moc = self.get_moc(moc_name)

        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)


        instances = moc.get_db_contain().find_objs(order_by_sql, num_per_page, current_page, **conditions)

        return instances



    def lookup_attrs(self, moc_name, attr_names, order_by_sql = None, num_per_page=None, current_page=None, **conditions):
        """
        Method:    lookup_attrs
        Description: ��ѯָ��������
        Parameter: 
            moc_name: �����ҵ�MOC������
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

        # ����moc_name���õ�MOC�࣬ͨ��MOC���MocDbContain��������

        moc = self.get_moc(moc_name)

        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)

        rst = moc.get_db_contain().lookup_attrs(attr_names, order_by_sql, num_per_page, current_page, **conditions)

        return rst


    def find_objs_by_sql(self, moc_name, where_sql):
        """
        Method:    find_objs_by_sql
        Description: ����SQL����ѯ�����б�
        Parameter: 
            moc_name: �����ҵ�MOC������
            where_sql: MultiSQLʵ��, ������SQL����where�Ӿ䣬������where�ؼ���
                    ע��, oracle�У���Ҫ���ֶ���ʹ��˫���Ű�����
        Return: ���������Ķ���ʵ���б�
        Others: 
        """

        # ����moc_name���õ�MOC�࣬ͨ��MOC���MocDbContain��������

        moc = self.get_moc(moc_name)

        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)

        rst = moc.get_db_contain().find_objs_by_sql(where_sql)

        return rst

    
    
    def is_exist(self, moc_name, moid = None, **key_attr_values):
        """
        Method:    is_exist
        Description: �ж϶���ʵ���Ƿ����
        Parameter: 
            moc_name: MOC������
            moid: ����ʵ����moid
            key_attr_values:�ؼ����Ե�ֵ
        Return: ����ʵ���Ƿ����
        Others: 
            ���ָ����moid����ô��ֱ��ʹ��moidȥ���ң���ʱkey_attr_values�������κ�����
            ���û��ָ��moid����ô��ʹ��key_attr_values����moid��Ȼ��ȥ����
            ���ͨ��key_attr_values���ң���ôkey_attr_values������ȫ���Ĺؼ����Ե�ֵ
        """

        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
        
        return  moc.get_db_contain().is_exist(moid, **key_attr_values)

    def count(self, moc_name, **conditions):
        """
        Method:    count
        Description: ͳ�Ʒ��������Ķ���ĸ���
        Parameter: 
            moc_name: MOC������
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ���������Ķ���ĸ���
        Others: 
        """

        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
      
        return  moc.get_db_contain().count(**conditions)


    def remove_all(self, moc_name):
        """
        Method:    remove_all
        Description: ɾ��ָ���Ķ�������м�¼
        Parameter: 
            moc_name: MOC������
        Return: 
        Others: 
            ע�⣬�����ʹ�ñ��ӿ�
                  ���ӿ�ֱ��ɾ��MOC�����м�¼���Ҳ���У�����ù���                  
        """
        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
      
        return  moc.get_db_contain(self.__db_sync).remove_all()

        
        
    
    def get_attr_max_value(self, moc_name, attr_name, **conditions):
        """
        Method:    get_attr_max_value
        Description: ��ȡ�������ֵ
        Parameter: 
            moc_name: MOC������
            attr_name: ���Ե�����
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ���������Ķ�������Ե����ֵ�����û�з��������Ķ����򷵻�None
        Others: 
        """
        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
      
        return  moc.get_db_contain().get_attr_max_value(attr_name, **conditions)


    def get_attr_min_value(self, moc_name, attr_name, **conditions):
        """
        Method:    get_attr_min_value
        Description: ��ȡ������Сֵ
        Parameter: 
            moc_name: MOC������
            attr_name: ���Ե�����
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ���������Ķ�������Ե���Сֵ�����û�з��������Ķ����򷵻�None
        Others: 
        """
        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)
      
        return  moc.get_db_contain().get_attr_min_value(attr_name, **conditions)
        
    def raw_select(self, sql, *agrs, **kw):    
        """
        Method:    raw_select
        Description: �����ݿ���ִ��һ��SELECT��䣬���ؽ����
        Parameter: 
            sql: SQL���
        Return: ���ݿ�����
        Others: ��Ҫ���øýӿ�ִ�зǲ�ѯ��SQL������ᵼ��cache��ͬ��������
        """

        db_con = self.__db_mgr.get_active_db()
        rst = db_con.get_query().select(sql, *agrs, **kw)        
        return rst

    def raw_select_ex(self, multisql, *agrs, **kw):    
        """
        Method:    raw_select_ex
        Description: �����ݿ���ִ��һ��SELECT��䣬���ؽ����
        Parameter: 
            multi_sql: MultiSQLʵ��������˲�ͬ���ݿ�ϵͳ��SQL���
        Return: ���ݿ�����
        Others: ��Ҫ���øýӿ�ִ�зǲ�ѯ��SQL������ᵼ��cache��ͬ��������
        """

        db_con = self.__db_mgr.get_active_db()

        dbms_type = db_con.get_dbms_type()
        sql = multisql.get_sql(dbms_type)

        rst = db_con.get_query().select(sql, *agrs, **kw)        
        return rst


    def raw_exec(self, moc_name, sql, *agrs, **kw):
        """
        Method:    raw_exec
        Description: �����ݿ���ִ��һ����SELECT��SQL��䣬���ؽ����
        Parameter: 
            moc_name: ��sql�У����ᷢ���޸ĵ�MOC������
            sql: SQL���
        Return: ���ݿ�����
        Others: 
            1) ��Ҫ���øýӿ�ִ��SELECT����䣬����ᵼ��cache��ͬ��������
            2) ����ȷָ��moc_name������ᵼ��cache��ͬ��������
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
        Description: �����ݿ���ִ��һ����SELECT��SQL��䣬���ؽ����
        Parameter: 
            moc_name: ��sql�У����ᷢ���޸ĵ�MOC������
            multisql: MultiSQLʵ��������˲�ͬ���ݿ�ϵͳ��SQL���
        Return: ���ݿ�����
        Others: 
            1) ��Ҫ���øýӿ�ִ��SELECT����䣬����ᵼ��cache��ͬ��������
            2) ����ȷָ��moc_name������ᵼ��cache��ͬ��������
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
        Description: ����MOCʵ������RawDataMoiʵ��
        Parameter: 
            instance: MOCʵ��
            **attr_values: ���ӵ�����ֵ
        Return: RawDataMoiʵ�� 
        Others: ���ָ����attr_values����ô�ڸ���MOCʵ������RawDataMoiʵ����
                ����ʹ��attr_values�е�����ֵ���õ����ɵ�RawDataMoiʵ����
        """

        rdm = RawDataMoi(instance.get_moc_name(), **attr_values)

        keys, nonkeys = instance.get_attr_names()
        
        # �ؼ�����
        for attr in keys:
            if attr not in attr_values:
                setattr(rdm, attr, getattr(instance, attr))

        # �ǹؼ�����
        for attr in nonkeys:
            if attr not in attr_values:
                setattr(rdm, attr, getattr(instance, attr))


        return rdm


    def gen_moid(self, moc_name, **key_attr_values):
        """
        Method:    gen_moid
        Description: ����moid
        Parameter: 
            moc_name: MOC����
            **key_attr_values: �ؼ����Ե�ֵ
        Return: 
        Others: 
        """

        moc = self.get_moc(moc_name)
        if moc is None:
            raise Exception(ERR_MSG_MOC_NOT_REG % moc_name)

        return moc.gen_moid(**key_attr_values)
        
