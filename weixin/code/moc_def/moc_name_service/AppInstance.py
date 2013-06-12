#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class AppInstance(MocBase):
    __MOC_NAME__ = "AppInstance"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'pid', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'instance_name', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'service_name', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'instance_id', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'system_ip', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'node_type', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'endpoint', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'endpoint_protocol', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'update_time', is_key = False, attr_type = type_def.TYPE_UINT32, max_len = 64),
                MocAttrDef(name = 'state', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [pid], [instance_name], [service_name], [instance_id], [system_ip], [node_type], [endpoint], [endpoint_protocol], [update_time], [state] from tbl_AppInstance' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "pid", "instance_name", "service_name", "instance_id", "system_ip", "node_type", "endpoint", "endpoint_protocol", "update_time", "state" from tbl_AppInstance' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_AppInstance ([moid], [pid], [instance_name], [service_name], [instance_id], [system_ip], [node_type], [endpoint], [endpoint_protocol], [update_time], [state]) values(?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_AppInstance ("moid", "pid", "instance_name", "service_name", "instance_id", "system_ip", "node_type", "endpoint", "endpoint_protocol", "update_time", "state") values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_AppInstance set [instance_name]=?1, [service_name]=?2, [instance_id]=?3, [system_ip]=?4, [node_type]=?5, [endpoint]=?6, [endpoint_protocol]=?7, [update_time]=?8, [state]=?9 where [moid]=?10' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_AppInstance set "instance_name"=:1, "service_name"=:2, "instance_id"=:3, "system_ip"=:4, "node_type"=:5, "endpoint"=:6, "endpoint_protocol"=:7, "update_time"=:8, "state"=:9 where "moid"=:10' 
    
    pid                            = 0
    instance_name                  = ''
    service_name                   = ''
    instance_id                    = 0
    system_ip                      = ''
    node_type                      = ''
    endpoint                       = ''
    endpoint_protocol              = ''
    update_time                    = 0
    state                          = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "AppInstance_%d" % (kw["pid"])
    
    def get_moid(self):
        return "AppInstance_%d" % (self.pid)
    
    @classmethod
    def get_attr_names(cls): 
        return ('pid',), ('instance_name', 'service_name', 'instance_id', 'system_ip', 'node_type', 'endpoint', 'endpoint_protocol', 'update_time', 'state')
    
    def from_db_record(self, record):
        self.pid                            = record[1]
        self.instance_name                  = record[2]
        self.service_name                   = record[3]
        self.instance_id                    = record[4]
        self.system_ip                      = record[5]
        self.node_type                      = record[6]
        self.endpoint                       = record[7]
        self.endpoint_protocol              = record[8]
        self.update_time                    = record[9]
        self.state                          = record[10]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.pid
                , self.instance_name
                , self.service_name
                , self.instance_id
                , self.system_ip
                , self.node_type
                , self.endpoint
                , self.endpoint_protocol
                , self.update_time
                , self.state
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.instance_name
                , self.service_name
                , self.instance_id
                , self.system_ip
                , self.node_type
                , self.endpoint
                , self.endpoint_protocol
                , self.update_time
                , self.state
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class AppInstanceRule(MocRule):
    pass
