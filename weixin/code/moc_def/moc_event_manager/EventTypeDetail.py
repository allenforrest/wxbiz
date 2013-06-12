#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class EventTypeDetail(MocBase):
    __MOC_NAME__ = "EventTypeDetail"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'event_id', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 128),
                MocAttrDef(name = 'language', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'name', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'description', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 1024),
                MocAttrDef(name = 'cause', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 1024),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [event_id], [language], [name], [description], [cause] from tbl_EventTypeDetail' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "event_id", "language", "name", "description", "cause" from tbl_EventTypeDetail' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_EventTypeDetail ([moid], [event_id], [language], [name], [description], [cause]) values(?1, ?2, ?3, ?4, ?5, ?6)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_EventTypeDetail ("moid", "event_id", "language", "name", "description", "cause") values(:1, :2, :3, :4, :5, :6)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_EventTypeDetail set [name]=?1, [description]=?2, [cause]=?3 where [moid]=?4' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_EventTypeDetail set "name"=:1, "description"=:2, "cause"=:3 where "moid"=:4' 
    
    event_id                       = ''
    language                       = 'chn'
    name                           = ''
    description                    = ''
    cause                          = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "EventTypeDetail_%s_%s" % (repr(kw["event_id"]), repr(kw["language"]))
    
    def get_moid(self):
        return "EventTypeDetail_%s_%s" % (repr(self.event_id), repr(self.language))
    
    @classmethod
    def get_attr_names(cls): 
        return ('event_id', 'language'), ('name', 'description', 'cause')
    
    def from_db_record(self, record):
        self.event_id                       = record[1]
        self.language                       = record[2]
        self.name                           = record[3]
        self.description                    = record[4]
        self.cause                          = record[5]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.event_id
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
class EventTypeDetailRule(MocRule):
    pass
