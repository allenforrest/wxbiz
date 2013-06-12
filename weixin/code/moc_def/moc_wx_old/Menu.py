#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class Menu(MocBase):
    __MOC_NAME__ = "Menu"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'menu_id', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'name', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'description', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 256),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                ComplexAttrDef(name = 'vegetables', attr_type = 'VegetableList', is_list = True),
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [menu_id], [name], [description] from tbl_Menu' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "menu_id", "name", "description" from tbl_Menu' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_Menu ([moid], [menu_id], [name], [description]) values(?1, ?2, ?3, ?4)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_Menu ("moid", "menu_id", "name", "description") values(:1, :2, :3, :4)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_Menu set [name]=?1, [description]=?2 where [moid]=?3' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_Menu set "name"=:1, "description"=:2 where "moid"=:3' 
    
    menu_id                        = 0
    name                           = ''
    description                    = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "Menu_%d" % (kw["menu_id"])
    
    def get_moid(self):
        return "Menu_%d" % (self.menu_id)
    
    @classmethod
    def get_attr_names(cls): 
        return ('menu_id',), ('name', 'description')
    
    def from_db_record(self, record):
        self.menu_id                        = record[1]
        self.name                           = record[2]
        self.description                    = record[3]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.menu_id
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
class MenuRule(MocRule):
    pass
