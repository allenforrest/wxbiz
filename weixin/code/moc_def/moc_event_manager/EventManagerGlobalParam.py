#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class EventManagerGlobalParam(MocBase):
    __MOC_NAME__ = "EventManagerGlobalParam"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'key', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'default_language', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'max_running_export_task', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'exported_file_nums_policy', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'exported_file_days_policy', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'max_query_records_per_page', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [key], [default_language], [max_running_export_task], [exported_file_nums_policy], [exported_file_days_policy], [max_query_records_per_page] from tbl_EventManagerGlobalParam' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "key", "default_language", "max_running_export_task", "exported_file_nums_policy", "exported_file_days_policy", "max_query_records_per_page" from tbl_EventManagerGlobalParam' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_EventManagerGlobalParam ([moid], [key], [default_language], [max_running_export_task], [exported_file_nums_policy], [exported_file_days_policy], [max_query_records_per_page]) values(?1, ?2, ?3, ?4, ?5, ?6, ?7)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_EventManagerGlobalParam ("moid", "key", "default_language", "max_running_export_task", "exported_file_nums_policy", "exported_file_days_policy", "max_query_records_per_page") values(:1, :2, :3, :4, :5, :6, :7)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_EventManagerGlobalParam set [default_language]=?1, [max_running_export_task]=?2, [exported_file_nums_policy]=?3, [exported_file_days_policy]=?4, [max_query_records_per_page]=?5 where [moid]=?6' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_EventManagerGlobalParam set "default_language"=:1, "max_running_export_task"=:2, "exported_file_nums_policy"=:3, "exported_file_days_policy"=:4, "max_query_records_per_page"=:5 where "moid"=:6' 
    
    key                            = 'global'
    default_language               = 'chn'
    max_running_export_task        = 5
    exported_file_nums_policy      = 10
    exported_file_days_policy      = 7
    max_query_records_per_page     = 100
    
    @classmethod
    def gen_moid(cls, **kw):
        return "EventManagerGlobalParam_%s" % (repr(kw["key"]))
    
    def get_moid(self):
        return "EventManagerGlobalParam_%s" % (repr(self.key))
    
    @classmethod
    def get_attr_names(cls): 
        return ('key',), ('default_language', 'max_running_export_task', 'exported_file_nums_policy', 'exported_file_days_policy', 'max_query_records_per_page')
    
    def from_db_record(self, record):
        self.key                            = record[1]
        self.default_language               = record[2]
        self.max_running_export_task        = record[3]
        self.exported_file_nums_policy      = record[4]
        self.exported_file_days_policy      = record[5]
        self.max_query_records_per_page     = record[6]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.key
                , self.default_language
                , self.max_running_export_task
                , self.exported_file_nums_policy
                , self.exported_file_days_policy
                , self.max_query_records_per_page
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.default_language
                , self.max_running_export_task
                , self.exported_file_nums_policy
                , self.exported_file_days_policy
                , self.max_query_records_per_page
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class EventManagerGlobalParamRule(MocRule):
    pass
