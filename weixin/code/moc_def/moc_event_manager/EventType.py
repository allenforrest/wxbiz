#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class EventType(MocBase):
    __MOC_NAME__ = "EventType"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'event_id', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 128),
                MocAttrDef(name = 'event_flag', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'level', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'device_type', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'object_type', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [event_id], [event_flag], [level], [device_type], [object_type] from tbl_EventType' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "event_id", "event_flag", "level", "device_type", "object_type" from tbl_EventType' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_EventType ([moid], [event_id], [event_flag], [level], [device_type], [object_type]) values(?1, ?2, ?3, ?4, ?5, ?6)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_EventType ("moid", "event_id", "event_flag", "level", "device_type", "object_type") values(:1, :2, :3, :4, :5, :6)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_EventType set [event_flag]=?1, [level]=?2, [device_type]=?3, [object_type]=?4 where [moid]=?5' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_EventType set "event_flag"=:1, "level"=:2, "device_type"=:3, "object_type"=:4 where "moid"=:5' 
    
    event_id                       = ''
    event_flag                     = ''
    level                          = ''
    device_type                    = ''
    object_type                    = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "EventType_%s" % (repr(kw["event_id"]))
    
    def get_moid(self):
        return "EventType_%s" % (repr(self.event_id))
    
    @classmethod
    def get_attr_names(cls): 
        return ('event_id',), ('event_flag', 'level', 'device_type', 'object_type')
    
    def from_db_record(self, record):
        self.event_id                       = record[1]
        self.event_flag                     = record[2]
        self.level                          = record[3]
        self.device_type                    = record[4]
        self.object_type                    = record[5]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.event_id
                , self.event_flag
                , self.level
                , self.device_type
                , self.object_type
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.event_flag
                , self.level
                , self.device_type
                , self.object_type
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class EventTypeRule(MocRule):
    pass
