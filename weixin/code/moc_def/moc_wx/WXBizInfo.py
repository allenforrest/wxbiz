#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class WXBizInfo(MocBase):
    __MOC_NAME__ = "WXBizInfo"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'biz_id', is_key = True, attr_type = type_def.TYPE_UINT32, max_len = 0),
                MocAttrDef(name = 'access_token', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'login_user', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'login_pwd', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 128),
                MocAttrDef(name = 'auto_ip_update', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 8),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [biz_id], [access_token], [login_user], [login_pwd], [auto_ip_update] from tbl_WXBizInfo' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "biz_id", "access_token", "login_user", "login_pwd", "auto_ip_update" from tbl_WXBizInfo' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_WXBizInfo ([moid], [biz_id], [access_token], [login_user], [login_pwd], [auto_ip_update]) values(?1, ?2, ?3, ?4, ?5, ?6)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_WXBizInfo ("moid", "biz_id", "access_token", "login_user", "login_pwd", "auto_ip_update") values(:1, :2, :3, :4, :5, :6)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_WXBizInfo set [access_token]=?1, [login_user]=?2, [login_pwd]=?3, [auto_ip_update]=?4 where [moid]=?5' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_WXBizInfo set "access_token"=:1, "login_user"=:2, "login_pwd"=:3, "auto_ip_update"=:4 where "moid"=:5' 
    
    biz_id                         = 0
    access_token                   = ''
    login_user                     = ''
    login_pwd                      = ''
    auto_ip_update                 = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "WXBizInfo_%d" % (kw["biz_id"])
    
    def get_moid(self):
        return "WXBizInfo_%d" % (self.biz_id)
    
    @classmethod
    def get_attr_names(cls): 
        return ('biz_id',), ('access_token', 'login_user', 'login_pwd', 'auto_ip_update')
    
    def from_db_record(self, record):
        self.biz_id                         = record[1]
        self.access_token                   = record[2]
        self.login_user                     = record[3]
        self.login_pwd                      = record[4]
        self.auto_ip_update                 = record[5]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.biz_id
                , self.access_token
                , self.login_user
                , self.login_pwd
                , self.auto_ip_update
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.access_token
                , self.login_user
                , self.login_pwd
                , self.auto_ip_update
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class WXBizInfoRule(MocRule):
    pass
