#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class OraSyncEvent(MocBase):
    __MOC_NAME__ = "OraSyncEvent"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'id', is_key = True, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'type', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'target', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 255),
                MocAttrDef(name = 'priority', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'operation', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'data', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 65535),
                MocAttrDef(name = 'condition', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 65535),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [id], [type], [target], [priority], [operation], [data], [condition] from tbl_OraSyncEvent' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "id", "type", "target", "priority", "operation", "data", "condition" from tbl_OraSyncEvent' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_OraSyncEvent ([moid], [id], [type], [target], [priority], [operation], [data], [condition]) values(?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_OraSyncEvent ("moid", "id", "type", "target", "priority", "operation", "data", "condition") values(:1, :2, :3, :4, :5, :6, :7, :8)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_OraSyncEvent set [type]=?1, [target]=?2, [priority]=?3, [operation]=?4, [data]=?5, [condition]=?6 where [moid]=?7' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_OraSyncEvent set "type"=:1, "target"=:2, "priority"=:3, "operation"=:4, "data"=:5, "condition"=:6 where "moid"=:7' 
    
    id                             = 0
    type                           = 0
    target                         = ''
    priority                       = 0
    operation                      = 0
    data                           = ''
    condition                      = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "OraSyncEvent_%d" % (kw["id"])
    
    def get_moid(self):
        return "OraSyncEvent_%d" % (self.id)
    
    @classmethod
    def get_attr_names(cls): 
        return ('id',), ('type', 'target', 'priority', 'operation', 'data', 'condition')
    
    def from_db_record(self, record):
        self.id                             = record[1]
        self.type                           = record[2]
        self.target                         = record[3]
        self.priority                       = record[4]
        self.operation                      = record[5]
        if record[6] is not None:
            self.data                       = record[6].read()
        if record[7] is not None:
            self.condition                  = record[7].read()
    
    def to_db_record(self):
        return [self.get_moid()
                , self.id
                , self.type
                , self.target
                , self.priority
                , self.operation
                , self.data
                , self.condition
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.type
                , self.target
                , self.priority
                , self.operation
                , self.data
                , self.condition
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class OraSyncEventRule(MocRule):
    pass
