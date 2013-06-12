#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class NtpdSubnetMOC(MocBase):
    __MOC_NAME__ = "NtpdSubnetMOC"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'subnetip', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'mask', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [subnetip], [mask] from tbl_NtpdSubnetMOC' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "subnetip", "mask" from tbl_NtpdSubnetMOC' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_NtpdSubnetMOC ([moid], [subnetip], [mask]) values(?1, ?2, ?3)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_NtpdSubnetMOC ("moid", "subnetip", "mask") values(:1, :2, :3)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_NtpdSubnetMOC set  where [moid]=?1' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_NtpdSubnetMOC set  where "moid"=:1' 
    
    subnetip                       = ''
    mask                           = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "NtpdSubnetMOC_%s_%s" % (repr(kw["subnetip"]), repr(kw["mask"]))
    
    def get_moid(self):
        return "NtpdSubnetMOC_%s_%s" % (repr(self.subnetip), repr(self.mask))
    
    @classmethod
    def get_attr_names(cls): 
        return ('subnetip', 'mask'), ()
    
    def from_db_record(self, record):
        self.subnetip                       = record[1]
        self.mask                           = record[2]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.subnetip
                , self.mask
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.get_moid()
                ]
    
    
# The automatic generated rule.
class NtpdSubnetMOCRule(MocRule):
    pass
