#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class MtnLogMgrParamMoc(MocBase):
    __MOC_NAME__ = "MtnLogMgrParamMoc"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'max_running_export_task', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [max_running_export_task] from tbl_MtnLogMgrParamMoc' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "max_running_export_task" from tbl_MtnLogMgrParamMoc' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_MtnLogMgrParamMoc ([moid], [max_running_export_task]) values(?1, ?2)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_MtnLogMgrParamMoc ("moid", "max_running_export_task") values(:1, :2)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_MtnLogMgrParamMoc set [max_running_export_task]=?1 where [moid]=?2' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_MtnLogMgrParamMoc set "max_running_export_task"=:1 where "moid"=:2' 
    
    max_running_export_task        = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "MtnLogMgrParamMoc"
    
    def get_moid(self):
        return "MtnLogMgrParamMoc"
    
    @classmethod
    def get_attr_names(cls): 
        return (), ('max_running_export_task',)
    
    def from_db_record(self, record):
        self.max_running_export_task        = record[1]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.max_running_export_task
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.max_running_export_task
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class MtnLogMgrParamMocRule(MocRule):
    pass
