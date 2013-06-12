#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-19
Description: 本文件中定义boundframework使用的错误码
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""



# 1001~2000  framework的错误码区间

error_defs = {"ER_TOO_MUCH_COMMANDS_WAITING"    : (1001, "worker中有太多的任务在等待应答", "Thera are too much commands waitting for ACK")
             , "ER_RECEIVE_FRAME_FAILED"        :  (1002, "接收消息失败", "")
             , "ER_MULTI_REGISTER_NAME_FAILED"        :  (1003, "多次尝试注册名字服务失败", "Multiple attempts of register nameservice failed")
             , "ER_GET_AVAILIABLE_PORT_FAILED"        :  (1004, "获取可用端口失败", "get available port failed")
             }


