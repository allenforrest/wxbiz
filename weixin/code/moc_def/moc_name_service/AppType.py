#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class AppType(MocBase):
    __MOC_NAME__ = "AppType"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'service_name', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'instance_num', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [service_name], [instance_num] from tbl_AppType' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "service_name", "instance_num" from tbl_AppType' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_AppType ([moid], [service_name], [instance_num]) values(?1, ?2, ?3)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_AppType ("moid", "service_name", "instance_num") values(:1, :2, :3)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_AppType set [instance_num]=?1 where [moid]=?2' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_AppType set "instance_num"=:1 where "moid"=:2' 
    
    service_name                   = ''
    instance_num                   = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "AppType_%s" % (repr(kw["service_name"]))
    
    def get_moid(self):
        return "AppType_%s" % (repr(self.service_name))
    
    @classmethod
    def get_attr_names(cls): 
        return ('service_name',), ('instance_num',)
    
    def from_db_record(self, record):
        self.service_name                   = record[1]
        self.instance_num                   = record[2]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.service_name
                , self.instance_num
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.instance_num
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class AppTypeRule(MocRule):
    pass
