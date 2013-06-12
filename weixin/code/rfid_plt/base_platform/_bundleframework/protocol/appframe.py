#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-08-31
Description: ���ļ���ʵ���˽��̼�ͨ�ŵ�ͳһ��Ϣ��ʽ
Others:      
Key Class&Method List: 
             1. AppFrame: ���̼�ͨ�ŵ�ͳһ��Ϣ��ʽ
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
    Description: ���̼�ͨ�ŵ�ͳһ��Ϣ��ʽ
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
        Description: ���캯��
        Parameter: ��
        Return: 
        Others: 
        """

        # �����ߵ�pid
        self.__sender_pid       = 0

        # �����ߵ�pid
        self.__receiver_pid     = 0

        # �ڿ�ϵͳ������Ϣʱ��original_pid�����ݴ�sender_pid
        self.__original_pid      = 0

        # ����Ҫͨ���м�ģ��ת����Ϣʱ��ʹ��next_pid��ʾ��һ��
        self.__next_pid         = 0
        
        # ������
        self.__cmd_code         = 0

        # �����
        self.__task_id          = 0

        # �ִε�id
        self.__round_id           = 0

        # ��Ϣ�ı��(��֡�����һ֡���м�֡����β֡)
        self.__frame_tag        = 0

        # ��֡����µ�֡���
        self.__frame_no         = 0

        # ���ȼ�
        self.__priority         = AppFrame.medium_priority

        # ��Ϣ�Ĵ���ʱ��
        self.__created_time     = time.time()


        # __custom_bytes�����Ȳ�����255�ֽڣ�������ʹ�����Զ��塣
        # �����ڲ�������Ϣ������������¶�ȡһЩ��Ϣ
        # ���һ���prepare_for_ack�л���
        self.__custom_bytes     = "" 

        # ���ݵ��ܳ���
        self.__data_length      = 0

        # ���е����ݲ���
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
        Description: ��¡��ǰ��Ϣ
        Parameter: ��
        Return: ��¡������Ϣ
        Others: 
        """

        return copy.deepcopy(self)

    def set_cmd_code(self, cmd_code):
        """
        Method:    set_cmd_code
        Description: ����������
        Parameter: 
            cmd_code: ������
        Return: 
        Others: 
        """

        self.__cmd_code = cmd_code

    def get_cmd_code(self):
        """
        Method:    get_cmd_code
        Description: ��ȡ������
        Parameter: ��
        Return: ������
        Others: 
        """

        return self.__cmd_code

        
    def set_sender_pid(self, pid):
        """
        Method:    set_sender_pid
        Description: ���÷����ߵ�pid
        Parameter: 
            pid: �����ߵ�pid
        Return: 
        Others: 
        """

        self.__sender_pid = pid

    def get_sender_pid(self):
        """
        Method:    get_sender_pid
        Description: ��ȡ�����ߵ�pid
        Parameter: ��
        Return: �����ߵ�pid
        Others: 
        """

        return self.__sender_pid

    def set_receiver_pid(self, pid):
        """
        Method:    set_receiver_pid
        Description: ���ý����ߵ�pid
        Parameter: 
            pid: �����ߵ�pid
        Return: 
        Others: 
        """

        self.__receiver_pid = pid

    def get_receiver_pid(self):
        """
        Method:    get_receiver_pid
        Description: ��ȡ�����ߵ�pid
        Parameter: ��
        Return: �����ߵ�pid
        Others: 
        """

        return self.__receiver_pid

    def set_original_pid(self, pid):
        """
        Method:    set_original_pid
        Description: ����ԭʼ�ķ�����pid
        Parameter: 
            pid: ԭʼ�ķ�����pid
        Return: 
        Others: 
        """

        self.__original_pid = pid

    def get_original_pid(self):
        """
        Method:    get_original_pid
        Description: ��ȡԭʼ�ķ�����pid
        Parameter: ��
        Return: ԭʼ�ķ�����pid
        Others: 
        """

        return self.__original_pid

    def set_next_pid(self, pid):
        """
        Method:    set_next_pid
        Description: ������һ����pid
        Parameter: ��
        Return:  
        Others: 
        """    
        self.__next_pid = pid

    def get_next_pid(self):
        """
        Method:    get_next_pid
        Description: ����һ����pid
        Parameter: ��
        Return: ��һ����pid
        Others: 
        """    
        return self.__next_pid
        

    def set_task_id(self, task_id):
        """
        Method:    set_task_id
        Description: ���������
        Parameter: 
            task_id: �����
        Return: 
        Others: 
        """

        self.__task_id = task_id

    def get_task_id(self):
        """
        Method:    get_task_id
        Description: ��ȡ�����
        Parameter: ��
        Return: �����
        Others: 
        """

        return self.__task_id

    #def get_ws_type(self):
    #    return self.__task_id & 0XFFFF

    def set_priority(self, priority):
        """
        Method:    set_priority
        Description: �������ȼ�
        Parameter: 
            priority: ���ȼ�
        Return: 
        Others: 
        """

        self.__priority = priority

    def get_priority(self):
        """
        Method:    get_priority
        Description: ��ȡ���ȼ�
        Parameter: ��
        Return: ���ȼ�
        Others: 
        """

        return self.__priority

    def set_round_id(self, round_id):
        """
        Method:    set_round_id
        Description: �����ִε�id
        Parameter: 
            round_id: �ִε�id
        Return: 
        Others: 
        """

        self.__round_id = round_id

    def get_round_id(self):
        """
        Method:    get_round_id
        Description: ��ȡ�ִε�id
        Parameter: ��
        Return: �ִε�id
        Others: 
        """

        return self.__round_id

    def get_create_time(self):
        """
        Method:    get_create_time
        Description: ��ȡ��ǰ��Ϣ�Ĵ���ʱ��
        Parameter: ��
        Return: ��ǰ��Ϣ�Ĵ���ʱ��
        Others: 
        """

        return self.__created_time

    def is_last(self):
        """
        Method:    is_last
        Description: �ж��Ƿ������һ����Ϣ
        Parameter: ��
        Return: �Ƿ������һ����Ϣ
        Others: 
        """

        return self.__frame_tag in (AppFrame.single, AppFrame.end)

    def get_tag(self):
        """
        Method:    get_tag
        Description: ��ȡ��Ϣ�ı��
        Parameter: ��
        Return: ��Ϣ�ı��
        Others: 
        """

        return self.__frame_tag

    def set_tag(self, tag):
        """
        Method:    set_tag
        Description: ������Ϣ�ı��
        Parameter: 
            tag: ��Ϣ�ı��
        Return: 
        Others: 
        """

        self.__frame_tag = tag

    def get_frame_no(self):
        """
        Method:    get_frame_no
        Description: ��ȡ��Ϣ�����
        Parameter: ��
        Return: ��Ϣ�����
        Others: 
        """

        return self.__frame_no

    def set_frame_no(self, frame_no):
        """
        Method:    set_frame_no
        Description: ������Ϣ�����
        Parameter: 
            frame_no: ��Ϣ�����
        Return: 
        Others: 
        """

        self.__frame_no = frame_no

    def set_custom_bytes(self, bytes):
        """
        Method:    set_custom_bytes
        Description: �����Զ�����ֽ�
        Parameter: 
            bytes: �Զ�����ֽ�
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
        Description: ��ȡ�Զ�����ֽ�
        Parameter: ��
        Return: �Զ�����ֽ�
        Others: 
        """

        return self.__custom_bytes
    
    def add_data(self, data):
        """
        Method:    add_data
        Description: ����һ�����ݵ�������
        Parameter: 
            data: ����������
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
        Description: ��ȡָ���±������
        Parameter: 
            index: ���ݵ��±�
        Return: ����������
        Others: 
        """

        if index == 0 and len(self.__datas) == 0:
            return ""
            
        return self.__datas[index]

    def get_data_size(self, index = 0):
        """
        Method:    get_data_size
        Description: ��ȡָ���±�����ݵĳ���
        Parameter: 
            index: �±�
        Return: ָ���±�����ݵĳ���
        Others: 
        """

        if index == 0 and len(self.__datas) == 0:
            return 0

        return len(self.__datas[index])
        
    def get_data_num(self):
        """
        Method:    get_data_num
        Description: ��ȡ���ݵĸ���
        Parameter: ��
        Return: ���ݵĸ���
        Others: 
        """

        return len(self.__datas)

    def clear_data(self):
        """
        Method:    clear_data
        Description: ���������
        Parameter: ��
        Return: 
        Others: 
        """
        self.__datas = []
        self.__data_length = 0
        

    def get_total_size(self):        
        """
        Method:    get_total_size
        Description: ��ȡ���ݵ��ܳ���
        Parameter: ��
        Return: ���ݵ��ܳ���
        Others: 
        """

        return (self.__header_length 
                    + len(self.__custom_bytes) 
                    + len(self.__datas) * self.__uint_len 
                    + self.__data_length)


    def __get_data_format(self, index):    
        """
        Method:    __get_data_format
        Description: ��ȡָ���±�����ݵĸ�ʽ����struct.packʹ��
        Parameter: 
            index: �±�
        Return: 
        Others: 
        """

        return "%us" % len(self.__datas[index])

    def serialize_to_buffer(self):
        """
        Method:    serialize_to_buffer
        Description: ����ǰ��Ϣ���л���һ��buffer��
        Parameter: ��
        Return: ���л���Ķ�������
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
            
            # �Զ����ֽ�
            if custom_bytes_len > 0:
                pack_into("%us" % custom_bytes_len, buffer, offset, self.__custom_bytes)
                offset += custom_bytes_len
            

            # ������
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
        Description: ��һ��buffer�з����л�
        Parameter: 
            buffer: ������buffer
            position: buffer��ƫ��
        Return: 
            0: �ɹ�
            ��0: ʧ��
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
            
            # �Զ����ֽ�
            if custom_bytes_len > 0:
                self.__custom_bytes = unpack_from("%us" % custom_bytes_len, buffer, offset)[0]
                offset += custom_bytes_len
            else:
                self.__custom_bytes = ""
            
            # ������
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
        Description: ���л�Ϊһ��python�ַ�������
        Parameter: ��
        Return: ���л����python�ַ�������
        Others: 
        """

        return self.serialize_to_buffer()
        

    @classmethod
    def serialize_from_str(cls, strIn):
        """
        Method:    serialize_from_str
        Description: ��python���ַ����������л�
        Parameter: 
            strIn: ������python�ַ���
        Return: 
            None: �����л�ʧ��
            ��None: �����л����AppFrame
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

            
            # ������
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
        Description: �������ͷ��ͽ��շ�����Ϣ
        Parameter: ��
        Return: 
        Others: 
        """

        #self.__sender_ip, self.__receiver_ip = self.__receiver_ip, self.__sender_ip
        self.__sender_pid, self.__receiver_pid = self.__receiver_pid, self.__sender_pid
        

    def prepare_for_ack(self, req_frame):
        """
        Method:    prepare_for_ack
        Description: ���������������Ϣreq_frame�����Ϣ����������Ӧ����Ϣ��ص��ֶ�
        Parameter: 
            req_frame: �����������Ϣ
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
    Description: ����������֪ͨ��Ϣ
    Base: 
    Others: 
    """

    def __init__(self, process_id, pid):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            process_id: ������OS�е�pid
            pid: ���з����id
        Return: 
        Others: 
        """

        self.__process_id = process_id
        self.__pid = pid

    def get_pid(self):
        """
        Method:    get_pid
        Description: ��ȡpid
        Parameter: ��
        Return: ֪ͨ��Ϣ�еĽ��̵�pid
        Others: 
        """

        return self.__pid

    def to_frame(self):
        """
        Method:    to_frame
        Description: ����AppFrame
        Parameter: ��
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
        Description: ��AppFrame�����л�
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
    Description: �¼�֪ͨ
    Base: 
    Others: 
    """

    def __init__(self, code, para1, para2):
        """
        Method:    __init__
        Description: ���캯��
        Parameter: 
            code: �¼�id
            para1: ����1
            para2: ����2
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
        Description: ��AppFrame�����л�
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
        Description: ����AppFrame
        Parameter: ��
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
        Description: ��ȡ�¼�id
        Parameter: ��
        Return: �¼�id
        Others: 
        """

        return self.__code

    def get_para1(self):
        """
        Method:    get_para1
        Description: ��ȡ����1
        Parameter: ��
        Return: ����1
        Others: 
        """

        return self.__para1

    def get_para2(self):
        """
        Method:    get_para2
        Description: ��ȡ����2
        Parameter: ��
        Return: ����2
        Others: 
        """

        return self.__para2

    @classmethod
    def __serialize_struct(cls):
        """
        Method:    __serialize_struct
        Description: �õ�structģ��ʹ�õĽṹ��Ϣ
        Parameter: ��
        Return: 
        Others: 
        """

        return struct.Struct("III")


