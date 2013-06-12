#coding=gbk
import err_code_mgr

#PLT 命令码
MONITOR_ERROR_BASE = 2100


name_service_error_defs = {"ER_APP_TYPE_NOT_EXIST_EXCEPTION" : (MONITOR_ERROR_BASE + 1
                                             , "AppType %(app_type)s 不存在"
                                             , "the AppType %(app_type)s does not exist")
                            , "ER_PID_NOT_EXIST_EXCEPTION" : (MONITOR_ERROR_BASE + 2
                                            , "Pid %(pid)s 不存在"
                                            , "the Pid %(pid)s does not exist")
                            ,"ER_INSTANCE_NAME_NOT_EXIST_EXCEPTION": (MONITOR_ERROR_BASE+3
                                            ,"实例名称  %(instance_name)s 不存在"
                                            ,"the Instance Name %(instance_name)s does not exist")             
                           ,"ER_ENDPOINT_NOT_EXIST_EXCEPTION": (MONITOR_ERROR_BASE+4
                                            ,"endpoint %(endpoint)s 不存在"
                                            ,"the endpoint %(endpoint)s does not exist")
                           ,"ER_UNREGISTER_PARAMETER_NOT_EXIST_EXCEPTION": (MONITOR_ERROR_BASE+5
                                            ,"unregister 参数 不存在"
                                            ,"unregister parameter does not exist")                           
                           ,"ER_INVALID_DESERIALIZE_STRING_ERROR": (MONITOR_ERROR_BASE+6
                                            ,"从命令   %(cmd)s 的参数  %(param_name)s 为非法的反序列化字符串"
                                            ,"invalid string to deserialize from command %(cmd)s parameter  %(param_name)s")
                           ,"ER_ENDPOINT_EXIST_EXCEPTION": (MONITOR_ERROR_BASE+7
                                            ,"Endpoint   %(endpoint)s 已经存在"
                                            ,"Endpoint   %(endpoint)s exists")
                           ,"ER_NAME_SERVER_IS_NOT_MASTER": (MONITOR_ERROR_BASE+8
                                            , "当前名字服务不是master, 真正的master为%(ip)s"
                                            , "the current name service is not master. The real master is %(ip)s")
                                            
                           ,"ER_CLUSTER_IS_DISABLE": (MONITOR_ERROR_BASE+9
                                            , "集群功能被禁用"
                                            , "the cluster is disabled")
                                            
                            
             }
err_code_mgr.regist_errors(name_service_error_defs)
