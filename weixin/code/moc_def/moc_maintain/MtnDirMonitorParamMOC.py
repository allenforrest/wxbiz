#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class MtnDirMonitorParamMOC(MocBase):
    __MOC_NAME__ = "MtnDirMonitorParamMOC"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'directory_path', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 512),
                MocAttrDef(name = 'max_size', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'whether_to_report', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [directory_path], [max_size], [whether_to_report] from tbl_MtnDirMonitorParamMOC' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "directory_path", "max_size", "whether_to_report" from tbl_MtnDirMonitorParamMOC' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_MtnDirMonitorParamMOC ([moid], [directory_path], [max_size], [whether_to_report]) values(?1, ?2, ?3, ?4)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_MtnDirMonitorParamMOC ("moid", "directory_path", "max_size", "whether_to_report") values(:1, :2, :3, :4)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_MtnDirMonitorParamMOC set [max_size]=?1, [whether_to_report]=?2 where [moid]=?3' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_MtnDirMonitorParamMOC set "max_size"=:1, "whether_to_report"=:2 where "moid"=:3' 
    
    directory_path                 = ''
    max_size                       = 0
    whether_to_report              = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "MtnDirMonitorParamMOC_%s" % (repr(kw["directory_path"]))
    
    def get_moid(self):
        return "MtnDirMonitorParamMOC_%s" % (repr(self.directory_path))
    
    @classmethod
    def get_attr_names(cls): 
        return ('directory_path',), ('max_size', 'whether_to_report')
    
    def from_db_record(self, record):
        self.directory_path                 = record[1]
        self.max_size                       = record[2]
        self.whether_to_report              = record[3]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.directory_path
                , self.max_size
                , self.whether_to_report
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.max_size
                , self.whether_to_report
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class MtnDirMonitorParamMOCRule(MocRule):
    pass
