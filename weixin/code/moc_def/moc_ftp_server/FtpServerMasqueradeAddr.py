#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class FtpServerMasqueradeAddr(MocBase):
    __MOC_NAME__ = "FtpServerMasqueradeAddr"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'private_ip', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'public_ip', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [private_ip], [public_ip] from tbl_FtpServerMasqueradeAddr' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "private_ip", "public_ip" from tbl_FtpServerMasqueradeAddr' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_FtpServerMasqueradeAddr ([moid], [private_ip], [public_ip]) values(?1, ?2, ?3)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_FtpServerMasqueradeAddr ("moid", "private_ip", "public_ip") values(:1, :2, :3)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_FtpServerMasqueradeAddr set [public_ip]=?1 where [moid]=?2' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_FtpServerMasqueradeAddr set "public_ip"=:1 where "moid"=:2' 
    
    private_ip                     = ''
    public_ip                      = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "FtpServerMasqueradeAddr_%s" % (repr(kw["private_ip"]))
    
    def get_moid(self):
        return "FtpServerMasqueradeAddr_%s" % (repr(self.private_ip))
    
    @classmethod
    def get_attr_names(cls): 
        return ('private_ip',), ('public_ip',)
    
    def from_db_record(self, record):
        self.private_ip                     = record[1]
        self.public_ip                      = record[2]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.private_ip
                , self.public_ip
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.public_ip
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class FtpServerMasqueradeAddrRule(MocRule):
    pass
