#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class EventDetail(MocBase):
    __MOC_NAME__ = "EventDetail"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'sequence_no', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'language', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'name', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'description', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 1024),
                MocAttrDef(name = 'cause', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 1024),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [sequence_no], [language], [name], [description], [cause] from tbl_EventDetail' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "sequence_no", "language", "name", "description", "cause" from tbl_EventDetail' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_EventDetail ([moid], [sequence_no], [language], [name], [description], [cause]) values(?1, ?2, ?3, ?4, ?5, ?6)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_EventDetail ("moid", "sequence_no", "language", "name", "description", "cause") values(:1, :2, :3, :4, :5, :6)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_EventDetail set [name]=?1, [description]=?2, [cause]=?3 where [moid]=?4' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_EventDetail set "name"=:1, "description"=:2, "cause"=:3 where "moid"=:4' 
    
    sequence_no                    = 0
    language                       = 'chn'
    name                           = ''
    description                    = ''
    cause                          = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "EventDetail_%d_%s" % (kw["sequence_no"], repr(kw["language"]))
    
    def get_moid(self):
        return "EventDetail_%d_%s" % (self.sequence_no, repr(self.language))
    
    @classmethod
    def get_attr_names(cls): 
        return ('sequence_no', 'language'), ('name', 'description', 'cause')
    
    def from_db_record(self, record):
        self.sequence_no                    = record[1]
        self.language                       = record[2]
        self.name                           = record[3]
        self.description                    = record[4]
        self.cause                          = record[5]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.sequence_no
                , self.language
                , self.name
                , self.description
                , self.cause
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.name
                , self.description
                , self.cause
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class EventDetailRule(MocRule):
    pass
