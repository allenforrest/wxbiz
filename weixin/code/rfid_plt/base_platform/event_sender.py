#coding=gbk

import time
import cPickle

import bundleframework as bf


"""
EVENT_REPORT_COMMAND
命令码必须和event_manager处的定义保持一致
data区有1个参数
event_data:上报event数据,cPickle编码
没有返回信息
"""
EVENT_REPORT_COMMAND = 0x02000000 + 0x0 + 0

class EventData():
    def __init__(self):
        self.__event_id = ''
        self.__event_flag = ''
        self.__generate_time_inner = 0
        self.__generate_time = ''
        self.__device_id = ''
        self.__object_id = ''
        self.__param = {}
    
    def get_event_id(self):
        return self.__event_id
    
    def set_event_id(self, event_id):
        self.__event_id = event_id
        
    def get_event_flag(self):
        return self.__event_flag
    
    def set_event_flag(self, event_flag):
        self.__event_flag = event_flag
    
    def get_generate_time(self):
        return (self.__generate_time_inner, self.__generate_time)
    
    def set_generate_time(self, time_secs):
        self.__generate_time_inner = time_secs
        #self.__generate_time = time.ctime(self.__generate_time_inner)
        self.__generate_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_secs))
        
    def set_generate_time_as_now(self):
        self.__generate_time_inner = int(time.time())
        #self.__generate_time = time.ctime(self.__generate_time_inner)
        self.__generate_time = time.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_device_id(self):
        return self.__device_id
    
    def set_device_id(self, device_id):
        self.__device_id = device_id
    
    def get_object_id(self):
        return self.__object_id
    
    def set_object_id(self, object_id):
        self.__object_id = object_id
    
    def get_params(self):
        return self.__params
    
    def set_params(self, params):
        self.__params = params



g_local_app = None

def set_local_app(app):
    global g_local_app
    g_local_app = app

    
def send_event(event_data):
    if g_local_app is None:
        raise Exception('please set local app first')
    
    if isinstance(event_data, EventData) is not True:
        raise Exception('please give EventData')
    
    frame = bf.AppFrame()
    frame.set_cmd_code(EVENT_REPORT_COMMAND)
    event_data.set_generate_time_as_now()
    
    
    frame.add_data(cPickle.dumps(event_data))

    #向Master EventManagerApp发送
    frame.set_receiver_pid(g_local_app.get_pid("EventManagerApp", bf.MASTER_PID))
    g_local_app.dispatch_frame_to_process_by_pid(frame.get_receiver_pid(), frame)
    
    
    
    