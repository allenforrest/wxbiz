-- ftp_user的MD5值：4a1edf3937902551d4055b66973de27a
insert into tbl_FtpServerUserMOC("moid", "username", "password", "homedir", "perm")  values  ('FtpServerUserMOC_''ftp_user''', 'ftp_user', '4a1edf3937902551d4055b66973de27a', 'data/ftp', 'elrmw');
-- ftp_root的MD5值：199ad33624b688c0b980b11644307e00
insert into tbl_FtpServerUserMOC("moid", "username", "password", "homedir", "perm")  values  ('FtpServerUserMOC_''ftp_root''', 'ftp_root', '199ad33624b688c0b980b11644307e00', 'data/ftp', 'elradfmwM');  
  
insert into tbl_FtpServerPortMOC("moid", "ftp_port", "ip_listen") values ('FtpServerPortMOC', 7421, '0.0.0.0');

insert into tbl_FtpServerFTPSMOC("moid", "certfile", "keyfile", "tls_control_required", "tls_data_required") 
 values ('FtpServerFTPSMOC', 'data/ssl/cert.pem', 'data/ssl/key.pem', 0, 0);
 
insert into tbl_FtpServerDataLinkMOC("moid", "timeout", "ac_in_buffer_size", "ac_out_buffer_size","read_limit", "write_limit")
 values ('FtpServerDataLinkMOC', 300, 65535, 65535, 0, 0);

insert into tbl_FtpServerCtrlLinkMOC("moid", "timeout", "banner", "max_login_attempts", "permit_foreign_addresses"
              , "permit_privileged_ports", "passive_ports_min", "passive_ports_max", "use_gmt_times" , "tcp_no_delay", "use_sendfile")
 values ('FtpServerCtrlLinkMOC', 300, 'ftp ready', 3, 0, 0, 8000, 8999, 1, 1, 0);
 
insert into tbl_FtpServerAcceptorMOC("moid", "max_cons", "max_cons_per_ip") values('FtpServerAcceptorMOC', 512, 0);
