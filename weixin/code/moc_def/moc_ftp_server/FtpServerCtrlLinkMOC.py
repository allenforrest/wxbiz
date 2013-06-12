#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class FtpServerCtrlLinkMOC(MocBase):
    __MOC_NAME__ = "FtpServerCtrlLinkMOC"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'timeout', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'banner', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'max_login_attempts', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'permit_foreign_addresses', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'permit_privileged_ports', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'passive_ports_min', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'passive_ports_max', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'use_gmt_times', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'tcp_no_delay', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'use_sendfile', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [timeout], [banner], [max_login_attempts], [permit_foreign_addresses], [permit_privileged_ports], [passive_ports_min], [passive_ports_max], [use_gmt_times], [tcp_no_delay], [use_sendfile] from tbl_FtpServerCtrlLinkMOC' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "timeout", "banner", "max_login_attempts", "permit_foreign_addresses", "permit_privileged_ports", "passive_ports_min", "passive_ports_max", "use_gmt_times", "tcp_no_delay", "use_sendfile" from tbl_FtpServerCtrlLinkMOC' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_FtpServerCtrlLinkMOC ([moid], [timeout], [banner], [max_login_attempts], [permit_foreign_addresses], [permit_privileged_ports], [passive_ports_min], [passive_ports_max], [use_gmt_times], [tcp_no_delay], [use_sendfile]) values(?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_FtpServerCtrlLinkMOC ("moid", "timeout", "banner", "max_login_attempts", "permit_foreign_addresses", "permit_privileged_ports", "passive_ports_min", "passive_ports_max", "use_gmt_times", "tcp_no_delay", "use_sendfile") values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_FtpServerCtrlLinkMOC set [timeout]=?1, [banner]=?2, [max_login_attempts]=?3, [permit_foreign_addresses]=?4, [permit_privileged_ports]=?5, [passive_ports_min]=?6, [passive_ports_max]=?7, [use_gmt_times]=?8, [tcp_no_delay]=?9, [use_sendfile]=?10 where [moid]=?11' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_FtpServerCtrlLinkMOC set "timeout"=:1, "banner"=:2, "max_login_attempts"=:3, "permit_foreign_addresses"=:4, "permit_privileged_ports"=:5, "passive_ports_min"=:6, "passive_ports_max"=:7, "use_gmt_times"=:8, "tcp_no_delay"=:9, "use_sendfile"=:10 where "moid"=:11' 
    
    timeout                        = 0
    banner                         = ''
    max_login_attempts             = 0
    permit_foreign_addresses       = 0
    permit_privileged_ports        = 0
    passive_ports_min              = 0
    passive_ports_max              = 0
    use_gmt_times                  = 0
    tcp_no_delay                   = 0
    use_sendfile                   = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "FtpServerCtrlLinkMOC"
    
    def get_moid(self):
        return "FtpServerCtrlLinkMOC"
    
    @classmethod
    def get_attr_names(cls): 
        return (), ('timeout', 'banner', 'max_login_attempts', 'permit_foreign_addresses', 'permit_privileged_ports', 'passive_ports_min', 'passive_ports_max', 'use_gmt_times', 'tcp_no_delay', 'use_sendfile')
    
    def from_db_record(self, record):
        self.timeout                        = record[1]
        self.banner                         = record[2]
        self.max_login_attempts             = record[3]
        self.permit_foreign_addresses       = record[4]
        self.permit_privileged_ports        = record[5]
        self.passive_ports_min              = record[6]
        self.passive_ports_max              = record[7]
        self.use_gmt_times                  = record[8]
        self.tcp_no_delay                   = record[9]
        self.use_sendfile                   = record[10]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.timeout
                , self.banner
                , self.max_login_attempts
                , self.permit_foreign_addresses
                , self.permit_privileged_ports
                , self.passive_ports_min
                , self.passive_ports_max
                , self.use_gmt_times
                , self.tcp_no_delay
                , self.use_sendfile
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.timeout
                , self.banner
                , self.max_login_attempts
                , self.permit_foreign_addresses
                , self.permit_privileged_ports
                , self.passive_ports_min
                , self.passive_ports_max
                , self.use_gmt_times
                , self.tcp_no_delay
                , self.use_sendfile
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class FtpServerCtrlLinkMOCRule(MocRule):
    pass
