#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class OraSyncPriority(MocBase):
    __MOC_NAME__ = "OraSyncPriority"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'ne_id', is_key = True, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'priority', is_key = True, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'event_id', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [ne_id], [priority], [event_id] from tbl_OraSyncPriority' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "ne_id", "priority", "event_id" from tbl_OraSyncPriority' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_OraSyncPriority ([moid], [ne_id], [priority], [event_id]) values(?1, ?2, ?3, ?4)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_OraSyncPriority ("moid", "ne_id", "priority", "event_id") values(:1, :2, :3, :4)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_OraSyncPriority set [event_id]=?1 where [moid]=?2' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_OraSyncPriority set "event_id"=:1 where "moid"=:2' 
    
    ne_id                          = 0
    priority                       = 0
    event_id                       = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "OraSyncPriority_%d_%d" % (kw["ne_id"], kw["priority"])
    
    def get_moid(self):
        return "OraSyncPriority_%d_%d" % (self.ne_id, self.priority)
    
    @classmethod
    def get_attr_names(cls): 
        return ('ne_id', 'priority'), ('event_id',)
    
    def from_db_record(self, record):
        self.ne_id                          = record[1]
        self.priority                       = record[2]
        self.event_id                       = record[3]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.ne_id
                , self.priority
                , self.event_id
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.event_id
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class OraSyncPriorityRule(MocRule):
    pass
