#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-31
Description: 本文件中实现了进程间通信的统一消息格式
Others:      
Key Class&Method List: 
             1. AppFrame: 进程间通信的统一消息格式
History: 
1. Date:
   Author:
   Modification:
"""


from struct import pack_into, unpack_from, calcsize
import struct
from ctypes import create_string_buffer
import copy
import time

import tracelog
import err_code_mgr

from _bundleframework import local_cmd_code

class AppFrame():
    """
    Class: AppFrame
    Description: 进程间通信的统一消息格式
    Base: 
    Others: 
    """
    
    invalid_priority  = -1
    low_priority      = 0
    medium_priority   = 1
    high_priority     = 2
    event_priority    = 3
    total_priority    = 4

    cmd_code_for_event                      = 65535
    cmd_code_for_shake_hand_with_monitor    = 65534
    cmd_code_for_notify_monitor             = 65533
    cmd_code_for_stop_process               = 65532
    cmd_code_for_notify_update_peer_addr    = 65531

    ws_unify_bin = 13

    single = 0
    start  = 1
    middle = 2
    end    = 3

    __header_format = "IIIIIIIBHbdBI"
    __header_length = calcsize(__header_format)

    __uint_len = calcsize("I")

    def __init__(self):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 无
        Return: 
        Others: 
        """

        # 发送者的pid
        self.__sender_pid       = 0

        # 接收者的pid
        self.__receiver_pid     = 0

        # 在跨系统发送消息时，original_pid用来暂存sender_pid
        self.__original_pid      = 0

        # 当需要通过中间模块转发消息时，使用next_pid表示下一跳
        self.__next_pid         = 0
        
        # 命令码
        self.__cmd_code         = 0

        # 任务号
        self.__task_id          = 0

        # 轮次的id
        self.__round_id           = 0

        # 消息的标记(单帧，或第一帧、中间帧、结尾帧)
        self.__frame_tag        = 0

        # 多帧情况下的帧序号
        self.__frame_no         = 0

        # 优先级
        self.__priority         = AppFrame.medium_priority

        # 消息的创建时间
        self.__created_time     = time.time()


        # __custom_bytes，长度不超过255字节，可以让使用者自定义。
        # 方便在不解析消息数据区的情况下读取一些信息
        # 并且会在prepare_for_ack中回填
        self.__custom_bytes     = "" 

        # 数据的总长度
        self.__data_length      = 0

        # 所有的数据部分
        self.__datas = []

    def __str__(self):
        data = ""
        
        if len(self.__datas) > 0:
            data = self.__datas[0]
            if len(data) > 200:
                data = ", data[0]:" + repr(data[:200]) + "..."
            else:
                data = ", data[0]:" + repr(data)
            
        return ("<AppFrame cmd_code:%r, sender_pid:%r, receiver_pid:%r, "
                "original_pid:%r, next_pid:%r, task_id:%r, data_length:%d, "
                "datas num:%d%s>" % (
                     self.__cmd_code
                    , self.__sender_pid
                    , self.__receiver_pid
                    , self.__original_pid
                    , self.__next_pid
                    , self.__task_id
                    , self.__data_length
                    , len(self.__datas)
                    , data
                    ))

    def __repr__(self):
        return str(self)
        
    def clone(self):
        """
        Method:    clone
        Description: 克隆当前消息
        Parameter: 无
        Return: 克隆出的消息
        Others: 
        """

        return copy.deepcopy(self)

    def set_cmd_code(self, cmd_code):
        """
        Method:    set_cmd_code
        Description: 设置命令码
        Parameter: 
            cmd_code: 命令码
        Return: 
        Others: 
        """

        self.__cmd_code = cmd_code

    def get_cmd_code(self):
        """
        Method:    get_cmd_code
        Description: 获取命令码
        Parameter: 无
        Return: 命令码
        Others: 
        """

        return self.__cmd_code

        
    def set_sender_pid(self, pid):
        """
        Method:    set_sender_pid
        Description: 设置发送者的pid
        Parameter: 
            pid: 发送者的pid
        Return: 
        Others: 
        """

        self.__sender_pid = pid

    def get_sender_pid(self):
        """
        Method:    get_sender_pid
        Description: 获取发送者的pid
        Parameter: 无
        Return: 发送者的pid
        Others: 
        """

        return self.__sender_pid

    def set_receiver_pid(self, pid):
        """
        Method:    set_receiver_pid
        Description: 设置接收者的pid
        Parameter: 
            pid: 发送者的pid
        Return: 
        Others: 
        """

        self.__receiver_pid = pid

    def get_receiver_pid(self):
        """
        Method:    get_receiver_pid
        Description: 获取接收者的pid
        Parameter: 无
        Return: 接收者的pid
        Others: 
        """

        return self.__receiver_pid

    def set_original_pid(self, pid):
        """
        Method:    set_original_pid
        Description: 设置原始的发送者pid
        Parameter: 
            pid: 原始的发送者pid
        Return: 
        Others: 
        """

        self.__original_pid = pid

    def get_original_pid(self):
        """
        Method:    get_original_pid
        Description: 获取原始的发送者pid
        Parameter: 无
        Return: 原始的发送者pid
        Others: 
        """

        return self.__original_pid

    def set_next_pid(self, pid):
        """
        Method:    set_next_pid
        Description: 设置下一跳的pid
        Parameter: 无
        Return:  
        Others: 
        """    
        self.__next_pid = pid

    def get_next_pid(self):
        """
        Method:    get_next_pid
        Description: 获下一跳的pid
        Parameter: 无
        Return: 下一跳的pid
        Others: 
        """    
        return self.__next_pid
        

    def set_task_id(self, task_id):
        """
        Method:    set_task_id
        Description: 设置任务号
        Parameter: 
            task_id: 任务号
        Return: 
        Others: 
        """

        self.__task_id = task_id

    def get_task_id(self):
        """
        Method:    get_task_id
        Description: 获取任务号
        Parameter: 无
        Return: 任务号
        Others: 
        """

        return self.__task_id

    #def get_ws_type(self):
    #    return self.__task_id & 0XFFFF

    def set_priority(self, priority):
        """
        Method:    set_priority
        Description: 设置优先级
        Parameter: 
            priority: 优先级
        Return: 
        Others: 
        """

        self.__priority = priority

    def get_priority(self):
        """
        Method:    get_priority
        Description: 获取优先级
        Parameter: 无
        Return: 优先级
        Others: 
        """

        return self.__priority

    def set_round_id(self, round_id):
        """
        Method:    set_round_id
        Description: 设置轮次的id
        Parameter: 
            round_id: 轮次的id
        Return: 
        Others: 
        """

        self.__round_id = round_id

    def get_round_id(self):
        """
        Method:    get_round_id
        Description: 获取轮次的id
        Parameter: 无
        Return: 轮次的id
        Others: 
        """

        return self.__round_id

    def get_create_time(self):
        """
        Method:    get_create_time
        Description: 获取当前消息的创建时间
        Parameter: 无
        Return: 当前消息的创建时间
        Others: 
        """

        return self.__created_time

    def is_last(self):
        """
        Method:    is_last
        Description: 判断是否是最后一条消息
        Parameter: 无
        Return: 是否是最后一条消息
        Others: 
        """

        return self.__frame_tag in (AppFrame.single, AppFrame.end)

    def get_tag(self):
        """
        Method:    get_tag
        Description: 获取消息的标记
        Parameter: 无
        Return: 消息的标记
        Others: 
        """

        return self.__frame_tag

    def set_tag(self, tag):
        """
        Method:    set_tag
        Description: 设置消息的标记
        Parameter: 
            tag: 消息的标记
        Return: 
        Others: 
        """

        self.__frame_tag = tag

    def get_frame_no(self):
        """
        Method:    get_frame_no
        Description: 获取消息的序号
        Parameter: 无
        Return: 消息的序号
        Others: 
        """

        return self.__frame_no

    def set_frame_no(self, frame_no):
        """
        Method:    set_frame_no
        Description: 设置消息的序号
        Parameter: 
            frame_no: 消息的序号
        Return: 
        Others: 
        """

        self.__frame_no = frame_no

    def set_custom_bytes(self, bytes):
        """
        Method:    set_custom_bytes
        Description: 设置自定义的字节
        Parameter: 
            bytes: 自定义的字节
        Return: 
        Others: 
        """

        if len(bytes) > 255:
            self.__custom_bytes = bytes[:255]
        else:
            self.__custom_bytes = bytes
            
    def get_custom_bytes(self):
        """
        Method:    get_custom_bytes
        Description: 获取自定义的字节
        Parameter: 无
        Return: 自定义的字节
        Others: 
        """

        return self.__custom_bytes
    
    def add_data(self, data):
        """
        Method:    add_data
        Description: 增加一个数据到数据区
        Parameter: 
            data: 二进制数据
        Return: 
        Others: 
        """

        self.__datas.append(data)
        self.__data_length += len(data)

    def rmv_data(self, index=-1):
        data = self.__datas.pop(index)
        self.__data_length -= len(data)

    def get_data(self, index = 0):
        """
        Method:    get_data
        Description: 获取指定下标的数据
        Parameter: 
            index: 数据的下标
        Return: 二进制数据
        Others: 
        """

        if index == 0 and len(self.__datas) == 0:
            return ""
            
        return self.__datas[index]

    def get_data_size(self, index = 0):
        """
        Method:    get_data_size
        Description: 获取指定下标的数据的长度
        Parameter: 
            index: 下标
        Return: 指定下标的数据的长度
        Others: 
        """

        if index == 0 and len(self.__datas) == 0:
            return 0

        return len(self.__datas[index])
        
    def get_data_num(self):
        """
        Method:    get_data_num
        Description: 获取数据的个数
        Parameter: 无
        Return: 数据的个数
        Others: 
        """

        return len(self.__datas)

    def clear_data(self):
        """
        Method:    clear_data
        Description: 清空数据区
        Parameter: 无
        Return: 
        Others: 
        """
        self.__datas = []
        self.__data_length = 0
        

    def get_total_size(self):        
        """
        Method:    get_total_size
        Description: 获取数据的总长度
        Parameter: 无
        Return: 数据的总长度
        Others: 
        """

        return (self.__header_length 
                    + len(self.__custom_bytes) 
                    + len(self.__datas) * self.__uint_len 
                    + self.__data_length)


    def __get_data_format(self, index):    
        """
        Method:    __get_data_format
        Description: 获取指定下标的数据的格式，给struct.pack使用
        Parameter: 
            index: 下标
        Return: 
        Others: 
        """

        return "%us" % len(self.__datas[index])

    def serialize_to_buffer(self):
        """
        Method:    serialize_to_buffer
        Description: 将当前消息序列化到一段buffer中
        Parameter: 无
        Return: 序列化后的二进制流
        Others: 
        """

        try:
            buffer = create_string_buffer(self.get_total_size())

            custom_bytes_len = len(self.__custom_bytes)
            
            pack_into(self.__header_format, buffer, 0
                    , self.__sender_pid
                    , self.__receiver_pid
                    , self.__original_pid
                    , self.__next_pid
                    , self.__task_id
                    , self.__round_id
                    , self.__cmd_code
                    , self.__frame_tag
                    , self.__frame_no
                    , self.__priority
                    , self.__created_time
                    , custom_bytes_len
                    , len(self.__datas))

            offset = self.__header_length
            
            # 自定义字节
            if custom_bytes_len > 0:
                pack_into("%us" % custom_bytes_len, buffer, offset, self.__custom_bytes)
                offset += custom_bytes_len
            

            # 数据区
            if len(self.__datas) > 0:
                uint_len = self.__uint_len
                
                for data  in self.__datas:
                    pack_into("I", buffer, offset, len(data))
                    offset += uint_len

                for i, data in enumerate(self.__datas):
                    lenght = len(data)
                    pack_into("%us" % lenght, buffer, offset, data)
                    offset += lenght

            return buffer.raw
        except Exception, e:
            tracelog.error("AppFrame.serialize_to_buffer failed. cmd_code:%d" % self.__cmd_code)
            raise
    
    def serialize_from_buffer(self, buffer, position):
        """
        Method:    serialize_from_buffer
        Description: 从一个buffer中反序列化
        Parameter: 
            buffer: 给定的buffer
            position: buffer的偏移
        Return: 
            0: 成功
            非0: 失败
        Others: 
        """

        try:
            offset = position
            result = unpack_from(self.__header_format, buffer, offset)

            self.__sender_pid           = result[0]
            self.__receiver_pid         = result[1]
            self.__original_pid         = result[2]
            self.__next_pid             = result[3]
            self.__task_id             = result[4]
            self.__round_id             = result[5]
            self.__cmd_code             = result[6]
            self.__frame_tag            = result[7]
            self.__frame_no             = result[8]
            self.__priority             = result[9]
            self.__created_time         = result[10]
            custom_bytes_len            = result[11]
            data_num                    = result[12]

            offset += self.__header_length
            
            # 自定义字节
            if custom_bytes_len > 0:
                self.__custom_bytes = unpack_from("%us" % custom_bytes_len, buffer, offset)[0]
                offset += custom_bytes_len
            else:
                self.__custom_bytes = ""
            
            # 数据区
            self.clear_data()
            if data_num > 0:
                data_lens = unpack_from("%uI" % data_num, buffer, offset)

                offset += data_num * self.__uint_len
                
                for data_len in data_lens:
                    result = unpack_from("%us" % data_len, buffer, offset)
                    self.add_data(result[0])
                    offset += data_len
                        
            return 0
        except:
            tracelog.exception("serialize_from_buffer failed. cmd_code:%s", self.__cmd_code)
            
            return -1

    def serialize_to_str(self):
        """
        Method:    serialize_to_str
        Description: 序列化为一个python字符串对象
        Parameter: 无
        Return: 序列化后的python字符串对象
        Others: 
        """

        return self.serialize_to_buffer()
        

    @classmethod
    def serialize_from_str(cls, strIn):
        """
        Method:    serialize_from_str
        Description: 从python的字符串对象反序列化
        Parameter: 
            strIn: 给定的python字符串
        Return: 
            None: 反序列化失败
            非None: 反序列化后的AppFrame
        Others: 
        """

        try:

            #result = struct.unpack(cls.__header_format, strIn[0:cls.__header_length])
            result = unpack_from(cls.__header_format, strIn, 0)
            oneFrame = AppFrame()
            
            oneFrame.__sender_pid           = result[0]
            oneFrame.__receiver_pid         = result[1]
            oneFrame.__original_pid         = result[2]
            oneFrame.__next_pid             = result[3]
            oneFrame.__task_id             = result[4]
            oneFrame.__round_id             = result[5]
            oneFrame.__cmd_code             = result[6]
            oneFrame.__frame_tag            = result[7]
            oneFrame.__frame_no             = result[8]
            oneFrame.__priority             = result[9]
            oneFrame.__created_time         = result[10]
            custom_bytes_len                = result[11]
            data_num                        = result[12]

            offset = cls.__header_length

            if custom_bytes_len > 0:
                #oneFrame.__custom_bytes = struct.unpack("%us" % custom_bytes_len, strIn[offset: offset + custom_bytes_len])[0]
                oneFrame.__custom_bytes = unpack_from("%us" % custom_bytes_len, strIn, offset)[0]
                offset += custom_bytes_len

            
            # 数据区
            if data_num > 0:
                #data_lens = struct.unpack("%uI" % data_num, strIn[offset: offset + data_num * cls.__uint_len])
                data_lens = unpack_from("%uI" % data_num, strIn, offset)

                offset += data_num * cls.__uint_len
                
                for data_len in data_lens:                
                    oneFrame.add_data(strIn[offset : offset + data_len])
                    offset += data_len
                                                
            return oneFrame
            
        except:
            raise
            return None

    def swap(self):
        """
        Method:    swap
        Description: 交换发送方和接收方的信息
        Parameter: 无
        Return: 
        Others: 
        """

        #self.__sender_ip, self.__receiver_ip = self.__receiver_ip, self.__sender_ip
        self.__sender_pid, self.__receiver_pid = self.__receiver_pid, self.__sender_pid
        

    def prepare_for_ack(self, req_frame):
        """
        Method:    prepare_for_ack
        Description: 根据命令的请求消息req_frame里的信息，填充命令的应答消息相关的字段
        Parameter: 
            req_frame: 命令的请求消息
        Return: 
        Others: 
        """
        self.set_cmd_code(local_cmd_code.CMD_ACK_MSG)
        self.set_receiver_pid(req_frame.get_sender_pid())
        self.set_original_pid(req_frame.get_original_pid())
        self.set_task_id(req_frame.get_task_id())  
        self.set_round_id(req_frame.get_round_id())  
        self.set_custom_bytes(req_frame.get_custom_bytes())


    def is_ack_frame(self):
        return self.__cmd_code == local_cmd_code.CMD_ACK_MSG

