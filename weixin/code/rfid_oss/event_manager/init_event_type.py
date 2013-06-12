#coding=gbk
"""
Copyright (C), 2012-2015, Anything Connected Possibilities
Author: ACP2013
Version: 1.0
Date: 2012-11-08
Description: 
Others:      
Key Class&Method List: 
             1. ....
History: 
1. Date:2012-11-08
   Author:ACP2013
   Modification:新建文件
"""

import os
import os.path
import sys

if __name__ == "__main__":
    import import_paths
    
import mit
from dba import db_cfg_info

from moc_event_manager import EventType 
from moc_event_manager import EventTypeDetail
from moc_event_manager import Event
from moc_event_manager import EventDetail
from moc_event_manager import EventManagerGlobalParam


if __name__=='__main__':
    mit_manager = mit.Mit()
    
    mit_manager.regist_moc(EventType.EventType, EventType.EventTypeRule)
    mit_manager.regist_moc(EventTypeDetail.EventTypeDetail, EventTypeDetail.EventTypeDetailRule)
    mit_manager.regist_moc(Event.Event, Event.EventRule)
    mit_manager.regist_moc(EventDetail.EventDetail, EventDetail.EventDetailRule)
    mit_manager.regist_moc(EventManagerGlobalParam.EventManagerGlobalParam, EventManagerGlobalParam.EventManagerGlobalParamRule)
    
    
    db_file_path = "../../data/sqlite/event_manager.db"
    #清空所有
    try:
        os.remove(db_file_path)
    except:
        pass
    
    mit_manager.open_sqlite(db_file_path)
    
    #mit_manager.open_oracle(**db_cfg_info.get_configure(db_cfg_info.ORACLE_DEFAULT_CON_NAME))
    
    param_rdm = mit_manager.gen_rdm('EventManagerGlobalParam')
    param_rdm.key = 'default'
    param_rdm.default_language = 'chn'
    param_rdm.max_running_export_task = 5
    mit_manager.rdm_add(param_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.0'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Antenna'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.1'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'suggestive'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Antenna'
    mit_manager.rdm_add(event_type_rdm)
    
    # HoppingEvent
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.2'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    
    #GPIEvent start
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.3'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #GPIEvent end
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.4'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #ROSpecEvent start/end
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.5'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #ROSpecEvent end
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.6'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #ROSpecEvent preemption
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.7'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #ReportBufferLevelWarning
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.8'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    
    #ReportBufferOverflowError
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.9'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #RFSurveyEvent start
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.10'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #RFSurveyEvent end
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.11'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #AISpecEvent end
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.12'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #ConnectionAttemptEvent success
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.13'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #ConnectionAttemptEvent fail1
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.14'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #ConnectionAttemptEvent fail2
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.15'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #ConnectionAttemptEvent fail3
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.16'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #ConnectionAttemptEvent  fail4
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.17'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    #ConnectionCloseEvent
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.18'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)    
    
    #ReaderExceptionEvent
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.ControlApp.19'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'Reader'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.LLRPGatewayApp.0'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'PhysicalReader'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.LLRPGatewayApp.1'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'suggestive'
    event_type_rdm.device_type = 'Impinj_R420_Reader'
    event_type_rdm.object_type = 'PhysicalReader'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.MonitorApp.0'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'EAU'
    event_type_rdm.object_type = 'APP'
    mit_manager.rdm_add(event_type_rdm)
    
    #ftp_server
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.FtpServerApp.0'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'suggestive'
    event_type_rdm.device_type = 'EAU'
    event_type_rdm.object_type = 'FTP_USER'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.FtpServerApp.1'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'EAU'
    event_type_rdm.object_type = 'FTP_USER'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.FtpServerApp.2'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'suggestive'
    event_type_rdm.device_type = 'EAU'
    event_type_rdm.object_type = 'FTP_USER'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.FtpServerApp.3'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'suggestive'
    event_type_rdm.device_type = 'EAU'
    event_type_rdm.object_type = 'FTP_FILE'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.FtpServerApp.4'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'suggestive'
    event_type_rdm.device_type = 'EAU'
    event_type_rdm.object_type = 'FTP_FILE'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.FtpServerApp.5'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'EAU'
    event_type_rdm.object_type = 'FTP_FILE'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.FtpServerApp.6'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'EAU'
    event_type_rdm.object_type = 'FTP_FILE'
    mit_manager.rdm_add(event_type_rdm)

    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.0'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='天线断开'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器 %(reader_id)s 的天线  %(antenna_id)s 断开'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='读写器  %(reader_id)s和天线 %(antenna_id)s 之间的连接射频馈线不通，或者天线  %(antenna_id)s 被移走'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.0'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='antenna disconnected'
    event_type_detail_rdm.description='the antenna %(antenna_id)s of the reader %(reader_id)s is disconnected'    
    event_type_detail_rdm.cause='the feeder between reader %(reader_id)s and antenna %(antenna_id)s is blocked up, or the antenna %(antenna_id)s is removed'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.1'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='天线连接'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器 %(reader_id)s 的天线  %(antenna_id)s 连接成功'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.1'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='antenna connected'
    event_type_detail_rdm.description='the antenna %(antenna_id)s of the reader %(reader_id)s is connected'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    

    # HoppingEvent
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.2'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='频率跳变'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器%(reader_id)s跳至%(hop_table_id)s 的第  %(next_channel_index)s 个扫描频道'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)

    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.LLRPGatewayApp.0'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='读写器连接断开'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器 %(reader_id)s 连接断开'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='读写器  %(reader_id)s 设备故障，或者网络故障'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)

    

    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.2'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='hop frequency'
    event_type_detail_rdm.description='the reader %(reader_id)s scan hop to frequency channel %(next_channel_index)s of hop table %(hop_table_id)s '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)

    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.LLRPGatewayApp.0'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='physical reader disconnected'
    event_type_detail_rdm.description='the physical reader %(reader_id)s is disconnected'    
    event_type_detail_rdm.cause='the reader %(reader_id)s fault, or the network fault'
    mit_manager.rdm_add(event_type_detail_rdm)

    

    #GPIEvent start
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.3'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='GPI启用'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器%(reader_id)s的GPI %(gpi_port_number)s 开启'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.3'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='GPIstart'
    event_type_detail_rdm.description='The start of GPI %(gpi_port_number)s for reader %(reader_id)s'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #GPIEvent end
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.4'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='GPI结束'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器%(reader_id)s的GPI %(gpi_port_number)s 关闭'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.4'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='GPI end'
    event_type_detail_rdm.description='The end of GPI %(gpi_port_number)s for reader %(reader_id)s'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ROSpecEvent start
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.5'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='ROSpec开始执行'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(rospec_id)s 开始执行'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.5'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='ROSpec start execute'
    event_type_detail_rdm.description='Start execute ROSpec  %(rospec_id)s   '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ROSpecEvent end
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.6'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='ROSpec执行结束'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(rospec_id)s 执行结束'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.6'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='ROSpec execute end'
    event_type_detail_rdm.description='End execute of ROSpec  %(rospec_id)s   '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ROSpecEvent preemption
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.7'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='ROSpec优先执行'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(preempting_rospec)s在 %(preempted_rospec)s结束之前优先执行'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.7s'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='ROSpec preemption'
    event_type_detail_rdm.description='The ROSpec %(preempting_rospec)s is preempting over current ROSpec  %(preempted_rospec)s'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ReportBufferLevelWarning
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.8'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='缓存不足预警'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器%(reader_id)s报告缓存空间已使用%(percentage)s'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.8'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='Report Buffer Filling up warnings'
    event_type_detail_rdm.description='%(percentage)s of the report buffer of reader %(reader_id)s is filled '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ReportBufferOverflowError
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.9'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='缓存溢出'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器%(reader_id)s缓存溢出'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.9'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='Reader %(reader_id)s Report buffer overflow'
    event_type_detail_rdm.description='Report buffer overflow '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #RFSurveyEvent start
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.10'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='RF扫描开启'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(rospec_id)s 的第 %(index)s个通道扫描开始'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.10'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='RF surrvey start'
    event_type_detail_rdm.descriptio='The %(index)s channel survey of ROSpec %(rospec_id)s start， '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #RFSurveyEvent end
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.11'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='RF扫描结束'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(rospec_id)s 的第 %(index)s个通道扫描结束'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.11'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='RF survey end'
    event_type_detail_rdm.description='The %(index)s channel survey of ROSpec %(rospec_id)s end '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #AISpecEvent Parameter
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.12'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='AI扫描结束'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(rospec_id)s 的第 %(index)s个天线频道列表扫描结束,%(collision_slots)s个事件片段扫描冲突，%(empty_slots)s个事件片段扫描为空'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.12'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='RF survey end'
    event_type_detail_rdm.description='The %(index)s channel survey of ROSpec %(rospec_id)s end，%(collision_slots)s collision slots, %(empty_slots)s empty slots'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ConnectionAttemptEvent success
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.13'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='读写器%(reader_id)s连接成功'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器连接成功'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.13'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='Reader connection success'
    event_type_detail_rdm.description='Reader %(reader_id)s connection success '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ConnectionAttemptEvent failed1
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.14'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='读写器连接失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='已经存在由其他读写器发起的导致读写器%(reader_id)s连接失败'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.14'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='Reader connection failed'
    event_type_detail_rdm.description='A Reader initiated connection to reader %(reader_id)s already exists '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ConnectionAttemptEvent failed2
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.15'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='读写器连接失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='已经存在由其他用户发起的导致读写器%(reader_id)s连接失败'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.15'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='Reader connection failed'
    event_type_detail_rdm.description='A Client initiated connection to reader %(reader_id)s already exists '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ConnectionAttemptEvent failed3
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.16'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='读写器连接失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='除已经存在连接以外的其他原因导致的读写器%(reader_id)s连接失败'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.16'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='Reader connection failed'
    event_type_detail_rdm.description='Any reason other than a connection to reader %(reader_id)s already exists '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ConnectionAttemptEvent failed4
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.17'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='读写器连接失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='多个读写器连接操作同时进行导致读写器%(reader_id)s连接失败'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.17'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='Reader connection failed'
    event_type_detail_rdm.description='Another connection attempted to reader %(reader_id)s '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ConnectionCloseEvent
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.18'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='断开读写器连接'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='断开读写器%(reader_id)s连接'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.18'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='Reader disconnection'
    event_type_detail_rdm.description='Reader %(reader_id)s disconnection '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ReaderExceptionEvent
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.19'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='读写器异常'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器%(reader_id)s异常事件：%(message)s'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.19'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='ReaderException'
    event_type_detail_rdm.description='Reader%(reader_id)s Exception：%(message)s'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)

    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.LLRPGatewayApp.1'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='读写器连接'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='读写器 %(reader_id)s 和EAU连接成功'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.LLRPGatewayApp.1'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='physical reader connected'
    event_type_detail_rdm.description='the physical reader %(reader_id)s is connected'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.MonitorApp.0'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='APP 服务停止'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='APP %(app_name)s 服务服务'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.MonitorApp.0'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='APP stopped'
    event_type_detail_rdm.description='APP %(app_name)s stopped'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.0'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='用户登入'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='用户  %(user_name)s 登入'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.0'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Login'
    event_type_detail_rdm.description='%(user_name)s Login'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.1'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='用户登入失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='用户 %(user_name)s 密码登入失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='用户名或者密码错误'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.1'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Login Failed'
    event_type_detail_rdm.description='%(user_name)s Login Failed'    
    event_type_detail_rdm.cause='Wrong User Name or Wrong Password'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.2'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='用户退出'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='用户  %(user_name)s 退出'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.2'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Logout'
    event_type_detail_rdm.description='%(user_name)s Logout'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.3'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='文件传输成功'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='文件 %(file_name)s 传输成功'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.3'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='File Sent Success'
    event_type_detail_rdm.description='%(file_name)s Sent Success'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.4'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='文件接受成功'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='文件 %(file_name)s 接受成功'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.4'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='File Received Success'
    event_type_detail_rdm.description='%(file_name)s Received Success'
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.5'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='文件传输未完成'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='文件  %(file_name)s 传输失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='网络拥塞'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.5'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='File Sent Not Finish'
    event_type_detail_rdm.description='%(file_name)s Sent Failed'
    event_type_detail_rdm.cause='Network Busy'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.6'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='文件接受未完成'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='文件  %(file_name)s 接受失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='网络拥塞'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.FtpServerApp.6'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='File Received Not Finish'
    event_type_detail_rdm.description='%(file_name)s Received Failed'
    event_type_detail_rdm.cause='Network Busy'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    
    # maintain monitor
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.MaintainApp.0'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'minor'
    event_type_rdm.device_type = 'Common'
    event_type_rdm.object_type = 'APP'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.MaintainApp.0'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='文件被自动删除'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='定时检查监控目录，超过限定大小就删除最旧文件:%(file_name)s'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='监控目录%(dir_name)s超过限定大小'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.MaintainApp.0'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='File is automatically deleted'
    event_type_detail_rdm.description='Monitor the required directory and delete the oldest file(%(file_name)s) once the size of monitored directory exceeds the max size'
    event_type_detail_rdm.cause='The size of the monitored directory %(dir_name)s exceeds the max size'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    # cluster ################################################################################
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.Cluster.be_master'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'minor'
    event_type_rdm.device_type = 'Common'
    event_type_rdm.object_type = 'APP'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.Cluster.be_master'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='集群节点成为master'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='集群节点(%(ip)s)成为master'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='集群状态自动判决'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.Cluster.be_master'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='The cluster node become to master'
    event_type_detail_rdm.description='The cluster node (%(ip)s) become to master'
    event_type_detail_rdm.cause='The cluster status automatically judgment'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    ###
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.Cluster.be_online'
    event_type_rdm.event_flag = 'event'
    event_type_rdm.level = 'minor'
    event_type_rdm.device_type = 'Common'
    event_type_rdm.object_type = 'APP'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.Cluster.be_online'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='集群节点在线'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='集群节点(%(ip)s)在线'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='无'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.Cluster.be_online'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='The cluster node is online'
    event_type_detail_rdm.description='The cluster node (%(ip)s) is online'
    event_type_detail_rdm.cause='None'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    ###
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'event.Cluster.be_offline'
    event_type_rdm.event_flag = 'warn'
    event_type_rdm.level = 'major'
    event_type_rdm.device_type = 'Common'
    event_type_rdm.object_type = 'APP'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.Cluster.be_offline'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='集群节点离线'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='集群节点(%(ip)s)离线'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='无'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.Cluster.be_offline'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='The cluster node is offline'
    event_type_detail_rdm.description='The cluster node (%(ip)s) is offline'
    event_type_detail_rdm.cause='None'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #############################################################
    
    #web security event
    #############################################################
    
    #login
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'security.web.login_success'
    event_type_rdm.event_flag = 'security'
    event_type_rdm.level = 'minor'
    event_type_rdm.device_type = 'Common'
    event_type_rdm.object_type = 'WEB'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_success'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='用户登录成功'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='用户  %(user)s 在 %(ip)s 登录成功'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='登录合法'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_success'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Login Success'
    event_type_detail_rdm.description='The user %(user)s login success by %(ip)s '
    event_type_detail_rdm.cause='This login is allowed'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #现在不支持一个事件可以根据原因码选择不同的事件，因此定义多个事件来解决
    #登录失败有 用户名非法，密码非法，用户未激活，用户被禁止这些原因
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'security.web.login_invalid_user'
    event_type_rdm.event_flag = 'security'
    event_type_rdm.level = 'minor'
    event_type_rdm.device_type = 'Common'
    event_type_rdm.object_type = 'WEB'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_invalid_user'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='用户登录失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='用户  %(user)s 在 %(ip)s 登录失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='用户  %(user)s 非法'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_invalid_user'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Login Failed'
    event_type_detail_rdm.description='The user %(user)s login failed by %(ip)s '
    event_type_detail_rdm.cause='The user %(user)s invalid'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'security.web.login_invalid_password'
    event_type_rdm.event_flag = 'security'
    event_type_rdm.level = 'minor'
    event_type_rdm.device_type = 'Common'
    event_type_rdm.object_type = 'WEB'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_invalid_password'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='用户登录失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='用户  %(user)s 在 %(ip)s 登录失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='密码 非法'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_invalid_password'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Login Failed'
    event_type_detail_rdm.description='The user %(user)s login failed by %(ip)s '
    event_type_detail_rdm.cause='Password is invalid'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'security.web.login_user_not_active'
    event_type_rdm.event_flag = 'security'
    event_type_rdm.level = 'minor'
    event_type_rdm.device_type = 'Common'
    event_type_rdm.object_type = 'WEB'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_user_not_active'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='用户登录失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='用户  %(user)s 在 %(ip)s 登录失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='用户  %(user)s 没有激活'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_user_not_active'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Login Failed'
    event_type_detail_rdm.description='The user %(user)s login failed by %(ip)s '
    event_type_detail_rdm.cause='The user %(user)s is not active'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'security.web.login_user_blocked'
    event_type_rdm.event_flag = 'security'
    event_type_rdm.level = 'minor'
    event_type_rdm.device_type = 'Common'
    event_type_rdm.object_type = 'WEB'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_user_blocked'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='用户登录失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='用户  %(user)s 在 %(ip)s 登录失败'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='用户  %(user)s 被禁用'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_user_blocked'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Login Failed'
    event_type_detail_rdm.description='The user %(user)s login failed by %(ip)s '
    event_type_detail_rdm.cause='The user %(user)s is blocked'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #logout
    event_type_rdm = mit_manager.gen_rdm("EventType")
    event_type_rdm.event_id = 'security.web.logout'
    event_type_rdm.event_flag = 'security'
    event_type_rdm.level = 'minor'
    event_type_rdm.device_type = 'Common'
    event_type_rdm.object_type = 'WEB'
    mit_manager.rdm_add(event_type_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.logout'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='用户登出'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='用户  %(user)s 在  %(ip)s  登出'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause=''.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.logout'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Login'
    event_type_detail_rdm.description='The user %(user)s  logout by %(ip)s'
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    