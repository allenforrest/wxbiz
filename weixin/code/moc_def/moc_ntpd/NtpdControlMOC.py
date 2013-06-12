#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class NtpdControlMOC(MocBase):
    __MOC_NAME__ = "NtpdControlMOC"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'openserver', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'stratum', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [openserver], [stratum] from tbl_NtpdControlMOC' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "openserver", "stratum" from tbl_NtpdControlMOC' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_NtpdControlMOC ([moid], [openserver], [stratum]) values(?1, ?2, ?3)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_NtpdControlMOC ("moid", "openserver", "stratum") values(:1, :2, :3)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_NtpdControlMOC set [openserver]=?1, [stratum]=?2 where [moid]=?3' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_NtpdControlMOC set "openserver"=:1, "stratum"=:2 where "moid"=:3' 
    
    openserver                     = ''
    stratum                        = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "NtpdControlMOC"
    
    def get_moid(self):
        return "NtpdControlMOC"
    
    @classmethod
    def get_attr_names(cls): 
        return (), ('openserver', 'stratum')
    
    def from_db_record(self, record):
        self.openserver                     = record[1]
        self.stratum                        = record[2]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.openserver
                , self.stratum
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.openserver
                , self.stratum
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class NtpdControlMOCRule(MocRule):
    pass
