#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-27
Description: ������ʵ����MOC�Ļ����У�����Ļ���
Others:      
Key Class&Method List: 
             1. MocBase: MOC�Ļ���
History:     2. MocRule: MOC��У�����Ļ���
1. Date:
   Author:
   Modification:
"""

from _mit import const

    
class MocBase:
    """
    Class: MocBase
    Description: MOC�Ļ���
    Base: 
    Others: �����еĴ󲿷����Ժͷ�����������Ҫ�������ص�
    """

    # MOC������
    __MOC_NAME__ = ""

    # EAU->IMCͬ���ı�ʶ
    __IMC_SYNC_PRIORITY__ = const.IMC_SYNC_NOT_SYNC

    # ��ͨ���Զ���
    __ATTR_DEF__ = ()

    # ���ϵ����Զ���
    __COMPLEX_ATTR_DEF__ =()

    # ���Զ�����ֵ�
    __ATTR_DEF_MAP__ = {}

    # ����
    __ATTR_INDEX__ = ()

    # sqlite��Oracle�ĸ���sql���
    __SQLITE_SELECT_SQL__ = ''
    __ORACLE_SELECT_SQL__ = ''

    __SQLITE_INSERT_SQL__ = ''
    __ORACLE_INSERT_SQL__ = ''

    __SQLITE_UPDATE_SQL__ = ''
    __ORACLE_UPDATE_SQL__ = ''



    # ��������json��ʽ�洢�������е�ʱ��_db_contain��None
    _db_contain = None
    _mit_context = None
    _rule_class = None  # ��Ӧ��MocRule��

    
    
    def __init__(self):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
        """

        pass

    @classmethod
    def gen_moid(cls, **kw):
        """
        Method:    gen_moid
        Description: �����ؼ����Ե�ֵ������moid
        Parameter: 
            **kw: �ؼ����Ե�ֵ
        Return: 
        Others: ����������
        """

        return ""
        
    
    def get_moid(self):
        """
        Method:    get_moid
        Description: ��ȡ��ǰ�����moid
        Parameter: ��
        Return: 
        Others: 
            moid���ַ������ͣ�����ʽΪ: XXXX_yyy_zzz
            ���У�XXXX��__MOC_NAME__
                  yyy��zzz�ǹؼ����Ե�ֵ���������ֵ���ַ���������Ҫʹ�õ�����

            ����������
        """

        return ""

    @classmethod
    def get_moc_name(cls):
        """
        Method:    get_moc_name
        Description: ��ȡMOC������
        Parameter: ��
        Return: MOC������
        Others: ������������
        """

        return cls.__MOC_NAME__

    @classmethod
    def is_need_sync_to_ems(cls):
        """
        Method: is_need_sync_to_ems
        Description: �жϵ�ǰMOC�Ƿ���Ҫ����ͬ�����ϲ����ܣ�����IMC
        Parameter: ��
        Return:
        Others: 
        """
        return cls.__IMC_SYNC_PRIORITY__ != const.IMC_SYNC_NOT_SYNC
    
    @classmethod
    def get_attr_def(cls, attr_name):
        """
        Method:    get_attr_def
        Description: ��ȡ���Զ���
        Parameter: 
            attr_name: ���Ե�����
        Return: ���Զ���
        Others: ������������
        """

        return cls.__ATTR_DEF_MAP__.get(attr_name)
        
    @classmethod
    def get_db_contain(cls, db_sync = False):
        """
        Method:    get_db_contain
        Description: ��ȡ������ǰMOC�����ݿ���ʶ���
        Parameter:
            db_sync: �Ƿ�Ҫ����DBͬ��
        Return: ��ǰMOC�����ݿ���ʶ���
        Others: ������������
        """
        db_contain = cls._db_contain
        db_contain.set_db_sync(db_sync)
        return db_contain

    @classmethod
    def get_mit_context(cls):
        """
        Method:    get_mit_context
        Description: ��ȡmit��������
        Parameter: ��
        Return: mit��������
        Others: ������������
        """

        return cls._mit_context


    @classmethod
    def set_moc_rule(cls, moc_rule):
        """
        Method:    set_moc_rule
        Description: ����MOC��У�������
        Parameter: 
            moc_rule: У�������
        Return: 
        Others: ������������
        """

        cls._rule = moc_rule

    @classmethod
    def get_moc_rule(cls):
        """
        Method:    get_moc_rule
        Description: ��ȡMOCУ�����
        Parameter: ��
        Return: 
        Others: ������������
        """

        return cls._rule

    @classmethod
    def get_attr_names(cls):
        """
        Method:    get_attr_names
        Description: ��ȡ���Ե������б�
        Parameter: ��
        Return: ���Ե������б�
        Others: �������������б��ֳ��������֣��ֱ��ǹؼ��ֺͷǹؼ��������б�
                ����������
        """

        # key, non key
        return (), ()

    #def get_attr_values(cls):
    #    # ��get_attr_names��Ӧ�����ﷵ�ص������Ե�ֵ
    #    return (), ()
        
    def from_db_record(self, record):
        """
        Method:    from_db_record
        Description: ����һ�����ݿ��¼������Ե�ֵ
        Parameter: 
            record: ���ݿ��¼
        Return: 
        Others: ����������
        """

        pass
        
    def to_db_record(self):
        """
        Method:    to_db_record
        Description: �������Թ���һ�����Բ������ݿ�ļ�¼
        Parameter: ��
        Return: ���Բ������ݿ�ļ�¼
        Others: ����������
        """

        pass

    def to_db_record_for_update(self):
        """
        Method:    to_db_record
        Description: �������Թ���һ������update�����ݿ�ļ�¼
        Parameter: ��
        Return: ����update�����ݿ�ļ�¼
        Others: ����������
        """

        pass

    def from_binary(self):
        """
        Method:    from_binary
        Description: 
        Parameter: ��
        Return: 
        Others: ��չ�Ľӿڣ���ʱ��ʹ��
        """

        pass

    def to_binary(self):
        """
        Method:    to_binary
        Description: 
        Parameter: ��
        Return: 
        Others: ��չ�Ľӿڣ���ʱ��ʹ��
        """

        pass

        
