----------- moc group: cluster ----------
-- moc: MocClusterNode
exec sys.proc_drop_table('tbl_MocClusterNode'); 
create table tbl_MocClusterNode( 
            "moid" varchar2(128)
            , "ip" varchar2(15)
            , "is_enable" number(10, 0)
            , primary key("moid")
            );

create index idx_MocClusterNode on tbl_MocClusterNode("ip");

----------- moc group: name_service ----------
-- moc: AppInstance
exec sys.proc_drop_table('tbl_AppInstance'); 
create table tbl_AppInstance( 
            "moid" varchar2(128)
            , "pid" number(10, 0)
            , "instance_name" varchar2(64)
            , "service_name" varchar2(64)
            , "instance_id" number(10, 0)
            , "system_ip" varchar2(64)
            , "node_type" varchar2(64)
            , "endpoint" varchar2(64)
            , "endpoint_protocol" varchar2(64)
            , "update_time" number(10, 0)
            , "state" varchar2(64)
            , primary key("moid")
            );

create index idx_AppInstance on tbl_AppInstance("pid");

-- moc: AppType
exec sys.proc_drop_table('tbl_AppType'); 
create table tbl_AppType( 
            "moid" varchar2(128)
            , "service_name" varchar2(64)
            , "instance_num" varchar2(64)
            , primary key("moid")
            );

create index idx_AppType on tbl_AppType("service_name");

----------- moc group: event_manager ----------
-- moc: Event
exec sys.proc_drop_table('tbl_Event'); 
create table tbl_Event( 
            "moid" varchar2(128)
            , "sequence_no" number(10, 0)
            , "event_id" varchar2(64)
            , "event_flag" varchar2(64)
            , "level" varchar2(64)
            , "time_inner" number(10, 0)
            , "time" varchar2(64)
            , "device_type" varchar2(64)
            , "device_id" varchar2(64)
            , "object_type" varchar2(64)
            , "object_id" varchar2(64)
            , primary key("moid")
            );

create index idx_Event on tbl_Event("sequence_no");

-- moc: EventDetail
exec sys.proc_drop_table('tbl_EventDetail'); 
create table tbl_EventDetail( 
            "moid" varchar2(128)
            , "sequence_no" number(10, 0)
            , "language" varchar2(64)
            , "name" varchar2(64)
            , "description" varchar2(1024)
            , "cause" varchar2(1024)
            , primary key("moid")
            );

create index idx_EventDetail on tbl_EventDetail("language");

-- moc: EventManagerGlobalParam
exec sys.proc_drop_table('tbl_EventManagerGlobalParam'); 
create table tbl_EventManagerGlobalParam( 
            "moid" varchar2(128)
            , "key" varchar2(64)
            , "default_language" varchar2(64)
            , "max_running_export_task" number(10, 0)
            , "exported_file_nums_policy" number(10, 0)
            , "exported_file_days_policy" number(10, 0)
            , "max_query_records_per_page" number(10, 0)
            , primary key("moid")
            );

create index idx_EventManagerGlobalParam on tbl_EventManagerGlobalParam("key");

-- moc: EventType
exec sys.proc_drop_table('tbl_EventType'); 
create table tbl_EventType( 
            "moid" varchar2(128)
            , "event_id" varchar2(128)
            , "event_flag" varchar2(64)
            , "level" varchar2(64)
            , "device_type" varchar2(64)
            , "object_type" varchar2(64)
            , primary key("moid")
            );

create index idx_EventType on tbl_EventType("event_id");

-- moc: EventTypeDetail
exec sys.proc_drop_table('tbl_EventTypeDetail'); 
create table tbl_EventTypeDetail( 
            "moid" varchar2(128)
            , "event_id" varchar2(128)
            , "language" varchar2(64)
            , "name" varchar2(64)
            , "description" varchar2(1024)
            , "cause" varchar2(1024)
            , primary key("moid")
            );

create index idx_EventTypeDetail on tbl_EventTypeDetail("language");

----------- moc group: ftp_server ----------
-- moc: FtpServerCtrlLinkMOC
exec sys.proc_drop_table('tbl_FtpServerCtrlLinkMOC'); 
create table tbl_FtpServerCtrlLinkMOC( 
            "moid" varchar2(128)
            , "timeout" number(10, 0)
            , "banner" varchar2(64)
            , "max_login_attempts" number(10, 0)
            , "permit_foreign_addresses" number(10, 0)
            , "permit_privileged_ports" number(10, 0)
            , "passive_ports_min" number(10, 0)
            , "passive_ports_max" number(10, 0)
            , "use_gmt_times" number(10, 0)
            , "tcp_no_delay" number(10, 0)
            , "use_sendfile" number(10, 0)
            , primary key("moid")
            );


