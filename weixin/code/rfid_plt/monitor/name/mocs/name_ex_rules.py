#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-12
Description: 扩展的moc规则类
Others:      
Key Class&Method List: 
             1. AppInstancesRuleEx
History: 
1. Date:2012-12-12
   Author:ACP2013
   Modification:新建文件
"""


import err_code_mgr

import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef

from moc_name_service import AppInstance

class AppInstancesRuleEx(AppInstance.AppInstanceRule):    
    """
    Class: AppInstancesRuleEx
    Description: AppInstance的扩展规则类
    Base: AppInstanceRule
    Others: 
    """

    def pre_add_check(self, new_instance):
        """
        Method: pre_add_check
        Description: 增加对象前的校验规则，判断endpoint必须唯一
        Parameter: 
            new_instance: 增加的对象实例
        Return: 
        Others: 
        """
        

        AppInstance.AppInstanceRule.pre_add_check(self, new_instance)

        mit_context = self.get_mit_context()
        
        #endpoint必须唯一
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
        Description: 增加对象后，如果需要联动修改其他对象，则在这里处理
        Parameter: 
            new_instance: 增加的对象实例
            rdm: RawDataMoi实例
        Return: 
        Others: 
        """
        AppInstance.AppInstanceRule.post_add_obj(self, new_instance, rdm)

        # 如果存在相同的endpoint，那么删除之
        self.rmv_same_endpoint_record(new_instance)


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
        AppInstance.AppInstanceRule.post_mod_obj(self, new_instance, old_instance, rdm)
        
        # 如果存在相同的endpoint，那么删除之
        self.rmv_same_endpoint_record(new_instance)
        

