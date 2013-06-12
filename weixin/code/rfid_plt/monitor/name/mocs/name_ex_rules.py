#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-12
Description: ��չ��moc������
Others:      
Key Class&Method List: 
             1. AppInstancesRuleEx
History: 
1. Date:2012-12-12
   Author:ACP2013
   Modification:�½��ļ�
"""


import err_code_mgr

import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef

from moc_name_service import AppInstance

class AppInstancesRuleEx(AppInstance.AppInstanceRule):    
    """
    Class: AppInstancesRuleEx
    Description: AppInstance����չ������
    Base: AppInstanceRule
    Others: 
    """

    def pre_add_check(self, new_instance):
        """
        Method: pre_add_check
        Description: ���Ӷ���ǰ��У������ж�endpoint����Ψһ
        Parameter: 
            new_instance: ���ӵĶ���ʵ��
        Return: 
        Others: 
        """
        

        AppInstance.AppInstanceRule.pre_add_check(self, new_instance)

        mit_context = self.get_mit_context()
        
        #endpoint����Ψһ
        rdms = mit_context.find_objs('AppInstance', endpoint=new_instance.endpoint, state = 'online')        
        self.check(len(rdms)==0, err_code_mgr.ER_ENDPOINT_EXIST_EXCEPTION, endpoint=new_instance.endpoint)
        
    def rmv_same_endpoint_record(self, new_instance):
        rdms = self._moc.get_db_contain().find_objs(endpoint=new_instance.endpoint, state = 'online')

        for rdm in rdms:
            if rdm.pid != new_instance.pid:
                self.get_mit_context().rdm_remove(rdm)
        
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
        AppInstance.AppInstanceRule.post_add_obj(self, new_instance, rdm)

        # ���������ͬ��endpoint����ôɾ��֮
        self.rmv_same_endpoint_record(new_instance)


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
        AppInstance.AppInstanceRule.post_mod_obj(self, new_instance, old_instance, rdm)
        
        # ���������ͬ��endpoint����ôɾ��֮
        self.rmv_same_endpoint_record(new_instance)
        

