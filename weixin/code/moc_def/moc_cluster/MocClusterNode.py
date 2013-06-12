#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class MocClusterNode(MocBase):
    __MOC_NAME__ = "MocClusterNode"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'ip', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 15),
                MocAttrDef(name = 'is_enable', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [ip], [is_enable] from tbl_MocClusterNode' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "ip", "is_enable" from tbl_MocClusterNode' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_MocClusterNode ([moid], [ip], [is_enable]) values(?1, ?2, ?3)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_MocClusterNode ("moid", "ip", "is_enable") values(:1, :2, :3)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_MocClusterNode set [is_enable]=?1 where [moid]=?2' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_MocClusterNode set "is_enable"=:1 where "moid"=:2' 
    
    ip                             = ''
    is_enable                      = 1
    
    @classmethod
    def gen_moid(cls, **kw):
        return "MocClusterNode_%s" % (repr(kw["ip"]))
    
    def get_moid(self):
        return "MocClusterNode_%s" % (repr(self.ip))
    
    @classmethod
    def get_attr_names(cls): 
        return ('ip',), ('is_enable',)
    
    def from_db_record(self, record):
        self.ip                             = record[1]
        self.is_enable                      = record[2]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.ip
                , self.is_enable
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.is_enable
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class MocClusterNodeRule(MocRule):
    pass
