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
                MocAttrDef(name = 'sequence_no', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'event_id', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'event_flag', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'level', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'time_inner', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'time', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'device_type', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'device_id', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'object_type', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'object_id', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [sequence_no], [event_id], [event_flag], [level], [time_inner], [time], [device_type], [device_id], [object_type], [object_id] from tbl_Event' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "sequence_no", "event_id", "event_flag", "level", "time_inner", "time", "device_type", "device_id", "object_type", "object_id" from tbl_Event' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_Event ([moid], [sequence_no], [event_id], [event_flag], [level], [time_inner], [time], [device_type], [device_id], [object_type], [object_id]) values(?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_Event ("moid", "sequence_no", "event_id", "event_flag", "level", "time_inner", "time", "device_type", "device_id", "object_type", "object_id") values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_Event set [event_id]=?1, [event_flag]=?2, [level]=?3, [time_inner]=?4, [time]=?5, [device_type]=?6, [device_id]=?7, [object_type]=?8, [object_id]=?9 where [moid]=?10' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_Event set "event_id"=:1, "event_flag"=:2, "level"=:3, "time_inner"=:4, "time"=:5, "device_type"=:6, "device_id"=:7, "object_type"=:8, "object_id"=:9 where "moid"=:10' 
    
    sequence_no                    = 0
    event_id                       = ''
    event_flag                     = ''
    level                          = ''
    time_inner                     = 0
    time                           = ''
    device_type                    = ''
    device_id                      = ''
    object_type                    = ''
    object_id                      = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "Event_%d" % (kw["sequence_no"])
    
    def get_moid(self):
        return "Event_%d" % (self.sequence_no)
    
    @classmethod
    def get_attr_names(cls): 
        return ('sequence_no',), ('event_id', 'event_flag', 'level', 'time_inner', 'time', 'device_type', 'device_id', 'object_type', 'object_id')
    
    def from_db_record(self, record):
        self.sequence_no                    = record[1]
        self.event_id                       = record[2]
        self.event_flag                     = record[3]
        self.level                          = record[4]
        self.time_inner                     = record[5]
        self.time                           = record[6]
        self.device_type                    = record[7]
        self.device_id                      = record[8]
        self.object_type                    = record[9]
        self.object_id                      = record[10]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.sequence_no
                , self.event_id
                , self.event_flag
                , self.level
                , self.time_inner
                , self.time
                , self.device_type
                , self.device_id
                , self.object_type
                , self.object_id
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.event_id
                , self.event_flag
                , self.level
                , self.time_inner
                , self.time
                , self.device_type
                , self.device_id
                , self.object_type
                , self.object_id
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class EventRule(MocRule):
    pass
