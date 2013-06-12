#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class FtpServerUserMOC(MocBase):
    __MOC_NAME__ = "FtpServerUserMOC"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'username', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'password', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'homedir', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'perm', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [username], [password], [homedir], [perm] from tbl_FtpServerUserMOC' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "username", "password", "homedir", "perm" from tbl_FtpServerUserMOC' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_FtpServerUserMOC ([moid], [username], [password], [homedir], [perm]) values(?1, ?2, ?3, ?4, ?5)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_FtpServerUserMOC ("moid", "username", "password", "homedir", "perm") values(:1, :2, :3, :4, :5)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_FtpServerUserMOC set [password]=?1, [homedir]=?2, [perm]=?3 where [moid]=?4' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_FtpServerUserMOC set "password"=:1, "homedir"=:2, "perm"=:3 where "moid"=:4' 
    
    username                       = ''
    password                       = ''
    homedir                        = ''
    perm                           = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "FtpServerUserMOC_%s" % (repr(kw["username"]))
    
    def get_moid(self):
        return "FtpServerUserMOC_%s" % (repr(self.username))
    
    @classmethod
    def get_attr_names(cls): 
        return ('username',), ('password', 'homedir', 'perm')
    
    def from_db_record(self, record):
        self.username                       = record[1]
        self.password                       = record[2]
        self.homedir                        = record[3]
        self.perm                           = record[4]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.username
                , self.password
                , self.homedir
                , self.perm
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.password
                , self.homedir
                , self.perm
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class FtpServerUserMOCRule(MocRule):
    pass
