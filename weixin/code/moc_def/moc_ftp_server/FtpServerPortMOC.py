#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class FtpServerPortMOC(MocBase):
    __MOC_NAME__ = "FtpServerPortMOC"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'ftp_port', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'ip_listen', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [ftp_port], [ip_listen] from tbl_FtpServerPortMOC' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "ftp_port", "ip_listen" from tbl_FtpServerPortMOC' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_FtpServerPortMOC ([moid], [ftp_port], [ip_listen]) values(?1, ?2, ?3)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_FtpServerPortMOC ("moid", "ftp_port", "ip_listen") values(:1, :2, :3)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_FtpServerPortMOC set [ftp_port]=?1, [ip_listen]=?2 where [moid]=?3' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_FtpServerPortMOC set "ftp_port"=:1, "ip_listen"=:2 where "moid"=:3' 
    
    ftp_port                       = 0
    ip_listen                      = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "FtpServerPortMOC"
    
    def get_moid(self):
        return "FtpServerPortMOC"
    
    @classmethod
    def get_attr_names(cls): 
        return (), ('ftp_port', 'ip_listen')
    
    def from_db_record(self, record):
        self.ftp_port                       = record[1]
        self.ip_listen                      = record[2]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.ftp_port
                , self.ip_listen
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.ftp_port
                , self.ip_listen
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class FtpServerPortMOCRule(MocRule):
    pass
