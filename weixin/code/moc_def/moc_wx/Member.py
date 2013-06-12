#coding=gbk
import mit
from mit import MocBase, MocRule
from mit import MocAttrDef, ComplexAttrDef
import type_def
import err_code_mgr

# The automatic generated MOC. It is not recommended to inherit.
class Member(MocBase):
    __MOC_NAME__ = "Member"
    __IMC_SYNC_PRIORITY__ = mit.IMC_SYNC_NOT_SYNC
    __ATTR_DEF__ = (
                MocAttrDef(name = 'member_id', is_key = True, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'name', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 32),
                MocAttrDef(name = 'cellphone', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 32),
                MocAttrDef(name = 'weixin_id', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'delivery_addr', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 256),
                MocAttrDef(name = 'delivery_time', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'delivery_menu_id', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                MocAttrDef(name = 'subscriber_open_id', is_key = False, attr_type = type_def.TYPE_STRING, max_len = 64),
                )
    __COMPLEX_ATTR_DEF__ = ( 
                )
    
    __ATTR_DEF_MAP__ = {attr.name:attr for attr in __ATTR_DEF__ + __COMPLEX_ATTR_DEF__}
    __ATTR_INDEX__ = () 
    
    __SQLITE_SELECT_SQL__ = 'select [moid], [member_id], [name], [cellphone], [weixin_id], [delivery_addr], [delivery_time], [delivery_menu_id], [subscriber_open_id] from tbl_Member' 
    __ORACLE_SELECT_SQL__ = 'select "moid", "member_id", "name", "cellphone", "weixin_id", "delivery_addr", "delivery_time", "delivery_menu_id", "subscriber_open_id" from tbl_Member' 
    __SQLITE_INSERT_SQL__ = 'insert into tbl_Member ([moid], [member_id], [name], [cellphone], [weixin_id], [delivery_addr], [delivery_time], [delivery_menu_id], [subscriber_open_id]) values(?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)' 
    __ORACLE_INSERT_SQL__ = 'insert into tbl_Member ("moid", "member_id", "name", "cellphone", "weixin_id", "delivery_addr", "delivery_time", "delivery_menu_id", "subscriber_open_id") values(:1, :2, :3, :4, :5, :6, :7, :8, :9)' 
    
    __SQLITE_UPDATE_SQL__ = 'update tbl_Member set [name]=?1, [cellphone]=?2, [weixin_id]=?3, [delivery_addr]=?4, [delivery_time]=?5, [delivery_menu_id]=?6, [subscriber_open_id]=?7 where [moid]=?8' 
    __ORACLE_UPDATE_SQL__ = 'update tbl_Member set "name"=:1, "cellphone"=:2, "weixin_id"=:3, "delivery_addr"=:4, "delivery_time"=:5, "delivery_menu_id"=:6, "subscriber_open_id"=:7 where "moid"=:8' 
    
    member_id                      = ''
    name                           = ''
    cellphone                      = ''
    weixin_id                      = ''
    delivery_addr                  = ''
    delivery_time                  = ''
    delivery_menu_id               = ''
    subscriber_open_id             = ''
    
    @classmethod
    def gen_moid(cls, **kw):
        return "Member_%s" % (repr(kw["member_id"]))
    
    def get_moid(self):
        return "Member_%s" % (repr(self.member_id))
    
    @classmethod
    def get_attr_names(cls): 
        return ('member_id',), ('name', 'cellphone', 'weixin_id', 'delivery_addr', 'delivery_time', 'delivery_menu_id', 'subscriber_open_id')
    
    def from_db_record(self, record):
        self.member_id                      = record[1]
        self.name                           = record[2]
        self.cellphone                      = record[3]
        self.weixin_id                      = record[4]
        self.delivery_addr                  = record[5]
        self.delivery_time                  = record[6]
        self.delivery_menu_id               = record[7]
        self.subscriber_open_id             = record[8]
    
    def to_db_record(self):
        return [self.get_moid()
                , self.member_id
                , self.name
                , self.cellphone
                , self.weixin_id
                , self.delivery_addr
                , self.delivery_time
                , self.delivery_menu_id
                , self.subscriber_open_id
                ]
    
    def to_db_record_for_update(self):
        return [
                  self.name
                , self.cellphone
                , self.weixin_id
                , self.delivery_addr
                , self.delivery_time
                , self.delivery_menu_id
                , self.subscriber_open_id
                , self.get_moid()
                ]
    
    
# The automatic generated rule.
class MemberRule(MocRule):
    pass
