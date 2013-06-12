#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class FtpServerAcceptorMOC(MocBase):
    __MOC_NAME__ = "FtpServerAcceptorMOC"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'max_cons', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'max_cons_per_ip', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [max_cons], [max_cons_per_ip] from tbl_FtpServerAcceptorMOC' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "max_cons", "max_cons_per_ip" from tbl_FtpServerAcceptorMOC' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_FtpServerAcceptorMOC ([moid], [max_cons], [max_cons_per_ip]) values(?1, ?2, ?3)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_FtpServerAcceptorMOC ("moid", "max_cons", "max_cons_per_ip") values(:1, :2, :3)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_FtpServerAcceptorMOC set [max_cons]=?1, [max_cons_per_ip]=?2 where [moid]=?3' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_FtpServerAcceptorMOC set "max_cons"=:1, "max_cons_per_ip"=:2 where "moid"=:3' 
    
    max_cons                       = 0
    max_cons_per_ip                = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "FtpServerAcceptorMOC"
    
    def get_moid(self):
        return "FtpServerAcceptorMOC"
    
    @classmethod
    def get_attr_names(cls): 
        return (), ('max_cons', 'max_cons_per_ip')
    
    def from_db_record(self, record):
        self.max_cons                       = record[1]
        self.max_cons_per_ip                = record[2]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.max_cons
                , self.max_cons_per_ip
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.max_cons
                , self.max_cons_per_ip
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class FtpServerAcceptorMOCRule(MocRule):
    pass
