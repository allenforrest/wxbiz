#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class HelpTips(MocBase):
    __MOC_NAME__ = "HelpTips"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'tips_id', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'content', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 1024),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [tips_id], [content] from tbl_HelpTips' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "tips_id", "content" from tbl_HelpTips' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_HelpTips ([moid], [tips_id], [content]) values(?1, ?2, ?3)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_HelpTips ("moid", "tips_id", "content") values(:1, :2, :3)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_HelpTips set [content]=?1 where [moid]=?2' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_HelpTips set "content"=:1 where "moid"=:2' 
    
    tips_id                        = 0
    content                        = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "HelpTips_%d" % (kw["tips_id"])
    
    def get_moid(self):
        return "HelpTips_%d" % (self.tips_id)
    
    @classmethod
    def get_attr_names(cls): 
        return ('tips_id',), ('content',)
    
    def from_db_record(self, record):
        self.tips_id                        = record[1]
        self.content                        = record[2]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.tips_id
                , self.content
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.content
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class HelpTipsRule(MocRule):
    pass
