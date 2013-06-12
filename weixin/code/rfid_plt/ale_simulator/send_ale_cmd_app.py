#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-25
Description: 发送ALE命令的模拟器
Others:     
    举例:
    python send_ale_cmd_app.py --case="case1 para, case2, case1 para2 para2"

Key Class&Method List: 
History: 
1. Date:
   Author:
   Modification:
"""


import os.path
import sys
import getopt

if __name__ == "__main__":
    import import_paths

import bundleframework as bf
import tracelog
import plt_cmd_code_def



def prase_opt():
    """
    Function: prase_opt
    Description: 解析命令行参数
    Parameter: 
    Return: 
    Others: 
    """


    case = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h',  
          [ 
            'case=',   
            'help' 
            ] 
          ) 
    except Exception, e:
        tracelog.error(str(e))
        exit(1)
        
    for option, value in opts:
        if  option in ["-h","--help"]: 
            print (
                '--help : print this message\n'
                '--case="xxxx"\n'
                'example: python send_cmd_app.py --case="case1 para, case2, case1 para2, para2"'
                )
            exit(0)
        
        if  option == "--case": 
            case = value
            continue


    if case == "":        
        tracelog.error("--case is not found!")
        exit(1)

    return case

    



class ALECase:
    """
    Class: ALECase
    Description: ALE命令用例，从命令行的参数解析得到了
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
            case_name: 用例名称
            args: 用例参数
            case_entity:用例实体
        """

        self.case_name = ""
        self.agrs = []

        self.case_entity = None

    def __str__(self):

        if len(self.agrs) == 0:
            return self.case_name

        else:
            return "%s%s" % (self.case_name, str(self.agrs))




class RequestDirver:
    """
    Class: RequestDirver
    Description: ALE用例的驱动器
    Base: 
    Others: 
    """

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            ale_server_addr: 接收ALE命令的server端的地址(ip, port)
            __taskid: 当前用例的任务号，每当执行一个用例后，任务号加1
        Return: 
        Others: 
        """
        pass    

    def run(self, app, option):
        """
        Method:    run
        Description: 运行所有的用例
        Parameter: 
            option: 命令行中的case选项的值
        Return: 
        Others: 
        """


        try:
            all_case = self.prase_case(option)

            for case in all_case:
                if self.run_case(app, case) != 0:
                    tracelog.error("run case failed. stop.")
                    break
        except:
            tracelog.exception("run ALE case failed.")
            

    def prase_case(self, option):
        """
        Method:    prase_case
        Description: 解析命令行中case选项的字符串
        Parameter: 
            option: 命令行中case选项的值
        Return: 解析出的用例列表
        Others: 
        """

        # case1 para, case2, case1 para2, para2
        all_case = []

        option = option.strip('" ')
        
        cases = option.split(",")
        for case in cases:
            case = case.strip()
            if case == '':
                continue

            case_obj = ALECase()
            tmp = case.split(" ")
            case_obj.case_name = tmp[0]
            case_obj.agrs = [item for item in tmp[1:] if item != '']
            all_case.append(case_obj)

        return all_case


    def run_case(self, app, case):
        """
        Method:    run_case
        Description: 运行一个用例
        Parameter: 
            case: 一个用例, instance of ALECase
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        tracelog.info("run case %s..." % str(case))

        ret = self.find_case_entity(case)    
        if ret != 0:
            return -1

        case.case_entity

        frame = bf.AppFrame()
        frame.set_cmd_code(case.case_entity.get_cmd_code())
        frame.add_data(case.case_entity.gen_request())
        frame.set_receiver_pid(app.get_pid("AleGate"))

        ack_frames = bf.rpc_request(frame, case.case_entity.get_timeout())
        if len(ack_frames) == 0:
            tracelog.error("wait for response timeout. case:%s" % str(case)) 
        else:
            case.case_entity.handle_ack(ack_frames[0].get_data())
        
        return 0
        

    def find_case_entity(self, case):
        """
        Method:    find_case_entity
        Description: 根据用例的名称加载用例实体
        Parameter: 
            case: 用例
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        try:
            exec("from cmd_case.%s import %s as case_entity_def" % (case.case_name, case.case_name))
        except:
            tracelog.exception("load case.%s.%s failed." % (case.case_name, case.case_name))
            return -1
                        
        case.case_entity = case_entity_def(case.agrs)
        return 0




            
class SendALECmdThread(bf.WatchedThread):

    def __init__(self, app, case_opt):
        bf.WatchedThread.__init__(self)

        self.__app = app
        self.__case_opt = case_opt
        
    def run(self):
        
        
        RequestDirver().run(self.__app, self.__case_opt)

        self.over()
        self.__app.stop(0)

        

class SendALECmdApp(bf.BasicApp):

    def __init__(self, case_opt):
        bf.BasicApp.__init__(self, "ALESimulator_SendAleCmd")

        self.__case_opt = case_opt
            
    def _is_need_shake_with_monitor(self):
        return False

    def _ready_for_work(self):
        
        self.register_watched_thread(SendALECmdThread(self, self.__case_opt))
        
        return 0


if __name__ == "__main__":
    #case_opt = prase_opt()
    case_opt = "ADD_ECSpec"
    SendALECmdApp(case_opt).run()      



