#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-08
Description: 本文件中实现了monitor进程app类
Others:      
Key Class&Method List: 
             1. MonitorApp: monitor进程app类
History: 
1. Date:
   Author:
   Modification:
"""


import sys
import time
import socket
import md5
import os.path

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import tracelog
import err_code_mgr
import cluster
import event_sender
import utility

from cluster_monitor import monitor_cluster

from process_monitor import process_monitor_worker
from process_monitor.process_stat_mgr import ProcessStatMgr


from name import name_manage_worker
from cluster_monitor import cluster_cfg_worker

import error_code





MONITOR_EIPC_PORT = 6001


class MonitorApp(bf.BasicApp):
    """
    Class: MonitorApp
    Description: monitor进程app类
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
        """

        bf.BasicApp.__init__(self, "Monitor")
        
                
        self.__cluster_node = None
        
        self.__name_manage_worker = None
        self.__process_mointor_worker = None
        
        event_sender.set_local_app(self)

    
    def _initialize(self):
        """
        Method:    _initialize
        Description: 重载BasicApp的方法
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败   
        Others: 
        """
        ret = bf.BasicApp._initialize(self)
        
        if ret!=0:
            return ret

        self._device_info.log_device_info()

        ret = self.__check_acp_sn()
        if ret != 0:
            tracelog.error("check ACP serial number failed.")
            return ret
            
        if self._device_info.is_cluster_enable():
            # 启动cluster
            ret = self.__start_cluster()

            if ret != 0:
                tracelog.error("start cluster failed. ret:%d" % ret)
                return ret
        
    
        name_worker = name_manage_worker.NameManageWorker()
        name_worker.set_app(self)
        ret = name_worker.init_mit_and_name_srv()
        if ret != 0:
            tracelog.error("initialize name service failed.")
            return ret

         
        if self.__cluster_node is not None:
            name_worker.set_cluster_role(self.is_cluster_master())
            self._name_master_ip = self.__cluster_node.get_master_ip()
            name_worker.set_cluster_master_ip(self._name_master_ip)
        else:
            name_worker.set_cluster_role(True)            
            name_worker.set_cluster_master_ip(self._name_master_ip)
        
        self.__name_manage_worker = name_worker
        
        return ret



    def __check_acp_sn(self):
        # 校验SN是否合法，避免软件被复制到其他设备上后可以运行

        # TODO, 后续开发安装盘的时候，再去掉下面的语句
        return 0

        
        if utility.is_windows():
            return 0 # windows暂时不校验

        inter_nic = self._device_info.get_device_internal_NIC()
        try:
            mac = utility.get_hw_address(inter_nic)
        except:
            tracelog.exception("get hardware address of %s failed." % inter_nic)
            return -1

        m = md5.new()
        m.update("acp software")
        m.update(mac)
        actual_sn = m.hexdigest()

        # 读取文件中的sn
        sn_file_path = os.path.join(self.get_app_top_path(), "data/sn/sn.dat")
        try:
            sn_file = open(sn_file_path, "r")
            expect_sn = sn_file.read()
            sn_file.close()
        except:
            tracelog.exception("read %s failed." % sn_file_path)
            return -1

        if expect_sn != actual_sn:
            tracelog.error("the serial number does not match!")
            return -1
            
        return 0

    def on_master_change(self, old_master_ip, new_master_ip):
        #print "on_master_change!!!", new_master_ip
        
        self._name_master_ip = new_master_ip
        
        if self.__name_manage_worker is not None:
            self.__name_manage_worker.set_cluster_master_ip(new_master_ip)

        # 重新注册名字服务
        if self.get_my_pid() != bf.INVALID_PID: # 防止正在启动过程中主线程正在注册名字服务
            ret = self.regist_name_service()
            
            if ret != 0:
                tracelog.error("regist name service failed when master changed. stop now."
                                "new master:%s" % (new_master_ip))
                self.stop()
                return
            
        # 重启所有的进程
        ProcessStatMgr.set_sys_to_restart()
        
    def on_cluster_state_change(self, old_role, old_stats, new_role, new_state, master_ip):
        
        # 发送事件
        if new_role == cluster.CLUSTER_ROLE_MASTER and old_role != cluster.CLUSTER_ROLE_MASTER:            
            self.__send_cluster_event("event.Cluster.be_master", master_ip)
        
    
        self._name_master_ip = master_ip
        #print "on_cluster_state_change!!!", master_ip, self.__name_manage_worker
        
        if self.__name_manage_worker is not None:
            self.__name_manage_worker.set_cluster_master_ip(master_ip)
            self.__name_manage_worker.set_cluster_role(new_role == cluster.CLUSTER_ROLE_MASTER) 

            # 重新注册名字服务
            if self.get_my_pid() != bf.INVALID_PID: # 防止正在启动过程中主线程正在注册名字服务
                ret = self.regist_name_service()
                if ret != 0:
                    tracelog.error("regist name service failed when cluster state changed. stop now."
                                    "new master:%s" % (master_ip))
                    self.stop()
                    return
        
        if new_role == cluster.CLUSTER_ROLE_MASTER:
            if new_state == cluster.CLUSTER_STATE_ONLY_MASTER:
                ProcessStatMgr.set_ha_master(True)
            else:
                ProcessStatMgr.set_ha_master(False)
        else:
            ProcessStatMgr.set_ha_slave()

        # 重启所有的进程
        ProcessStatMgr.set_sys_to_restart()

        
    
    def on_node_offline(self, node_ip):
        # 通知名字服务注销相应的名字信息

        req = bf.AppUnRegisterRequest()
        req.init_all_attr()  
        req.system_ip = node_ip
        req.need_reponse = False
        
        frame = bf.AppFrame()
        frame.set_cmd_code(bf.UNREGISTER_NAME_COMMAND)
        frame.set_sender_pid(self.get_my_pid())
        frame.add_data(req.serialize())
        
        self.dispatch_frame_to_worker("NameManageWorker", frame)

        # 发送事件
        self.__send_cluster_event("event.Cluster.be_offline", node_ip)
        
    def on_node_online(self, node_ip):
        # 发送事件
        self.__send_cluster_event("event.Cluster.be_online", node_ip)


    def __send_cluster_event(self, event_id, node_ip):
        # 如果EventManagerApp没有启动，那么就不发送该事件
        # 以免日志中记录无用的日志
        if self.get_pid("EventManagerApp", bf.MASTER_PID) == bf.INVALID_PID:
            return
        
        # 发送事件
        event_data = event_sender.EventData()
        event_data.set_event_id(event_id)
        event_data.set_object_id("Mointor")
        event_data.set_device_id(self.get_device_id())
        
        params = {'ip': node_ip}
        event_data.set_params(params)
        event_sender.send_event(event_data)

        

        
    def __start_cluster(self):
        cluster_node = monitor_cluster.MonitorCluster(self)

        cluster_cfg_info = cluster.ClusterCfgInfo()
        cluster_cfg_info.virtual_cluster_ip = self._device_info.get_cluster_virtual_ip()
        cluster_cfg_info.virtual_cluster_mask = self._device_info.get_cluster_virtual_mask()
        cluster_cfg_info.external_NIC = self._device_info.get_device_external_NIC()
        cluster_cfg_info.my_inner_ip = self._device_info.get_device_internal_ip()
        cluster_cfg_info.max_nodes_num = self._device_info.get_cluster_max_nodes_num()

        if cluster_cfg_info.my_inner_ip == "":
            if self._device_info.get_device_internal_NIC() == "":
                tracelog.error("can not start cluster, device internal NIC is not configured. ")
            else:
                tracelog.error("can not start cluster, device internal ip is null. ")
            return -1
            
        ret = cluster_node.start(cluster_cfg_info, self.get_app_top_path())
        
        if ret != 0:
            tracelog.error("start cluster node failed. ret:%d" % ret)
            return ret

        self.__cluster_node = cluster_node
        
        # 等待cluster启动时判决角色结束
        if cluster_node.wait_until_start():
            return 0
        else:
            tracelog.error("the cluster start timeout!")
            return -1

        return 0


    def _ready_for_work(self):
        """
        Method:    _ready_for_work
        Description: 进程启动时的初始化函数
        Parameter: 无
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """                
        # name_manage_worker和ClusterCfgWorker可以共用一个线程，减少线程数目
        wrk_thrd = bf.WorkThread()
        
   
        self.register_worker(cluster_cfg_worker.ClusterCfgWorker(self.__cluster_node)
                        , wrk_thrd = wrk_thrd
                        , start_thread = False)
    
        self.register_worker(self.__name_manage_worker, wrk_thrd = wrk_thrd, start_thread = True)
        
        self.__process_mointor_worker = process_monitor_worker.ProcessMonitorWorker()
        self.register_worker(self.__process_mointor_worker)
        
        return 0

    def _is_need_shake_with_monitor(self):
        """
        Method:    _is_need_shake_with_monitor
        Description: 判断是否需要与monitor握手
        Parameter: 无
        Return: 是否需要与monitor握手
        Others: monitor自己就不需要跟自己握手了
        """
        
        return False


    def _pre_exit(self):
        """
        Method:    _pre_exit
        Description: monitor退出前的处理函数，停止其他进程
        Parameter: 无
        Return: 
        Others: 
        """
        
        ProcessStatMgr.set_sys_to_stop()
        for i in xrange(30):
            if ProcessStatMgr.is_all_process_stoped():
                break
            time.sleep(1)
            print "."
        else:
            ProcessStatMgr.force_stop_all_process()


        # BasicApp._pre_exit中注销了当前进程的名字服务，导致其他app无法与monitor握手退出
        bf.BasicApp._pre_exit(self)

        if self.__name_manage_worker is not None:
            self.__name_manage_worker.close_mit_and_name_srv()

        if self.__cluster_node is not None:
            self.__cluster_node.stop()


    def soft_restart(self):
        """
        Method:    soft_restart
        Description: 软复位ACP软件系统
        Parameter: 无
        Return: 
        Others: 
        """        
        # 重新启动ACP软件系统
        # 这里只需要停止即可，由操作系统的服务自动启动之
        self.stop()   

    
#    def regist_name_service(self):
#        """
#        Method:    regist_name_service
#        Description: 向名字服务中心注册服务，重载basic_app的注册函数，对于是名字服务的monitor，需要直接注册
#        Parameter: 无
#        Return: 
#            0: 成功
#            非0: 失败
#        Others: 
#        """
#        
#        tracelog.info("regist_name_service, service name:%s " % (self._service_name))
#
#        if self.is_cluster_master():
#            rep = self.__reg_name_direct()
#        else:
#            rep = self._reg_name_by_udp()
#        
#        if rep.return_code==0:
#            self._pid = rep.app_info.pid            
#            
#            tracelog.info("regist_name_service successfully. InstanceName:%s  Pid:%s  Endpoint:%s"%(self._instance_name, self._pid, self._endpoint)) 
#
#            #注册成功需要直接更新名字信息 
#            self.on_process_app_register(rep.all_app_infos)
#        else:
#            tracelog.error("regist_name_service failed.%s"%rep.description)
#        
#        
#        return rep.return_code
#
    def unregist_name_service(self):
        """
        Method:    unregist_name_service
        Description: 向名字服务中心注销服务
        Parameter: 无
        Return: 
        Others: 
        """
        if self.is_cluster_master():
            if self.__name_manage_worker is not None:
                #按pid注销
                
                req = bf.AppUnRegisterRequest()
                req.init_all_attr()
                req.pid = self._pid        
                
                #不用关心结果
                self.__name_manage_worker.unregister_app(req)
        else:
            bf.BasicApp.unregist_name_service(self) 

