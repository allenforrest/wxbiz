#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class Vegetable(MocBase):
    __MOC_NAME__ = "Vegetable"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'v_id', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'name', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'description', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 256),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [v_id], [name], [description] from tbl_Vegetable' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "v_id", "name", "description" from tbl_Vegetable' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_Vegetable ([moid], [v_id], [name], [description]) values(?1, ?2, ?3, ?4)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_Vegetable ("moid", "v_id", "name", "description") values(:1, :2, :3, :4)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_Vegetable set [name]=?1, [description]=?2 where [moid]=?3' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_Vegetable set "name"=:1, "description"=:2 where "moid"=:3' 
    
    v_id                           = 0
    name                           = ''
    description                    = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "Vegetable_%d" % (kw["v_id"])
    
    def get_moid(self):
        return "Vegetable_%d" % (self.v_id)
    
    @classmethod
    def get_attr_names(cls): 
        return ('v_id',), ('name', 'description')
    
    def from_db_record(self, record):
        self.v_id                           = record[1]
        self.name                           = record[2]
        self.description                    = record[3]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.v_id
                , self.name
                , self.description
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.name
                , self.description
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class VegetableRule(MocRule):
    pass
