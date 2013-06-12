#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class FtpServerDataLinkMOC(MocBase):
    __MOC_NAME__ = "FtpServerDataLinkMOC"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'timeout', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'ac_in_buffer_size', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'ac_out_buffer_size', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'read_limit', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                MocAttrDef(name = 'write_limit', is_key = False, attr_type = type_def.TYPE_INT32, max_len = 0),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [timeout], [ac_in_buffer_size], [ac_out_buffer_size], [read_limit], [write_limit] from tbl_FtpServerDataLinkMOC' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "timeout", "ac_in_buffer_size", "ac_out_buffer_size", "read_limit", "write_limit" from tbl_FtpServerDataLinkMOC' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_FtpServerDataLinkMOC ([moid], [timeout], [ac_in_buffer_size], [ac_out_buffer_size], [read_limit], [write_limit]) values(?1, ?2, ?3, ?4, ?5, ?6)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_FtpServerDataLinkMOC ("moid", "timeout", "ac_in_buffer_size", "ac_out_buffer_size", "read_limit", "write_limit") values(:1, :2, :3, :4, :5, :6)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_FtpServerDataLinkMOC set [timeout]=?1, [ac_in_buffer_size]=?2, [ac_out_buffer_size]=?3, [read_limit]=?4, [write_limit]=?5 where [moid]=?6' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_FtpServerDataLinkMOC set "timeout"=:1, "ac_in_buffer_size"=:2, "ac_out_buffer_size"=:3, "read_limit"=:4, "write_limit"=:5 where "moid"=:6' 
    
    timeout                        = 0
    ac_in_buffer_size              = 0
    ac_out_buffer_size             = 0
    read_limit                     = 0
    write_limit                    = 0
    
    @classmethod
    def gen_moid(cls, **kw):
        return "FtpServerDataLinkMOC"
    
    def get_moid(self):
        return "FtpServerDataLinkMOC"
    
    @classmethod
    def get_attr_names(cls): 
        return (), ('timeout', 'ac_in_buffer_size', 'ac_out_buffer_size', 'read_limit', 'write_limit')
    
    def from_db_record(self, record):
        self.timeout                        = record[1]
        self.ac_in_buffer_size              = record[2]
        self.ac_out_buffer_size             = record[3]
        self.read_limit                     = record[4]
        self.write_limit                    = record[5]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.timeout
                , self.ac_in_buffer_size
                , self.ac_out_buffer_size
                , self.read_limit
                , self.write_limit
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.timeout
                , self.ac_in_buffer_size
                , self.ac_out_buffer_size
                , self.read_limit
                , self.write_limit
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class FtpServerDataLinkMOCRule(MocRule):
    pass
