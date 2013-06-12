#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""

import bundleframework as bf

# 命令转发的对应表
# [(起始命令码, 结束命令码, 进程的服务名字，get_pid()的策略), ... ]
# 其中get_pid()的策略有bf.FIRSTLOCAL_PID、bf.ONLYLOCAL_PID、bf.RANDOM_PID、bf.MASTER_PID
cmd_dispatch_map = [

# maintain
#    (0x02005000, 0x02005001, 'MaintainApp', bf.ONLYLOCAL_PID),

# EventManager
#    (0x02000000, 0x02000FFF, 'EventManagerApp', bf.MASTER_PID),

# ImcDeviceMgr
#    (0x02001000, 0x02001FFF, 'IMCDeviceMgr', bf.MASTER_PID),
    
# WeixinPublicApp
    (0x01010000, 0x0101FFFF, 'WXGateApp', bf.ONLYLOCAL_PID),    
    (0x01020000, 0x01024FFF, 'PortalManApp', bf.ONLYLOCAL_PID),
    (0x01025000, 0x01025FFF, 'EventCenterApp', bf.ONLYLOCAL_PID)
    
]




def get_duty_service(cmd_code):
    """
    Function: get_duty_service
    Description: 根据命令码获取处理该命令的服务名和进程转发的策略
    Parameter: 
        cmd_code: 命令码
    Return: 
        处理该命令的服务名
    Others: 
    """

    global cmd_dispatch_map
    
    for strat_cmd, end_cmd, service_name, strategy in cmd_dispatch_map:
        if strat_cmd <= cmd_code <= end_cmd:
            return service_name, strategy

    return (None, None)
    