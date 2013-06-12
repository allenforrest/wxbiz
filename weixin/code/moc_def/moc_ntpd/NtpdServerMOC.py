#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class NtpdServerMOC(MocBase):
    __MOC_NAME__ = "NtpdServerMOC"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'serverip', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [serverip] from tbl_NtpdServerMOC' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "serverip" from tbl_NtpdServerMOC' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_NtpdServerMOC ([moid], [serverip]) values(?1, ?2)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_NtpdServerMOC ("moid", "serverip") values(:1, :2)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_NtpdServerMOC set  where [moid]=?1' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_NtpdServerMOC set  where "moid"=:1' 
    
    serverip                       = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "NtpdServerMOC_%s" % (repr(kw["serverip"]))
    
    def get_moid(self):
        return "NtpdServerMOC_%s" % (repr(self.serverip))
    
    @classmethod
    def get_attr_names(cls): 
        return ('serverip',), ()
    
    def from_db_record(self, record):
        self.serverip                       = record[1]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.serverip
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.get_moid()
                ]
    
    
# The automatic generated rule.
class NtpdServerMOCRule(MocRule):
    pass
