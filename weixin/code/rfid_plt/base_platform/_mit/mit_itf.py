#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-24
Description: ���ļ���ʵ����mit�����ṩ�Ľӿ���
Others:      
Key Class&Method List: 
             1. Mit: mit�����ṩ�Ľӿ���
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

# ��mit�Ĳ�������ͨ��Mit��������
# ������ֱ�Ӷ�ģ����в������������ԱȽϷ������ͬһ���������������mitʵ��
# ���������У�Ҫ������Щʹ��ͬһ��������mit���ܶ�ʵ����������:
#   1) ��Ҫ���ֿ����޸ĵ������������ͬһ�����޷�������mit��ͬʱʹ��
#   2) ��Ҫ����ģ�鼶��ı���(��������)����������mit�ụ�����


class NonLock:
    """
    Class: NonLock
    Description: Ϊ��Mit�ķ�����ʹ�����ĵط�����ͳһ�������Ƿ����������Ҫд���ִ���
                �������ļ���(�������������������κ�����)
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
    Description: Ϊ��ʹ��mit�����ṩwith�﷨
    Base: 
    Others: 
    """
    
    def __init__(self, mit):
        """
        Method: ���캯��
        Description: 
        Parameter: ��
        Return: 
        Others: 
        """

        self.__mit = mit
        self.__has_rollback = False

    def __enter__(self):
        """
        Method: __enter__
        Description: ����with���
        Parameter: ��
        Return: ��ǰMitTran����
        Others: 
        """
        self.__mit.begin_tran()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Method: __exit__
        Description: �˳�with���
        Parameter: ��
        Return: 
        Others: ������쳣�����ˣ���ô�Զ��ع����񣻷����Զ��ύ����
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
        Description: �ع�����
        Parameter: ��
        Return: 
        Others: 
            ���rollbackû�б����ã���ô��with������ʱ���Զ��ύ����
        """
        self.__mit.rollback_tran()
        self.__has_rollback = True
        
        
class Mit:
    """
    Class: Mit
    Description: mit�����ṩ�Ľӿ���
    Base: 
    Others: 
    """


    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
            __context:mit��������
            __lock:��mit�ӿڵ���ʱ���������ͬһ��mit������Ҫ�ڶ���߳��е���
                   ��ô��Ҫͨ��init_mit_lock����ʼ����֮�󣬲��ܱ�֤�̰߳�ȫ
        Others: 
        """

        self.__context = mit_context.MitContext()
        self.__lock = NonLock()

        # �Ƿ��Ѿ���������
        self.__is_in_tran = False

    def set_db_sync(self, db_sync):
        self.__context.set_db_sync(db_sync)

    def get_db_sync(self, db_sync):
        return self.__context.get_db_sync()

    def close(self):
        """
        Method:    close
        Description: �ر�mit
        Parameter: ��
        Return: 
        Others: 
        """

        self.__context.get_db_mgr().close_all()


    def init_mit_lock(self):
        """
        Method:    init_mit_lock
        Description: ��ʼ����
        Parameter: ��
        Return: 
        Others: ���ͬһ��mit������Ҫ�ڶ���߳��е���
                ��ô��Ҫͨ��init_mit_lock����ʼ����֮�󣬲��ܱ�֤�̰߳�ȫ
        """

        self.__lock = threading.RLock()

    def get_lock(self):
        """
        Method: get_lock
        Description: ��ȡmit����������һ��mit���󱻶���̷߳���ʱʹ��
        Parameter: ��
        Return:
        Others: 
        """
        return self.__lock
        
    def regist_moc(self, moc, rule_class):
        """
        Method:    regist_moc
        Description: ע��MOC��
        Parameter: 
            moc: MOC��
            rule_class: ��MOC��ƥ��Ĺ���У����
        Return: 
        Others: 
            �����ǰmoc��ֻ���ģ���ôrule_class����ΪNone
        """

        # �����ٿ���һ��model�࣬ͨ��model�������Զ����ɵģ����������е�moc��asso
        # ��������һ���Գ�ʼ��mit�е�ģ��
        with self.__lock:
            self.__context.regist_moc(moc, rule_class)

    def regist_complex_attr_type(self, attr_type_class):
        """
        Method:    regist_complex_attr_type
        Description: ע�Ḵ�����͵�����
        Parameter: 
            attr_type_class: �������͵����Զ���
        Return: 
        Others: 
        """

        with self.__lock:
            self.__context.regist_complex_attr_type(attr_type_class)

        
    def regist_asso(self, asso):    
        """
        Method:    regist_asso
        Description: ע�������ϵ
        Parameter: 
            asso: ��ϵ����
        Return: 
        Others: 
        """

        # TODO
        pass
        
        #self.__context.regist_asso(asso)
    

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

                ע: 
                1)������mit��ͨ��MitContext�����Զ��庯��������������mit�������Ƶ�
                2)ͨ��call_custom_function�����Զ��庯��ʱ���ڲ����ݸ��Զ�������ĵ�һ��������ʼ����MitContext����
                
        """
        
        self.__context.regist_custom_function(function_name, call_obj, is_need_tran)
        
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
        
        with self.__lock:
            ret = None
            
            call_obj, is_need_tran = self.__context.get_custom_function(function_name)
            if call_obj is None:
                raise Exception("custom function (%s) is not registed!" % function_name)

            try:
                if is_need_tran is True:

                    # ���mit���������У���ô���Զ�����������ύ����
                    need_tran = not self.is_in_tran()
                    
                    if need_tran is True:
                        self.begin_tran()
                    else:
                        # Ϊ���ڹ���У��ʧ�ܵ�����£����Իع����ѽ��޸ĵ�����
                        # �Զ�����savepoint
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
        Description: �������Ե�ֵ������RawDataMoiʵ��
        Parameter: 
            moc_name: MOC������
            **attr_values: ���Ե�ֵ
        Return: 
        Others: 
        """

        # rdm --- RawDataMoi����д
        moc = self.__context.get_moc(moc_name)

        if moc is None:
            return None
            
        
        instance = moc()
        rdm = self.__context.gen_rdm_by_instance(instance, **attr_values)

        return rdm

    def gen_moid(self, moc_name, **key_attr_values):
        """
        Method:    gen_moid
        Description: ���ݹؼ����Ե�ֵ����moid
        Parameter: 
            moc_name: MOC������
            **key_attr_values: �ؼ����Ե�ֵ
        Return: 
        Others: 
        """

        return  self.__context.gen_moid(moc_name, **key_attr_values)

        
    def __call_mod_data_method(self, method_name, *args, **kw):
        """
        Method:    __call_mod_data_method
        Description: ����MitContext������ɾ���ĵķ���
        Parameter: 
            method_name: ��������
            *args: ������
            **kw: �ֵ���ʽ�Ĳ�����
        Return: ����ռ���
        Others: 
        """

        with self.__lock:
            rst_collect = self.__context.reset_rst_collect()
            
            try:

                # ���mit���������У���ô���Զ�����������ύ����
                need_tran = not self.is_in_tran()
                
                if need_tran is True:
                    self.begin_tran()
                else:
                    # Ϊ���ڹ���У��ʧ�ܵ�����£����Իع����ѽ��޸ĵ�����
                    # �Զ�����savepoint
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
        Description: ����һ������ʵ��
        Parameter: 
            rdm: RawDataMoi��ʵ��
        Return: 
        Others: 
        """
        
        return self.__call_mod_data_method("rdm_add", rdm)

    def rdms_add(self, rdms):
        """
        Method:    rdm_add
        Description: ���Ӷ������ʵ��
        Parameter: 
            rdms: RawDataMoi��ʵ���б�
        Return: 
        Others: 
        """
        
        return self.__call_mod_data_method("rdms_add", rdms)


    def rdm_mod(self, rdm):
        """
        Method:    rdm_mod
        Description: �޸�һ������ʵ��
        Parameter: 
            rdm: RawDataMoi��ʵ��
        Return: 
        Others: 
        """


        return self.__call_mod_data_method("rdm_mod", rdm)

    def rdms_mod(self, rdms):
        """
        Method:    rdms_mod
        Description: �޸�һ������ʵ��
        Parameter: 
            rdms: RawDataMoi��ʵ��
        Return: 
        Others: 
        """

        return self.__call_mod_data_method("rdms_mod", rdms)



    def rdm_remove(self, rdm):
        """
        Method:    rdm_remove
        Description: ɾ��һ������ʵ��
        Parameter: 
            rdm: RawDataMoi��ʵ��
        Return: 
        Others: 
        """
        return self.__call_mod_data_method("rdm_remove", rdm)

    def rdms_remove(self, rdms):
        """
        Method:    rdm_remove
        Description: ɾ���������ʵ��
        Parameter: 
            rdms: RawDataMoi��ʵ���б�
        Return: 
        Others: 
        """
        return self.__call_mod_data_method("rdms_remove", rdms)
        
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
        return self.__call_mod_data_method("remove_all", moc_name)
        
    def rdm_lookup(self, moc_name, moid = None, **key_attr_values):
        """
        Method:    rdm_lookup
        Description: ����moid���Ҷ���ʵ��
        Parameter: 
            moc_name: MOC������
            moid: �����ҵ�ʵ����moid
            key_attr_values:�ؼ����Ե�ֵ
        Return: RawDataMoi��ʵ��
        Others: 
            ���ָ����moid����ô��ֱ��ʹ��moidȥ���ң���ʱkey_attr_values�������κ�����
            ���û��ָ��moid����ô��ʹ��key_attr_values����moid��Ȼ��ȥ����
            ���ͨ��key_attr_values���ң���ôkey_attr_values������ȫ���Ĺؼ����Ե�ֵ
        """

        with self.__lock:            
            obj = self.__context.lookup(moc_name, moid, **key_attr_values)

            if obj is None:
                return None

            return self.__context.gen_rdm_by_instance(obj)


    def rdm_find(self, moc_name, order_by_sql = None, num_per_page=None, current_page=None, **conditions):
        """
        Method:    rdm_find
        Description: ����һ���������Ҷ���
        Parameter: 
            moc_name: MOC������
            order_by_sql: ��������, ��MultiSQLʵ��
                      ���磬����name����: order_by = "name"
                      ���磬����name����+id����: order_by = "name desc, id asc"
                      ע��, oracle�У���Ҫ���ֶ���ʹ��˫���Ű�����
            num_per_page:��ѯ�����ҳ��ʾʱ��ÿҳ��ʾ�ļ�¼���� 
            current_page:��ѯ�����ҳ��ʾʱ����ǰҳ�����, 0��ʾ��һҳ
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ����������RawDataMoi����ʵ��
        Others: 
        """

        with self.__lock: 
            objs = self.__context.find_objs(moc_name, order_by_sql, num_per_page, current_page, **conditions)

            rdms = [self.__context.gen_rdm_by_instance(obj) for obj in objs]

            return  rdms


    def lookup_attrs(self, moc_name, attr_names, order_by_sql = None, num_per_page=None, current_page=None, **conditions):
        """
        Method:    lookup_attrs
        Description: ��ѯ���������Ķ�������
        Parameter: 
            moc_name: MOC������
            attr_names: ������ѯ�������б�
            order_by_sql: ��������, ��MultiSQLʵ��
                      ���磬����name����: order_by = "name"
                      ���磬����name����+id����: order_by = "name desc, id asc"
                      ע��, oracle�У���Ҫ���ֶ���ʹ��˫���Ű�����
            num_per_page:��ѯ�����ҳ��ʾʱ��ÿҳ��ʾ�ļ�¼���� 
            current_page:��ѯ�����ҳ��ʾʱ����ǰҳ�����, 0��ʾ��һҳ
            **conditions: ������������ʽ��: ������=����ֵ
        Return: ���������Ķ��������ֵ
        Others: 
        """

        with self.__lock:         
            return self.__context.lookup_attrs( moc_name, attr_names, order_by_sql, num_per_page, current_page, **conditions)

    def find_objs_by_sql(self, moc_name, where_sql):
        """
        Method:    find_objs_by_sql
        Description: ����SQL����ѯ����ʵ��
        Parameter: 
            moc_name: MOC������
            where_sql: ��MultiSQLʵ��, ������SQL����where�Ӿ䣬������where�ؼ���
                       ע��, oracle�У���Ҫ���ֶ���ʹ��˫���Ű�����
        Return: ����������RawDataMoi����ʵ���б�
        Others: 
        """

        with self.__lock:         
            return self.__context.find_objs_by_sql(moc_name, where_sql)

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

        with self.__lock:         
            return self.__context.count(moc_name, **conditions)

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

        with self.__lock:  
            return self.__context.is_exist(moc_name, moid, **key_attr_values)

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
        with self.__lock:  
            return self.__context.get_attr_max_value(moc_name, attr_name, **conditions)
            
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
        with self.__lock:  
            return self.__context.get_attr_min_value(moc_name, attr_name, **conditions)


    def raw_select_ex(self, multisql, *agrs, **kw):    
        """
        Method:    raw_select_ex
        Description: �����ݿ���ִ��һ��SELECT��䣬���ؽ����
        Parameter: 
            multi_sql: MultiSQLʵ��������˲�ͬ���ݿ�ϵͳ��SQL���
        Return: ���ݿ�����
        Others: ��Ҫ���øýӿ�ִ�зǲ�ѯ��SQL������ᵼ��cache��ͬ��������
        """
        with self.__lock:  
            return self.__context.raw_select_ex(multisql, *agrs, **kw)

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
        
        return self.__call_mod_data_method("raw_exec_ex", moc_name, multisql, *agrs, **kw)


    def mod_complex_attr(self, moc_name, moid, **complex_attr_value):
        """
        Method:    mod_complex_attr
        Description: �޸ĸ�����������
        Parameter: 
            moc_name: ���޸ĵ�MOC������
            moid: ���޸ĵĶ���ʵ����moid
            **complex_attr_value: �������Ե�ֵ����ʽ��: ������=����ֵ��
                            ��������ֵӦ����SerializableObj������Ķ���ʵ��
        Return: 
        Others: 
        """

        return self.__call_mod_data_method("mod_complex_attr", moc_name, moid, **complex_attr_value)


    def open_sqlite(self, db_file):
        """
        Method:    open_sqlite
        Description:  ��sqlite���ݿ�
        Parameter: 
            db_file: sqlite���ݿ��ļ�·��(������ :memory:)
        Return: 
        Others: ���db_file���ڴ�db����ôopen�����ݿ��ǿյģ�
                ��Ҫ����init_sqlite_db�����������
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
        Description: ��ʼ��sqlite���ݿ�
        Parameter: ��
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

            # ������ʱ����Ҫ�����������͵�����
            fields += [attr.name for attr in moc.__COMPLEX_ATTR_DEF__]

            table_name = "tbl_" + moc.get_moc_name()
            
            sql = "create table if not exists %s (%s)" % (table_name, ",".join(fields))
                        
            db_query.execute(sql)
            db_query.execute("create index if not exists idx_%s_moid on %s(moid)" % (
                              table_name
                            , table_name))

            

            # �ڹؼ����ϴ�������
            if len(keys) > 0:
                db_query.execute("create index if not exists idx_%s_%s on %s(%s)" % (
                                  table_name
                                  , "_".join(keys)
                                , table_name
                                , ",".join(keys)))

            # �����Զ��������
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
        Description: ��Oracle���ݿ�����
        Parameter: ��
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
        Description: �ж�mit�Ƿ�����������
        Parameter: ��
        Return: 
        Others: 
        """

        with self.__lock:
            return self.__is_in_tran
        
    def begin_tran(self):
        """
        Method:    begin_tran
        Description: �������ݿ�����
        Parameter: ��
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
        Description: �ع����ݿ�����
        Parameter: ��
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
        Description: �ύ���ݿ�����
        Parameter: ��
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
        Description: ���������
        Parameter: 
            savepoint_name: ���������
        Return: 
        Others: 
        """

        with self.__lock:
            db_con = self.__context.get_db_mgr().get_active_db()
            db_con.begin(savepoint_name)

    def __rollback_savepoint(self, savepoint_name):
        """
        Method:    __rollback_savepoint
        Description: �ع������
        Parameter: 
            savepoint_name: ���������
        Return: 
        Others: 
        """

        with self.__lock:
            db_con = self.__context.get_db_mgr().get_active_db()
            db_con.rollback(savepoint_name)

    def __release_savepoint(self, savepoint_name):
        """
        Method:    __release_savepoint
        Description: �ͷű����
        Parameter: 
            savepoint_name: ���������
        Return: 
        Others: 
        """

        with self.__lock:
            db_con = self.__context.get_db_mgr().get_active_db()
            db_con.commit(savepoint_name)