class MocRule:
    """
    Class: MocRule
    Description: MOCУ�����Ļ���
    Base: 
    Others: ��MOC�Ķ���͹���ֿ�������ʵ��ͳһMOC�ڲ�ͬ��mit�еĹ���һ��
    """
    
    def __init__(self, moc, mit_context, rule_engine):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            moc: �󶨵�MOC��
            mit_context: mit������
            rule_engine: У���������
        Return: 
        Others: 
        """

        self._moc = moc
        self._mit_context = mit_context
        self._rule_engine = rule_engine


    ######################### ����У��ӿ� begin #########################
    def get_moc(self, moc_name):
        """
        Method:    get_moc
        Description: ����MOC�����ƻ�ȡMOC��
        Parameter: 
            moc_name: MOC������
        Return: MOC��
        Others: 
            mit�У������Ҫ��ȡMOC�࣬��Ҫͨ��import�ķ�ʽ������MOC�࣬
            ����ͨ��get_moc()�ķ�ʽ����ȡMOC��
        """

        return self._mit_context.get_moc(moc_name)


    def get_mit_context(self):
        """
        Method:    get_mit_context
        Description: ��ȡmit������
        Parameter: ��
        Return: mit������
        Others: 
        """

        return self._mit_context

    def check(self, is_True, err_code, **msg_paras):
        """
        Method:    check
        Description: У��һ������
        Parameter: 
            is_True: ���������Ƿ����㣬������һ��boolֵ���߱��ʽ
            err_code: ��is_TrueΪFalseʱ����������err_codeΪ������
            **msg_paras: ������������ж�̬��������ôͨ��msg_paras��ָ��
        Return: 
        Others: 
        """

        self._rule_engine.check(is_True, err_code, **msg_paras)


    
    def class_check(self):
        """
        Method:    class_check
        Description: MOC�༶���У�����
        Parameter: ��
        Return: 
        Others: 
        """

        pass

    def object_check(self, new_instance):
        """
        Method:    object_check
        Description: �����ӡ��޸Ķ���ʱ����Զ�������й�����
        Parameter: 
            new_instance: ���ӻ��޸ĺ�Ķ���ʵ��
        Return: 
        Others: 
        """
        self.check_attr_value(new_instance)
        

    def asso_check(self, new_instance):
        """
        Method:    asso_check
        Description: �����ӡ��޸Ķ���ʱ����Զ��������ϵ���й�����
        Parameter: 
            new_instance: ���ӻ��޸ĺ�Ķ���ʵ��
        Return: 
        Others: 
        """

        pass


    
    def pre_add_check(self, new_instance):
        """
        Method:    pre_add_check
        Description: ���Ӷ���ǰ��У�����
        Parameter: 
            new_instance: ���ӵĶ���ʵ��
        Return: 
        Others: 
        """

        pass
    
    def post_add_check(self, new_instance):
        """
        Method:    post_add_check
        Description: ���Ӷ�����У�����
        Parameter: 
            new_instance: ���ӵĶ���ʵ��
        Return: 
        Others: 
        """

        pass
    
    def pre_mod_check(self, new_instance, old_instance):
        """
        Method:    pre_mod_check
        Description: �޸Ķ���ǰ��У�����
        Parameter: 
            new_instance: �޸ĺ�Ķ���ʵ��
            old_instance: �޸�ǰ�Ķ���ʵ��
        Return: 
        Others: 
        """

        pass

    def post_mod_check(self, new_instance, old_instance):
        """
        Method:    post_mod_check
        Description: �޸Ķ�����У�����
        Parameter: 
            new_instance: �޸ĺ�Ķ���ʵ��
            old_instance: �޸�ǰ�Ķ���ʵ�� 
        Return: 
        Others: 
        """

        pass
    
    def pre_rmv_check(self, old_instance):
        """
        Method:    pre_rmv_check
        Description: ɾ������ǰ��У�����
        Parameter: 
            old_instance: ɾ��ǰ�Ķ���ʵ�� 
        Return: 
        Others: 
        """

        pass
    
    def post_rmv_check(self, old_instance):
        """
        Method:    post_rmv_check
        Description: ɾ��������У�����
        Parameter: 
            old_instance: ɾ��ǰ�Ķ���ʵ�� 
        Return: 
        Others: 
        """

        pass


    def check_attr_value(self, new_instance):
        """
        Method:    check_attr_value
        Description: ���ӡ��޸Ķ���ǰ��У��������ͨ����
        Parameter: 
            new_instance: ���ӻ��޸ĺ�Ķ���ʵ��
        Return: 
        Others: 
        """

        pass


    def check_complex_attr(self, moid, attr_name, attr_value):
        """
        Method:    check_complex_attr
        Description: �޸ĸ�������ǰ��У�鸴������
        Parameter: 
            moid: ���޸ĵĶ���ʵ����moid
            attr_name: ���޸ĵ����Ե�����
            attr_value: �޸ĺ������ֵ
        Return: 
        Others: 
        """

        pass

    
    ######################### ����У��ӿ� end #########################
    

    ####################### �����޸Ľӿ� begin #########################
    

    #def alloc_resource(self, new_instance):
    #    """
    #    ���Ӷ���ʱ��������Դ
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
        Description: ���Ӷ���ǰ�������Ҫ�����޸��������󡢷�����Դ�ȣ��������ﴦ��
        Parameter: 
            new_instance: ���ӵĶ���ʵ��
            rdm: RawDataMoiʵ��
        Return: 
        Others: 
        """


        pass
        
    def post_add_obj(self, new_instance, rdm):
        """
        Method:    post_add_obj
        Description: ���Ӷ���������Ҫ�����޸����������������ﴦ��
        Parameter: 
            new_instance: ���ӵĶ���ʵ��
            rdm: RawDataMoiʵ��
        Return: 
        Others: 
        """

        pass

        
    def pre_mod_obj(self, new_instance, old_instance, rdm):
        """
        Method:    pre_mod_obj
        Description: �޸Ķ���ǰ�������Ҫ�����޸����������������ﴦ��
        Parameter: 
            new_instance: �޸ĺ�Ķ���ʵ��
            old_instance: �޸�ǰ�Ķ���ʵ��
            rdm: RawDataMoiʵ��
        Return: 
        Others: 
        """

        pass
        
    def post_mod_obj(self, new_instance, old_instance, rdm):
        """
        Method:    post_mod_obj
        Description: �޸Ķ���������Ҫ�����޸����������������ﴦ��
        Parameter: 
            new_instance: �޸ĺ�Ķ���ʵ��
            old_instance: �޸�ǰ�Ķ���ʵ��
            rdm: RawDataMoiʵ��
        Return: 
        Others: 
        """

        pass

        
    def pre_rmv_obj(self, old_instance, rdm):
        """
        Method:    pre_rmv_obj
        Description: ɾ������ǰ�������Ҫ�����޸����������������ﴦ��
        Parameter: 
            old_instance: ɾ��ǰ�Ķ���ʵ��
            rdm: RawDataMoiʵ��
        Return: 
        Others: 
        """

        pass    

    def post_rmv_obj(self, old_instance, rdm):
        """
        Method:    post_rmv_obj
        Description: ɾ������������Ҫ�����޸����������ͷ���Դ�ȣ��������ﴦ��
        Parameter: 
            old_instance: ɾ��ǰ�Ķ���ʵ��
            rdm: RawDataMoiʵ��
        Return: 
        Others: 
        """

        pass


    def rmv_sub_objs(self, old_instance):
        """
        Method:    rmv_sub_objs
        Description: ɾ���Ӷ���
        Parameter: 
            old_instance: ɾ��ǰ�Ķ���ʵ��
        Return: 
        Others: 
        """

        pass



    def post_mod_complex_attr(self, moid, attr_name, attr_value):
        """
        Method:    post_mod_complex_attr
        Description: �޸��긴�����Ժ������޸�����
        Parameter: 
            moid: ���޸ĵĶ���ʵ����moid
            attr_name: ���޸ĵ����Ե�����
            attr_value: �޸ĺ������ֵ
        Return: 
        Others: 
        """
    
        pass
    
    ####################### �����޸Ľӿ� end #########################



    

    
