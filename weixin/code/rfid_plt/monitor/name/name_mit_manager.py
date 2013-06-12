#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-09
Description: 提供名字服务mit处理接口
Others:      
Key Class&Method List: 
             1. NameMitManager
History: 
1. Date:2012-12-09
   Author:ACP2013
   Modification:新建文件
"""

import time
import copy

import bundleframework as bf
import sequence_no_creator
import err_code_mgr
import mit
import tracelog

from moc_name_service import AppType
from moc_name_service import AppInstance
from mocs import name_ex_rules

class NameMitManager(mit.Mit):
    """
    Class: NameMitManager
    Description: 名字服务Mit管理类，从mit类继承
    Base: Mit
    Others: 
        __pid_creator，pid生成器
    """

    def __init__(self, db_file):
        """
        Method: __init__
        Description: 类初始化函数
        Parameter: 
            db_file: sqlite db文件所在路径
        Return: 
        Others: 
        """

        mit.Mit.__init__(self)    
        self.init_mit_lock()        
        self.regist_moc(AppType.AppType, AppType.AppTypeRule)
        self.regist_moc(AppInstance.AppInstance, name_ex_rules.AppInstancesRuleEx)

        # 名字服务只使用sqlite就可以了，不需要放到oracle中，不需要长久保存
        
        if 0: # for test
            self.open_sqlite(db_file)

            # 清空掉数据表
            self.remove_all('AppInstance')
        else:
            self.open_sqlite(":memory:")
        
        
        #初始化pid creator, 获取当前MIT中的最大pid,可以分配的pid最小为1000
        # 1~1000作为特殊的pid        
        #pid = self.get_attr_max_value('AppInstance', 'pid')        
        min_pid = 1000
        #if pid is None or pid<min_pid:
        #    pid =  min_pid
        pid = min_pid
        
        self.__pid_creator = sequence_no_creator.SequenceNoCreator()
        self.__pid_creator.init_creator(2**32, pid, min_pid)

    def clear_all_name(self):
        rst_collect = self.remove_all('AppInstance')
        
        if rst_collect.get_err_code() != 0:
            tracelog.error("clear all name failed. %s" % rst_collect.get_msg())
            
        
    def get_new_avalible_pid(self):
        """
        Method: get_new_avalible_pid
        Description: 获取新的pid，通过pid_creator获取pid
        Parameter: 无
        Return: pid
        Others: 
        """
        pid = self.__pid_creator.get_new_no()        
        while True:
            rdms = self.rdm_find('AppInstance', pid = pid)
            if len(rdms)!=0:
                pid = self.__pid_creator.get_new_no()
            else:
                break 
        return pid
    
    def register_app(self, req):
        """
        Method: register_app
        Description: 提供注册名字到mit的函数，如果已经发现存在旧的注册信息，更新注册信息；否则，生成新的注册信息
        Parameter: 
            req: 注册请求消息
        Return: 注册结果信息
        Others: 
        """
        result = bf.AppRegisterResponse()
        result.init_all_attr()
        rdms = self.rdm_find('AppInstance'
                            , service_name = req.service_name
                            , instance_id = req.instance_id
                            , system_ip = req.system_ip
                            )
        #没有发现已经注册的信息    
        if len(rdms)==0:            
            new_pid = self.get_new_avalible_pid()
            app_instance = self.gen_rdm('AppInstance'
                                      , pid = new_pid
                                      , service_name = req.service_name
                                      , instance_name = '%s_%s'%(req.service_name, req.instance_id)
                                      , instance_id = req.instance_id
                                      , system_ip = req.system_ip
                                      , node_type = req.node_type
                                      , endpoint = req.endpoint
                                      , endpoint_protocol = req.endpoint_protocol
                                      , update_time = int(time.time())
                                      , state = 'online')
            ret = self.rdm_add(app_instance)
        #发现已经注册的信息,不用考虑多个对象的情况
        else:
            app_instance = self.gen_rdm('AppInstance'
                                      , pid = rdms[0].pid
                                      , service_name = req.service_name
                                      , instance_name = '%s_%s'%(req.service_name, req.instance_id)
                                      , instance_id = req.instance_id
                                      , system_ip = req.system_ip
                                      , node_type = req.node_type
                                      , endpoint = req.endpoint
                                      , endpoint_protocol = req.endpoint_protocol
                                      , update_time = int(time.time())
                                      , state = 'online')
            ret = self.rdm_mod(app_instance)        

        result.return_code = ret.get_err_code()
        result.description = ret.get_msg()
        if result.return_code==err_code_mgr.ER_SUCCESS:
            app_info = bf.AppInfo()
            app_info.init_all_attr()
            app_info.instance_name = app_instance.instance_name
            app_info.service_name = app_instance.service_name
            app_info.instance_id = app_instance.instance_id
            app_info.system_ip = app_instance.system_ip
            app_info.node_type = app_instance.node_type
            app_info.pid = app_instance.pid
            app_info.endpoint = app_instance.endpoint
            app_info.endpoint_protocol = app_instance.endpoint_protocol
            result.app_info = app_info
            
            #查找所有的 pid
            if req.need_return_all_app_info is True:            
                rdms = self.rdm_find('AppInstance', state='online')
                result.all_app_infos = [None]*len(rdms)
                for i, rdm in enumerate(rdms):
                    app_info = bf.AppInfo()
                    app_info.init_all_attr()
                    app_info.instance_name = rdm.instance_name
                    app_info.service_name = rdm.service_name
                    app_info.instance_id = rdm.instance_id
                    app_info.system_ip = rdm.system_ip
                    app_info.node_type = rdm.node_type                
                    app_info.pid = rdm.pid
                    app_info.endpoint = rdm.endpoint
                    app_info.endpoint_protocol = rdm.endpoint_protocol
                    result.all_app_infos[i] = app_info
            else:
                result.all_app_infos = []
                
            
        return result

    def unregister_app(self, req):
        """
        Method: unregister_app
        Description: 提供从mit中注销名字信息的函数
        Parameter: 
            req: 注销名字请求
        Return: 注销名字的返回信息
        Others: 
        """
   
        result = bf.AppUnRegisterResponse()
        result.init_all_attr()
        
        #按pid注销
        if req.pid is not None and req.pid!=0:
            rdms = self.rdm_find('AppInstance', pid = req.pid, state='online')
            if len(rdms) ==0:
                result.return_code = err_code_mgr.ER_PID_NOT_EXIST_EXCEPTION
                result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_PID_NOT_EXIST_EXCEPTION
                                                                    , pid=req.pid)                
            else:
                app_instance = rdms[0]
                app_instance.update_time = int(time.time())
                app_instance.state = 'offline'                
                ret = self.rdm_mod(app_instance)
                result.return_code = ret.get_err_code()
                result.description = ret.get_msg()

        #按endpoint注销
        elif req.endpoint is not None and req.endpoint!='':
            rdms = self.rdm_find('AppInstance', endpoint = req.endpoint, state='online')
            if len(rdms) ==0:
                result.return_code = err_code_mgr.ER_ENDPOINT_NOT_EXIST_EXCEPTION
                result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_ENDPOINT_NOT_EXIST_EXCEPTION
                                                                    , endpoint=req.endpoint)                
            else:
                app_instance = rdms[0]
                app_instance.update_time = int(time.time())
                app_instance.state = 'offline'                
                ret = self.rdm_mod(app_instance)
                result.return_code = ret.get_err_code()
                result.description = ret.get_msg()
        #按system ip注销
        elif req.system_ip is not None and req.system_ip!='':
            rdms = self.rdm_find('AppInstance', system_ip = req.system_ip, state='online')            

            self.rdms_remove(rdms)
            #多次删除，就不考虑不成功的异常情况    
            result.return_code = err_code_mgr.ER_SUCCESS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        #按service_name注销
        elif req.service_name is not None and req.service_name!='':
            rdms = self.rdm_find('AppInstance', service_name = req.service_name, state='online')            

            self.rdms_remove(rdms)
            #多次删除，就不考虑不成功的异常情况    
            result.return_code = err_code_mgr.ER_SUCCESS
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        else:
            result.return_code = err_code_mgr.ER_UNREGISTER_PARAMETER_NOT_EXIST_EXCEPTION
            result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_UNREGISTER_PARAMETER_NOT_EXIST_EXCEPTION)        

        return result



    def query_all_registered_app(self):
        req = bf.AppQueryRequest()
        req.init_all_attr()
        return self.query_registered_app(req)

        
    def query_registered_app(self, req):
        """
        Method: query_registered_app
        Description: 从mit中查询名字信息
        Parameter: 
            req: 名字查询请求
        Return: 名字查询请求的返回信息
        Others: 
        """
   
        result = bf.AppQueryResponse()
        result.init_all_attr()        
        
        #按pid查询
        if req.pid is not None and req.pid!=0:
            rdms = self.rdm_find('AppInstance', pid=req.pid, state='online')
        #按instance_name查询
        elif req.instance_name is not None and req.instance_name!="":
            rdms = self.rdm_find('AppInstance', instance_name=req.instance_name, state='online')
        #按service_name查询
        elif req.service_name is not None and req.service_name!="":
            rdms = self.rdm_find('AppInstance', service_name=req.service_name, state='online')
        #按endpoint查询
        elif req.endpoint is not None and req.endpoint!="":
            rdms = self.rdm_find('AppInstance', endpoint=req.endpoint, state='online')
        #按system_ip查询
        elif req.system_ip is not None and req.system_ip!="":
            rdms = self.rdm_find('AppInstance', system_ip=req.system_ip, state='online')
        #查询所有
        else:
            rdms = self.rdm_find('AppInstance', state='online')
            
        result.return_code = err_code_mgr.ER_SUCCESS
        result.description = err_code_mgr.get_error_msg(err_code_mgr.ER_SUCCESS)
        result.app_infos = [None]*len(rdms)
        for i, rdm in enumerate(rdms):
            app_info = bf.AppInfo()
            app_info.init_all_attr()
            app_info.instance_name = rdm.instance_name
            app_info.service_name = rdm.service_name
            app_info.instance_id = rdm.instance_id
            app_info.system_ip = rdm.system_ip
            app_info.node_type = rdm.node_type 
            app_info.pid = rdm.pid
            app_info.endpoint = rdm.endpoint
            app_info.endpoint_protocol = rdm.endpoint_protocol
            result.app_infos[i] = app_info

        return result      

    def clear_offline_app(self):
    
        max_timeout = 30 * 60  # 约30分钟
        
        rdms = self.rdm_find('AppInstance', state='offline')
        c_time = int(time.time())
        
        self.begin_tran()
        
        for rdm in rdms:
            #超时
            if rdm.update_time + max_timeout < c_time:
                ret = self.rdm_remove(rdm)
                if ret.get_err_code()!=err_code_mgr.ER_SUCCESS:
                    tracelog.error('clear register infomation exception\n%s'%ret.get_msg())
                
        self.commit_tran()        

    def on_notify_running_pids(self, monitor_pid, running_pids):
        # 返回是否注销了某些进程
       
        # 根据发送者的pid，找到其ip
        attrs = self.lookup_attrs("AppInstance", ["system_ip"], pid = monitor_pid)
        if len(attrs) == 0:
            return False

        monitor_ip = attrs[0][0]

        # 根据ip查找出所有的名字信息
        attrs = self.lookup_attrs("AppInstance"
                                , ["pid", "instance_name", "update_time"]
                                , system_ip = monitor_ip
                                , state='online'
                                , endpoint_protocol = bf.EIPC_PROTOCOL)
        if len(attrs) == 0:
            return False
        
        # 得到已经不再运行的进程    
        # 判断最后更新时间, 如果时间超过了30秒，则注销之
        running_pids = set(running_pids)

        now = int(time.time())
        time_out = 30
        unregist_someone = False
        for pid, instance_name, update_time in attrs:
            if pid == monitor_pid:
                # monitor本身不running_pids中，这里需要过滤掉，否则monitor自己将被注销了
                continue
            if pid in running_pids:
                continue 

            if update_time + time_out < now:
                unregist_someone = True
                app_instance = mit.RawDataMoi("AppInstance"
                                            , pid = pid
                                            , update_time = now
                                            , state='offline')                      
                ret = self.rdm_mod(app_instance)
                if ret.get_err_code() != 0:
                    tracelog.error("unregist stopped app failed, pid:%d,%s, msg:%s" % 
                                        (pid, instance_name, ret.get_msg()))
                else:
                    tracelog.info("unregist stopped app, pid:%d, %s" % (pid, instance_name))
            
        return unregist_someone
            
