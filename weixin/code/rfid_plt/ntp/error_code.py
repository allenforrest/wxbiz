#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-12-14
Description: ntp_app�����붨��
Others: ��
Key Class&Method List: ��
History: 
1. Date:2012-12-14
   Author:ACP2013
   Modification:�½��ļ�
"""

import err_code_mgr

NTPD_ERROR_BASE = 3101

ntpd_error_defs = {"ER_NTPD_IO_WRONG" : (NTPD_ERROR_BASE + 1
                                             , "д��NTPD�����ļ���������"
                                             , "Write NTPD configuration files wrong" )  
                   , "ER_NTPD_INVALID_DESERIALIZE_ERROR" : (NTPD_ERROR_BASE + 2
                                            , "�õ��Ƿ��ķ����л��ַ���"
                                            ,"invalid string to deserialize")
                   , "ER_NTPD_IP_ERROR" : (NTPD_ERROR_BASE + 3
                                            , "�����IP %(name)s��ַ�Ƿ�"
                                            ,"IP (%(name)s) address is invalid") 
                   , "ER_NTPD_MASK_ERROR" : (NTPD_ERROR_BASE + 4
                                            , "�������������  %(name)s �Ƿ�"
                                            ,"Mask( %(name)s) is invalid")   
                   , "ER_NTPD_SERVER_NOT_EXIST" : (NTPD_ERROR_BASE + 5
                                            , "û���ҵ�NTPD�ϲ����"
                                            ,"Can not find NTPD Server Set")  
                   , "ER_NTPD_SUBNET_NOT_EXIST" : (NTPD_ERROR_BASE + 6
                                            , "û���ҵ�NTPD�ɷ��������������"
                                            ,"Can not find NTPD Subnetwork Set")  
                    , "ER_DUPLICATE_NTPD_SERVER_ERROR" : (NTPD_ERROR_BASE + 7
                                            , "NTPD���ϲ���������ظ�"
                                            ,"NTPD Server Set DUPLICATE Exception") 
                    , "ER_DUPLICATE_NTPD_SUBNET_ERROR" : (NTPD_ERROR_BASE + 8
                                            , "NTPD�ɷ���������������ظ�"
                                            ,"NTPD Subnetwork Set DUPLICATE Exception")
                    , "ER_NTPD_RESTORE_ERROR" : (NTPD_ERROR_BASE + 9
                                            , "NTPDAPP����ʱ��ԭ����ʧ��"
                                            ,"NTPD APP Restore fail")   
                   , "ER_NTPD_CHANGE_ERROR" : (NTPD_ERROR_BASE + 10
                                            , "�޸�NTPD����״̬ʧ��"
                                            ,"Close or Open NTPD Server fail") 
                   , "ER_NTPD_SERVICE_OPEN_ERROR" : (NTPD_ERROR_BASE + 11
                                            , "NTPD��������ʧ��"
                                            ,"SYSREM ERROR:Can Not Srart NTPD Service") 
                   , "ER_NTPD_CONTROL_ERROR" : (NTPD_ERROR_BASE + 12
                                            , "NTPD�������߿������ô���"
                                            ,"ntpd openserver (%(open_param)s) or stratum (%(stratum_param)d) is invalid")  
                   , "ER_NTPD_DB_ERROR" : (NTPD_ERROR_BASE + 13
                                            , "���ݿ���û�й���NTPD�����رյ�����"
                                            ,"Can not find data in DateBase") 
                   , "ER_NTPD_HAS_OP_ERROR" : (NTPD_ERROR_BASE + 14
                                            , "�Ѿ��򿪻��߹ر�NTPD����"
                                            ,"Has Opened or Closed NTPD Service")  
             }

err_code_mgr.regist_errors(ntpd_error_defs)