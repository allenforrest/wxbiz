#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class NEDbSyncState(MocBase):
    __MOC_NAME__ = "NEDbSyncState"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'ne_id', is_key = True, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'need_sync_full', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'sync_state', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'sync_sn', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [ne_id], [need_sync_full], [sync_state], [sync_sn] from tbl_NEDbSyncState' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "ne_id", "need_sync_full", "sync_state", "sync_sn" from tbl_NEDbSyncState' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_NEDbSyncState ([moid], [ne_id], [need_sync_full], [sync_state], [sync_sn]) values(?1, ?2, ?3, ?4, ?5)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_NEDbSyncState ("moid", "ne_id", "need_sync_full", "sync_state", "sync_sn") values(:1, :2, :3, :4, :5)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_NEDbSyncState set [need_sync_full]=?1, [sync_state]=?2, [sync_sn]=?3 where [moid]=?4' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_NEDbSyncState set "need_sync_full"=:1, "sync_state"=:2, "sync_sn"=:3 where "moid"=:4' 
    
    ne_id                          = 0
    need_sync_full                 = 1
    sync_state                     = 0
    sync_sn                        = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "NEDbSyncState_%d" % (kw["ne_id"])
    
    def get_moid(self):
        return "NEDbSyncState_%d" % (self.ne_id)
    
    @classmethod
    def get_attr_names(cls): 
        return ('ne_id',), ('need_sync_full', 'sync_state', 'sync_sn')
    
    def from_db_record(self, record):
        self.ne_id                          = record[1]
        self.need_sync_full                 = record[2]
        self.sync_state                     = record[3]
        self.sync_sn                        = record[4]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.ne_id
                , self.need_sync_full
                , self.sync_state
                , self.sync_sn
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.need_sync_full
                , self.sync_state
                , self.sync_sn
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class NEDbSyncStateRule(MocRule):
    pass
