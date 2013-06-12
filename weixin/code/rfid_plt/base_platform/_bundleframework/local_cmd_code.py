#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-10
Description: 本文件中定义boundframework使用的命令码
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


# 1001~2000 framework的命令码区间

CMD_SHAKEHAND_WITH_MONITOR = 1001
CMD_ACK_MSG = 1002
BROADCAST_NAME = 1003

#framework发送给monitor的命令码 2101-2150
"""
请求：AppRegisterRequest
响应：AppRegisterResponse
"""
REGISTER_NAME_COMMAND = 2101

"""
请求：AppUnRegisterRequest
响应：AppUnRegisterResponse
"""
UNREGISTER_NAME_COMMAND = 2102

"""
请求：AppUnRegisterRequest
响应：AppUnRegisterResponse
"""
QUERY_APP_COMMAND = 2103

# 查询master的命令码
# 请求消息
CMD_QUERY_CLUSTER_MASTER_IP = 2104


