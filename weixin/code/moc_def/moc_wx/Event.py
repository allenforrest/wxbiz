#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class Event(MocBase):
    __MOC_NAME__ = "Event"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'event_id', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'event_type', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 32),
                MocAttrDef(name = 'content', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 1024),
                MocAttrDef(name = 'read_flag', is_key = False, attr_type = type_def.TYPE_BOOL, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [event_id], [event_type], [content], [read_flag] from tbl_Event' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "event_id", "event_type", "content", "read_flag" from tbl_Event' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_Event ([moid], [event_id], [event_type], [content], [read_flag]) values(?1, ?2, ?3, ?4, ?5)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_Event ("moid", "event_id", "event_type", "content", "read_flag") values(:1, :2, :3, :4, :5)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_Event set [event_type]=?1, [content]=?2, [read_flag]=?3 where [moid]=?4' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_Event set "event_type"=:1, "content"=:2, "read_flag"=:3 where "moid"=:4' 
    
    event_id                       = 0
    event_type                     = ''
    content                        = ''
    read_flag                      = False
    
    @classmethod
    def gen_moid(cls, **kw):
        return "Event_%d" % (kw["event_id"])
    
    def get_moid(self):
        return "Event_%d" % (self.event_id)
    
    @classmethod
    def get_attr_names(cls): 
        return ('event_id',), ('event_type', 'content', 'read_flag')
    
    def from_db_record(self, record):
        self.event_id                       = record[1]
        self.event_type                     = record[2]
        self.content                        = record[3]
        self.read_flag                      = record[4]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.event_id
                , self.event_type
                , self.content
                , self.read_flag
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.event_type
                , self.content
                , self.read_flag
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class EventRule(MocRule):
    pass