class ProcessStartNotify():
    """
    Class: ProcessStartNotify
    Description: 进程启动的通知消息
    Base: 
    Others: 
    """

    def __init__(self, process_id, pid):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            process_id: 进程在OS中的pid
            pid: 自行分配的id
        Return: 
        Others: 
        """

        self.__process_id = process_id
        self.__pid = pid

    def get_pid(self):
        """
        Method:    get_pid
        Description: 获取pid
        Parameter: 无
        Return: 通知消息中的进程的pid
        Others: 
        """

        return self.__pid

    def to_frame(self):
        """
        Method:    to_frame
        Description: 生成AppFrame
        Parameter: 无
        Return: instance of AppFrame
        Others: 
        """

        frame = AppFrame()
        if frame:
            frame.set_cmd_code(AppFrame.cmd_code_for_notify_monitor)
            frame.add_data(struct.Struct("II").pack(self.__process_id, self.__pid))
        return frame

    @classmethod
    def from_frame(cls, frame):
        """
        Method:    from_frame
        Description: 从AppFrame反序列化
        Parameter: 
            frame: 
        Return: 
        Others: 
        """

        if frame == None:
            return None

        if frame.get_cmd_code() != AppFrame.cmd_code_for_notify_monitor:
            return None

        try:
            result = struct.Struct("II").unpack(frame.get_data())
            return ProcessStartNotify(result[0], result[1])
        except Exception, e:
            return None

class AppEvent(object):
    """
    Class: AppEvent
    Description: 事件通知
    Base: 
    Others: 
    """

    def __init__(self, code, para1, para2):
        """
        Method:    __init__
        Description: 构造函数
        Parameter: 
            code: 事件id
            para1: 参数1
            para2: 参数2
        Return: 
        Others: 
        """

        self.__code  = code
        self.__para1 = para1
        self.__para2 = para2

    @classmethod
    def from_frame(cls, frame):
        """
        Method:    from_frame
        Description: 从AppFrame反序列化
        Parameter: 
            frame: AppFrame
        Return: 
        Others: 
        """

        if frame == None:
            return None

        if frame.get_cmd_code() != AppFrame.cmd_code_for_event:
            return None

        try:
            result = AppEvent.__serialize_struct().unpack(frame.get_data())
            return AppEvent(result(0), result(1), result(2))
        except Exception, e:
            tracelog.exception("invalid event" + e)
            return None

    def to_frame(self):
        """
        Method:    to_frame
        Description: 生成AppFrame
        Parameter: 无
        Return: instance of AppFrame
        Others: 
        """

        frame = AppFrame()

        frame.set_cmd_code(AppFrame.cmd_code_for_event)

        data = AppEvent.__serialize_struct().pack(self.__code, self.__para1, self.__para2)
        frame.add_data(data)

        return frame

    def get_code(self):
        """
        Method:    get_code
        Description: 获取事件id
        Parameter: 无
        Return: 事件id
        Others: 
        """

        return self.__code

    def get_para1(self):
        """
        Method:    get_para1
        Description: 获取参数1
        Parameter: 无
        Return: 参数1
        Others: 
        """

        return self.__para1

    def get_para2(self):
        """
        Method:    get_para2
        Description: 获取参数2
        Parameter: 无
        Return: 参数2
        Others: 
        """

        return self.__para2

    @classmethod
    def __serialize_struct(cls):
        """
        Method:    __serialize_struct
        Description: 得到struct模块使用的结构信息
        Parameter: 无
        Return: 
        Others: 
        """

        return struct.Struct("III")


