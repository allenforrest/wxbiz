#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2013-03-07
Description: 
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


import err_code_mgr

REINFOECE_ERROR_BASE = 3301

maintainlog_error_defs = {  
                     "ER_REINFOECE_TELNET_ERROR" : (REINFOECE_ERROR_BASE + 1
                                            , "telnet服务已经打开"
                                            ,"telnet service is running")
                   , "ER_USER_ERROR" : (REINFOECE_ERROR_BASE + 2
                                            , "存在不必要的用户"
                                            ,"Some Users is unnecessary") 
                    , "ER_CMD_ERROR" : (REINFOECE_ERROR_BASE + 3
                                            , "控制台命令执行发送错误"
                                            ,"CMD Execute Failed")    
                    , "ER_USER_CYCLE_ERROR" : (REINFOECE_ERROR_BASE + 4
                                            , "账户口令周期存在风险"
                                            ,"Risk exists in the User Cylce validity ")
                    , "ER_IO_ERROR" : (REINFOECE_ERROR_BASE + 5
                                            , "读取文件发送错误"
                                            ,"Read File Failed")
             }

err_code_mgr.regist_errors(maintainlog_error_defs)