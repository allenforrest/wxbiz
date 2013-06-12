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
   Modification:�½��ļ�
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
    #�������
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
    event_type_detail_rdm.name='���߶Ͽ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д�� %(reader_id)s ������  %(antenna_id)s �Ͽ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='��д��  %(reader_id)s������ %(antenna_id)s ֮���������Ƶ���߲�ͨ����������  %(antenna_id)s ������'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='��������'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д�� %(reader_id)s ������  %(antenna_id)s ���ӳɹ�'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='Ƶ������'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д��%(reader_id)s����%(hop_table_id)s �ĵ�  %(next_channel_index)s ��ɨ��Ƶ��'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)

    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.LLRPGatewayApp.0'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='��д�����ӶϿ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д�� %(reader_id)s ���ӶϿ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='��д��  %(reader_id)s �豸���ϣ������������'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='GPI����'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д��%(reader_id)s��GPI %(gpi_port_number)s ����'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='GPI����'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д��%(reader_id)s��GPI %(gpi_port_number)s �ر�'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='ROSpec��ʼִ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(rospec_id)s ��ʼִ��'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='ROSpecִ�н���'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(rospec_id)s ִ�н���'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='ROSpec����ִ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(preempting_rospec)s�� %(preempted_rospec)s����֮ǰ����ִ��'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='���治��Ԥ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д��%(reader_id)s���滺��ռ���ʹ��%(percentage)s'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='�������'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д��%(reader_id)s�������'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='RFɨ�迪��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(rospec_id)s �ĵ� %(index)s��ͨ��ɨ�迪ʼ'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.10'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='RF surrvey start'
    event_type_detail_rdm.descriptio='The %(index)s channel survey of ROSpec %(rospec_id)s start�� '    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #RFSurveyEvent end
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.11'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='RFɨ�����'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(rospec_id)s �ĵ� %(index)s��ͨ��ɨ�����'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='AIɨ�����'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='ROSpec %(rospec_id)s �ĵ� %(index)s������Ƶ���б�ɨ�����,%(collision_slots)s���¼�Ƭ��ɨ���ͻ��%(empty_slots)s���¼�Ƭ��ɨ��Ϊ��'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.12'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='RF survey end'
    event_type_detail_rdm.description='The %(index)s channel survey of ROSpec %(rospec_id)s end��%(collision_slots)s collision slots, %(empty_slots)s empty slots'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #ConnectionAttemptEvent success
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.13'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='��д��%(reader_id)s���ӳɹ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д�����ӳɹ�'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='��д������ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�Ѿ�������������д������ĵ��¶�д��%(reader_id)s����ʧ��'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='��д������ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�Ѿ������������û�����ĵ��¶�д��%(reader_id)s����ʧ��'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='��д������ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='���Ѿ������������������ԭ���µĶ�д��%(reader_id)s����ʧ��'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='��д������ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�����д�����Ӳ���ͬʱ���е��¶�д��%(reader_id)s����ʧ��'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='�Ͽ���д������'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�Ͽ���д��%(reader_id)s����'.decode('gbk').encode('utf-8') 
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
    event_type_detail_rdm.name='��д���쳣'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д��%(reader_id)s�쳣�¼���%(message)s'.decode('gbk').encode('utf-8') 
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.ControlApp.19'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='ReaderException'
    event_type_detail_rdm.description='Reader%(reader_id)s Exception��%(message)s'    
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)

    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='event.LLRPGatewayApp.1'
    event_type_detail_rdm.language='chn'
    event_type_detail_rdm.name='��д������'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��д�� %(reader_id)s ��EAU���ӳɹ�'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='APP ����ֹͣ'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='APP %(app_name)s �������'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�û�����'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�û�  %(user_name)s ����'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�û�����ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�û� %(user_name)s �������ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='�û��������������'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�û��˳�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�û�  %(user_name)s �˳�'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�ļ�����ɹ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�ļ� %(file_name)s ����ɹ�'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�ļ����ܳɹ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�ļ� %(file_name)s ���ܳɹ�'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�ļ�����δ���'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�ļ�  %(file_name)s ����ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='����ӵ��'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�ļ�����δ���'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�ļ�  %(file_name)s ����ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='����ӵ��'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�ļ����Զ�ɾ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��ʱ�����Ŀ¼�������޶���С��ɾ������ļ�:%(file_name)s'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='���Ŀ¼%(dir_name)s�����޶���С'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='��Ⱥ�ڵ��Ϊmaster'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��Ⱥ�ڵ�(%(ip)s)��Ϊmaster'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='��Ⱥ״̬�Զ��о�'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='��Ⱥ�ڵ�����'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��Ⱥ�ڵ�(%(ip)s)����'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='��'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='��Ⱥ�ڵ�����'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='��Ⱥ�ڵ�(%(ip)s)����'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='��'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�û���¼�ɹ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�û�  %(user)s �� %(ip)s ��¼�ɹ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='��¼�Ϸ�'.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.login_success'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Login Success'
    event_type_detail_rdm.description='The user %(user)s login success by %(ip)s '
    event_type_detail_rdm.cause='This login is allowed'
    mit_manager.rdm_add(event_type_detail_rdm)
    
    #���ڲ�֧��һ���¼����Ը���ԭ����ѡ��ͬ���¼�����˶������¼������
    #��¼ʧ���� �û����Ƿ�������Ƿ����û�δ����û�����ֹ��Щԭ��
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
    event_type_detail_rdm.name='�û���¼ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�û�  %(user)s �� %(ip)s ��¼ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='�û�  %(user)s �Ƿ�'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�û���¼ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�û�  %(user)s �� %(ip)s ��¼ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='���� �Ƿ�'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�û���¼ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�û�  %(user)s �� %(ip)s ��¼ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='�û�  %(user)s û�м���'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�û���¼ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�û�  %(user)s �� %(ip)s ��¼ʧ��'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause='�û�  %(user)s ������'.decode('gbk').encode('utf-8')
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
    event_type_detail_rdm.name='�û��ǳ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.description='�û�  %(user)s ��  %(ip)s  �ǳ�'.decode('gbk').encode('utf-8')
    event_type_detail_rdm.cause=''.decode('gbk').encode('utf-8')
    mit_manager.rdm_add(event_type_detail_rdm)
    
    event_type_detail_rdm = mit_manager.gen_rdm("EventTypeDetail")
    event_type_detail_rdm.event_id='security.web.logout'
    event_type_detail_rdm.language='eng'
    event_type_detail_rdm.name='User Login'
    event_type_detail_rdm.description='The user %(user)s  logout by %(ip)s'
    event_type_detail_rdm.cause=''
    mit_manager.rdm_add(event_type_detail_rdm)
    