-- moc: FtpServerDataLinkMOC
exec sys.proc_drop_table('tbl_FtpServerDataLinkMOC'); 
create table tbl_FtpServerDataLinkMOC( 
            "moid" varchar2(128)
            , "timeout" number(10, 0)
            , "ac_in_buffer_size" number(10, 0)
            , "ac_out_buffer_size" number(10, 0)
            , "read_limit" number(10, 0)
            , "write_limit" number(10, 0)
            , primary key("moid")
            );


-- moc: FtpServerFTPSMOC
exec sys.proc_drop_table('tbl_FtpServerFTPSMOC'); 
create table tbl_FtpServerFTPSMOC( 
            "moid" varchar2(128)
            , "certfile" varchar2(64)
            , "keyfile" varchar2(64)
            , "tls_control_required" number(10, 0)
            , "tls_data_required" number(10, 0)
            , primary key("moid")
            );


-- moc: FtpServerMasqueradeAddr
exec sys.proc_drop_table('tbl_FtpServerMasqueradeAddr'); 
create table tbl_FtpServerMasqueradeAddr( 
            "moid" varchar2(128)
            , "private_ip" varchar2(64)
            , "public_ip" varchar2(64)
            , primary key("moid")
            );

create index idx_FtpServerMasqueradeAddr on tbl_FtpServerMasqueradeAddr("private_ip");

-- moc: FtpServerPortMOC
exec sys.proc_drop_table('tbl_FtpServerPortMOC'); 
create table tbl_FtpServerPortMOC( 
            "moid" varchar2(128)
            , "ftp_port" number(10, 0)
            , "ip_listen" varchar2(64)
            , primary key("moid")
            );


-- moc: FtpServerUserMOC
exec sys.proc_drop_table('tbl_FtpServerUserMOC'); 
create table tbl_FtpServerUserMOC( 
            "moid" varchar2(128)
            , "username" varchar2(64)
            , "password" varchar2(64)
            , "homedir" varchar2(64)
            , "perm" varchar2(64)
            , primary key("moid")
            );

create index idx_FtpServerUserMOC on tbl_FtpServerUserMOC("username");

-- moc: FtpServerAcceptorMOC
exec sys.proc_drop_table('tbl_FtpServerAcceptorMOC'); 
create table tbl_FtpServerAcceptorMOC( 
            "moid" varchar2(128)
            , "max_cons" number(10, 0)
            , "max_cons_per_ip" number(10, 0)
            , primary key("moid")
            );


----------- moc group: maintain ----------
-- moc: MtnLogMgrParamMoc
exec sys.proc_drop_table('tbl_MtnLogMgrParamMoc'); 
create table tbl_MtnLogMgrParamMoc( 
            "moid" varchar2(128)
            , "max_running_export_task" number(10, 0)
            , primary key("moid")
            );


-- moc: MtnDirMonitorParamMOC
exec sys.proc_drop_table('tbl_MtnDirMonitorParamMOC'); 
create table tbl_MtnDirMonitorParamMOC( 
            "moid" varchar2(128)
            , "directory_path" varchar2(512)
            , "max_size" number(10, 0)
            , "whether_to_report" number(10, 0)
            , primary key("moid")
            );

create index idx_MtnDirMonitorParamMOC on tbl_MtnDirMonitorParamMOC("directory_path");

----------- moc group: ntpd ----------
-- moc: NtpdControlMOC
exec sys.proc_drop_table('tbl_NtpdControlMOC'); 
create table tbl_NtpdControlMOC( 
            "moid" varchar2(128)
            , "openserver" varchar2(64)
            , "stratum" number(10, 0)
            , primary key("moid")
            );


-- moc: NtpdServerMOC
exec sys.proc_drop_table('tbl_NtpdServerMOC'); 
create table tbl_NtpdServerMOC( 
            "moid" varchar2(128)
            , "serverip" varchar2(64)
            , primary key("moid")
            );

create index idx_NtpdServerMOC on tbl_NtpdServerMOC("serverip");

-- moc: NtpdSubnetMOC
exec sys.proc_drop_table('tbl_NtpdSubnetMOC'); 
create table tbl_NtpdSubnetMOC( 
            "moid" varchar2(128)
            , "subnetip" varchar2(64)
            , "mask" varchar2(64)
            , primary key("moid")
            );

create index idx_NtpdSubnetMOC on tbl_NtpdSubnetMOC("mask");

