#coding=gbk


import threading
import collections

import tracelog
import err_code_mgr

from _bundleframework.protocol.appframe import AppFrame
from _bundleframework.cmdhandler.cmd_worker import CmdWorker
from _bundleframework.cmdhandler.cmd_handler import CmdHandler

from _bundleframework.dispatch.work_thread import WorkThread
from _bundleframework import local_cmd_code

from _bundleframework.name.msg_def import NameBroadCastMessage

class NameBroadcastHandler(CmdHandler):
    def handle_cmd(self, frame):
        buf = frame.get_data()
        try:
            msg = NameBroadCastMessage.deserialize(buf)            
        except Exception:            
            tracelog.exception('deserialize NameBroadCastMessage exception! buf:%s'%buf)
            return

        #print "==NameBroadcastHandler", msg
        self.get_worker().get_app().on_process_app_register(msg.all_app_infos)
        
        
        
class CommonCmdWorker(CmdWorker):
    """
    Class: RpcWorker
    Description: 处理RPC请求的worker
    Base: CmdWorker
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

        CmdWorker.__init__(self, name = "CommonCmdWorker", min_task_id = 0xFFFE0000, max_task_id = 0xFFFEFFF0)
    
    def ready_for_work(self):
        self.register_handler(NameBroadcastHandler(), local_cmd_code.BROADCAST_NAME)
        
       
        
        return 0

        

