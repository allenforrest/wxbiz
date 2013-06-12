#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class Group(MocBase):
    __MOC_NAME__ = "Group"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'group_id', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'group_name', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 128),
                MocAttrDef(name = 'description', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 256),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [group_id], [group_name], [description] from tbl_Group' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "group_id", "group_name", "description" from tbl_Group' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_Group ([moid], [group_id], [group_name], [description]) values(?1, ?2, ?3, ?4)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_Group ("moid", "group_id", "group_name", "description") values(:1, :2, :3, :4)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_Group set [group_name]=?1, [description]=?2 where [moid]=?3' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_Group set "group_name"=:1, "description"=:2 where "moid"=:3' 
    
    group_id                       = 0
    group_name                     = ''
    description                    = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "Group_%d" % (kw["group_id"])
    
    def get_moid(self):
        return "Group_%d" % (self.group_id)
    
    @classmethod
    def get_attr_names(cls): 
        return ('group_id',), ('group_name', 'description')
    
    def from_db_record(self, record):
        self.group_id                       = record[1]
        self.group_name                     = record[2]
        self.description                    = record[3]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.group_id
                , self.group_name
                , self.description
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.group_name
                , self.description
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class GroupRule(MocRule):
    pass
