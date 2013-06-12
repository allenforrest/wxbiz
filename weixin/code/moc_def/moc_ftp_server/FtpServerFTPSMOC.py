#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class FtpServerFTPSMOC(MocBase):
    __MOC_NAME__ = "FtpServerFTPSMOC"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'certfile', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'keyfile', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'tls_control_required', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'tls_data_required', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [certfile], [keyfile], [tls_control_required], [tls_data_required] from tbl_FtpServerFTPSMOC' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "certfile", "keyfile", "tls_control_required", "tls_data_required" from tbl_FtpServerFTPSMOC' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_FtpServerFTPSMOC ([moid], [certfile], [keyfile], [tls_control_required], [tls_data_required]) values(?1, ?2, ?3, ?4, ?5)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_FtpServerFTPSMOC ("moid", "certfile", "keyfile", "tls_control_required", "tls_data_required") values(:1, :2, :3, :4, :5)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_FtpServerFTPSMOC set [certfile]=?1, [keyfile]=?2, [tls_control_required]=?3, [tls_data_required]=?4 where [moid]=?5' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_FtpServerFTPSMOC set "certfile"=:1, "keyfile"=:2, "tls_control_required"=:3, "tls_data_required"=:4 where "moid"=:5' 
    
    certfile                       = ''
    keyfile                        = ''
    tls_control_required           = 0
    tls_data_required              = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "FtpServerFTPSMOC"
    
    def get_moid(self):
        return "FtpServerFTPSMOC"
    
    @classmethod
    def get_attr_names(cls): 
        return (), ('certfile', 'keyfile', 'tls_control_required', 'tls_data_required')
    
    def from_db_record(self, record):
        self.certfile                       = record[1]
        self.keyfile                        = record[2]
        self.tls_control_required           = record[3]
        self.tls_data_required              = record[4]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.certfile
                , self.keyfile
                , self.tls_control_required
                , self.tls_data_required
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.certfile
                , self.keyfile
                , self.tls_control_required
                , self.tls_data_required
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class FtpServerFTPSMOCRule(MocRule):
    pass