#    def __reg_name_direct(self):
#        req = bf.AppRegisterRequest()
#        req.init_all_attr()
#        req.service_name = self._service_name
#        req.instance_id = self._instance_id
#        req.system_ip = self.get_my_name_ip()
#        req.node_type = "MASTER" if self.is_cluster_master() else "SLAVE"
#        req.need_return_all_app_info = False
#        ret, endpoint = self._get_avalible_tcp_endpoint(0, 0)
#        #获取失败
#        if ret!=0:
#            rep = bf.AppRegisterResponse()
#            rep.init_all_attr()
#            rep.return_code = err_code_mgr.ER_GET_AVAILIABLE_PORT_FAILED
#            rep.description = err_code_mgr.get_error_msg(err_code_mgr.ER_GET_AVAILIABLE_PORT_FAILED)
#            return rep      
#                
#        req.endpoint = endpoint
#        req.endpoint_protocol = bf.EIPC_PROTOCOL
#                
#        rep = self.__name_manage_worker.register_app(req)
#        if rep.return_code!=0:
#            tracelog.error('__reg_name_direct error %s'%rep.description)
#        
#        return rep
#
#
#    def is_cluster_master(self):
#        # 当不使用cluster时，就可以认为当前节点就是master
#        return self.__cluster_node is None or self.__cluster_node.is_master()

    def is_cluster_only_master(self):
        return self.__cluster_node is None or self.__cluster_node.is_only_master()
        
        
    def broadcast_reg_names(self, all_app_infos):
        #发送BROADCAST_NAME消息  到各个进程，不包括自身，自身已经在注册成功以后直接调用on_process_app_register了
        b_msg = bf.NameBroadCastMessage()
        b_msg.init_all_attr()
        b_msg.all_app_infos =  all_app_infos
        frame = bf.AppFrame()
        frame.set_cmd_code(bf.BROADCAST_NAME)
        frame.add_data(b_msg.serialize())        
        #print "===send broadcast_reg_names!!", all_app_infos
        self.dispatch_frame_to_any_other_processes(frame)

            
    def _query_from_nameservice(self):
        """
        Method:    _query_from_nameservice
        Description: 从名字服务查询所有注册信息,重载
        Parameter: 无
        Return: 
        Others: 
        """
        all_app_infos = []
        if self.is_cluster_master():
            req = bf.AppQueryRequest()
            req.init_all_attr()
            query_result = self.__name_manage_worker.query_registered_app(req)
            all_app_infos = query_result.app_infos
            
        else:
            all_app_infos = bf.BasicApp._query_from_nameservice(self)
        
        return all_app_infos


    def _get_name_port_range(self):
        return MONITOR_EIPC_PORT, MONITOR_EIPC_PORT
        
if __name__ == "__main__":
    MonitorApp().run()
    
