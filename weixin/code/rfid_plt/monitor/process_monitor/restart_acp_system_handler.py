#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-01
Description: 本文中实现了复位ACP软件系统的handler
Others:      
Key Class&Method List: 
             1. RestartACPSystemHandler: 复位ACP软件系统的handler
History: 
1. Date:
   Author:
   Modification:
"""

import bundleframework as bf
import tracelog

from process_stat_mgr import ProcessStatMgr

class RestartACPSystemHandler(bf.CmdHandler):
    """
    Class: RestartACPSystemHandler
    Description: 复位ACP软件系统的handler
    Base: 
    Others: 
    """
    
    def handle_cmd(self, frame):

        tracelog.info("receive restart ACP system command.")
        
        worker = self.get_worker()
        app = worker.get_app()
        app.soft_restart()
        

        
