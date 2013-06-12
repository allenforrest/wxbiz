#coding=gbk
import err_code_mgr

#PLT ������
MONITOR_ERROR_BASE = 2100


name_service_error_defs = {"ER_APP_TYPE_NOT_EXIST_EXCEPTION" : (MONITOR_ERROR_BASE + 1
                                             , "AppType %(app_type)s ������"
                                             , "the AppType %(app_type)s does not exist")
                            , "ER_PID_NOT_EXIST_EXCEPTION" : (MONITOR_ERROR_BASE + 2
                                            , "Pid %(pid)s ������"
                                            , "the Pid %(pid)s does not exist")
                            ,"ER_INSTANCE_NAME_NOT_EXIST_EXCEPTION": (MONITOR_ERROR_BASE+3
                                            ,"ʵ������  %(instance_name)s ������"
                                            ,"the Instance Name %(instance_name)s does not exist")             
                           ,"ER_ENDPOINT_NOT_EXIST_EXCEPTION": (MONITOR_ERROR_BASE+4
                                            ,"endpoint %(endpoint)s ������"
                                            ,"the endpoint %(endpoint)s does not exist")
                           ,"ER_UNREGISTER_PARAMETER_NOT_EXIST_EXCEPTION": (MONITOR_ERROR_BASE+5
                                            ,"unregister ���� ������"
                                            ,"unregister parameter does not exist")                           
                           ,"ER_INVALID_DESERIALIZE_STRING_ERROR": (MONITOR_ERROR_BASE+6
                                            ,"������   %(cmd)s �Ĳ���  %(param_name)s Ϊ�Ƿ��ķ����л��ַ���"
                                            ,"invalid string to deserialize from command %(cmd)s parameter  %(param_name)s")
                           ,"ER_ENDPOINT_EXIST_EXCEPTION": (MONITOR_ERROR_BASE+7
                                            ,"Endpoint   %(endpoint)s �Ѿ�����"
                                            ,"Endpoint   %(endpoint)s exists")
                           ,"ER_NAME_SERVER_IS_NOT_MASTER": (MONITOR_ERROR_BASE+8
                                            , "��ǰ���ַ�����master, ������masterΪ%(ip)s"
                                            , "the current name service is not master. The real master is %(ip)s")
                                            
                           ,"ER_CLUSTER_IS_DISABLE": (MONITOR_ERROR_BASE+9
                                            , "��Ⱥ���ܱ�����"
                                            , "the cluster is disabled")
                                            
                            
             }
err_code_mgr.regist_errors(name_service_error_defs)
