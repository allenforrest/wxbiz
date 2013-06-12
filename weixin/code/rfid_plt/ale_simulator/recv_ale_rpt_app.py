#coding=gbk
#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-09-20
Description: 收取ALE报告的模拟器
Others:      
Key Class&Method List: 
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
import plt_cmd_code_def

class RecvALERptHandler(bf.CmdHandler):

    def handle_cmd(self, frame):
        print "=================================================="
        print frame.get_data()


class RecvALERptWorker(bf.CmdWorker):

    
    def __init__(self, min_task_id, max_task_id):
        bf.CmdWorker.__init__(self, "RecvALERptWorker", min_task_id, max_task_id)

        
    def ready_for_work(self):
        
        self.register_handler(RecvALERptHandler(), plt_cmd_code_def.CMD_REPORT_FROM_ALE_APP)

        return 0



class RecvALERptApp(bf.BasicApp):

    def __init__(self):
        bf.BasicApp.__init__(self, "ALESimulator_RecvAleRpt")
            
    def _is_need_shake_with_monitor(self):
        return False

    def _ready_for_work(self):

        
        worker = RecvALERptWorker(min_task_id=1, max_task_id=9999)
        
        self.register_worker(worker)
        
        return 0


RecvALERptApp().run()      
