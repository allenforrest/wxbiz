#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 
Description: 本文中定义了web、后台app之间消息转发的进程
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:
   Author:
   Modification:
"""


import os.path
import sys

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import tracelog

from message_dispath_worker import MessageDispathWorker


class WebGateApp(bf.BasicApp):
    """
    Class:    WebGateApp
    Description: WebGate模块的进程类
    Base: BasicApp    
    Others: 无
    """

    def __init__(self):
        """
        Method: __init__
        Description: 类初始化
        Parameter: 无
        Return: 
        Others: 
        """

        bf.BasicApp.__init__(self, "WebGate")
            
    
    def _ready_for_work(self):
        """
        Method:    _ready_for_work
        Description: 进程启动时的初始化工作，注册线程和worker
        Parameter:  无
        Return: 
                0   -- 成功
                                      非0 -- 失败
        Others: 无
        """
        
        worker = MessageDispathWorker(min_task_id=1, max_task_id=9999)
        
        self.register_worker(worker)
        
        return 0



if __name__ == "__main__":
    WebGateApp().run()




